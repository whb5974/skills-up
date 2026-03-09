#!/usr/bin/env python3
"""
自动检查脚本 - 每日运行
检查持仓盈亏、风险状况、生成日报
"""

import json
import csv
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent / 'data'
LOGS_DIR = Path(__file__).parent / 'logs'
LOGS_DIR.mkdir(exist_ok=True)


def load_portfolio():
    """加载持仓数据"""
    portfolio_file = DATA_DIR / 'portfolio.json'
    if portfolio_file.exists():
        with open(portfolio_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def generate_daily_report():
    """生成日报"""
    portfolio = load_portfolio()
    if not portfolio:
        return "❌ 未找到持仓数据，请先运行 init-portfolio.py"
    
    report = []
    report.append("=" * 60)
    report.append("📊 投资日报")
    report.append(f"日期：{datetime.now().strftime('%Y年%m月%d日 %A')}")
    report.append("=" * 60)
    
    # 总体情况
    initial = portfolio['initial_capital']
    invested = portfolio['total_invested']
    cash = portfolio['cash']
    
    # 计算持仓市值
    positions_value = sum(
        pos['shares'] * pos['current_price']
        for pos in portfolio['positions'].values()
    )
    
    # 现金类
    cash_total = cash + portfolio['cash_allocation'].get('cash_money_market', 0)
    alt_total = portfolio['cash_allocation'].get('alternative', 0)
    
    total_value = positions_value + cash_total + alt_total
    total_return = total_value - initial
    return_pct = (total_return / initial) * 100
    
    report.append("")
    report.append("💰 总体情况")
    report.append(f"   总资产：{total_value:,.2f} 元")
    report.append(f"   初始资金：{initial:,.2f} 元")
    report.append(f"   总收益：{total_return:+,.2f} 元 ({return_pct:+.2f}%)")
    report.append("")
    
    # 持仓明细
    report.append("📋 持仓明细")
    report.append("-" * 60)
    
    for symbol, pos in sorted(portfolio['positions'].items(), 
                               key=lambda x: x[1]['shares']*x[1]['current_price'], 
                               reverse=True):
        market_value = pos['shares'] * pos['current_price']
        cost_value = pos['shares'] * pos['cost_basis']
        profit = market_value - cost_value
        profit_pct = (profit / cost_value) * 100 if cost_value > 0 else 0
        weight = (market_value / total_value) * 100 if total_value > 0 else 0
        
        status = "📈" if profit >= 0 else "📉"
        report.append(f"   {status} {pos['name']}({symbol})")
        report.append(f"      持仓：{pos['shares']}股 | 现价：{pos['current_price']:.2f}元")
        report.append(f"      市值：{market_value:,.2f}元 ({weight:.1f}%)")
        report.append(f"      盈亏：{profit:+,.2f}元 ({profit_pct:+.2f}%)")
        report.append("")
    
    # 现金类
    report.append("💵 现金及另类")
    report.append(f"   可用现金：{cash:,.2f} 元")
    report.append(f"   货币基金：{cash_total:,.2f} 元")
    report.append(f"   另类投资：{alt_total:,.2f} 元")
    report.append("")
    
    # 风险提示
    report.append("⚠️ 风险提示")
    
    # 检查止损
    alerts = []
    for symbol, pos in portfolio['positions'].items():
        cost = pos['cost_basis']
        current = pos['current_price']
        loss_pct = (current - cost) / cost * 100
        
        if loss_pct < -15:
            alerts.append(f"🔴 {pos['name']} 亏损 {loss_pct:.1f}%，已触及止损线！")
        elif loss_pct < -10:
            alerts.append(f"🟠 {pos['name']} 亏损 {loss_pct:.1f}%，注意风险！")
        elif loss_pct < -5:
            alerts.append(f"🟡 {pos['name']} 亏损 {loss_pct:.1f}%，关注中")
        
        # 检查止盈
        if loss_pct > 30:
            alerts.append(f"✅ {pos['name']} 盈利 {loss_pct:.1f}%，考虑部分止盈")
    
    if alerts:
        for alert in alerts:
            report.append(f"   {alert}")
    else:
        report.append("   ✅ 无风险警示，持仓正常")
    
    report.append("")
    report.append("=" * 60)
    report.append("📌 今日操作建议")
    
    if return_pct < -10:
        report.append("   ⚠️ 组合亏损较大，建议检查是否触及止损线")
    elif return_pct > 20:
        report.append("   ✅ 收益良好，可考虑适度止盈锁定利润")
    else:
        report.append("   ✅ 组合运行正常，继续持有")
    
    report.append("")
    report.append("💡 提醒:")
    report.append("   • 每日查看不超过 3 次，避免过度关注")
    report.append("   • 关注财经新闻，但不要被短期波动影响")
    report.append("   • 严格执行止损纪律")
    report.append("=" * 60)
    
    # 保存报告
    report_text = '\n'.join(report)
    report_file = LOGS_DIR / f'daily_{datetime.now().strftime("%Y%m%d")}.txt'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    return report_text


if __name__ == "__main__":
    report = generate_daily_report()
    print(report)
    
    # 同时输出到文件
    print(f"\n📄 日报已保存至：{LOGS_DIR / f'daily_{datetime.now().strftime("%Y%m%d")}.txt'}")
