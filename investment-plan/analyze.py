#!/usr/bin/env python3
"""
投资分析主控脚本
整合所有分析功能，一键生成完整分析报告

使用方法:
    python3 analyze.py              # 完整分析
    python3 analyze.py --quick      # 快速检查
    python3 analyze.py --valuation  # 估值分析
    python3 analyze.py --rebalance  # 调仓建议
    python3 analyze.py --screen     # 股票筛选
    python3 analyze.py --charts     # 可视化图表
"""

import sys
import argparse
from datetime import datetime
from pathlib import Path
import importlib.util

# 添加路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / 'src'))

def load_module(name, path):
    """动态加载模块"""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# 加载模块
auto_check = load_module('auto_check', PROJECT_ROOT / 'auto-check.py')
visualizer = load_module('visualizer', PROJECT_ROOT / 'src' / 'visualizer.py')
valuation_mod = load_module('valuation', PROJECT_ROOT / 'src' / 'valuation.py')
rebalancer_mod = load_module('rebalancer', PROJECT_ROOT / 'src' / 'rebalancer.py')
screener_mod = load_module('screener', PROJECT_ROOT / 'src' / 'screener.py')

generate_daily_report = auto_check.generate_daily_report
generate_all_charts = visualizer.generate_all_charts
ValuationAnalyzer = valuation_mod.ValuationAnalyzer
Rebalancer = rebalancer_mod.Rebalancer
StockScreener = screener_mod.StockScreener


def print_header(title):
    """打印标题"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70 + "\n")


def quick_check():
    """快速检查"""
    print_header("🚀 快速检查")
    
    # 日报摘要
    print("📊 今日持仓摘要:")
    report = generate_daily_report()
    
    # 提取关键信息
    for line in report.split('\n'):
        if '总资产' in line or '总收益' in line or '无风险警示' in line:
            print(line)
    
    # 调仓检查
    print("\n🔄 配置检查:")
    rebalancer = Rebalancer()
    check = rebalancer.quick_check()
    print(f"   {check['message']}")
    
    print("\n✅ 快速检查完成\n")


def full_analysis():
    """完整分析"""
    print_header("📊 投资组合完整分析")
    
    print("📌 本次分析将包含:")
    print("   1. 持仓日报")
    print("   2. 估值分析")
    print("   3. 调仓建议")
    print("   4. 可视化图表")
    print("   5. 股票筛选")
    print("\n开始分析...\n")
    
    # 1. 日报
    print_header("📰 1. 投资日报")
    generate_daily_report()
    
    # 2. 估值分析
    print_header("💰 2. 估值分析")
    valuation = ValuationAnalyzer()
    valuation.print_report()
    
    # 3. 调仓建议
    print_header("🔄 3. 调仓建议")
    rebalancer = Rebalancer()
    rebalancer.generate_rebalance_plan()
    
    # 4. 可视化
    print_header("📈 4. 可视化图表")
    generate_all_charts()
    
    # 5. 股票筛选
    print_header("🔍 5. 股票筛选示例")
    screener = StockScreener()
    screener.screen_preset('价值股')
    
    print("\n" + "=" * 70)
    print("✅ 完整分析完成！")
    print("=" * 70)
    print("\n📁 报告已保存至:")
    print(f"   • 日报：logs/daily_{datetime.now().strftime('%Y%m%d')}.txt")
    print(f"   • 估值：reports/valuation_*.txt")
    print(f"   • 调仓：reports/rebalance_*.txt")
    print(f"   • 图表：charts/*.txt")
    print(f"   • 筛选：reports/screener_*.txt")
    print("\n" + "=" * 70 + "\n")


def valuation_analysis():
    """估值分析"""
    print_header("💰 估值分析")
    valuation = ValuationAnalyzer()
    valuation.print_report()


def rebalance_analysis():
    """调仓分析"""
    print_header("🔄 调仓建议")
    rebalancer = Rebalancer()
    rebalancer.generate_rebalance_plan()


def screen_stocks(preset='价值股'):
    """股票筛选"""
    print_header(f"🔍 股票筛选 - {preset}")
    screener = StockScreener()
    screener.screen_preset(preset)


def show_charts():
    """生成图表"""
    print_header("📈 可视化图表")
    generate_all_charts()


def main():
    parser = argparse.ArgumentParser(
        description='投资分析工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 analyze.py              # 完整分析
  python3 analyze.py --quick      # 快速检查
  python3 analyze.py --valuation  # 估值分析
  python3 analyze.py --rebalance  # 调仓建议
  python3 analyze.py --screen 成长股  # 筛选成长股
  python3 analyze.py --charts     # 可视化图表
        """
    )
    
    parser.add_argument('--quick', '-q', action='store_true', help='快速检查')
    parser.add_argument('--full', '-f', action='store_true', help='完整分析')
    parser.add_argument('--valuation', '-v', action='store_true', help='估值分析')
    parser.add_argument('--rebalance', '-r', action='store_true', help='调仓建议')
    parser.add_argument('--screen', '-s', type=str, metavar='预设', help='股票筛选')
    parser.add_argument('--charts', '-c', action='store_true', help='可视化图表')
    
    args = parser.parse_args()
    
    # 如果没有参数，默认执行完整分析
    if len(sys.argv) == 1:
        full_analysis()
        return
    
    if args.quick:
        quick_check()
    
    if args.full:
        full_analysis()
    
    if args.valuation:
        valuation_analysis()
    
    if args.rebalance:
        rebalance_analysis()
    
    if args.screen:
        screen_stocks(args.screen)
    
    if args.charts:
        show_charts()


if __name__ == "__main__":
    main()
