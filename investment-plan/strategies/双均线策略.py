"""
策略：双均线策略
描述：双均线策略示例
"""


# 双均线交易策略
# 金叉买入，死叉卖出

def generate_signals(prices, short_window=5, long_window=20):
    """
    生成交易信号
    
    参数:
        prices: 价格序列
        short_window: 短期均线周期
        long_window: 长期均线周期
    """
    signals = []
    short_ma = prices.rolling(window=short_window).mean()
    long_ma = prices.rolling(window=long_window).mean()
    
    position = 0
    for i in range(len(prices)):
        if short_ma[i] > long_ma[i] and position == 0:
            signals.append(1)  # 买入信号
            position = 1
        elif short_ma[i] < long_ma[i] and position == 1:
            signals.append(-1)  # 卖出信号
            position = 0
        else:
            signals.append(0)  # 持有
    
    return signals
