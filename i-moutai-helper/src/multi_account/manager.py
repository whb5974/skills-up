#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多账号管理模块
支持家人账号一起申购，提高中签率
"""

from typing import List, Dict, Optional
from datetime import datetime
from loguru import logger


class AccountManager:
    """多账号管理类"""
    
    def __init__(self, db):
        """
        初始化账号管理器
        
        Args:
            db: 数据库对象
        """
        self.db = db
        self.accounts = []
        self.load_accounts()
    
    def load_accounts(self):
        """加载所有账号"""
        # 从数据库加载所有用户
        conn = self.db.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM users ORDER BY id")
            self.accounts = [dict(row) for row in cursor.fetchall()]
        finally:
            self.db.close()
        
        logger.info(f"✅ 加载 {len(self.accounts)} 个账号")
    
    def add_account(self, phone: str, name: str, relation: str = "本人") -> int:
        """
        添加账号
        
        Args:
            phone: 手机号
            name: 姓名
            relation: 关系 (本人/配偶/父母/子女等)
            
        Returns:
            用户 ID
        """
        user_id = self.db.add_user(phone, name)
        
        # 保存关系信息
        conn = self.db.connect()
        cursor = conn.cursor()
        
        try:
            # 检查是否有关系信息表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS account_relations (
                    user_id INTEGER PRIMARY KEY,
                    relation TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)
            
            cursor.execute(
                "INSERT OR REPLACE INTO account_relations (user_id, relation) VALUES (?, ?)",
                (user_id, relation)
            )
            conn.commit()
        finally:
            self.db.close()
        
        self.load_accounts()
        logger.info(f"✅ 添加账号：{name} ({phone}) - {relation}")
        return user_id
    
    def remove_account(self, phone: str) -> bool:
        """
        移除账号
        
        Args:
            phone: 手机号
            
        Returns:
            是否成功
        """
        conn = self.db.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM users WHERE phone = ?", (phone,))
            conn.commit()
            success = cursor.rowcount > 0
        finally:
            self.db.close()
        
        if success:
            self.load_accounts()
            logger.info(f"✅ 移除账号：{phone}")
        
        return success
    
    def get_accounts(self) -> List[Dict]:
        """获取所有账号"""
        return self.accounts
    
    def get_account_by_phone(self, phone: str) -> Optional[Dict]:
        """根据手机号获取账号"""
        for acc in self.accounts:
            if acc["phone"] == phone:
                return acc
        return None
    
    def get_main_account(self) -> Optional[Dict]:
        """获取主账号 (第一个账号)"""
        return self.accounts[0] if self.accounts else None
    
    def get_stats_summary(self) -> Dict:
        """获取所有账号的统计汇总"""
        total_reservations = 0
        total_wins = 0
        
        account_stats = []
        
        for acc in self.accounts:
            stats = self.db.get_stats(acc["id"])
            total_reservations += stats.get("total_reservations", 0)
            total_wins += stats.get("total_wins", 0)
            
            account_stats.append({
                "phone": acc["phone"],
                "name": acc["name"],
                **stats
            })
        
        # 计算家庭综合中签率
        family_win_rate = f"{total_wins / total_reservations:.1%}" if total_reservations > 0 else "0%"
        
        return {
            "total_accounts": len(self.accounts),
            "total_reservations": total_reservations,
            "total_wins": total_wins,
            "family_win_rate": family_win_rate,
            "account_stats": account_stats
        }


class FamilyReservationHelper:
    """家庭申购助手"""
    
    def __init__(self, account_manager: AccountManager):
        """
        初始化家庭申购助手
        
        Args:
            account_manager: 账号管理器
        """
        self.account_manager = account_manager
    
    def generate_reservation_plan(self, product_name: str, preferred_stores: List[str]) -> List[Dict]:
        """
        生成家庭申购计划
        
        Args:
            product_name: 产品名称
            preferred_stores: 首选门店列表
            
        Returns:
            申购计划
        """
        accounts = self.account_manager.get_accounts()
        
        if not accounts:
            return []
        
        plan = []
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 为每个账号分配门店 (避免同一门店竞争)
        for i, acc in enumerate(accounts):
            # 轮换门店，避免所有账号选择同一门店
            store_idx = i % len(preferred_stores) if preferred_stores else 0
            store = preferred_stores[store_idx] if preferred_stores else "待选择"
            
            plan.append({
                "account": acc["name"],
                "phone": acc["phone"],
                "product": product_name,
                "store": store,
                "date": today,
                "status": "待申购"
            })
        
        return plan
    
    def check_conflicts(self, reservations: List[Dict]) -> List[str]:
        """
        检查申购冲突
        
        Args:
            reservations: 申购记录列表
            
        Returns:
            冲突警告列表
        """
        warnings = []
        
        # 检查同一门店多账号申购
        store_accounts = {}
        for res in reservations:
            store = res.get("store", "")
            phone = res.get("phone", "")
            
            if store not in store_accounts:
                store_accounts[store] = []
            store_accounts[store].append(phone)
        
        for store, phones in store_accounts.items():
            if len(phones) > 1:
                warnings.append(f"⚠️ 门店 {store} 有 {len(phones)} 个账号申购，建议分散")
        
        return warnings
