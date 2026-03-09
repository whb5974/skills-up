#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
等保测评自动化项目 - 每日进度报告
每天上午 10 点自动发送项目执行过程和结果到飞书群
"""

import json
import os
import subprocess
from datetime import datetime, timedelta

# 飞书群 ID
FEISHU_CHAT_ID = "oc_79169c8c6daa7864f85ad4404de3be22"

# 项目路径
PROJECT_PATH = "/home/ghost/.openclaw/workspace/dbp-automation"
WORKSPACE_PATH = "/home/ghost/.openclaw/workspace"

# GitHub 仓库
GITHUB_REPO = "https://github.com/whb5974/DBsecurity.git"

def get_project_status():
    """获取项目当前状态"""
    status = {
        'phase': '方案设计与评审阶段',
        'progress': '15%',
        'next_milestone': 'M0 项目启动',
        'milestone_date': '2026-03-07',
        'health': '🟢 正常'
    }
    
    # 检查项目目录
    if os.path.exists(PROJECT_PATH):
        docs = [f for f in os.listdir(os.path.join(PROJECT_PATH, 'docs')) if f.endswith('.md')]
        status['docs_count'] = len(docs)
    else:
        status['docs_count'] = 0
        status['health'] = '🔴 异常'
    
    # 检查 Git 状态
    try:
        result = subprocess.run(
            ['git', '-C', PROJECT_PATH, 'log', '--oneline', '-1'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            status['last_commit'] = result.stdout.strip()
        else:
            status['last_commit'] = '暂无提交'
    except:
        status['last_commit'] = '获取失败'
    
    # 检查 GitHub 推送状态
    try:
        result = subprocess.run(
            ['git', '-C', PROJECT_PATH, 'ls-remote', '--heads', 'origin'],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            status['github_status'] = '✅ 已同步'
        else:
            status['github_status'] = '⚠️ 未推送'
    except:
        status['github_status'] = '❌ 连接失败'
    
    return status

def get_recent_tasks():
    """获取近期任务执行情况"""
    tasks = []
    
    # 检查是否有新的脚本文件
    scripts_path = os.path.join(PROJECT_PATH, 'scripts')
    if os.path.exists(scripts_path):
        scripts = [f for f in os.listdir(scripts_path) if f.endswith('.py')]
        if scripts:
            tasks.append(f"✅ 检测脚本开发：{len(scripts)} 个脚本已创建")
        else:
            tasks.append("⏳ 检测脚本开发：准备中")
    else:
        tasks.append("⏳ 检测脚本开发：目录待创建")
    
    # 检查文档完整性
    docs_path = os.path.join(PROJECT_PATH, 'docs')
    if os.path.exists(docs_path):
        docs = os.listdir(docs_path)
        tasks.append(f"✅ 项目文档：{len(docs)} 份文档已归档")
    else:
        tasks.append("⚠️ 项目文档：目录不存在")
    
    # GitHub 推送任务
    tasks.append("⏳ GitHub 推送：等待网络恢复")
    
    return tasks

def get_next_actions():
    """获取下一步行动计划"""
    today = datetime.now()
    
    actions = [
        "📋 项目立项审批（2026-03-07 前）",
        "👥 组建项目团队（2026-03-10 前）",
        "🚀 召开项目启动会（2026-03-14 前）",
        "📝 启动需求分析（2026-03-15）",
        "💻 搭建开发环境（2026-03-20）"
    ]
    
    return actions

def generate_report():
    """生成飞书消息报告"""
    status = get_project_status()
    tasks = get_recent_tasks()
    actions = get_next_actions()
    
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 构建飞书消息
    report = f"""🔐 **等保测评自动化项目日报** - {today}

📊 **项目状态**
━━━━━━━━━━━━━━━━━━
📁 项目阶段：{status['phase']}
📈 整体进度：{status['progress']}
🎯 下一里程碑：{status['next_milestone']}
📅 里程碑日期：{status['milestone_date']}
💚 项目健康度：{status['health']}

━━━━━━━━━━━━━━━━━━

📝 **今日执行情况**
━━━━━━━━━━━━━━━━━━
{chr(10).join(tasks)}

━━━━━━━━━━━━━━━━━━

📋 **下一步行动计划**
━━━━━━━━━━━━━━━━━━
{chr(10).join(actions)}

━━━━━━━━━━━━━━━━━━

💾 **代码管理状态**
━━━━━━━━━━━━━━━━━━
📦 最后提交：{status.get('last_commit', '暂无')}
🌐 GitHub 状态：{status.get('github_status', '未知')}
🔗 仓库地址：{GITHUB_REPO}

━━━━━━━━━━━━━━━━━━

📂 **项目文档**
━━━━━━━━━━━━━━━━━━
✅ 细化工作方案 v2.0
✅ 完整方案 v3.0
✅ 交付成果汇总
✅ 测评项设计
✅ 研讨记录
✅ 学习报告
✅ 工作计划

━━━━━━━━━━━━━━━━━━

🎯 **项目周期：** 2026-03-01 至 2026-08-31（6 个月）
👥 **资源配置：** 项目经理 1 人 + 安全专家 1 人 + 开发 3 人 + 测试 1 人

---
_自动推送 by 等保测评自动化项目助手_"""

    return report

def send_to_feishu(message):
    """发送到飞书群"""
    # 使用 OpenClaw 的 message 工具发送
    # 这里输出消息内容，由外部脚本调用 OpenClaw 发送
    print(message)
    return True

if __name__ == "__main__":
    report = generate_report()
    send_to_feishu(report)
    print("\n✅ 项目日报已生成")
