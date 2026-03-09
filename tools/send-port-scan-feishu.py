#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
端口扫描报告 - 飞书推送脚本
发送本地端口扫描结果到飞书群
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
    """生成端口扫描报告"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    report = f"""🔍 本地端口扫描报告 - {timestamp}

📊 扫描目标：本机 (localhost)
🛠️ 扫描方式：系统端口检测 (ss -ltnp)
⚠️ 备注：nmap 尚未安装

━━━━━━━━━━━━━━━━━━

📋 开放端口列表:

🟢 低风险 (本地监听):
• 53 - DNS (systemd-resolved)
• 631 - CUPS (打印机服务)
• 18789 - OpenClaw Gateway
• 18791/18792 - OpenClaw 内部

🟡 中风险:
• 22 - SSH (确保密钥认证)
• 3456 - Node.js 应用
• 3350 - 未知服务 (需调查)

🟠 较高风险:
• 3389 - RDP (远程桌面)

━━━━━━━━━━━━━━━━━━

⚠️ 安全建议:

1. 端口 3389 (RDP) - 如不需要请关闭
2. 端口 3350 (未知) - 建议调查此服务
3. 端口 22 (SSH) - 确保禁用 root 登录
4. 建议安装 nmap 进行详细扫描

━━━━━━━━━━━━━━━━━━

🔧 安装 Nmap:
sudo apt-get install -y nmap

📄 完整报告已保存:
/home/ghost/.openclaw/workspace/nmap-scans/local-port-scan-2026-03-01.md

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
        
        print("✅ 端口扫描报告已成功发送到飞书群!")
    except Exception as e:
        print(f"❌ 发送失败：{e}")
        exit(1)
