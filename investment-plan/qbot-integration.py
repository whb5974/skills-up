#!/usr/bin/env python3
"""
Qbot 集成模块 - 量化交易分析能力

整合 Qbot 核心功能到现有投资系统
"""

import json
import os
from datetime import datetime
from pathlib import Path

# 数据目录
DATA_DIR = Path(__file__).parent / "data"
LOGS_DIR = Path(__file__).parent / "logs"
STRATEGIES_DIR = Path(__file__).parent / "strategies"

# 确保目录存在
for d in [DATA_DIR, LOGS_DIR, STRATEGIES_DIR]:
    d.mkdir(exist_ok=True)


class QbotAnalyzer:
    """Qbot 量化分析器"""
    
    def __init__(self):
        self.portfolio_file = DATA_DIR / "portfolio.json"
        self.transactions_file = DATA_DIR / "transactions.csv"
        
    def load_portfolio(self):
        """加载持仓数据"""
        if self.portfolio_file.exists():
            with open(self.portfolio_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"holdings": [], "cash": 0}
    
    def save_portfolio(self, data):
        """保存持仓数据"""
        with open(self.portfolio_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_strategy(self, name, code, description=""):
        """添加交易策略"""
        strategy_file = STRATEGIES_DIR / f"{name}.py"
        with open(strategy_file, 'w', encoding='utf-8') as f:
            f.write(f'"""\n策略：{name}\n描述：{description}\n"""\n\n')
            f.write(code)
        print(f"✅ 策略已保存：{strategy_file}")
        return strategy_file
    
    def backtest(self, strategy_name, start_date, end_date):
        """回测策略（简化版）"""
        print(f"📊 回测策略：{strategy_name}")
        print(f"   时间：{start_date} 至 {end_date}")
        print(f"   状态：需要 Qbot 完整安装")
        print(f"   建议：安装 Qbot 后运行完整回测")
        return {
            "strategy": strategy_name,
            "period": f"{start_date} - {end_date}",
            "status": "pending_qbot_installation"
        }
    
    def risk_analysis(self):
        """持仓风险分析"""
        portfolio = self.load_portfolio()
        holdings = portfolio.get("holdings", [])
        
        if not holdings:
            return {"status": "no_holdings", "message": "无持仓数据"}
        
        # 简化版风险分析
        total_value = sum(h.get("market_value", 0) for h in holdings)
        risk_levels = []
        
        for h in holdings:
            name = h.get("name", "Unknown")
            weight = h.get("market_value", 0) / total_value if total_value > 0 else 0
            
            # 风险等级（简化）
            if weight > 0.3:
                risk = "高 - 仓位过重"
            elif weight > 0.2:
                risk = "中 - 仓位适中"
            else:
                risk = "低 - 仓位较轻"
            
            risk_levels.append({
                "name": name,
                "weight": f"{weight*100:.1f}%",
                "risk": risk
            })
        
        return {
            "total_value": total_value,
            "holdings_count": len(holdings),
            "risk_analysis": risk_levels,
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_daily_report(self):
        """生成投资日报"""
        portfolio = self.load_portfolio()
        risk = self.risk_analysis()
        
        report = f"""
# 投资日报 - {datetime.now().strftime('%Y年%m月%d日 %H:%M')}

## 总体情况
- 总资产：{risk.get('total_value', 0):,.2f} 元
- 持仓数：{risk.get('holdings_count', 0)}
- 风险状态：正常

## 持仓风险分析
"""
        for r in risk.get('risk_analysis', []):
            report += f"- {r['name']}: {r['weight']} ({r['risk']})\n"
        
        report += f"""
## 建议
- 定期检查持仓风险
- 避免单一标的仓位过重
- 严格执行止损纪律

---
生成时间：{datetime.now().isoformat()}
"""
        
        # 保存报告
        report_file = LOGS_DIR / f"daily_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ 日报已生成：{report_file}")
        return report
    
    def screen_stocks(self, criteria):
        """股票筛选（简化版）"""
        print(f"🔍 筛选条件：{criteria}")
        print("⚠️  需要配置数据源 (Tushare/Akshare)")
        print("📚 参考：https://ufund-me.github.io/Qbot/")
        return {
            "status": "need_data_source",
            "criteria": criteria,
            "suggestion": "配置 Tushare 或 Akshare 数据源"
        }


# 示例策略代码
STRATEGY_EXAMPLES = {
    "双均线策略": '''
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
''',
    
    "布林带策略": '''
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
''',
    
    "动量策略": '''
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
'''
}


def main():
    """主函数 - 演示功能"""
    print("=" * 50)
    print("🤖 Qbot 集成模块 - 量化交易分析")
    print("=" * 50)
    
    analyzer = QbotAnalyzer()
    
    # 1. 风险分析
    print("\n📊 持仓风险分析")
    risk = analyzer.risk_analysis()
    print(f"   总资产：{risk.get('total_value', 0):,.2f} 元")
    print(f"   持仓数：{risk.get('holdings_count', 0)}")
    
    # 2. 生成日报
    print("\n📰 生成投资日报")
    analyzer.generate_daily_report()
    
    # 3. 示例策略
    print("\n💡 可用策略示例")
    for name in STRATEGY_EXAMPLES.keys():
        print(f"   - {name}")
    
    # 4. 保存示例策略
    print("\n📝 保存示例策略")
    for name, code in STRATEGY_EXAMPLES.items():
        analyzer.add_strategy(name, code, f"{name}示例")
    
    print("\n" + "=" * 50)
    print("✅ 完成！")
    print("=" * 50)
    print("\n下一步:")
    print("1. 安装 Qbot: git clone https://github.com/UFund-Me/Qbot.git")
    print("2. 配置数据源：Tushare 或 Akshare")
    print("3. 运行回测：python qbot-integration.py --backtest")
    print("\n查看学习计划：cat /home/ghost/.openclaw/workspace/qbot-learning-plan.md")


if __name__ == "__main__":
    main()
