#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据可视化模块
"""

from datetime import datetime
from typing import Dict, List, Any
from loguru import logger


class DashboardVisualizer:
    """数据看板可视化类"""
    
    def __init__(self, config, db):
        """
        初始化看板
        
        Args:
            config: 配置对象
            db: 数据库对象
        """
        self.config = config
        self.db = db
        self.phone = config.get("user.phone", "")
    
    def generate_summary(self) -> str:
        """
        生成统计摘要
        
        Returns:
            格式化统计文本
        """
        user = self.db.get_user_by_phone(self.phone)
        if not user:
            return "暂无数据"
        
        stats = self.db.get_stats(user["id"])
        
        summary = f"""
╔════════════════════════════════════════════════════════╗
║           🍶 i 茅台申购统计看板                          ║
╠════════════════════════════════════════════════════════╣
║  📊 总体统计                                            ║
║  ┌──────────────────────────────────────────────┐      ║
║  │  累计申购次数：{stats.get('total_reservations', 0):>6} 次                    │      ║
║  │  累计中签次数：{stats.get('total_wins', 0):>6} 次                    │      ║
║  │  综合中签率：  {stats.get('win_rate', '0%'):>8}                      │      ║
║  └──────────────────────────────────────────────┘      ║
╚════════════════════════════════════════════════════════╝
"""
        return summary
    
    def generate_calendar(self, year: int, month: int) -> str:
        """
        生成申购日历
        
        Args:
            year: 年份
            month: 月份
            
        Returns:
            格式化日历文本
        """
        user = self.db.get_user_by_phone(self.phone)
        if not user:
            return "暂无数据"
        
        reservations = self.db.get_reservations(user["id"], f"{year}-{month:02d}")
        
        # 创建日期到状态的映射
        date_status = {}
        for r in reservations:
            date = r.get("reservation_date", "")
            status = r.get("status", "pending")
            date_status[date] = status
        
        # 生成日历
        today = datetime.now()
        if year == today.year and month == today.month:
            current_day = today.day
        else:
            current_day = -1
        
        # 计算当月第一天是星期几
        first_day = datetime(year, month, 1)
        start_weekday = first_day.weekday()
        
        # 计算当月天数
        if month == 12:
            next_month = datetime(year + 1, 1, 1)
        else:
            next_month = datetime(year, month + 1, 1)
        days_in_month = (next_month - datetime(year, month, 1)).days
        
        calendar_lines = []
        calendar_lines.append(f"📅 {year}年{month}月 申购日历")
        calendar_lines.append("┌─────┬─────┬─────┬─────┬─────┬─────┬─────┐")
        calendar_lines.append("│ 一  │ 二  │ 三  │ 四  │ 五  │ 六  │ 日  │")
        calendar_lines.append("├─────┼─────┼─────┼─────┼─────┼─────┼─────┤")
        
        week_line = "│"
        for _ in range(start_weekday):
            week_line += "     │"
        
        for day in range(1, days_in_month + 1):
            date_str = f"{year}-{month:02d}-{day:02d}"
            status = date_status.get(date_str, "")
            
            if status == "success":
                cell = f" 🟢{day:>2} "
            elif status == "failed":
                cell = f" 🔴{day:>2} "
            elif status == "pending":
                cell = f" 🟡{day:>2} "
            else:
                cell = f"  {day:>2}  "
            
            week_line += cell + "│"
            
            if (start_weekday + day) % 7 == 0:
                calendar_lines.append(week_line)
                calendar_lines.append("├─────┼─────┼─────┼─────┼─────┼─────┼─────┤")
                week_line = "│"
        
        # 填充最后一行
        while len(week_line) < 50:
            week_line += "     │"
        calendar_lines.append(week_line)
        calendar_lines.append("└─────┴─────┴─────┴─────┴─────┴─────┴─────┘")
        calendar_lines.append("")
        calendar_lines.append("图例：🟢 已申购  🟡 待抽签  🔴 已中签")
        
        return "\n".join(calendar_lines)
    
    def generate_product_stats(self) -> str:
        """
        生成产品统计
        
        Returns:
            格式化产品统计文本
        """
        user = self.db.get_user_by_phone(self.phone)
        if not user:
            return "暂无数据"
        
        reservations = self.db.get_reservations(user["id"])
        
        # 按产品统计
        product_stats = {}
        for r in reservations:
            product = r.get("product_name", "未知")
            if product not in product_stats:
                product_stats[product] = {"total": 0, "wins": 0}
            product_stats[product]["total"] += 1
            if r.get("status") == "success":
                product_stats[product]["wins"] += 1
        
        if not product_stats:
            return "暂无申购记录"
        
        lines = []
        lines.append("📦 产品中签统计")
        lines.append("=" * 50)
        
        for product, stats in product_stats.items():
            total = stats["total"]
            wins = stats["wins"]
            rate = f"{wins/total:.1%}" if total > 0 else "0%"
            
            # 简化的条形图
            bar_length = 20
            filled = int(bar_length * wins / total) if total > 0 else 0
            bar = "█" * filled + "░" * (bar_length - filled)
            
            lines.append(f"{product[:20]:<20} {bar} {wins}/{total} ({rate})")
        
        lines.append("=" * 50)
        
        return "\n".join(lines)
    
    def generate_full_report(self) -> str:
        """
        生成完整报告
        
        Returns:
            完整报告文本
        """
        today = datetime.now()
        
        report = []
        report.append(self.generate_summary())
        report.append("")
        report.append(self.generate_calendar(today.year, today.month))
        report.append("")
        report.append(self.generate_product_stats())
        
        return "\n".join(report)
