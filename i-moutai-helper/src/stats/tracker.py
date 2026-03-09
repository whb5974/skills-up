#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
申购统计模块
"""

import csv
from datetime import datetime
from typing import Dict, List, Any, Optional
from loguru import logger


class StatsTracker:
    """统计追踪类"""
    
    def __init__(self, config, db):
        """
        初始化统计器
        
        Args:
            config: 配置对象
            db: 数据库对象
        """
        self.config = config
        self.db = db
        self.phone = config.get("user.phone", "")
    
    def get_summary(self) -> Dict[str, Any]:
        """
        获取统计摘要
        
        Returns:
            统计数据
        """
        user = self.db.get_user_by_phone(self.phone)
        if not user:
            return {
                "total_reservations": 0,
                "total_wins": 0,
                "win_rate": "0%"
            }
        
        return self.db.get_stats(user["id"])
    
    def get_monthly_stats(self, month: str) -> Dict[str, Any]:
        """
        获取月度统计
        
        Args:
            month: 月份 (格式：2026-03)
            
        Returns:
            月度统计数据
        """
        user = self.db.get_user_by_phone(self.phone)
        if not user:
            return {}
        
        reservations = self.db.get_reservations(user["id"], month)
        
        total = len(reservations)
        wins = sum(1 for r in reservations if r.get("status") == "success")
        win_rate = f"{wins / total:.1%}" if total > 0 else "0%"
        
        # 按产品统计
        product_stats = {}
        for r in reservations:
            product = r.get("product_name", "未知")
            if product not in product_stats:
                product_stats[product] = {"total": 0, "wins": 0}
            product_stats[product]["total"] += 1
            if r.get("status") == "success":
                product_stats[product]["wins"] += 1
        
        return {
            "month": month,
            "total_reservations": total,
            "total_wins": wins,
            "win_rate": win_rate,
            "product_stats": product_stats
        }
    
    def add_reservation(self, store_id: str, product_name: str, 
                       reservation_date: Optional[str] = None) -> int:
        """
        添加申购记录
        
        Args:
            store_id: 门店 ID
            product_name: 产品名称
            reservation_date: 申购日期 (默认今天)
            
        Returns:
            记录 ID
        """
        if reservation_date is None:
            reservation_date = datetime.now().strftime("%Y-%m-%d")
        
        user = self.db.get_user_by_phone(self.phone)
        if not user:
            # 自动创建用户
            user_id = self.db.add_user(self.phone, self.config.get("user.name", ""))
        else:
            user_id = user["id"]
        
        record_id = self.db.add_reservation(
            user_id=user_id,
            store_id=store_id,
            product_name=product_name,
            reservation_date=reservation_date
        )
        
        logger.info(f"✅ 已添加申购记录：{product_name} @ {reservation_date}")
        return record_id
    
    def update_result(self, reservation_id: int, is_win: bool):
        """
        更新中签结果
        
        Args:
            reservation_id: 申购记录 ID
            is_win: 是否中签
        """
        status = "success" if is_win else "failed"
        self.db.update_reservation_status(reservation_id, status)
        self.db.add_lottery_result(reservation_id, status)
        
        logger.info(f"✅ 已更新中签结果：{'中签' if is_win else '未中签'}")
    
    def export_to_csv(self, output_path: str):
        """
        导出数据到 CSV
        
        Args:
            output_path: 输出文件路径
        """
        user = self.db.get_user_by_phone(self.phone)
        if not user:
            logger.warning("⚠️ 无用户数据，无法导出")
            return
        
        reservations = self.db.get_reservations(user["id"])
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["申购日期", "产品", "门店", "状态", "创建时间"])
            
            for r in reservations:
                writer.writerow([
                    r.get("reservation_date", ""),
                    r.get("product_name", ""),
                    r.get("store_id", ""),
                    r.get("status", ""),
                    r.get("created_at", "")
                ])
        
        logger.info(f"✅ 已导出 {len(reservations)} 条记录到 {output_path}")
