#!/usr/bin/env python3
"""
投资组合初始化脚本 - 无需外部依赖
自动创建示例持仓（按 2026 投资计划配置）
"""

import json
import csv
import os
from datetime import datetime
from pathlib import Path

# 配置
INITIAL_CAPITAL = 100000  # 初始资金 10 万元
DATA_DIR = Path(__file__).parent / 'data'
REPORTS_DIR = DATA_DIR / 'reports'

# 创建目录
DATA_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# 按投资计划配置的示例持仓
# 股票 40% = 40000 元
# 基金 25% = 25000 元
# 债券 15% = 15000 元
# 现金 15% = 15000 元
# 另类 5% = 5000 元

SAMPLE_POSITIONS = {
    # 股票类 (40% = 40,000 元)
    '600519': {'name': '贵州茅台', 'shares': 20, 'cost_basis': 1800.00, 'current_price': 1800.00, 'category': '股票 - 蓝筹'},  # 36,000 元
    '600036': {'name': '招商银行', 'shares': 100, 'cost_basis': 35.00, 'current_price': 35.00, 'category': '股票 - 蓝筹'},  # 3,500 元
    
    # 基金类 (25% = 25,000 元) - 用 ETF 模拟
    '510300': {'name': '沪深 300ETF', 'shares': 3000, 'cost_basis': 3.80, 'current_price': 3.80, 'category': '基金 - 宽基'},  # 11,400 元
    '510500': {'name': '中证 500ETF', 'shares': 2000, 'cost_basis': 5.50, 'current_price': 5.50, 'category': '基金 - 宽基'},  # 11,000 元
    '512660': {'name': '军工 ETF', 'shares': 300, 'cost_basis': 8.50, 'current_price': 8.50, 'category': '基金 - 行业'},  # 2,550 元
    
    # 债券类 (15% = 15,000 元) - 用债券 ETF 模拟
    '511260': {'name': '国债 ETF', 'shares': 150, 'cost_basis': 100.00, 'current_price': 100.00, 'category': '债券'},  # 15,000 元
}

# 现金和另类投资单独记录
CASH_ALLOCATION = {
    'cash_money_market': 15000,  # 货币基金
    'alternative': 5000,  # 另类投资（黄金/REITs 等）
}


def init_portfolio():
    """初始化投资组合"""
    print("\n" + "="*60)
    print("🚀 2026 投资组合初始化")
    print("="*60)
    
    # 计算总投入
    positions_total = sum(
        pos['shares'] * pos['cost_basis'] 
        for pos in SAMPLE_POSITIONS.values()
    )
    cash_total = sum(CASH_ALLOCATION.values())
    total_invested = positions_total + cash_total
    
    print(f"\n📊 配置概览:")
    print(f"   初始资金：{INITIAL_CAPITAL:,.2f} 元")
    print(f"   股票持仓：{positions_total:,.2f} 元")
    print(f"   现金/另类：{cash_total:,.2f} 元")
    print(f"   总计投入：{total_invested:,.2f} 元")
    print(f"   剩余现金：{INITIAL_CAPITAL - total_invested:,.2f} 元")
    
    # 创建持仓数据
    portfolio = {
        'cash': INITIAL_CAPITAL - total_invested,
        'cash_allocation': CASH_ALLOCATION,
        'positions': SAMPLE_POSITIONS,
        'start_date': datetime.now().strftime('%Y-%m-%d'),
        'initial_capital': INITIAL_CAPITAL,
        'total_invested': total_invested,
    }
    
    # 保存持仓
    portfolio_file = DATA_DIR / 'portfolio.json'
    with open(portfolio_file, 'w', encoding='utf-8') as f:
        json.dump(portfolio, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 持仓数据已保存：{portfolio_file}")
    
    # 创建交易记录
    transactions_file = DATA_DIR / 'transactions.csv'
    with open(transactions_file, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['date', 'type', 'symbol', 'name', 'price', 'shares', 'amount', 'fee', 'note', 'category']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        # 写入初始建仓记录
        for symbol, pos in SAMPLE_POSITIONS.items():
            amount = pos['shares'] * pos['cost_basis']
            writer.writerow({
                'date': datetime.now().strftime('%Y-%m-%d'),
                'type': 'BUY',
                'symbol': symbol,
                'name': pos['name'],
                'price': pos['cost_basis'],
                'shares': pos['shares'],
                'amount': amount,
                'fee': 0,
                'note': '初始建仓',
                'category': pos['category']
            })
        
        # 写入现金配置记录
        writer.writerow({
            'date': datetime.now().strftime('%Y-%m-%d'),
            'type': 'ALLOCATE',
            'symbol': 'CASH',
            'name': '货币基金',
            'price': 1.0,
            'shares': CASH_ALLOCATION['cash_money_market'],
            'amount': CASH_ALLOCATION['cash_money_market'],
            'fee': 0,
            'note': '现金配置',
            'category': '现金'
        })
        
        writer.writerow({
            'date': datetime.now().strftime('%Y-%m-%d'),
            'type': 'ALLOCATE',
            'symbol': 'ALT',
            'name': '另类投资',
            'price': 1.0,
            'shares': CASH_ALLOCATION['alternative'],
            'amount': CASH_ALLOCATION['alternative'],
            'fee': 0,
            'note': '另类投资配置（黄金/REITs）',
            'category': '另类'
        })
    
    print(f"✅ 交易记录已保存：{transactions_file}")
    
    # 生成配置报告
    print("\n" + "="*60)
    print("📋 资产配置明细")
    print("="*60)
    
    # 按类别统计
    categories = {}
    for symbol, pos in SAMPLE_POSITIONS.items():
        cat = pos['category'].split(' - ')[0] if ' - ' in pos['category'] else pos['category']
        if cat not in categories:
            categories[cat] = 0
        categories[cat] += pos['shares'] * pos['cost_basis']
    
    for cat, amount in CASH_ALLOCATION.items():
        cat_name = '现金' if 'cash' in cat else '另类'
        if cat_name not in categories:
            categories[cat_name] = 0
        categories[cat_name] += amount
    
    print(f"\n{'类别':<15} {'金额 (元)':>12} {'占比':>10} {'计划占比':>10}")
    print("-"*50)
    
    category_map = {
        '股票': '股票 40%',
        '基金': '基金 25%',
        '债券': '债券 15%',
        '现金': '现金 15%',
        '另类': '另类 5%'
    }
    
    for cat, amount in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        pct = (amount / total_invested) * 100
        plan = category_map.get(cat, 'N/A')
        print(f"{cat:<15} {amount:>12,.2f} {pct:>9.1f}% {plan:>10}")
    
    print("-"*50)
    print(f"{'总计':<15} {total_invested:>12,.2f} {100:>9.1f}%")
    
    # 保存报告
    report_file = REPORTS_DIR / f'init_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"2026 投资组合初始化报告\n")
        f.write(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"初始资金：{INITIAL_CAPITAL:,.2f} 元\n")
        f.write(f"总投入：{total_invested:,.2f} 元\n")
        f.write(f"\n持仓数量：{len(SAMPLE_POSITIONS)} 只\n")
        for symbol, pos in SAMPLE_POSITIONS.items():
            f.write(f"  {pos['name']}({symbol}): {pos['shares']}股 @ {pos['cost_basis']:.2f}元 = {pos['shares']*pos['cost_basis']:,.2f}元\n")
    
    print(f"\n✅ 初始化报告已保存：{report_file}")
    
    print("\n" + "="*60)
    print("✅ 投资组合初始化完成！")
    print("="*60)
    print("\n📌 下一步:")
    print("   1. 查看持仓：cat data/portfolio.json")
    print("   2. 查看交易记录：cat data/transactions.csv")
    print("   3. 更新价格后运行：python3 portfolio-tracker.py --report")
    print("="*60 + "\n")
    
    return portfolio


if __name__ == "__main__":
    init_portfolio()
