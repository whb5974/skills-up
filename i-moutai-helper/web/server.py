#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web 数据看板服务器
提供可视化 Web 界面
"""

import json
import sys
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.config import Config
from src.utils.database import Database
from src.multi_account.manager import AccountManager


class DashboardAPIHandler(SimpleHTTPRequestHandler):
    """API 请求处理器"""
    
    def __init__(self, *args, config=None, db=None, **kwargs):
        self.config = config
        self.db = db
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """处理 GET 请求"""
        if self.path == '/api/stats':
            self.send_json_response(self.get_stats())
        elif self.path == '/api/calendar':
            self.send_json_response(self.get_calendar())
        elif self.path == '/api/products':
            self.send_json_response(self.get_products())
        elif self.path == '/api/accounts':
            self.send_json_response(self.get_accounts())
        elif self.path == '/':
            self.serve_file('index.html')
        else:
            self.serve_file(self.path[1:])
    
    def send_json_response(self, data):
        """发送 JSON 响应"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def serve_file(self, filename):
        """提供文件"""
        file_path = Path(__file__).parent / filename
        
        if not file_path.exists():
            self.send_error(404, 'File not found')
            return
        
        self.send_response(200)
        
        if filename.endswith('.html'):
            self.send_header('Content-Type', 'text/html; charset=utf-8')
        elif filename.endswith('.css'):
            self.send_header('Content-Type', 'text/css')
        elif filename.endswith('.js'):
            self.send_header('Content-Type', 'application/javascript')
        
        self.end_headers()
        
        with open(file_path, 'rb') as f:
            self.wfile.write(f.read())
    
    def get_stats(self):
        """获取统计数据"""
        manager = AccountManager(self.db)
        stats = manager.get_stats_summary()
        
        return {
            "success": True,
            "data": {
                "totalReservations": stats["total_reservations"],
                "totalWins": stats["total_wins"],
                "winRate": stats["family_win_rate"],
                "accountCount": stats["total_accounts"]
            }
        }
    
    def get_calendar(self):
        """获取日历数据"""
        user = self.db.get_user_by_phone(self.config.get("user.phone", ""))
        if not user:
            return {"success": True, "data": {"reservations": {}}}
        
        today = datetime.now()
        reservations = self.db.get_reservations(user["id"], f"{today.year}-{today.month:02d}")
        
        res_dict = {}
        for r in reservations:
            date = r.get("reservation_date", "")
            status = r.get("status", "pending")
            res_dict[date] = status
        
        return {
            "success": True,
            "data": {
                "year": today.year,
                "month": today.month,
                "reservations": res_dict
            }
        }
    
    def get_products(self):
        """获取产品统计"""
        user = self.db.get_user_by_phone(self.config.get("user.phone", ""))
        if not user:
            return {"success": True, "data": []}
        
        reservations = self.db.get_reservations(user["id"])
        
        product_stats = {}
        for r in reservations:
            product = r.get("product_name", "未知")[:20]
            if product not in product_stats:
                product_stats[product] = {"total": 0, "wins": 0}
            product_stats[product]["total"] += 1
            if r.get("status") == "success":
                product_stats[product]["wins"] += 1
        
        products = [
            {"name": name, **stats}
            for name, stats in product_stats.items()
        ]
        
        return {"success": True, "data": products}
    
    def get_accounts(self):
        """获取账号列表"""
        manager = AccountManager(self.db)
        accounts = manager.get_accounts()
        
        return {
            "success": True,
            "data": [
                {
                    "name": acc["name"],
                    "phone": acc["phone"][:3] + "****" + acc["phone"][-4:],
                    "relation": "本人" if i == 0 else "家人"
                }
                for i, acc in enumerate(accounts)
            ]
        }
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[Web] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {args[0]}")


def run_server(host='0.0.0.0', port=8080):
    """运行 Web 服务器"""
    # 加载配置
    config_path = Path(__file__).parent.parent / "config.yaml"
    config = Config(config_path)
    
    # 初始化数据库
    db = Database(config)
    db.init_tables()
    
    # 创建服务器
    server_address = (host, port)
    
    # 创建处理器类 (带配置和数据库)
    def handler(*args, **kwargs):
        return DashboardAPIHandler(*args, config=config, db=db, **kwargs)
    
    httpd = HTTPServer(server_address, handler)
    
    print(f"🌐 Web 数据看板已启动")
    print(f"📍 访问地址：http://localhost:{port}")
    print(f"📊 API 端点:")
    print(f"   - http://localhost:{port}/api/stats")
    print(f"   - http://localhost:{port}/api/calendar")
    print(f"   - http://localhost:{port}/api/products")
    print(f"   - http://localhost:{port}/api/accounts")
    print(f"\n按 Ctrl+C 停止服务")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 正在停止服务...")
        httpd.shutdown()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Web 数据看板服务器")
    parser.add_argument("--host", default="0.0.0.0", help="监听地址")
    parser.add_argument("--port", type=int, default=8080, help="监听端口")
    
    args = parser.parse_args()
    
    run_server(args.host, args.port)
