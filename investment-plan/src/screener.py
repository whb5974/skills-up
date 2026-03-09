#!/usr/bin/env python3
"""
股票筛选模块
根据基本面、技术面、估值等条件筛选股票
"""

from datetime import datetime
from pathlib import Path

REPORTS_DIR = Path(__file__).parent.parent / 'reports'


class StockScreener:
    """股票筛选器"""
    
    # 预设筛选条件
    SCREEN_PRESETS = {
        '价值股': {
            'pe_max': 15,
            'pb_max': 2,
            'dividend_yield_min': 0.03,
            'roe_min': 0.10,
        },
        '成长股': {
            'revenue_growth_min': 0.20,
            'profit_growth_min': 0.25,
            'pe_max': 40,
        },
        '蓝筹股': {
            'market_cap_min': 10000000000,  # 100 亿
            'roe_min': 0.15,
            'debt_ratio_max': 0.60,
            'pe_max': 25,
        },
        '高股息': {
            'dividend_yield_min': 0.05,
            'payout_ratio_max': 0.70,
            'consecutive_years_min': 3,
        },
        '低估值': {
            'pe_percentile_max': 30,  # PE 历史百分位
            'pb_percentile_max': 30,
        },
    }
    
    def __init__(self):
        self.stock_pool = self.get_default_stock_pool()
    
    def get_default_stock_pool(self):
        """获取默认股票池（简化版）"""
        return [
            {'symbol': '600519', 'name': '贵州茅台', 'industry': '白酒', 'pe': 30, 'pb': 10, 'roe': 0.30, 'dividend_yield': 0.015},
            {'symbol': '600036', 'name': '招商银行', 'industry': '银行', 'pe': 7, 'pb': 1.2, 'roe': 0.17, 'dividend_yield': 0.035},
            {'symbol': '601318', 'name': '中国平安', 'industry': '保险', 'pe': 9, 'pb': 1.5, 'roe': 0.18, 'dividend_yield': 0.03},
            {'symbol': '600030', 'name': '中信证券', 'industry': '证券', 'pe': 18, 'pb': 1.8, 'roe': 0.10, 'dividend_yield': 0.02},
            {'symbol': '000858', 'name': '五粮液', 'industry': '白酒', 'pe': 25, 'pb': 8, 'roe': 0.25, 'dividend_yield': 0.02},
            {'symbol': '000333', 'name': '美的集团', 'industry': '家电', 'pe': 13, 'pb': 3.5, 'roe': 0.27, 'dividend_yield': 0.03},
            {'symbol': '002415', 'name': '海康威视', 'industry': '科技', 'pe': 22, 'pb': 5, 'roe': 0.23, 'dividend_yield': 0.025},
            {'symbol': '601166', 'name': '兴业银行', 'industry': '银行', 'pe': 5, 'pb': 0.8, 'roe': 0.15, 'dividend_yield': 0.04},
            {'symbol': '000001', 'name': '平安银行', 'industry': '银行', 'pe': 6, 'pb': 0.9, 'roe': 0.12, 'dividend_yield': 0.03},
            {'symbol': '600900', 'name': '长江电力', 'industry': '电力', 'pe': 20, 'pb': 3, 'roe': 0.15, 'dividend_yield': 0.04},
        ]
    
    def screen(self, criteria):
        """
        根据条件筛选股票
        
        Args:
            criteria: dict, 筛选条件
        
        Returns:
            list: 符合条件的股票
        """
        results = []
        
        for stock in self.stock_pool:
            if self.matches_criteria(stock, criteria):
                results.append(stock)
        
        return results
    
    def matches_criteria(self, stock, criteria):
        """检查股票是否符合条件"""
        for key, value in criteria.items():
            if key.endswith('_max'):
                field = key[:-4]
                if stock.get(field, 0) > value:
                    return False
            elif key.endswith('_min'):
                field = key[:-4]
                if stock.get(field, 0) < value:
                    return False
        
        return True
    
    def screen_preset(self, preset_name):
        """使用预设条件筛选"""
        if preset_name not in self.SCREEN_PRESETS:
            return f"❌ 未找到预设条件：{preset_name}"
        
        criteria = self.SCREEN_PRESETS[preset_name]
        results = self.screen(criteria)
        
        return self.format_results(results, preset_name)
    
    def format_results(self, results, preset_name):
        """格式化筛选结果"""
        lines = []
        lines.append("=" * 70)
        lines.append(f"🔍 股票筛选结果 - {preset_name}")
        lines.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 70)
        lines.append("")
        lines.append(f"✅ 筛选出 {len(results)} 只符合条件的股票")
        lines.append("")
        
        if results:
            lines.append("📋 股票列表:")
            lines.append("-" * 70)
            lines.append(f"{'代码':<8} {'名称':<12} {'行业':<10} {'PE':>8} {'PB':>8} {'ROE':>8} {'股息率':>8}")
            lines.append("-" * 70)
            
            for stock in sorted(results, key=lambda x: x.get('roe', 0), reverse=True):
                lines.append(
                    f"{stock['symbol']:<8} {stock['name']:<12} {stock['industry']:<10} "
                    f"{stock['pe']:>8} {stock['pb']:>8.2f} {stock['roe']:>7.1%} {stock['dividend_yield']:>7.1%}"
                )
            
            lines.append("-" * 70)
            lines.append("")
            
            # 统计信息
            avg_pe = sum(s['pe'] for s in results) / len(results)
            avg_roe = sum(s['roe'] for s in results) / len(results)
            avg_dividend = sum(s['dividend_yield'] for s in results) / len(results)
            
            lines.append("📊 平均指标:")
            lines.append(f"   平均 PE: {avg_pe:.1f}")
            lines.append(f"   平均 ROE: {avg_roe:.1%}")
            lines.append(f"   平均股息率：{avg_dividend:.1%}")
        else:
            lines.append("❌ 未找到符合条件的股票")
            lines.append("")
            lines.append("💡 建议:")
            lines.append("   • 放宽筛选条件")
            lines.append("   • 扩大股票池范围")
        
        lines.append("")
        lines.append("⚠️ 说明:")
        lines.append("   • 数据为示例数据，实际投资请查阅最新财报")
        lines.append("   • 筛选结果仅供参考，不构成投资建议")
        lines.append("=" * 70)
        
        report = '\n'.join(lines)
        print(report)
        
        # 保存报告
        report_file = REPORTS_DIR / f"screener_{preset_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        REPORTS_DIR.mkdir(exist_ok=True)
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report
    
    def list_presets(self):
        """列出所有预设条件"""
        lines = []
        lines.append("=" * 70)
        lines.append("🔍 股票筛选预设条件")
        lines.append("=" * 70)
        lines.append("")
        
        for name, criteria in self.SCREEN_PRESETS.items():
            lines.append(f"📌 {name}:")
            for key, value in criteria.items():
                field = key.replace('_min', '≥').replace('_max', '≤')
                if 'yield' in field or 'ratio' in field or 'roe' in field:
                    value_str = f"{value:.0%}"
                elif 'growth' in field:
                    value_str = f"{value:.0%}"
                else:
                    value_str = str(value)
                lines.append(f"   • {field}: {value_str}")
            lines.append("")
        
        lines.append("使用方法:")
        lines.append("  python3 src/screener.py <预设名称>")
        lines.append("")
        lines.append("示例:")
        lines.append("  python3 src/screener.py 价值股")
        lines.append("  python3 src/screener.py 成长股")
        lines.append("  python3 src/screener.py 高股息")
        lines.append("=" * 70)
        
        return '\n'.join(lines)


if __name__ == "__main__":
    import sys
    
    screener = StockScreener()
    
    if len(sys.argv) > 1:
        preset = sys.argv[1]
        if preset in ['--list', '-l', 'list']:
            print(screener.list_presets())
        else:
            screener.screen_preset(preset)
    else:
        # 默认显示所有预设
        print(screener.list_presets())
