"""
动量策略模块
基于价格动量和趋势的交易策略
"""
import pandas as pd
import numpy as np
from loguru import logger

class MomentumStrategy:
    """动量交易策略"""
    
    def __init__(self, lookback_period=20, threshold=0.05):
        """
        初始化动量策略
        
        Args:
            lookback_period: 回看周期 (天)
            threshold: 动量阈值 (超过此值才交易)
        """
        self.lookback = lookback_period
        self.threshold = threshold
        logger.info(f"✅ 动量策略初始化 (回看:{lookback_period}天，阈值:{threshold:.1%})")
    
    def calculate_momentum(self, prices):
        """
        计算动量指标
        
        Returns:
            Series: 动量值
        """
        momentum = prices.pct_change(periods=self.lookback)
        return momentum
    
    def generate_signal(self, df):
        """
        生成交易信号
        
        规则:
        - 动量 > 阈值 且 价格在 MA20 之上 → 买入
        - 动量 < -阈值 或 价格跌破 MA20 → 卖出
        
        Returns:
            DataFrame: 添加 signal 列
        """
        df = df.copy()
        
        # 计算动量
        df['momentum'] = self.calculate_momentum(df['close'])
        
        # 计算 MA20
        df['ma20'] = df['close'].rolling(window=20).mean()
        
        # 初始化信号
        df['signal'] = 0
        
        # 买入条件
        buy_condition = (
            (df['momentum'] > self.threshold) & 
            (df['close'] > df['ma20'])
        )
        df.loc[buy_condition, 'signal'] = 1
        
        # 卖出条件
        sell_condition = (
            (df['momentum'] < -self.threshold) | 
            (df['close'] < df['ma20'])
        )
        df.loc[sell_condition, 'signal'] = -1
        
        # 只保留信号变化点
        df['signal_change'] = df['signal'].diff()
        
        return df
    
    def backtest(self, df, capital=100000, commission=0.001):
        """
        简单回测
        
        Args:
            df: 包含 OHLCV 数据的 DataFrame
            capital: 初始资金
            commission: 手续费率
        
        Returns:
            dict: 回测结果
        """
        df = self.generate_signal(df).copy()
        
        # 持仓和资金
        position = 0
        cash = capital
        trades = []
        
        for i in range(1, len(df)):
            signal = df.iloc[i]['signal']
            price = df.iloc[i]['close']
            
            # 买入
            if signal == 1 and position == 0:
                shares = int(cash * 0.95 / price)  # 用 95% 资金
                if shares > 0:
                    cost = shares * price * (1 + commission)
                    cash -= cost
                    position = shares
                    trades.append({
                        'date': df.index[i],
                        'type': 'BUY',
                        'price': price,
                        'shares': shares,
                        'cash': cash
                    })
            
            # 卖出
            elif signal == -1 and position > 0:
                revenue = position * price * (1 - commission)
                cash += revenue
                trades.append({
                    'date': df.index[i],
                    'type': 'SELL',
                    'price': price,
                    'shares': position,
                    'cash': cash
                })
                position = 0
        
        # 计算最终价值
        final_price = df.iloc[-1]['close']
        final_value = cash + (position * final_price)
        
        # 计算收益率
        total_return = (final_value - capital) / capital
        
        # 计算交易次数
        buy_trades = [t for t in trades if t['type'] == 'BUY']
        
        return {
            'initial_capital': capital,
            'final_value': final_value,
            'total_return': total_return,
            'total_return_pct': f"{total_return:.2%}",
            'num_trades': len(buy_trades),
            'trades': trades
        }


# 测试
if __name__ == "__main__":
    # 创建测试数据
    np.random.seed(42)
    dates = pd.date_range('2025-01-01', periods=252, freq='D')
    prices = 100 + np.cumsum(np.random.randn(252))
    
    df = pd.DataFrame({
        'open': prices + np.random.randn(252),
        'high': prices + np.abs(np.random.randn(252)),
        'low': prices - np.abs(np.random.randn(252)),
        'close': prices,
        'volume': np.random.randint(1000, 10000, 252)
    }, index=dates)
    
    # 回测
    strategy = MomentumStrategy(lookback_period=20, threshold=0.05)
    result = strategy.backtest(df, capital=100000)
    
    print("\n📊 动量策略回测结果:")
    print(f"   初始资金：{result['initial_capital']:,.0f} 元")
    print(f"   最终价值：{result['final_value']:,.0f} 元")
    print(f"   总收益率：{result['total_return_pct']}")
    print(f"   交易次数：{result['num_trades']} 次")
