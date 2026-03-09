#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
布林带策略模块
基于布林带上下轨的交易策略
"""

import pandas as pd
import numpy as np
from loguru import logger


class BollingerStrategy:
    """布林带交易策略"""
    
    def __init__(self, window=20, num_std=2):
        """
        初始化布林带策略
        
        Args:
            window: 均线周期 (默认 20)
            num_std: 标准差倍数 (默认 2)
        """
        self.window = window
        self.num_std = num_std
        logger.info(f"✅ 布林带策略初始化 (Window={window}, Std={num_std})")
    
    def calculate_bollinger(self, df):
        """
        计算布林带
        
        Args:
            df: 包含 OHLCV 数据的 DataFrame
        
        Returns:
            DataFrame: 添加 upper, middle, lower 列
        """
        df = df.copy()
        
        # 中轨 = 20 日均线
        df['middle'] = df['close'].rolling(window=self.window).mean()
        
        # 标准差
        std = df['close'].rolling(window=self.window).std()
        
        # 上轨 = 中轨 + 2 倍标准差
        df['upper'] = df['middle'] + (self.num_std * std)
        
        # 下轨 = 中轨 - 2 倍标准差
        df['lower'] = df['middle'] - (self.num_std * std)
        
        # 布林带宽度
        df['bandwidth'] = (df['upper'] - df['lower']) / df['middle']
        
        # %B 指标 (价格在布林带中的位置)
        df['percent_b'] = (df['close'] - df['lower']) / (df['upper'] - df['lower'])
        
        logger.info(f"📊 布林带指标计算完成")
        
        return df
    
    def generate_signal(self, df):
        """
        生成交易信号
        
        规则:
        - 价格触及下轨 → 超卖 → 买入信号 (1)
        - 价格触及上轨 → 超买 → 卖出信号 (-1)
        - 价格突破上轨 → 强势上涨 → 持仓
        - 价格跌破下轨 → 强势下跌 → 空仓
        
        Returns:
            DataFrame: 添加 signal 列
        """
        df = self.calculate_bollinger(df)
        
        # 初始化信号
        df['signal'] = 0
        
        # 买入信号：价格触及或跌破下轨 (超卖)
        oversold = df['close'] <= df['lower']
        df.loc[oversold, 'signal'] = 1
        
        # 卖出信号：价格触及或突破上轨 (超买)
        overbought = df['close'] >= df['upper']
        df.loc[overbought, 'signal'] = -1
        
        # 标记信号
        df['oversold'] = oversold
        df['overbought'] = overbought
        
        # %B 指标信号
        # %B < 0: 价格低于下轨，极度超卖
        # %B > 1: 价格高于上轨，极度超买
        df['extreme_oversold'] = df['percent_b'] < 0
        df['extreme_overbought'] = df['percent_b'] > 1
        
        logger.info(f"📊 生成信号：{oversold.sum()} 个超卖信号，{overbought.sum()} 个超买信号")
        
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
            percent_b = df.iloc[i]['percent_b']
            
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
                        'percent_b': percent_b,
                        'is_extreme': percent_b < 0  # 极度超卖
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
                    'percent_b': percent_b,
                    'is_extreme': percent_b > 1  # 极度超买
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
    strategy = BollingerStrategy(window=20, num_std=2)
    
    # 生成信号
    df_with_signals = strategy.generate_signal(df)
    
    print("\n📊 布林带策略信号统计:")
    print(f"   超卖信号：{df_with_signals['oversold'].sum()}")
    print(f"   超买信号：{df_with_signals['overbought'].sum()}")
    print(f"   极度超卖：%B < 0: {df_with_signals['extreme_oversold'].sum()}")
    print(f"   极度超买：%B > 1: {df_with_signals['extreme_overbought'].sum()}")
    
    # 回测
    result = strategy.backtest(df, capital=100000)
    
    print("\n💰 布林带策略回测结果:")
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
            print(f"   {i+1}. {trade['type']} @ {trade['price']:.2f} x {trade['shares']} 股 (B={trade['percent_b']:.2f}) {extreme_marker}")
