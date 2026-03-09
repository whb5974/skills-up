#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时任务调度器
"""

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from loguru import logger
from .notifier import Notifier


class ReminderScheduler:
    """提醒调度器类"""
    
    def __init__(self, config, db):
        """
        初始化调度器
        
        Args:
            config: 配置对象
            db: 数据库对象
        """
        self.config = config
        self.db = db
        self.notifier = Notifier(config)
        self.scheduler = BlockingScheduler(timezone=config.get("reminder.timezone", "Asia/Shanghai"))
        self._setup_jobs()
    
    def _setup_jobs(self):
        """设置定时任务"""
        # 申购开始提醒
        purchase_start = self.config.get("reminder.purchase_start", "08:55")
        hour, minute = map(int, purchase_start.split(':'))
        
        self.scheduler.add_job(
            self._purchase_start_job,
            trigger=CronTrigger(hour=hour, minute=minute),
            id="purchase_start",
            name="申购开始提醒"
        )
        logger.info(f"⏰ 已设置申购开始提醒：{purchase_start}")
        
        # 申购截止提醒
        purchase_end = self.config.get("reminder.purchase_end", "20:30")
        hour, minute = map(int, purchase_end.split(':'))
        
        self.scheduler.add_job(
            self._purchase_end_job,
            trigger=CronTrigger(hour=hour, minute=minute),
            id="purchase_end",
            name="申购截止提醒"
        )
        logger.info(f"⏰ 已设置申购截止提醒：{purchase_end}")
        
        # 结果公布提醒
        result_notify = self.config.get("reminder.result_notify", "22:00")
        hour, minute = map(int, result_notify.split(':'))
        
        self.scheduler.add_job(
            self._result_job,
            trigger=CronTrigger(hour=hour, minute=minute),
            id="result_notify",
            name="结果公布提醒"
        )
        logger.info(f"⏰ 已设置结果公布提醒：{result_notify}")
    
    def _purchase_start_job(self):
        """申购开始提醒任务"""
        logger.info("🔔 执行申购开始提醒任务...")
        
        if self.config.get("reminder.enabled", True):
            self.notifier.send_purchase_start_reminder()
        else:
            logger.info("⏸️ 提醒已禁用，跳过")
    
    def _purchase_end_job(self):
        """申购截止提醒任务"""
        logger.info("🔔 执行申购截止提醒任务...")
        
        if self.config.get("reminder.enabled", True):
            self.notifier.send_purchase_end_reminder()
        else:
            logger.info("⏸️ 提醒已禁用，跳过")
    
    def _result_job(self):
        """结果公布提醒任务"""
        logger.info("🔔 执行结果公布提醒任务...")
        
        if self.config.get("reminder.enabled", True):
            self.notifier.send_result_reminder()
        else:
            logger.info("⏸️ 提醒已禁用，跳过")
    
    def start(self):
        """启动调度器"""
        logger.info("🚀 启动定时任务调度器...")
        self.scheduler.start()
    
    def stop(self):
        """停止调度器"""
        logger.info("🛑 停止定时任务调度器...")
        self.scheduler.shutdown(wait=False)
    
    def add_job(self, func, cron_expr: str, job_id: str, name: str):
        """
        添加自定义定时任务
        
        Args:
            func: 任务函数
            cron_expr: Cron 表达式 (如 "0 9 * * *")
            job_id: 任务 ID
            name: 任务名称
        """
        hour, minute, day, month, day_of_week = cron_expr.split()
        
        self.scheduler.add_job(
            func,
            trigger=CronTrigger(
                hour=int(hour) if hour != '*' else None,
                minute=int(minute) if minute != '*' else None,
                day=int(day) if day != '*' else None,
                month=int(month) if month != '*' else None,
                day_of_week=int(day_of_week) if day_of_week != '*' else None
            ),
            id=job_id,
            name=name
        )
        
        logger.info(f"✅ 已添加定时任务：{name} ({cron_expr})")
