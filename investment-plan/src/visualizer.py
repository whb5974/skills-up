#!/usr/bin/env python3
"""
投资可视化模块
生成资产配置图、收益曲线、持仓分布等图表
使用 ASCII 图表，无需外部依赖
"""

import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / 'data'
CHARTS_DIR = Path(__file__).parent.parent / 'charts'
CHARTS_DIR.mkdir(exist_ok=True)


class ASCIIChart:
    """ASCII 图表生成器"""
    
    @staticmethod
    def horizontal_bar_chart(data, title="条形图", width=50, show_value=True):
        """
        生成水平条形图
        
        Args:
            data: dict 或 list of tuples, 数据 {标签：值}
            title: 图表标题
            width: 最大宽度
            show_value: 是否显示数值
        """
        if isinstance(data, dict):
            data = list(data.items())
        
        if not data:
            return "无数据"
        
        max_val = max(v for _, v in data)
        if max_val == 0:
            max_val = 1
        
        lines = []
        lines.append(f"┌{'─' * (width + 30)}┐")
        lines.append(f"│ {title.center(width + 28)} │")
        lines.append(f"├{'─' * (width + 30)}┤")
        
        label_width = max(len(str(label)) for label, _ in data)
        label_width = min(label_width, 15)
        
        for label, value in data:
            label_str = str(label)[:label_width].ljust(label_width)
            bar_len = int((value / max_val) * width)
            bar = '█' * bar_len
            value_str = f"{value:>12,.2f}" if show_value else ""
            lines.append(f"│ {label_str} │{bar} {value_str} │")
        
        lines.append(f"└{'─' * (width + 30)}┘")
        return '\n'.join(lines)
    
    @staticmethod
    def pie_chart_ascii(data, title="饼图", radius=8):
        """
        生成简易 ASCII 饼图（用图例表示）
        """
        if isinstance(data, dict):
            data = list(data.items())
        
        total = sum(v for _, v in data)
        if total == 0:
            return "无数据"
        
        # 颜色/符号映射
        symbols = ['█', '▓', '▒', '░', '●', '◆', '■', '▲', '★', '♦']
        
        lines = []
        lines.append(f"┌{'─' * 50}┐")
        lines.append(f"│ {title.center(48)} │")
        lines.append(f"├{'─' * 50}┤")
        
        # 计算各部分占比
        cumulative = 0
        for i, (label, value) in enumerate(data):
            pct = (value / total) * 100
            symbol = symbols[i % len(symbols)]
            bar_len = int(pct / 2)  # 50 字符宽度
            bar = symbol * bar_len
            lines.append(f"│ {symbol} {str(label)[:12]:<12} {pct:>5.1f}% │{bar}{' ' * (50-bar_len)}│")
            cumulative += pct
        
        lines.append(f"├{'─' * 50}┤")
        lines.append(f"│ {'总计:':<20} {total:>12,.2f} {'100.0%':>10} {'':>6} │")
        lines.append(f"└{'─' * 50}┘")
        
        return '\n'.join(lines)
    
    @staticmethod
    def line_chart_ascii(data_points, title="趋势图", width=60, height=15):
        """
        生成简易 ASCII 折线图
        
        Args:
            data_points: list of (x, y) tuples
        """
        if not data_points:
            return "无数据"
        
        y_values = [y for _, y in data_points]
        min_y = min(y_values)
        max_y = max(y_values)
        y_range = max_y - min_y if max_y != min_y else 1
        
        lines = []
        lines.append(f"  {title}")
        lines.append(f"  {'─' * width}")
        
        # 从顶部到底部绘制
        for row in range(height, -1, -1):
            y_threshold = min_y + (y_range * row / height)
            
            # Y 轴标签
            if row == height:
                label = f"{max_y:>10.2f} │"
            elif row == 0:
                label = f"{min_y:>10.2f} │"
            elif row == height // 2:
                label = f"{(min_y + max_y) / 2:>10.2f} │"
            else:
                label = " " * 11 + "│"
            
            # 绘制数据点
            line = label
            for col in range(width):
                x_idx = int(col * len(data_points) / width)
                if x_idx < len(data_points):
                    _, y = data_points[x_idx]
                    if y >= y_threshold and (row == height or y < min_y + (y_range * (row + 1) / height)):
                        line += '●'
                    else:
                        line += ' '
                else:
                    line += ' '
            
            lines.append(line)
        
        # X 轴
        lines.append(" " * 11 + "└" + "─" * width)
        lines.append(" " * 11 + f"  起点 {' ' * (width - 10)} 终点")
        
        return '\n'.join(lines)
    
    @staticmethod
    def heatmap_ascii(data, title="热力图", row_labels=None, col_labels=None):
        """
        生成简易 ASCII 热力图
        
        Args:
            data: 2D list
        """
        if not data or not data[0]:
            return "无数据"
        
        # 展平找最大最小值
        all_values = [v for row in data for v in row]
        min_v = min(all_values)
        max_v = max(all_values)
        v_range = max_v - min_v if max_v != min_v else 1
        
        # 热力符号
        heat_chars = ' ░▒▓█'
        
        lines = []
        lines.append(f"  {title}")
        lines.append("  " + "─" * (len(data[0]) * 3 + 10))
        
        for i, row in enumerate(data):
            label = row_labels[i] if row_labels and i < len(row_labels) else f"行{i+1}"
            line = f"  {label[:6]:<6} │ "
            for val in row:
                idx = min(int((val - min_v) / v_range * (len(heat_chars) - 1)), len(heat_chars) - 1)
                line += heat_chars[idx] + "  "
            lines.append(line)
        
        lines.append("  " + "─" * (len(data[0]) * 3 + 10))
        return '\n'.join(lines)


def generate_allocation_chart():
    """生成资产配置图"""
    portfolio_file = DATA_DIR / 'portfolio.json'
    if not portfolio_file.exists():
        return "❌ 未找到持仓数据"
    
    with open(portfolio_file, 'r', encoding='utf-8') as f:
        portfolio = json.load(f)
    
    # 按类别统计
    categories = {}
    for symbol, pos in portfolio['positions'].items():
        cat = pos.get('category', '其他')
        # 简化类别名
        if ' - ' in cat:
            cat = cat.split(' - ')[0]
        if cat not in categories:
            categories[cat] = 0
        categories[cat] += pos['shares'] * pos['current_price']
    
    # 添加现金类
    cash_alloc = portfolio.get('cash_allocation', {})
    categories['现金'] = categories.get('现金', 0) + cash_alloc.get('cash_money_market', 0)
    categories['另类'] = categories.get('另类', 0) + cash_alloc.get('alternative', 0)
    categories['可用现金'] = portfolio.get('cash', 0)
    
    chart = ASCIIChart.pie_chart_ascii(categories, "📊 资产配置图")
    
    # 保存
    chart_file = CHARTS_DIR / f"allocation_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(chart_file, 'w', encoding='utf-8') as f:
        f.write(chart)
    
    return chart


def generate_profit_loss_chart():
    """生成盈亏分布图"""
    portfolio_file = DATA_DIR / 'portfolio.json'
    if not portfolio_file.exists():
        return "❌ 未找到持仓数据"
    
    with open(portfolio_file, 'r', encoding='utf-8') as f:
        portfolio = json.load(f)
    
    # 计算各持仓盈亏
    profits = {}
    for symbol, pos in portfolio['positions'].items():
        market_value = pos['shares'] * pos['current_price']
        cost_value = pos['shares'] * pos['cost_basis']
        profit = market_value - cost_value
        profits[pos['name']] = profit
    
    if not profits:
        return "❌ 无持仓数据"
    
    chart = ASCIIChart.horizontal_bar_chart(
        profits, 
        title="📈 持仓盈亏分布 (元)",
        width=40
    )
    
    # 保存
    chart_file = CHARTS_DIR / f"profit_loss_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(chart_file, 'w', encoding='utf-8') as f:
        f.write(chart)
    
    return chart


def generate_risk_distribution_chart():
    """生成风险等级分布图"""
    portfolio_file = DATA_DIR / 'portfolio.json'
    if not portfolio_file.exists():
        return "❌ 未找到持仓数据"
    
    with open(portfolio_file, 'r', encoding='utf-8') as f:
        portfolio = json.load(f)
    
    # 简单风险分类（基于波动率假设）
    risk_map = {
        '股票 - 蓝筹': '中风险',
        '股票 - 成长': '高风险',
        '基金 - 宽基': '中风险',
        '基金 - 行业': '中高风险',
        '债券': '低风险',
        '现金': '极低风险',
        '另类': '高风险'
    }
    
    risk_dist = {}
    for symbol, pos in portfolio['positions'].items():
        cat = pos.get('category', '其他')
        risk = risk_map.get(cat, '中风险')
        value = pos['shares'] * pos['current_price']
        risk_dist[risk] = risk_dist.get(risk, 0) + value
    
    # 添加现金类
    cash_alloc = portfolio.get('cash_allocation', {})
    risk_dist['极低风险'] = risk_dist.get('极低风险', 0) + cash_alloc.get('cash_money_market', 0) + portfolio.get('cash', 0)
    risk_dist['高风险'] = risk_dist.get('高风险', 0) + cash_alloc.get('alternative', 0)
    
    chart = ASCIIChart.pie_chart_ascii(risk_dist, "⚠️ 风险等级分布")
    
    # 保存
    chart_file = CHARTS_DIR / f"risk_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(chart_file, 'w', encoding='utf-8') as f:
        f.write(chart)
    
    return chart


def generate_all_charts():
    """生成所有图表"""
    print("\n" + "="*60)
    print("📊 生成投资可视化图表")
    print("="*60)
    
    charts = [
        ("资产配置图", generate_allocation_chart),
        ("盈亏分布图", generate_profit_loss_chart),
        ("风险分布图", generate_risk_distribution_chart),
    ]
    
    for name, func in charts:
        print(f"\n{name}:")
        chart = func()
        print(chart)
        print(f"✅ 已保存至 charts/ 目录")
    
    print("\n" + "="*60)
    print(f"📁 图表已保存至：{CHARTS_DIR}")
    print("="*60 + "\n")


if __name__ == "__main__":
    generate_all_charts()
