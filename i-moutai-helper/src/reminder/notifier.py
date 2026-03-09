#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书推送模块
"""

import json
import requests
from datetime import datetime
from typing import Optional
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential


class Notifier:
    """通知推送类"""
    
    def __init__(self, config):
        """
        初始化通知器
        
        Args:
            config: 配置对象
        """
        self.config = config
        self.enabled = config.get("notification.feishu.enabled", False)
        self.chat_id = config.get("notification.feishu.chat_id", "")
        self.app_id = config.get("notification.feishu.app_id", "")
        self.app_secret = config.get("notification.feishu.app_secret", "")
        
        if self.enabled and not self.chat_id:
            logger.warning("⚠️ 飞书推送已启用但未配置 chat_id")
    
    def get_access_token(self) -> Optional[str]:
        """获取飞书 access token"""
        if not self.app_id or not self.app_secret:
            return None
        
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            result = response.json()
            
            if result.get("code") == 0:
                return result.get("tenant_access_token")
            else:
                logger.error(f"❌ 获取 access token 失败：{result}")
                return None
        except Exception as e:
            logger.error(f"❌ 获取 access token 异常：{e}")
            return None
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def send_message(self, content: str, msg_type: str = "text") -> bool:
        """
        发送消息到飞书
        
        Args:
            content: 消息内容
            msg_type: 消息类型 (text/post/card)
            
        Returns:
            是否发送成功
        """
        if not self.enabled:
            logger.debug("📭 飞书推送未启用，跳过发送")
            return False
        
        token = self.get_access_token()
        if not token:
            return False
        
        url = "https://open.feishu.cn/open-apis/im/v1/messages"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "receive_id": self.chat_id,
            "msg_type": msg_type,
            "content": json.dumps({"text": content}, ensure_ascii=False)
        }
        
        params = {"receive_id_type": "chat_id"}
        
        try:
            response = requests.post(url, headers=headers, json=payload, params=params, timeout=10)
            result = response.json()
            
            if result.get("code") == 0:
                logger.info("✅ 飞书消息发送成功")
                return True
            else:
                logger.error(f"❌ 飞书消息发送失败：{result}")
                return False
        except Exception as e:
            logger.error(f"❌ 飞书消息发送异常：{e}")
            raise  # 触发重试
    
    def send_purchase_start_reminder(self):
        """发送申购开始提醒"""
        today = datetime.now().strftime("%Y-%m-%d")
        content = f"""🍶 i 茅台申购提醒

⏰ 申购时间：09:00-21:00
📅 今日日期：{today}

💡 小贴士：
• 提前选择好门店
• 准备好申购产品
• 保持网络畅通

👉 请打开 i 茅台 APP 进行申购

---
祝您好运！🍀"""
        
        self.send_message(content)
        logger.info("📤 已发送申购开始提醒")
    
    def send_purchase_end_reminder(self):
        """发送申购截止提醒"""
        today = datetime.now().strftime("%Y-%m-%d")
        content = f"""🍶 i 茅台申购截止提醒

⏰ 截止时间：21:00
📅 今日日期：{today}

⚠️ 距离截止还有 30 分钟！

💡 还未申购的话请尽快：
• 打开 i 茅台 APP
• 选择产品并申购

---
祝您好运！🍀"""
        
        self.send_message(content)
        logger.info("📤 已发送申购截止提醒")
    
    def send_result_reminder(self):
        """发送结果公布提醒"""
        today = datetime.now().strftime("%Y-%m-%d")
        content = f"""🍶 i 茅台中签结果提醒

📅 公布日期：{today}
⏰ 公布时间：22:00 后

📱 请查看 i 茅台 APP：
• 打开 APP → 我的申购
• 查看中签结果

🎉 如中签请在 24 小时内支付！

---
祝您好运！🍀"""
        
        self.send_message(content)
        logger.info("📤 已发送结果公布提醒")
    
    def send_win_notification(self, product_name: str, store_name: str):
        """
        发送中签通知
        
        Args:
            product_name: 产品名称
            store_name: 门店名称
        """
        today = datetime.now().strftime("%Y-%m-%d")
        content = f"""🎉 恭喜中签！

📦 中签产品：{product_name}
🏪 提货门店：{store_name}
📅 公布日期：{today}

⚠️ 重要提醒：
• 请在 24 小时内完成支付
• 请在 7 天内到店提货
• 逾期视为放弃

📍 门店地址请查看 i 茅台 APP

---
恭喜恭喜！🎊"""
        
        self.send_message(content)
        logger.info("📤 已发送中签通知")
