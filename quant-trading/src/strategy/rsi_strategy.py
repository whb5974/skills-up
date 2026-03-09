#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSI 策略模块
基于相对强弱指标 (RSI) 的交易策略
"""

import pandas as pd
import numpy as np
from loguru import logger


class RSIStrategy:
    """RSI 交易策略"""
    
    def __init__(self, period=14, oversold=30, overbought=70):
        """
        初始化 RSI 策略
        
        Args:
            period: RSI 计算周期 (默认 14)
            oversold: 超卖阈值 (默认 30)
            overbought: 超买阈值 (默认 70)
        """
        self.period = period
        self.oversold = oversold
        self.overbought = overbought
        logger.info(f"✅ RSI 策略初始化 (Period={period}, Oversold={oversold}, Overbought={overbought})")
    
    def calculate_rsi(self, df):
        """
        计算 RSI 指标
        
        Args:
            df: 包含 OHLCV 数据的 DataFrame
        
        Returns:
            DataFrame: 添加 RSI 列
        """
        df = df.copy()
        
        # 计算价格变化
        delta = df['close'].diff()
        
        # 分离上涨和下跌
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        # 计算平均涨幅和平均跌幅
        avg_gain = gain.rolling(window=self.period).mean()
        avg_loss = loss.rolling(window=self.period).mean()
        
        # 计算 RS (相对强度)
        rs = avg_gain / avg_loss
        
        # 计算 RSI
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # 填充 NaN 值
        df['RSI'] = df['RSI'].fillna(50)
        
        logger.info(f"📊 RSI 指标计算完成")
        
        return df
    
    def generate_signal(self, df):
        """
        生成交易信号
        
        规则:
        - RSI < 30 → 超卖 → 买入信号 (1)
        - RSI > 70 → 超买 → 卖出信号 (-1)
        - RSI < 20 → 极度超卖 → 强势买入
        - RSI > 80 → 极度超买 → 强势卖出
        
        Returns:
            DataFrame: 添加 signal 列
        """
        df = self.calculate_rsi(df)
        
        # 初始化信号
        df['signal'] = 0
        
        # 买入信号：RSI < 30 (超卖)
        oversold = df['RSI'] < self.oversold
        df.loc[oversold, 'signal'] = 1
        
        # 卖出信号：RSI > 70 (超买)
        overbought = df['RSI'] > self.overbought
        df.loc[overbought, 'signal'] = -1
        
        # 极度超卖/超买
        df['extreme_oversold'] = df['RSI'] < 20
        df['extreme_overbought'] = df['RSI'] > 80
        
        # RSI 背离检测 (简化版)
        # 价格创新低但 RSI 未创新低 →  bullish divergence
        # 价格创新高但 RSI 未创新高 →  bearish divergence
        df['price_low'] = df['close'] == df['close'].rolling(window=5).min()
        df['price_high'] = df['close'] == df['close'].rolling(window=5).max()
        df['rsi_low'] = df['RSI'] == df['RSI'].rolling(window=5).min()
        df['rsi_high'] = df['RSI'] == df['RSI'].rolling(window=5).max()
        
        #  bullish divergence (价格新低但 RSI 未新低)
        df['bullish_div'] = df['price_low'] & ~df['rsi_low']
        
        # bearish divergence (价格新高但 RSI 未新高)
        df['bearish_div'] = df['price_high'] & ~df['rsi_high']
        
        logger.info(f"📊 生成信号：{oversold.sum()} 个超卖信号，{overbought.sum()} 个超买信号")
        logger.info(f"📊 极度超卖：{df['extreme_oversold'].sum()} 个，极度超买：{df['extreme_overbought'].sum()} 个")
        logger.info(f"📊 顶背离：{df['bearish_div'].sum()} 个，底背离：{df['bullish_div'].sum()} 个")
        
        return df
    
    def backtest(self, df, capital=100000, commission=0.001, slippage=0.001):
        """
        简单回测
        
        Args:
            df: 包含 OHLCV 数据的 DataFrame
            capital: 初始资金
            commission: 手续费率
            slippage: 滑点
        
        Returns:
            dict: 回测结果
        """
        df = self.generate_signal(df).copy()
        
        # 持仓和资金
        position = 0
        cash = capital
        trades = []
        portfolio_values = []
        
        for i in range(1, len(df)):
            signal = df.iloc[i]['signal']
            price = df.iloc[i]['close']
            date = df.index[i] if hasattr(df.index[i], 'strftime') else i
            rsi = df.iloc[i]['RSI']
            
            # 买入信号 (超卖)
            if signal == 1 and position == 0:
                # 考虑滑点和手续费
                buy_price = price * (1 + slippage)
                shares = int(cash * 0.95 / buy_price)  # 用 95% 资金
                if shares > 0:
                    cost = shares * buy_price * (1 + commission)
                    cash -= cost
                    position = shares
                    trades.append({
                        'date': date,
                        'type': 'BUY',
                        'price': buy_price,
                        'shares': shares,
                        'cash': cash,
                        'cost': cost,
                        'rsi': rsi,
                        'is_extreme': df.iloc[i]['extreme_oversold'],
                        'has_divergence': df.iloc[i]['bullish_div']
                    })
            
            # 卖出信号 (超买)
            elif signal == -1 and position > 0:
                # 考虑滑点和手续费
                sell_price = price * (1 - slippage)
                revenue = position * sell_price * (1 - commission)
                cash += revenue
                trades.append({
                    'date': date,
                    'type': 'SELL',
                    'price': sell_price,
                    'shares': position,
                    'cash': cash,
                    'revenue': revenue,
                    'rsi': rsi,
                    'is_extreme': df.iloc[i]['extreme_overbought'],
                    'has_divergence': df.iloc[i]['bearish_div']
                })
                position = 0
            
            # 记录组合价值
            portfolio_value = cash + (position * price)
            portfolio_values.append({
                'date': date,
                'value': portfolio_value,
                'cash': cash,
                'position': position * price
            })
        
        # 计算最终价值
        final_price = df.iloc[-1]['close']
        final_value = cash + (position * final_price)
        
        # 计算收益率
        total_return = (final_value - capital) / capital
        
        # 计算交易次数
        buy_trades = [t for t in trades if t['type'] == 'BUY']
        sell_trades = [t for t in trades if t['type'] == 'SELL']
        
        # 计算胜率
        winning_trades = 0
        for i, sell in enumerate(sell_trades):
            if i < len(buy_trades):
                buy = buy_trades[i]
                if sell['price'] > buy['price']:
                    winning_trades += 1
        
        win_rate = winning_trades / len(buy_trades) if buy_trades else 0
        
        # 计算最大回撤
        portfolio_df = pd.DataFrame(portfolio_values)
        if len(portfolio_df) > 0:
            portfolio_df['peak'] = portfolio_df['value'].cummax()
            portfolio_df['drawdown'] = (portfolio_df['value'] - portfolio_df['peak']) / portfolio_df['peak']
            max_drawdown = portfolio_df['drawdown'].min()
        else:
            max_drawdown = 0
        
        # 计算夏普比率
        if len(portfolio_values) > 1:
            returns = pd.DataFrame(portfolio_values)['value'].pct_change().dropna()
            sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252) if returns.std() > 0 else 0
        else:
            sharpe_ratio = 0
        
        return {
            'initial_capital': capital,
            'final_value': final_value,
            'total_return': total_return,
            'total_return_pct': f"{total_return:.2%}",
            'num_buy_trades': len(buy_trades),
            'num_sell_trades': len(sell_trades),
            'win_rate': f"{win_rate:.2%}",
            'max_drawdown': f"{max_drawdown:.2%}",
            'sharpe_ratio': f"{sharpe_ratio:.2f}",
            'trades': trades,
            'portfolio_values': portfolio_values
        }


# 测试
if __name__ == "__main__":
    # 创建测试数据 (模拟股价走势)
    np.random.seed(42)
    dates = pd.date_range('2025-01-01', periods=252, freq='D')
    
    # 生成带震荡的随机游走
    trend = np.linspace(0, 20, 252)
    noise = np.cumsum(np.random.randn(252) * 0.5)
    prices = 100 + trend + noise
    
    df = pd.DataFrame({
        'open': prices + np.random.randn(252) * 0.3,
        'high': prices + np.abs(np.random.randn(252)) * 0.5,
        'low': prices - np.abs(np.random.randn(252)) * 0.5,
        'close': prices,
        'volume': np.random.randint(1000, 10000, 252)
    }, index=dates)
    
    # 创建策略
    strategy = RSIStrategy(period=14, oversold=30, overbought=70)
    
    # 生成信号
    df_with_signals = strategy.generate_signal(df)
    
    print("\n📊 RSI 策略信号统计:")
    print(f"   超卖信号 (RSI<30): {df_with_signals['signal'].eq(1).sum()}")
    print(f"   超买信号 (RSI>70): {df_with_signals['signal'].eq(-1).sum()}")
    print(f"   极度超卖 (RSI<20): {df_with_signals['extreme_oversold'].sum()}")
    print(f"   极度超买 (RSI>80): {df_with_signals['extreme_overbought'].sum()}")
    print(f"   底背离信号：{df_with_signals['bullish_div'].sum()}")
    print(f"   顶背离信号：{df_with_signals['bearish_div'].sum()}")
    
    # 回测
    result = strategy.backtest(df, capital=100000)
    
    print("\n💰 RSI 策略回测结果:")
    print(f"   初始资金：{result['initial_capital']:,.0f} 元")
    print(f"   最终价值：{result['final_value']:,.0f} 元")
    print(f"   总收益率：{result['total_return_pct']}")
    print(f"   交易次数：{result['num_buy_trades']} 次买入 / {result['num_sell_trades']} 次卖出")
    print(f"   胜率：{result['win_rate']}")
    print(f"   最大回撤：{result['max_drawdown']}")
    print(f"   夏普比率：{result['sharpe_ratio']}")
    
    # 显示部分交易记录
    if result['trades']:
        print("\n📝 前 5 笔交易:")
        for i, trade in enumerate(result['trades'][:5]):
            extreme_marker = "⭐" if trade.get('is_extreme', False) else ""
            div_marker = "🔄" if trade.get('has_divergence', False) else ""
            markers = extreme_marker + div_marker
            print(f"   {i+1}. {trade['type']} @ {trade['price']:.2f} x {trade['shares']} 股 (RSI={trade['rsi']:.1f}) {markers}")
