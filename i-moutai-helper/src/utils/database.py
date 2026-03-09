#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库操作模块
"""

import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from loguru import logger


class Database:
    """数据库操作类"""
    
    def __init__(self, config):
        """
        初始化数据库
        
        Args:
            config: 配置对象
        """
        db_path = config.get("database.path", "data/moutai.db")
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = None
    
    def connect(self):
        """连接数据库"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def init_tables(self):
        """初始化数据库表"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # 用户表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone TEXT UNIQUE NOT NULL,
                name TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 门店表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stores (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                address TEXT,
                phone TEXT,
                latitude REAL,
                longitude REAL,
                competition_level TEXT DEFAULT '中',
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 申购记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                store_id TEXT NOT NULL,
                product_name TEXT NOT NULL,
                reservation_date DATE NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (store_id) REFERENCES stores(id)
            )
        """)
        
        # 中签结果表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lottery_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reservation_id INTEGER NOT NULL,
                result TEXT NOT NULL,
                notify_time DATETIME,
                paid BOOLEAN DEFAULT FALSE,
                picked_up BOOLEAN DEFAULT FALSE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (reservation_id) REFERENCES reservations(id)
            )
        """)
        
        # 创建索引
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_reservations_date ON reservations(reservation_date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_reservations_user ON reservations(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_results_reservation ON lottery_results(reservation_id)")
        
        conn.commit()
        self.close()
        logger.info("✅ 数据库表初始化完成")
    
    def add_user(self, phone: str, name: str) -> int:
        """添加用户"""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT OR REPLACE INTO users (phone, name) VALUES (?, ?)",
                (phone, name)
            )
            conn.commit()
            user_id = cursor.lastrowid
            return user_id
        finally:
            self.close()
    
    def get_user_by_phone(self, phone: str) -> Optional[Dict]:
        """根据手机号获取用户"""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM users WHERE phone = ?", (phone,))
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            self.close()
    
    def add_reservation(self, user_id: int, store_id: str, product_name: str, 
                       reservation_date: str) -> int:
        """添加申购记录"""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """INSERT INTO reservations (user_id, store_id, product_name, reservation_date)
                   VALUES (?, ?, ?, ?)""",
                (user_id, store_id, product_name, reservation_date)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            self.close()
    
    def update_reservation_status(self, reservation_id: int, status: str):
        """更新申购记录状态"""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "UPDATE reservations SET status = ? WHERE id = ?",
                (status, reservation_id)
            )
            conn.commit()
        finally:
            self.close()
    
    def add_lottery_result(self, reservation_id: int, result: str):
        """添加中签结果"""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """INSERT INTO lottery_results (reservation_id, result, notify_time)
                   VALUES (?, ?, ?)""",
                (reservation_id, result, datetime.now())
            )
            conn.commit()
        finally:
            self.close()
    
    def get_reservations(self, user_id: int, month: Optional[str] = None) -> List[Dict]:
        """获取申购记录"""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            if month:
                cursor.execute(
                    """SELECT * FROM reservations 
                       WHERE user_id = ? AND reservation_date LIKE ?
                       ORDER BY reservation_date DESC""",
                    (user_id, f"{month}%")
                )
            else:
                cursor.execute(
                    "SELECT * FROM reservations WHERE user_id = ? ORDER BY reservation_date DESC",
                    (user_id,)
                )
            
            return [dict(row) for row in cursor.fetchall()]
        finally:
            self.close()
    
    def get_stats(self, user_id: int) -> Dict[str, Any]:
        """获取统计数据"""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            # 总申购次数
            cursor.execute(
                "SELECT COUNT(*) as count FROM reservations WHERE user_id = ?",
                (user_id,)
            )
            total = cursor.fetchone()['count']
            
            # 中签次数
            cursor.execute(
                """SELECT COUNT(*) as count FROM reservations r
                   JOIN lottery_results lr ON r.id = lr.reservation_id
                   WHERE r.user_id = ? AND lr.result = 'success'""",
                (user_id,)
            )
            wins = cursor.fetchone()['count']
            
            # 中签率
            win_rate = f"{wins / total:.1%}" if total > 0 else "0%"
            
            return {
                "total_reservations": total,
                "total_wins": wins,
                "win_rate": win_rate
            }
        finally:
            self.close()
