#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qbot 学习日报 - 飞书推送脚本
每天 12:00 自动发送学习报告到飞书群
"""

import json
import os
import requests
from datetime import datetime

# 飞书配置
APP_ID = "cli_a92910c88bf89bb3"
APP_SECRET = "O6WuZwPyHpkZbFW4fZkk8cMsQg4RwzfN"
FEISHU_CHAT_ID = "oc_61223fa3823a1a7373a10b6974358342"

# 学习日志路径
LOG_PATH = "/home/ghost/.openclaw/workspace/qbot-learning-log"

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
    """生成学习报告"""
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(LOG_PATH, f"{today}.md")
    
    if not os.path.exists(log_file):
        return f"⚠️ 今日 ({today}) 学习日志暂未更新"
    
    with open(log_file, 'r', encoding='utf-8') as f:
        log_content = f.read()
    
    # 提取关键信息
    stage = "未知"
    duration = "未知"
    status = "🟢 正常进行"
    completed = []
    issues = []
    plans = []
    
    in_completed = False
    in_issues = False
    in_plans = False
    
    for line in log_content.split('\n'):
        if '学习阶段：' in line:
            stage = line.split('学习阶段：')[1].strip().strip('**').strip()
        elif '学习时长：' in line:
            duration = line.split('学习时长：')[1].strip().strip('**').strip()
        elif '学习状态：' in line:
            status = line.split('学习状态：')[1].strip().strip('**').strip()
        elif '## ✅ 已完成' in line:
            in_completed = True
            in_issues = False
            in_plans = False
        elif '## ❌ 遇到问题' in line:
            in_completed = False
            in_issues = True
            in_plans = False
        elif '## 📈 明日计划' in line:
            in_completed = False
            in_issues = False
            in_plans = True
        elif line.startswith('- [x] ') and in_completed:
            task = line.replace('- [x] ', '').strip()
            if task and task not in completed:
                completed.append(task)
        elif line.startswith('- [ ] ') and in_plans:
            task = line.replace('- [ ] ', '').strip()
            if task and task not in plans:
                plans.append(task)
        elif line.startswith('### 问题') and in_issues:
            in_issues = True
        elif in_issues and line.startswith('**现象：**'):
            issue = line.replace('**现象：**', '').strip()
            if issue and issue not in issues:
                issues.append(issue)
    
    # 构建报告
    report = f"""📊 Qbot 学习日报 - {today}

📅 学习阶段：{stage}
⏱️ 学习时长：{duration}
📈 学习状态：{status}

━━━━━━━━━━━━━━━━━━

✅ 今日完成：
"""
    for item in completed:
        report += f"✅ {item}\n"
    
    if issues:
        report += "\n━━━━━━━━━━━━━━━━━━\n\n❌ 遇到问题：\n"
        for issue in issues:
            report += f"• {issue}\n"
    
    report += "\n━━━━━━━━━━━━━━━━━━\n\n📈 明日计划：\n"
    for plan in plans:
        report += f"⬜ {plan}\n"
    
    # 计算总进度
    day_num = stage.split('Day ')[1].split(' ')[0] if 'Day ' in stage else "?"
    week_num = "第？周"
    
    # 尝试从日志中提取周次（格式：第 X 周 或 第X周）
    for line in log_content.split('\n'):
        # 匹配 "周次：第 2 周" 或 "周次：第 2 周 (xxx)"
        if '周次：' in line:
            import re
            match = re.search(r'第\s*(\d+)\s*周', line)
            if match:
                week_num = f"第{match.group(1)}周"
                break
        # 备用：从学习阶段行提取
        elif '学习阶段：' in line and '第' in line and '周' in line:
            import re
            match = re.search(r'第\s*(\d+)\s*周', line)
            if match:
                week_num = f"第{match.group(1)}周"
    
    report += f"\n━━━━━━━━━━━━━━━━━━\n\n🎯 总进度：Day {day_num}/42 ({week_num})\n\n---\n自动推送 by AI Investment Assistant"

    return report

if __name__ == "__main__":
    try:
        report = generate_report()
        print("📤 准备发送飞书消息...")
        print(f"群聊 ID: {FEISHU_CHAT_ID}")
        print(f"消息内容:\n{report}\n")
        
        send_message(FEISHU_CHAT_ID, report)
        
        print("✅ 学习报告已成功发送到飞书群!")
    except Exception as e:
        print(f"❌ 发送失败：{e}")
        exit(1)
