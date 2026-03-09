#!/usr/bin/env python3
"""
Qbot 每日学习检查脚本
每天早上 9:00 自动生成学习报告
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# 工作区根目录
WORKSPACE = Path("/home/ghost/.openclaw/workspace")
LEARNING_LOG_DIR = WORKSPACE / "qbot-learning-log"
PLAN_FILE = WORKSPACE / "qbot-daily-learning-plan.md"
ISSUES_FILE = WORKSPACE / "qbot-issues" / "issues.md"

# 确保目录存在
LEARNING_LOG_DIR.mkdir(exist_ok=True)
ISSUES_FILE.parent.mkdir(exist_ok=True)


def get_day_number():
    """计算当前是第几天（从 2026-02-26 开始）"""
    start_date = datetime(2026, 2, 26)
    today = datetime.now()
    delta = today - start_date
    return delta.days


def get_week_number():
    """计算当前是第几周"""
    day = get_day_number()
    return (day // 7) + 1


def get_today_task():
    """获取今日学习任务"""
    day = get_day_number()
    week = get_week_number()
    
    # 6 周学习计划
    curriculum = {
        1: ["环境搭建", "数据源配置", "股票数据获取", "基金数据获取", "数据清洗", "技术指标", "周复盘"],
        2: ["双均线策略", "布林带策略", "MACD 策略", "RSI 策略", "参数优化", "策略对比", "周复盘"],
        3: ["Backtrader 框架", "回测数据", "策略回测", "绩效分析", "滑点手续费", "可视化", "周复盘"],
        4: ["止损策略", "止盈策略", "仓位管理", "风险敞口", "回撤控制", "组合分散", "周复盘"],
        5: ["特征工程", "LSTM 预测", "XGBoost 选股", "强化学习", "模型评估", "模型集成", "周复盘"],
        6: ["模拟交易", "实盘 API", "订单管理", "监控告警", "日志记录", "自动化", "毕业复盘"],
    }
    
    if week > 6:
        return "毕业复习", "复习所有内容，完善策略库"
    
    day_in_week = day % 7
    if day_in_week >= len(curriculum[week]):
        day_in_week = len(curriculum[week]) - 1
    
    task = curriculum[week][day_in_week]
    return task, f"第{week}周 - {task}"


def check_yesterday_log():
    """检查昨日学习日志"""
    yesterday = datetime.now() - timedelta(days=1)
    log_file = LEARNING_LOG_DIR / f"{yesterday.strftime('%Y-%m-%d')}.md"
    
    if log_file.exists():
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取关键信息
        completed = "✅" in content
        issues = "❌" in content
        hours = "学习时长" in content
        
        return {
            "exists": True,
            "completed": completed,
            "has_issues": issues,
            "has_time_record": hours,
            "content": content[:1000]  # 前 1000 字
        }
    else:
        return {"exists": False, "completed": False, "has_issues": False}


def load_issues():
    """加载问题记录"""
    if ISSUES_FILE.exists():
        with open(ISSUES_FILE, 'r', encoding='utf-8') as f:
            return f.read()[:500]  # 前 500 字
    return ""


def generate_daily_report():
    """生成每日学习报告"""
    day = get_day_number()
    week = get_week_number()
    today_task, task_desc = get_today_task()
    yesterday = check_yesterday_log()
    
    # 计算进度
    total_days = 42
    progress = (day / total_days) * 100
    
    # 生成报告
    report = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 Qbot 量化交易学习日报
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 日期：{datetime.now().strftime('%Y年%m月%d日 %A')}
⏰ 时间：{datetime.now().strftime('%H:%M')}
📊 进度：Day {day}/42 (第{week}周) - {progress:.1f}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 今日学习任务
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 任务：{today_task}
📝 说明：{task_desc}

✅ 建议完成：
  1. 学习 {today_task} 相关文档
  2. 完成实践练习
  3. 记录学习笔记
  4. 提交问题记录

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 昨日学习情况
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    if yesterday.get("exists"):
        report += f"""
✅ 日志：已提交
📝 完成状态：{"已完成" if yesterday["completed"] else "待确认"}
⚠️  问题：{"有" if yesterday["has_issues"] else "无"}
"""
    else:
        if day > 0:
            report += "\n⚠️  日志：未找到昨日学习日志\n"
        else:
            report += "\n🎉 今天是学习第一天！\n"
    
    # 问题追踪
    issues = load_issues()
    if issues:
        report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ 待解决问题
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{issues[:300]}...
"""
    
    # 学习建议
    report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 今日建议
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    if week == 1:
        report += """
🔧 本周重点：环境搭建
- 优先解决网络问题
- 确保依赖安装成功
- 配置好数据源
- 不必追求完美，先跑起来
"""
    elif week == 2:
        report += """
💻 本周重点：策略开发
- 理解每个策略的逻辑
- 手动实现代码
- 不要直接复制
- 多画图理解信号
"""
    elif week == 3:
        report += """
📊 本周重点：回测系统
- 学习 Backtrader API
- 注意回测陷阱
- 考虑交易成本
- 可视化结果
"""
    elif week == 4:
        report += """
🛡️  本周重点：风险控制
- 止损是生命线
- 仓位决定生死
- 不要满仓操作
- 分散投资
"""
    elif week == 5:
        report += """
🤖 本周重点：AI 模型
- 不要迷信模型
- 特征工程最重要
- 防止过拟合
- 实盘验证
"""
    elif week == 6:
        report += """
🚀 本周重点：实盘对接
- 先用模拟盘
- 小资金测试
- 做好监控
- 记录日志
"""
    else:
        report += """
🎓 毕业复习
- 整理策略库
- 完善文档
- 准备实盘
- 持续学习
"""
    
    # 快速命令
    report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ 快速开始
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 查看学习计划
cat qbot-daily-learning-plan.md

# 查看示例策略
cat investment-plan/strategies/*.py

# 运行集成模块
python3 investment-plan/qbot-integration.py

# 记录今日学习
echo "# Qbot 学习日志 - $(date +%Y-%m-%d)" >> qbot-learning-log/$(date +%Y-%m-%d).md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 开始今天的学习吧！加油！💪

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    return report


def save_daily_log():
    """保存今日学习日志模板"""
    today = datetime.now().strftime('%Y-%m-%d')
    day = get_day_number()
    week = get_week_number()
    today_task, task_desc = get_today_task()
    
    log_file = LEARNING_LOG_DIR / f"{today}.md"
    
    if log_file.exists():
        return False  # 已存在
    
    template = f"""# Qbot 学习日志 - {today}

## 📅 基本信息

- **学习阶段：** Day {day} - {today_task}
- **日期：** {today}
- **周次：** 第{week}周
- **学习时长：** _小时_

---

## 📊 今日进度

### 学习内容

1. 

---

## ✅ 已完成

- [ ] 

---

## ❌ 遇到问题

### 问题 1

**现象：**

**原因：**

**解决方案：**

**状态：** ⬜ 待解决 / ✅ 已解决

---

## 💡 学习心得



---

## 📈 明日计划

### 学习目标


### 任务清单
- [ ] 

### 预计耗时


---

## 🔄 优化建议



---

## 📝 笔记



---

## 🎯 进度追踪

| 指标 | 目标 | 当前 |
|------|------|------|
| 总进度 | 42 天 | Day {day}/42 |
| 策略开发 | 5+ 个 | /5 |
| 回测完成 | 3+ 次 | /3 |
| 问题记录 | 持续 | 个 |

---

**下次汇报：** {datetime.now().strftime('%Y-%m-%d')} 09:00

**学习状态：** 🟢 正常进行 / 🟡 遇到问题 / 🔴 停滞

---

*Generated by AI Investment Assistant*
"""
    
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(template)
    
    return True


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("🤖 Qbot 每日学习检查")
    print("=" * 60 + "\n")
    
    # 生成报告
    report = generate_daily_report()
    print(report)
    
    # 保存日志模板
    if save_daily_log():
        today = datetime.now().strftime('%Y-%m-%d')
        print(f"\n✅ 已创建今日学习日志：qbot-learning-log/{today}.md")
    
    # 返回报告（用于消息发送）
    return report


if __name__ == "__main__":
    main()
