#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MACD 策略模块
基于 MACD 金叉/死叉的交易策略
"""

import pandas as pd
import numpy as np
from loguru import logger


class MACDStrategy:
    """MACD 交易策略"""
    
    def __init__(self, fast_period=12, slow_period=26, signal_period=9):
        """
        初始化 MACD 策略
        
        Args:
            fast_period: 快线 EMA 周期 (默认 12)
            slow_period: 慢线 EMA 周期 (默认 26)
            signal_period: 信号线 EMA 周期 (默认 9)
        """
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
        logger.info(f"✅ MACD 策略初始化 (EMA{fast_period}/{slow_period}/{signal_period})")
    
    def calculate_macd(self, df):
        """
        计算 MACD 指标
        
        Args:
            df: 包含 OHLCV 数据的 DataFrame
        
        Returns:
            DataFrame: 添加 DIF, DEA, MACD_bar 列
        """
        df = df.copy()
        
        # 计算 EMA
        ema_fast = df['close'].ewm(span=self.fast_period, adjust=False).mean()
        ema_slow = df['close'].ewm(span=self.slow_period, adjust=False).mean()
        
        # DIF = 快 EMA - 慢 EMA
        df['DIF'] = ema_fast - ema_slow
        
        # DEA = DIF 的 EMA
        df['DEA'] = df['DIF'].ewm(span=self.signal_period, adjust=False).mean()
        
        # MACD 柱状图 = (DIF - DEA) * 2
        df['MACD_bar'] = (df['DIF'] - df['DEA']) * 2
        
        logger.info(f"📊 MACD 指标计算完成")
        
        return df
    
    def generate_signal(self, df):
        """
        生成交易信号
        
        规则:
        - 金叉：DIF 从下向上穿过 DEA → 买入信号 (1)
        - 死叉：DIF 从上向下穿过 DEA → 卖出信号 (-1)
        - 零轴上方金叉：强势买入信号
        - 零轴下方死叉：强势卖出信号
        
        Returns:
            DataFrame: 添加 signal 列
        """
        df = self.calculate_macd(df)
        
        # 初始化信号
        df['signal'] = 0
        
        # 金叉：DIF 从下向上穿过 DEA
        golden_cross = (
            (df['DIF'] > df['DEA']) & 
            (df['DIF'].shift(1) <= df['DEA'].shift(1))
        )
        df.loc[golden_cross, 'signal'] = 1
        
        # 死叉：DIF 从上向下穿过 DEA
        death_cross = (
            (df['DIF'] < df['DEA']) & 
            (df['DIF'].shift(1) >= df['DEA'].shift(1))
        )
        df.loc[death_cross, 'signal'] = -1
        
        # 零轴位置标记
        df['above_zero'] = df['DIF'] > 0
        
        # 强势信号 (零轴上方金叉)
        df['strong_golden'] = golden_cross & df['above_zero']
        
        # 弱势信号 (零轴下方死叉)
        df['strong_death'] = death_cross & ~df['above_zero']
        
        logger.info(f"📊 生成信号：{golden_cross.sum()} 个金叉，{death_cross.sum()} 个死叉")
        logger.info(f"📊 强势金叉：{df['strong_golden'].sum()} 个，弱势死叉：{df['strong_death'].sum()} 个")
        
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
            
            # 买入信号
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
                        'is_strong': df.iloc[i]['strong_golden']
                    })
            
            # 卖出信号
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
                    'is_strong': df.iloc[i]['strong_death']
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
        
        # 计算夏普比率 (简化版)
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
    
    def compare_with_dual_ma(self, df, dual_ma_result):
        """
        与双均线策略对比
        
        Args:
            df: 数据
            dual_ma_result: 双均线策略回测结果
        
        Returns:
            dict: 对比结果
        """
        macd_result = self.backtest(df)
        
        comparison = {
            'MACD': macd_result,
            'DualMA': dual_ma_result,
            'comparison': {
                'return_diff': macd_result['total_return'] - dual_ma_result['total_return'],
                'win_rate_diff': float(macd_result['win_rate'].strip('%')) - float(dual_ma_result['win_rate'].strip('%')),
                'drawdown_diff': float(macd_result['max_drawdown'].strip('%')) - float(dual_ma_result['max_drawdown'].strip('%'))
            }
        }
        
        return comparison


# 测试
if __name__ == "__main__":
    # 创建测试数据 (模拟股价走势)
    np.random.seed(42)
    dates = pd.date_range('2025-01-01', periods=252, freq='D')
    
    # 生成带趋势的随机游走
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
    strategy = MACDStrategy(fast_period=12, slow_period=26, signal_period=9)
    
    # 生成信号
    df_with_signals = strategy.generate_signal(df)
    
    print("\n📊 MACD 策略信号统计:")
    print(f"   金叉次数：{df_with_signals['signal'].eq(1).sum()}")
    print(f"   死叉次数：{df_with_signals['signal'].eq(-1).sum()}")
    print(f"   强势金叉：{df_with_signals['strong_golden'].sum()}")
    print(f"   弱势死叉：{df_with_signals['strong_death'].sum()}")
    
    # 回测
    result = strategy.backtest(df, capital=100000)
    
    print("\n💰 MACD 策略回测结果:")
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
            strong_marker = "⭐" if trade.get('is_strong', False) else ""
            print(f"   {i+1}. {trade['type']} @ {trade['price']:.2f} x {trade['shares']} 股 {strong_marker}")
