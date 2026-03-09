#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
i 茅台 i 购抢购提醒模块
支持多次倒计时提醒
"""

from datetime import datetime
from loguru import logger
from .notifier import Notifier


class IGouNotifier(Notifier):
    """i 购抢购通知器"""
    
    def __init__(self, config):
        """
        初始化 i 购通知器
        
        Args:
            config: 配置对象
        """
        super().__init__(config)
        self.config = config
    
    def send_10min_reminder(self, product_name="飞天 500ml"):
        """发送提前 10 分钟提醒"""
        content = f"""🚨 i 茅台 i 购抢购提醒

⏰ 抢购时间：09:00 (10 分钟后)
📦 抢购产品：{product_name}
🏪 推荐门店：郊区店/社区店

💡 准备事项:
• 打开 i 茅台 APP
• 选择门店
• 确认支付方式
• 检查网络 (推荐 5G)

👉 立即准备！

---
祝您好运！🍀"""
        
        self.send_message(content)
        logger.info("📤 已发送 10 分钟提醒")
    
    def send_5min_reminder(self, product_name="飞天 500ml"):
        """发送提前 5 分钟提醒"""
        content = f"""⚠️ i 茅台 i 购 - 5 分钟倒计时

⏰ 抢购时间：09:00 (5 分钟后)
📦 抢购产品：{product_name}

💡 最后确认:
• ✅ 已登录账号
• ✅ 已选择门店
• ✅ 支付已准备 (微信/支付宝余额)
• ✅ 网络已检查 (5G/WiFi)

👉 进入抢购页面！

---
准备！准备！🚀"""
        
        self.send_message(content)
        logger.info("📤 已发送 5 分钟提醒")
    
    def send_1min_reminder(self, product_name="飞天 500ml"):
        """发送提前 1 分钟提醒"""
        content = f"""🚨🚨🚨 i 茅台 i 购 - 1 分钟倒计时！

⏰ 抢购时间：09:00 (1 分钟后)
📦 抢购产品：{product_name}

💡 准备点击:
• 手指放在"立即购买"上
• 等待倒计时
• 09:00:00 准时提交！

👉 准备！准备！准备！

---
抢到就是赚到！💰"""
        
        self.send_message(content)
        logger.info("📤 已发送 1 分钟提醒")
    
    def send_success_notification(self, product_name, store_name, price):
        """发送抢购成功通知"""
        content = f"""🎉 恭喜！抢购成功！

📦 产品：{product_name}
🏪 门店：{store_name}
💰 价格：{price} 元

⚠️ 重要提醒:
• 请立即完成支付
• 支付时限：30 分钟
• 提货时限：7 天内

👉 立即支付！

---
恭喜恭喜！🎊"""
        
        self.send_message(content)
        logger.info("📤 已发送抢购成功通知")
    
    def send_failed_notification(self, product_name):
        """发送抢购失败通知"""
        content = f"""😢 抢购失败通知

📦 产品：{product_name}
⏰ 时间：09:00

💡 不要气馁:
• 还有 12:00/14:00/20:00 场次
• 明天继续
• 坚持就是胜利

👉 准备下一场！

---
下次好运！🍀"""
        
        self.send_message(content)
        logger.info("📤 已发送抢购失败通知")
