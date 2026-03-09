"""
双均线策略模块
基于 MA 金叉/死叉的交易策略
"""
import pandas as pd
import numpy as np
from loguru import logger


class DualMAStrategy:
    """双均线交易策略"""
    
    def __init__(self, short_window=5, long_window=20):
        """
        初始化双均线策略
        
        Args:
            short_window: 短期均线周期 (天)
            long_window: 长期均线周期 (天)
        """
        self.short_window = short_window
        self.long_window = long_window
        logger.info(f"✅ 双均线策略初始化 (MA{short_window}/MA{long_window})")
    
    def calculate_ma(self, df):
        """
        计算双均线
        
        Args:
            df: 包含 OHLCV 数据的 DataFrame
        
        Returns:
            DataFrame: 添加 ma_short 和 ma_long 列
        """
        df = df.copy()
        df['ma_short'] = df['close'].rolling(window=self.short_window).mean()
        df['ma_long'] = df['close'].rolling(window=self.long_window).mean()
        return df
    
    def generate_signal(self, df):
        """
        生成交易信号
        
        规则:
        - 金叉 (Golden Cross): 短均线上穿长均线 → 买入信号 (1)
        - 死叉 (Death Cross): 短均线下穿长均线 → 卖出信号 (-1)
        - 其他情况 → 持有 (0)
        
        Returns:
            DataFrame: 添加 signal 列
        """
        df = self.calculate_ma(df)
        
        # 初始化信号
        df['signal'] = 0
        
        # 金叉：短均线从下向上穿过长均线
        golden_cross = (
            (df['ma_short'] > df['ma_long']) & 
            (df['ma_short'].shift(1) <= df['ma_long'].shift(1))
        )
        df.loc[golden_cross, 'signal'] = 1
        
        # 死叉：短均线从上向下穿过长均线
        death_cross = (
            (df['ma_short'] < df['ma_long']) & 
            (df['ma_short'].shift(1) >= df['ma_long'].shift(1))
        )
        df.loc[death_cross, 'signal'] = -1
        
        # 标记交叉点
        df['golden_cross'] = golden_cross
        df['death_cross'] = death_cross
        
        logger.info(f"📊 生成信号：{golden_cross.sum()} 个金叉，{death_cross.sum()} 个死叉")
        
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
                        'cost': cost
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
                    'revenue': revenue
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
        
        return {
            'initial_capital': capital,
            'final_value': final_value,
            'total_return': total_return,
            'total_return_pct': f"{total_return:.2%}",
            'num_buy_trades': len(buy_trades),
            'num_sell_trades': len(sell_trades),
            'win_rate': f"{win_rate:.2%}",
            'max_drawdown': f"{max_drawdown:.2%}",
            'trades': trades,
            'portfolio_values': portfolio_values
        }
    
    def plot_signals(self, df, title="双均线策略信号"):
        """
        可视化策略信号 (需要 matplotlib)
        
        Args:
            df: 包含信号的数据
            title: 图表标题
        """
        try:
            import matplotlib.pyplot as plt
            from matplotlib.font_manager import FontProperties
            
            # 设置中文字体
            plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
            plt.rcParams['axes.unicode_minus'] = False
            
            fig, axes = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
            
            # 上图：价格和均线
            ax1 = axes[0]
            ax1.plot(df.index, df['close'], label='收盘价', linewidth=1.5)
            ax1.plot(df.index, df['ma_short'], label=f'MA{self.short_window}', linewidth=1, alpha=0.8)
            ax1.plot(df.index, df['ma_long'], label=f'MA{self.long_window}', linewidth=1, alpha=0.8)
            
            # 标记买卖点
            buys = df[df['golden_cross'] == True]
            sells = df[df['death_cross'] == True]
            ax1.scatter(buys.index, buys['close'], color='red', marker='^', s=100, label='买入', zorder=5)
            ax1.scatter(sells.index, sells['close'], color='green', marker='v', s=100, label='卖出', zorder=5)
            
            ax1.set_ylabel('价格')
            ax1.set_title(title)
            ax1.legend(loc='upper left')
            ax1.grid(True, alpha=0.3)
            
            # 下图：信号
            ax2 = axes[1]
            ax2.fill_between(df.index, 0, df['signal'], where=df['signal']>0, 
                           alpha=0.3, color='red', label='持仓')
            ax2.plot(df.index, df['signal'], linewidth=1, color='gray')
            ax2.set_ylabel('信号')
            ax2.set_xlabel('日期')
            ax2.legend(loc='upper left')
            ax2.grid(True, alpha=0.3)
            ax2.set_ylim(-1.5, 1.5)
            
            plt.tight_layout()
            plt.show()
            
        except ImportError:
            logger.warning("matplotlib 未安装，无法绘制图表")


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
    strategy = DualMAStrategy(short_window=5, long_window=20)
    
    # 生成信号
    df_with_signals = strategy.generate_signal(df)
    
    print("\n📊 双均线策略信号统计:")
    print(f"   金叉次数：{df_with_signals['golden_cross'].sum()}")
    print(f"   死叉次数：{df_with_signals['death_cross'].sum()}")
    
    # 回测
    result = strategy.backtest(df, capital=100000)
    
    print("\n💰 回测结果:")
    print(f"   初始资金：{result['initial_capital']:,.0f} 元")
    print(f"   最终价值：{result['final_value']:,.0f} 元")
    print(f"   总收益率：{result['total_return_pct']}")
    print(f"   交易次数：{result['num_buy_trades']} 次买入 / {result['num_sell_trades']} 次卖出")
    print(f"   胜率：{result['win_rate']}")
    print(f"   最大回撤：{result['max_drawdown']}")
    
    # 显示部分交易记录
    if result['trades']:
        print("\n📝 前 5 笔交易:")
        for i, trade in enumerate(result['trades'][:5]):
            print(f"   {i+1}. {trade['type']} @ {trade['price']:.2f} x {trade['shares']} 股")
