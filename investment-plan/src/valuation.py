#!/usr/bin/env python3
"""
估值分析模块
计算 PE、PB、PEG 等估值指标，判断股票是否低估/高估
"""

import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / 'data'


class ValuationAnalyzer:
    """估值分析器"""
    
    # A 股主要行业平均 PE 参考值（简化版）
    INDUSTRY_PE = {
        '银行': 5.5,
        '保险': 8.0,
        '证券': 15.0,
        '白酒': 25.0,
        '食品饮料': 30.0,
        '医药': 35.0,
        '科技': 40.0,
        '新能源': 35.0,
        '消费': 25.0,
        '地产': 8.0,
        '基建': 10.0,
        '制造': 20.0,
    }
    
    # 合理 PEG 范围
    PEG_LOW = 0.5
    PEG_HIGH = 1.5
    
    def __init__(self):
        self.portfolio = self.load_portfolio()
    
    def load_portfolio(self):
        """加载持仓数据"""
        portfolio_file = DATA_DIR / 'portfolio.json'
        if portfolio_file.exists():
            with open(portfolio_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def estimate_pe(self, symbol, name):
        """
        估算 PE（简化版，实际需要接入财务数据）
        
        基于行业和经验估算
        """
        # 根据股票名称判断行业
        industry = '其他'
        if any(kw in name for kw in ['银行', '保险', '券商', '证券']):
            industry = '金融'
            pe = 6.0
        elif any(kw in name for kw in ['茅台', '五粮液', '酒']):
            industry = '白酒'
            pe = 28.0
        elif any(kw in name for kw in ['药', '医疗', '生物']):
            industry = '医药'
            pe = 30.0
        elif any(kw in name for kw in ['科技', '电子', '芯片', '半导体']):
            industry = '科技'
            pe = 35.0
        elif any(kw in name for kw in ['能源', '光伏', '锂电', '电池']):
            industry = '新能源'
            pe = 30.0
        elif any(kw in name for kw in ['消费', '食品', '零售']):
            industry = '消费'
            pe = 22.0
        elif 'ETF' in name:
            industry = '指数基金'
            pe = 12.0  # 宽基指数平均
        else:
            pe = 15.0  # 默认
        
        return {
            'industry': industry,
            'estimated_pe': pe,
            'pe_range': (pe * 0.7, pe * 1.3)  # 合理区间
        }
    
    def analyze_valuation(self, symbol, pos):
        """
        分析单只股票的估值
        
        Returns:
            dict: 估值分析结果
        """
        name = pos['name']
        current_price = pos['current_price']
        
        # 获取估算 PE
        pe_info = self.estimate_pe(symbol, name)
        
        # 计算估值状态
        estimated_pe = pe_info['estimated_pe']
        pe_low, pe_high = pe_info['pe_range']
        
        # 假设每股收益（简化）
        eps = current_price / estimated_pe if estimated_pe > 0 else 0
        
        # 估值判断
        if estimated_pe < pe_low:
            valuation_status = '低估'
            status_icon = '🟢'
        elif estimated_pe > pe_high:
            valuation_status = '高估'
            status_icon = '🔴'
        else:
            valuation_status = '合理'
            status_icon = '🟡'
        
        # PB 估算（简化：假设 ROE=15%）
        roe = 0.15
        pb = estimated_pe * roe
        pb_status = '合理'
        if pb < 1:
            pb_status = '低估'
        elif pb > 3:
            pb_status = '高估'
        
        # PEG 估算（假设增长率=15%）
        growth = 0.15
        peg = estimated_pe / (growth * 100) if growth > 0 else 0
        peg_status = '合理'
        if peg < self.PEG_LOW:
            peg_status = '低估'
        elif peg > self.PEG_HIGH:
            peg_status = '高估'
        
        return {
            'symbol': symbol,
            'name': name,
            'price': current_price,
            'estimated_pe': estimated_pe,
            'pe_range': pe_info['pe_range'],
            'eps': eps,
            'valuation_status': valuation_status,
            'status_icon': status_icon,
            'estimated_pb': pb,
            'pb_status': pb_status,
            'peg': peg,
            'peg_status': peg_status,
            'industry': pe_info['industry'],
            'suggestion': self.get_suggestion(valuation_status)
        }
    
    def get_suggestion(self, valuation_status):
        """根据估值给出建议"""
        suggestions = {
            '低估': '✅ 估值较低，可考虑加仓',
            '合理': '✅ 估值合理，继续持有',
            '高估': '⚠️ 估值偏高，考虑减仓或止盈'
        }
        return suggestions.get(valuation_status, '')
    
    def analyze_all(self):
        """分析所有持仓的估值"""
        if not self.portfolio:
            return []
        
        results = []
        for symbol, pos in self.portfolio['positions'].items():
            result = self.analyze_valuation(symbol, pos)
            results.append(result)
        
        # 按估值状态排序
        status_order = {'低估': 0, '合理': 1, '高估': 2}
        results.sort(key=lambda x: status_order.get(x['valuation_status'], 1))
        
        return results
    
    def print_report(self):
        """打印估值分析报告"""
        results = self.analyze_all()
        
        if not results:
            return "❌ 无持仓数据"
        
        lines = []
        lines.append("=" * 70)
        lines.append("📊 持仓估值分析报告")
        lines.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 70)
        lines.append("")
        
        # 统计
        undervalued = [r for r in results if r['valuation_status'] == '低估']
        fair = [r for r in results if r['valuation_status'] == '合理']
        overvalued = [r for r in results if r['valuation_status'] == '高估']
        
        lines.append(f"📈 估值分布:")
        lines.append(f"   🟢 低估：{len(undervalued)} 只")
        lines.append(f"   🟡 合理：{len(fair)} 只")
        lines.append(f"   🔴 高估：{len(overvalued)} 只")
        lines.append("")
        
        lines.append("📋 详细分析:")
        lines.append("-" * 70)
        lines.append(f"{'代码':<8} {'名称':<12} {'价格':>8} {'PE':>8} {'PB':>6} {'PEG':>6} {'估值':>8} {'建议':>20}")
        lines.append("-" * 70)
        
        for r in results:
            icon = r['status_icon']
            pe_str = f"{r['estimated_pe']:.1f}"
            pb_str = f"{r['estimated_pb']:.1f}"
            peg_str = f"{r['peg']:.2f}"
            
            lines.append(
                f"{r['symbol']:<8} {r['name'][:12]:<12} {r['price']:>8.2f} "
                f"{pe_str:>8} {pb_str:>6} {peg_str:>6} "
                f"{icon} {r['valuation_status']:<6} {r['suggestion'][:20]}"
            )
        
        lines.append("-" * 70)
        lines.append("")
        
        # 操作建议
        lines.append("💡 操作建议:")
        if undervalued:
            lines.append("   🟢 低估标的（可关注加仓机会）:")
            for r in undervalued:
                lines.append(f"      • {r['name']}({r['symbol']}) - PE:{r['estimated_pe']:.1f}")
        
        if overvalued:
            lines.append("   🔴 高估标的（考虑减仓止盈）:")
            for r in overvalued:
                lines.append(f"      • {r['name']}({r['symbol']}) - PE:{r['estimated_pe']:.1f}")
        
        lines.append("")
        lines.append("⚠️ 说明:")
        lines.append("   • PE/PB 为估算值，实际数据请查阅财报")
        lines.append("   • 估值仅供参考，需结合基本面综合判断")
        lines.append("   • 低估值不代表立即上涨，高估值不代表立即下跌")
        lines.append("=" * 70)
        
        report = '\n'.join(lines)
        print(report)
        
        # 保存报告
        report_file = DATA_DIR.parent / 'reports' / f"valuation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        report_file.parent.mkdir(exist_ok=True)
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report


if __name__ == "__main__":
    analyzer = ValuationAnalyzer()
    analyzer.print_report()
