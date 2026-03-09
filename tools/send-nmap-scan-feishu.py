#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nmap 端口扫描报告 - 飞书推送脚本
发送完整 nmap 扫描结果到飞书群
"""

import json
import requests
from datetime import datetime

# 飞书配置
APP_ID = "cli_a92910c88bf89bb3"
APP_SECRET = "O6WuZwPyHpkZbFW4fZkk8cMsQg4RwzfN"
FEISHU_CHAT_ID = "oc_79169c8c6daa7864f85ad4404de3be22"

def get_access_token():
    """获取飞书 access token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }
    
    response = requests.post(url, json=payload, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result.get("tenant_access_token")
    else:
        raise Exception(f"获取 access token 失败：{result}")

def send_message(chat_id, content):
    """发送消息到飞书群"""
    token = get_access_token()
    
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "receive_id": chat_id,
        "msg_type": "text",
        "content": json.dumps({"text": content}, ensure_ascii=False)
    }
    
    params = {"receive_id_type": "chat_id"}
    
    response = requests.post(url, headers=headers, json=payload, params=params, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return True
    else:
        raise Exception(f"发送消息失败：{result}")

def generate_report():
    """生成 nmap 扫描报告"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    report = f"""🔍 Nmap 完整端口扫描报告 - {timestamp}

📊 扫描目标：localhost (127.0.0.1)
🛠️ 扫描方式：全端口 + 服务版本检测
📈 开放端口：7/65535

━━━━━━━━━━━━━━━━━━

📋 开放端口详情:

🟢 低风险:
• 631 - CUPS 2.4 (打印服务)
• 18789 - OpenClaw Control UI
• 18791 - Node.js Express (内部 API)
• 18792 - OpenClaw Gateway

🟡 中风险:
• 22 - OpenSSH 9.6p1 Ubuntu
• 3456 - PDF 下载中心 (Node.js)

🟠 较高风险:
• 3389 - xrdp (远程桌面)

━━━━━━━━━━━━━━━━━━

⚠️ 安全建议:

🔴 高优先级:
1. 端口 3389 (XRDP) - 建议关闭或限制访问
2. 端口 3456 (PDF 中心) - 检查访问控制

🟡 中优先级:
3. 端口 22 (SSH) - 确保密钥认证
4. 配置防火墙 (UFW)

🟢 低优先级:
5. 定期执行端口扫描

━━━━━━━━━━━━━━━━━━

🔧 快速修复:

# 关闭 XRDP (如不需要)
sudo systemctl stop xrdp
sudo systemctl disable xrdp

# 启用防火墙
sudo ufw enable
sudo ufw allow 22/tcp
sudo ufw deny 3389/tcp

━━━━━━━━━━━━━━━━━━

📄 完整报告:
/home/ghost/.openclaw/workspace/nmap-scans/nmap-localhost-full-2026-03-01.md

---
自动推送 by AI Security Assistant"""

    return report

if __name__ == "__main__":
    try:
        report = generate_report()
        print("📤 准备发送飞书消息...")
        print(f"群聊 ID: {FEISHU_CHAT_ID}")
        print(f"消息内容:\n{report}\n")
        
        send_message(FEISHU_CHAT_ID, report)
        
        print("✅ Nmap 扫描报告已成功发送到飞书群!")
    except Exception as e:
        print(f"❌ 发送失败：{e}")
        exit(1)
