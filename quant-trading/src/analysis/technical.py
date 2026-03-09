"""
技术分析模块
包含常用技术指标计算
"""
import pandas as pd
import numpy as np
from loguru import logger

try:
    import pandas_ta as ta
    HAS_TA = True
except ImportError:
    HAS_TA = False
    logger.warning("pandas_ta 未安装，使用基础指标计算")

class TechnicalAnalysis:
    """技术分析工具类"""
    
    @staticmethod
    def calculate_ma(df, windows=[5, 10, 20, 60]):
        """计算移动平均线"""
        for w in windows:
            df[f'ma{w}'] = df['close'].rolling(window=w).mean()
        return df
    
    @staticmethod
    def calculate_macd(df, fast=12, slow=26, signal=9):
        """计算 MACD 指标"""
        exp1 = df['close'].ewm(span=fast, adjust=False).mean()
        exp2 = df['close'].ewm(span=slow, adjust=False).mean()
        df['macd'] = exp1 - exp2
        df['signal'] = df['macd'].ewm(span=signal, adjust=False).mean()
        df['histogram'] = df['macd'] - df['signal']
        return df
    
    @staticmethod
    def calculate_rsi(df, period=14):
        """计算 RSI 指标"""
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        return df
    
    @staticmethod
    def calculate_bollinger(df, period=20, std_dev=2):
        """计算布林带"""
        df['bb_middle'] = df['close'].rolling(window=period).mean()
        std = df['close'].rolling(window=period).std()
        df['bb_upper'] = df['bb_middle'] + (std * std_dev)
        df['bb_lower'] = df['bb_middle'] - (std * std_dev)
        return df
    
    @staticmethod
    def calculate_kdj(df, n=9, m1=3, m2=3):
        """计算 KDJ 指标"""
        low_n = df['low'].rolling(window=n).min()
        high_n = df['high'].rolling(window=n).max()
        rsv = (df['close'] - low_n) / (high_n - low_n) * 100
        df['k'] = rsv.ewm(com=m1-1, adjust=False).mean()
        df['d'] = df['k'].ewm(com=m2-1, adjust=False).mean()
        df['j'] = 3 * df['k'] - 2 * df['d']
        return df
    
    @staticmethod
    def calculate_all(df):
        """计算所有技术指标"""
        logger.info("计算技术指标...")
        df = df.copy()
        df = TechnicalAnalysis.calculate_ma(df)
        df = TechnicalAnalysis.calculate_macd(df)
        df = TechnicalAnalysis.calculate_rsi(df)
        df = TechnicalAnalysis.calculate_bollinger(df)
        df = TechnicalAnalysis.calculate_kdj(df)
        logger.info(f"✅ 完成 {len(df.columns)} 个指标计算")
        return df
    
    @staticmethod
    def generate_signal(df):
        """
        生成简单的交易信号
        
        规则:
        - 买入：MA5 上穿 MA20 且 RSI<70
        - 卖出：MA5 下穿 MA20 或 RSI>80
        
        Returns:
            DataFrame: 添加 signal 列 (1=买入，-1=卖出，0=持有)
        """
        df = df.copy()
        df['signal'] = 0
        
        # MA 金叉死叉
        df['ma_cross'] = 0
        df.loc[df['ma5'] > df['ma20'], 'ma_cross'] = 1
        df.loc[df['ma5'] < df['ma20'], 'ma_cross'] = -1
        
        # 生成交叉信号
        df['cross_change'] = df['ma_cross'].diff()
        
        # 买入信号
        buy_condition = (df['cross_change'] == 2) & (df['rsi'] < 70)
        df.loc[buy_condition, 'signal'] = 1
        
        # 卖出信号
        sell_condition = ((df['cross_change'] == -2) | (df['rsi'] > 80))
        df.loc[sell_condition, 'signal'] = -1
        
        return df


# 测试
if __name__ == "__main__":
    # 创建测试数据
    np.random.seed(42)
    dates = pd.date_range('2026-01-01', periods=100, freq='D')
    df = pd.DataFrame({
        'date': dates,
        'open': np.random.uniform(10, 20, 100),
        'high': np.random.uniform(20, 25, 100),
        'low': np.random.uniform(8, 15, 100),
        'close': np.random.uniform(15, 22, 100),
        'volume': np.random.randint(1000, 10000, 100)
    })
    
    # 计算指标
    df = TechnicalAnalysis.calculate_all(df)
    print("\n📊 技术指标计算结果:")
    print(df[['date', 'close', 'ma5', 'ma20', 'macd', 'rsi']].tail(10))
    
    # 生成信号
    df = TechnicalAnalysis.generate_signal(df)
    signals = df[df['signal'] != 0]
    print(f"\n📈 生成 {len(signals)} 个交易信号:")
    print(signals[['date', 'close', 'signal']])
