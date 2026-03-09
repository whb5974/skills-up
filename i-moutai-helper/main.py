#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
i 茅台申购辅助工具 - 主程序入口

合法合规的申购辅助工具，提供时间提醒、门店查询、中签统计等功能
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

from loguru import logger
from src.utils.config import Config
from src.utils.database import Database
from src.reminder.scheduler import ReminderScheduler
from src.store.finder import StoreFinder
from src.stats.tracker import StatsTracker


def setup_logger(config: Config):
    """配置日志"""
    log_path = Path(config.get("logging.path", "data/logs"))
    log_path.mkdir(parents=True, exist_ok=True)
    
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level=config.get("logging.level", "INFO")
    )
    logger.add(
        log_path / "moutai_{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention=config.get("logging.backup_count", 5),
        level=config.get("logging.level", "INFO")
    )


def cmd_start(config: Config, db: Database):
    """启动提醒服务"""
    logger.info("🚀 启动 i 茅台申购辅助工具...")
    
    scheduler = ReminderScheduler(config, db)
    scheduler.start()
    
    logger.info("✅ 服务已启动，按 Ctrl+C 停止")
    
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("👋 正在停止服务...")
        scheduler.stop()
        logger.info("✅ 服务已停止")


def cmd_stats(config: Config, db: Database, args):
    """查看统计数据"""
    tracker = StatsTracker(config, db)
    
    if args.month:
        stats = tracker.get_monthly_stats(args.month)
    else:
        stats = tracker.get_summary()
    
    print("\n📊 申购统计")
    print("=" * 50)
    print(f"累计申购：{stats.get('total_reservations', 0)} 次")
    print(f"累计中签：{stats.get('total_wins', 0)} 次")
    print(f"综合中签率：{stats.get('win_rate', '0%')}")
    print("=" * 50)


def cmd_store(config: Config, args):
    """查询门店"""
    finder = StoreFinder(config)
    
    if args.nearby:
        stores = finder.find_nearby(args.distance or 10)
        print(f"\n📍 附近 {args.distance or 10} 公里内的门店:")
        print("=" * 50)
        for i, store in enumerate(stores, 1):
            print(f"{i}. {store['name']}")
            print(f"   地址：{store['address']}")
            print(f"   距离：{store['distance']:.1f}km")
            print(f"   竞争：{store.get('competition_level', '未知')}")
            print()


def cmd_remind(config: Config, db: Database, args):
    """手动触发提醒"""
    from src.reminder.notifier import Notifier
    
    notifier = Notifier(config)
    
    if args.type == "purchase_start":
        notifier.send_purchase_start_reminder()
    elif args.type == "purchase_end":
        notifier.send_purchase_end_reminder()
    elif args.type == "result":
        notifier.send_result_reminder()
    
    logger.info(f"✅ 已发送 {args.type} 提醒")


def cmd_export(config: Config, db: Database, args):
    """导出数据"""
    tracker = StatsTracker(config, db)
    
    output = args.output or "export_data.csv"
    tracker.export_to_csv(output)
    
    logger.info(f"✅ 数据已导出到 {output}")


def cmd_dashboard(config: Config, db: Database, args):
    """显示数据看板"""
    from src.dashboard.visualizer import DashboardVisualizer
    
    viz = DashboardVisualizer(config, db)
    
    if args.full:
        print(viz.generate_full_report())
    elif args.calendar:
        today = datetime.now()
        print(viz.generate_calendar(today.year, today.month))
    elif args.products:
        print(viz.generate_product_stats())
    else:
        print(viz.generate_summary())


def cmd_account(config: Config, db: Database, args):
    """多账号管理"""
    from src.multi_account.manager import AccountManager
    
    manager = AccountManager(db)
    
    if args.action == "list":
        accounts = manager.get_accounts()
        print("\n👨‍👩‍👧‍👦 家庭账号列表")
        print("=" * 50)
        if not accounts:
            print("暂无账号")
        else:
            for i, acc in enumerate(accounts, 1):
                marker = "👤" if i == 1 else "  "
                print(f"{marker} {i}. {acc['name']} ({acc['phone']})")
        print("=" * 50)
        
        # 显示汇总统计
        stats = manager.get_stats_summary()
        print(f"\n📊 家庭汇总:")
        print(f"   账号数：{stats['total_accounts']}")
        print(f"   总申购：{stats['total_reservations']} 次")
        print(f"   总中签：{stats['total_wins']} 次")
        print(f"   家庭中签率：{stats['family_win_rate']}")
    
    elif args.action == "add":
        manager.add_account(args.phone, args.name, args.relation or "家人")
        print(f"✅ 已添加账号：{args.name} ({args.phone})")
    
    elif args.action == "remove":
        if manager.remove_account(args.phone):
            print(f"✅ 已移除账号：{args.phone}")
        else:
            print(f"❌ 未找到账号：{args.phone}")
    
    elif args.action == "plan":
        from src.multi_account.manager import FamilyReservationHelper
        helper = FamilyReservationHelper(manager)
        
        stores = args.stores.split(",") if args.stores else ["store_001", "store_002", "store_003"]
        product = args.product or "53%vol 500ml 贵州茅台酒 (飞天)"
        
        plan = helper.generate_reservation_plan(product, stores)
        
        print("\n📋 今日申购计划")
        print("=" * 70)
        print(f"{'账号':<10} {'手机号':<13} {'产品':<25} {'门店':<15}")
        print("=" * 70)
        for item in plan:
            print(f"{item['account']:<10} {item['phone']:<13} {item['product'][:24]:<25} {item['store']:<15}")
        print("=" * 70)
        
        # 检查冲突
        warnings = helper.check_conflicts(plan)
        if warnings:
            print("\n⚠️ 冲突提醒:")
            for w in warnings:
                print(f"   {w}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="🍶 i 茅台申购辅助工具",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # start 命令
    subparsers.add_parser("start", help="启动提醒服务")
    
    # stats 命令
    stats_parser = subparsers.add_parser("stats", help="查看统计数据")
    stats_parser.add_argument("--month", type=str, help="月份 (格式：2026-03)")
    
    # store 命令
    store_parser = subparsers.add_parser("store", help="查询门店")
    store_parser.add_argument("--nearby", action="store_true", help="查询附近门店")
    store_parser.add_argument("--distance", type=float, help="距离 (公里)")
    
    # remind 命令
    remind_parser = subparsers.add_parser("remind", help="手动触发提醒")
    remind_parser.add_argument(
        "--type",
        choices=["purchase_start", "purchase_end", "result"],
        required=True,
        help="提醒类型"
    )
    
    # export 命令
    export_parser = subparsers.add_parser("export", help="导出数据")
    export_parser.add_argument("--format", choices=["csv", "json"], default="csv")
    export_parser.add_argument("--output", type=str, help="输出文件路径")
    
    # dashboard 命令
    dashboard_parser = subparsers.add_parser("dashboard", help="显示数据看板")
    dashboard_parser.add_argument("--full", action="store_true", help="显示完整报告")
    dashboard_parser.add_argument("--calendar", action="store_true", help="显示日历")
    dashboard_parser.add_argument("--products", action="store_true", help="显示产品统计")
    
    # account 命令
    account_parser = subparsers.add_parser("account", help="多账号管理")
    account_parser.add_argument("action", choices=["list", "add", "remove", "plan"], 
                               help="操作类型")
    account_parser.add_argument("--phone", type=str, help="手机号")
    account_parser.add_argument("--name", type=str, help="姓名")
    account_parser.add_argument("--relation", type=str, help="关系 (本人/配偶/父母/子女)")
    account_parser.add_argument("--product", type=str, help="产品名称")
    account_parser.add_argument("--stores", type=str, help="门店列表 (逗号分隔)")
    
    args = parser.parse_args()
    
    # 加载配置
    config_path = Path("config.yaml")
    if not config_path.exists():
        logger.error("❌ 配置文件不存在，请复制 config.yaml.example 为 config.yaml")
        sys.exit(1)
    
    config = Config(config_path)
    setup_logger(config)
    
    # 初始化数据库
    db = Database(config)
    db.init_tables()
    
    # 执行命令
    if args.command == "start":
        cmd_start(config, db)
    elif args.command == "stats":
        cmd_stats(config, db, args)
    elif args.command == "store":
        cmd_store(config, args)
    elif args.command == "remind":
        cmd_remind(config, db, args)
    elif args.command == "export":
        cmd_export(config, db, args)
    elif args.command == "dashboard":
        cmd_dashboard(config, db, args)
    elif args.command == "account":
        cmd_account(config, db, args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
