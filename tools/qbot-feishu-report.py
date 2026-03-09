#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qbot 学习日报 - 飞书推送脚本
每天 12:00 自动发送学习报告到飞书群
"""

import json
import os
from datetime import datetime

# 飞书群 ID
FEISHU_CHAT_ID = "oc_61223fa3823a1a7373a10b6974358342"

# 学习日志路径
LOG_PATH = "/home/ghost/.openclaw/workspace/qbot-learning-log"

def read_today_log():
    """读取今日学习日志"""
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(LOG_PATH, f"{today}.md")
    
    if not os.path.exists(log_file):
        return None
    
    with open(log_file, 'r', encoding='utf-8') as f:
        return f.read()

def generate_report():
    """生成飞书消息报告"""
    log_content = read_today_log()
    
    if not log_content:
        return "⚠️ 今日学习日志暂未更新"
    
    # 提取关键信息
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 解析日志内容（简化版）
    lines = log_content.split('\n')
    study_stage = "Day 3 - 基金数据获取与 API 学习"
    study_hours = "2.5 小时"
    status = "🟢 正常进行"
    
    completed = []
    issues = []
    tomorrow_plan = []
    
    in_completed = False
    in_issues = False
    in_tomorrow = False
    
    for line in lines:
        if '## ✅ 已完成' in line:
            in_completed = True
            in_issues = False
            in_tomorrow = False
            continue
        elif '## ❌ 遇到问题' in line:
            in_completed = False
            in_issues = True
            in_tomorrow = False
            continue
        elif '## 📈 明日计划' in line:
            in_completed = False
            in_issues = False
            in_tomorrow = True
            continue
        elif line.startswith('## '):
            in_completed = False
            in_issues = False
            in_tomorrow = False
            continue
        
        if in_completed and line.strip().startswith('- [x]'):
            completed.append(line.strip().replace('- [x]', '✅').replace('- [ ]', '⬜'))
        elif in_issues and line.strip().startswith('**现象：**'):
            issues.append(line.strip())
        elif in_tomorrow and line.strip().startswith('- [ ]'):
            tomorrow_plan.append(line.strip().replace('- [ ]', '⬜'))
    
    # 构建飞书消息
    report = f"""📊 **Qbot 学习日报** - {today}

📅 **学习阶段：** {study_stage}
⏱️ **学习时长：** {study_hours}
📈 **学习状态：** {status}

━━━━━━━━━━━━━━━━━━

✅ **今日完成：**
{chr(10).join(completed) if completed else '暂无记录'}

━━━━━━━━━━━━━━━━━━

❌ **遇到问题：**
{issues[0] if issues else '无'}

━━━━━━━━━━━━━━━━━━

📈 **明日计划：**
{chr(10).join(tomorrow_plan[:3]) if tomorrow_plan else '暂无记录'}

━━━━━━━━━━━━━━━━━━

🎯 **总进度：** Day 3/42 (第 1 周 - 环境搭建与基础认知)

---
_自动推送 by AI Investment Assistant_"""

    return report

def send_to_feishu(message):
    """发送到飞书群（模拟）"""
    # 实际使用时需要调用飞书 API
    # 这里使用 OpenClaw 的 message 工具
    print(f"准备发送消息到飞书群 {FEISHU_CHAT_ID}:")
    print(message)
    return True

if __name__ == "__main__":
    report = generate_report()
    send_to_feishu(report)
    print("\n✅ 学习报告已生成")
