"""
策略：布林带策略
描述：布林带策略示例
"""


# 布林带交易策略
# 下轨买入，上轨卖出

def bollinger_bands(prices, window=20, num_std=2):
    """
    计算布林带
    
    参数:
        prices: 价格序列
        window: 均线周期
        num_std: 标准差倍数
    """
    middle = prices.rolling(window=window).mean()
    std = prices.rolling(window=window).std()
    upper = middle + num_std * std
    lower = middle - num_std * std
    return upper, middle, lower

def generate_signals(prices):
    """生成交易信号"""
    upper, middle, lower = bollinger_bands(prices)
    signals = []
    
    for i in range(len(prices)):
        if prices[i] < lower[i]:
            signals.append(1)  # 买入
        elif prices[i] > upper[i]:
            signals.append(-1)  # 卖出
        else:
            signals.append(0)  # 持有
    
    return signals
