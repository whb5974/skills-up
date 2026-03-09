#!/usr/bin/env python3
"""
智能调仓模块
根据目标配置和当前持仓，生成调仓建议
"""

import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / 'data'


class Rebalancer:
    """智能调仓器"""
    
    # 目标资产配置比例
    TARGET_ALLOCATION = {
        '股票': 0.40,
        '基金': 0.25,
        '债券': 0.15,
        '现金': 0.15,
        '另类': 0.05,
    }
    
    # 调仓阈值（偏离超过此值才调仓）
    REBALANCE_THRESHOLD = 0.05  # 5%
    
    def __init__(self):
        self.portfolio = self.load_portfolio()
    
    def load_portfolio(self):
        """加载持仓数据"""
        portfolio_file = DATA_DIR / 'portfolio.json'
        if portfolio_file.exists():
            with open(portfolio_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def get_current_allocation(self):
        """获取当前资产配置"""
        if not self.portfolio:
            return {}
        
        categories = {}
        total = 0
        
        # 统计持仓
        for symbol, pos in self.portfolio['positions'].items():
            cat = pos.get('category', '其他')
            if ' - ' in cat:
                cat = cat.split(' - ')[0]
            
            value = pos['shares'] * pos['current_price']
            categories[cat] = categories.get(cat, 0) + value
            total += value
        
        # 添加现金类
        cash_alloc = self.portfolio.get('cash_allocation', {})
        cash_value = cash_alloc.get('cash_money_market', 0) + self.portfolio.get('cash', 0)
        categories['现金'] = categories.get('现金', 0) + cash_value
        total += cash_value
        
        alt_value = cash_alloc.get('alternative', 0)
        categories['另类'] = categories.get('另类', 0) + alt_value
        total += alt_value
        
        # 计算比例
        allocation_pct = {}
        for cat, value in categories.items():
            allocation_pct[cat] = {
                'value': value,
                'percentage': value / total if total > 0 else 0
            }
        
        return {
            'total': total,
            'categories': allocation_pct
        }
    
    def analyze_deviation(self):
        """分析配置偏离"""
        current = self.get_current_allocation()
        if not current:
            return []
        
        deviations = []
        for target_cat, target_pct in self.TARGET_ALLOCATION.items():
            current_info = current['categories'].get(target_cat, {'value': 0, 'percentage': 0})
            current_pct = current_info['percentage']
            
            deviation = current_pct - target_pct
            deviation_pct = deviation * 100
            
            # 判断是否需要调仓
            needs_rebalance = abs(deviation) > self.REBALANCE_THRESHOLD
            
            # 计算调仓金额
            total = current['total']
            target_value = total * target_pct
            current_value = current_info['value']
            adjust_amount = target_value - current_value
            
            deviations.append({
                'category': target_cat,
                'target_pct': target_pct,
                'current_pct': current_pct,
                'deviation': deviation,
                'deviation_pct': deviation_pct,
                'needs_rebalance': needs_rebalance,
                'current_value': current_value,
                'target_value': target_value,
                'adjust_amount': adjust_amount,
                'action': self.get_action(adjust_amount)
            })
        
        return deviations
    
    def get_action(self, amount):
        """根据金额给出操作建议"""
        if abs(amount) < 100:  # 小于 100 元不调整
            return '保持'
        elif amount > 0:
            return f'买入 {amount:,.0f}元'
        else:
            return f'卖出 {abs(amount):,.0f}元'
    
    def generate_rebalance_plan(self):
        """生成调仓计划"""
        deviations = self.analyze_deviation()
        
        lines = []
        lines.append("=" * 70)
        lines.append("🔄 智能调仓建议")
        lines.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 70)
        lines.append("")
        
        # 总体情况
        total = sum(d['current_value'] for d in deviations)
        lines.append(f"💰 总资产：{total:,.2f} 元")
        lines.append(f"⚙️ 调仓阈值：{self.REBALANCE_THRESHOLD:.0%}")
        lines.append("")
        
        # 配置对比表
        lines.append("📊 配置对比:")
        lines.append("-" * 70)
        lines.append(f"{'类别':<10} {'目标':>10} {'当前':>10} {'偏离':>10} {'操作':>15} {'金额':>15}")
        lines.append("-" * 70)
        
        needs_action = []
        for d in deviations:
            target_str = f"{d['target_pct']:.1%}"
            current_str = f"{d['current_pct']:.1%}"
            deviation_str = f"{d['deviation_pct']:+.1f}%"
            action_icon = '⚠️' if d['needs_rebalance'] else '✅'
            
            lines.append(
                f"{d['category']:<10} {target_str:>10} {current_str:>10} "
                f"{deviation_str:>10} {action_icon} {d['action']:<15} {d['adjust_amount']:>+15,.0f}"
            )
            
            if d['needs_rebalance'] and abs(d['adjust_amount']) >= 100:
                needs_action.append(d)
        
        lines.append("-" * 70)
        lines.append("")
        
        # 具体操作建议
        if needs_action:
            lines.append("📋 建议操作:")
            lines.append("")
            
            # 需要买入的
            buys = [d for d in needs_action if d['adjust_amount'] > 0]
            if buys:
                lines.append("   💚 买入操作:")
                for d in buys:
                    lines.append(f"      • {d['category']}: 买入 {d['adjust_amount']:,.0f} 元")
                    lines.append(f"        当前：{d['current_pct']:.1f}% → 目标：{d['target_pct']:.1f}%")
                lines.append("")
            
            # 需要卖出的
            sells = [d for d in needs_action if d['adjust_amount'] < 0]
            if sells:
                lines.append("   🔴 卖出操作:")
                for d in sells:
                    lines.append(f"      • {d['category']}: 卖出 {abs(d['adjust_amount']):,.0f} 元")
                    lines.append(f"        当前：{d['current_pct']:.1f}% → 目标：{d['target_pct']:.1f}%")
                lines.append("")
        else:
            lines.append("✅ 当前配置合理，无需调仓")
            lines.append("")
        
        # 调仓提示
        lines.append("💡 调仓提示:")
        lines.append("   • 调仓会产生交易费用，请考虑成本")
        lines.append("   • 建议每季度或半年调仓一次")
        lines.append("   • 市场大幅波动后可考虑临时调仓")
        lines.append("   • 优先使用新增资金调仓，减少卖出操作")
        lines.append("")
        
        # 税费估算
        total_turnover = sum(abs(d['adjust_amount']) for d in needs_action) / 2
        estimated_fee = total_turnover * 0.001  # 假设 0.1% 费率
        lines.append(f"💰 预估调仓成本:")
        lines.append(f"   总调仓金额：{total_turnover * 2:,.0f} 元")
        lines.append(f"   预估手续费：{estimated_fee:,.2f} 元")
        lines.append("")
        
        lines.append("=" * 70)
        
        report = '\n'.join(lines)
        print(report)
        
        # 保存报告
        report_file = DATA_DIR.parent / 'reports' / f"rebalance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        report_file.parent.mkdir(exist_ok=True)
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report
    
    def quick_check(self):
        """快速检查是否需要调仓"""
        deviations = self.analyze_deviation()
        needs_rebalance = any(d['needs_rebalance'] for d in deviations)
        
        if needs_rebalance:
            issues = [d for d in deviations if d['needs_rebalance']]
            return {
                'needs_rebalance': True,
                'message': f"⚠️ 需要调仓！{len(issues)} 个类别偏离超过阈值",
                'issues': issues
            }
        else:
            return {
                'needs_rebalance': False,
                'message': "✅ 配置合理，无需调仓"
            }


if __name__ == "__main__":
    rebalancer = Rebalancer()
    
    # 快速检查
    check = rebalancer.quick_check()
    print(check['message'])
    print()
    
    # 详细调仓计划
    rebalancer.generate_rebalance_plan()
