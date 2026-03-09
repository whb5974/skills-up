"""
策略：动量策略
描述：动量策略示例
"""


# 动量交易策略
# 买入强势股，卖出弱势股

def momentum_strategy(prices, lookback=20):
    """
    动量策略
    
    参数:
        prices: 价格序列
        lookback: 回看周期
    """
    momentum = prices.pct_change(periods=lookback)
    signals = []
    
    for i in range(len(momentum)):
        if momentum[i] > 0.1:  # 涨幅超过 10%
            signals.append(1)  # 买入
        elif momentum[i] < -0.1:  # 跌幅超过 10%
            signals.append(-1)  # 卖出
        else:
            signals.append(0)  # 持有
    
    return signals
