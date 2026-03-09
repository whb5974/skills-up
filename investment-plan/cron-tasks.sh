#!/bin/bash
# ===========================================
# 2026 投资计划 - 定时任务配置
# ===========================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"

echo "📅 投资计划定时任务配置"
echo "============================================"

# 显示当前的 cron 配置
echo ""
echo "当前用户的 cron 任务:"
crontab -l 2>/dev/null || echo "暂无 cron 任务"

echo ""
echo "============================================"
echo "建议添加以下 cron 任务 (需要手动执行):"
echo "============================================"

cat << 'EOF'

# 每日 9:30 开盘提醒
30 9 * * 1-5 echo "📈 股市开盘了！检查持仓和新闻" | wall

# 每周五 17:00 周复盘
0 17 * * 5 cd /home/ghost/.openclaw/workspace/investment-plan && python3 portfolio-tracker.py --report >> logs/weekly_$(date +\%Y\%m\%d).log 2>&1

# 每月 15 日 定投提醒
0 9 15 * * echo "💰 今天是基金定投日！建议定投 2000 元" | wall

# 每月最后一天 22:00 月复盘
0 22 28-31 * * [ "$(date +\%d -d tomorrow)" = "01" ] && cd /home/ghost/.openclaw/workspace/investment-plan && python3 portfolio-tracker.py --report >> logs/monthly_$(date +\%Y\%m).log 2>&1

# 每季度最后一天 20:00 季度复盘
0 20 28-31 3,6,9,12 * * [ "$(date +\%m -d tomorrow)" = "01" ] && echo "📊 季度复盘日！检查资产配置再平衡" | wall

EOF

echo ""
echo "============================================"
echo "添加 cron 任务方法:"
echo "============================================"
echo ""
echo "1. 编辑 crontab:"
echo "   crontab -e"
echo ""
echo "2. 粘贴上面的任务配置"
echo ""
echo "3. 保存退出"
echo ""
echo "============================================"

# 创建系统服务配置（可选）
SERVICE_FILE="/etc/systemd/system/investment-daily.service"
echo ""
echo "或者创建 systemd 服务 (需要 sudo):"
echo ""
echo "sudo tee $SERVICE_FILE > /dev/null << 'SERVICE'"

cat << 'SERVICE'
[Unit]
Description=Daily Investment Check
After=network.target

[Service]
Type=oneshot
ExecStart=/bin/bash -c 'cd /home/ghost/.openclaw/workspace/investment-plan && python3 portfolio-tracker.py --report'
WorkingDirectory=/home/ghost/.openclaw/workspace/investment-plan
StandardOutput=append:/var/log/investment-daily.log
StandardError=append:/var/log/investment-daily.log

[Install]
WantedBy=multi-user.target
SERVICE

echo ""
echo "然后创建定时器:"
echo ""
cat << 'TIMER'
sudo tee /etc/systemd/system/investment-daily.timer > /dev/null << 'EOF'
[Unit]
Description=Run investment check daily at 9:00 AM
Requires=investment-daily.service

[Timer]
OnCalendar=*-*-* 09:00:00
Persistent=true

[Install]
WantedBy=timers.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable investment-daily.timer
sudo systemctl start investment-daily.timer
TIMER

echo ""
echo "============================================"
echo "✅ 配置说明完成"
echo "============================================"
