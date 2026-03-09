#!/bin/bash
# 太原天气预报定时任务 - 简化版本
# 每天 17:50 执行，获取次日天气预报并推送到飞书群

set -e

# 设置 PATH
export PATH="$HOME/.npm-global/bin:$PATH"
export HOME="/home/ghost"

# 配置
WEATHER_LOG="/home/ghost/.openclaw/logs/weather.log"
FEISHU_CHAT_ID="oc_61223fa3823a1a7373a10b6974358342"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$WEATHER_LOG"
}

log "=== 天气推送任务开始 ==="

# 获取太原天气数据 (Open-Meteo API)
log "获取天气数据..."
RESPONSE=$(curl -s --max-time 10 "https://api.open-meteo.com/v1/forecast?latitude=37.8706&longitude=112.5489&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=Asia%2FShanghai&forecast_days=2")

if [ -z "$RESPONSE" ]; then
    log "❌ 错误：无法获取天气数据"
    exit 1
fi

# 解析天气数据
TOMORROW_DATE=$(echo "$RESPONSE" | grep -o '"time":\["[^"]*","[^"]*"' | cut -d'"' -f4)
WEATHER_CODE=$(echo "$RESPONSE" | grep -o '"weather_code":\[[0-9]*,[0-9]*\]' | cut -d'[' -f2 | cut -d',' -f2 | tr -d ' ')
TEMP_MAX=$(echo "$RESPONSE" | grep -o '"temperature_2m_max":\[[0-9.]*,[0-9.]*\]' | cut -d'[' -f2 | cut -d',' -f2 | tr -d ' ')
TEMP_MIN=$(echo "$RESPONSE" | grep -o '"temperature_2m_min":\[[0-9.-]*,[0-9.-]*\]' | cut -d'[' -f2 | cut -d',' -f2 | tr -d ' ')
PRECIP=$(echo "$RESPONSE" | grep -o '"precipitation_probability_max":\[[0-9]*,[0-9]*\]' | cut -d'[' -f2 | cut -d',' -f2 | tr -d ' ')

# 天气代码转中文描述
case $WEATHER_CODE in
  0) WEATHER="☀️ 晴" ;;
  1|2|3) WEATHER="⛅ 多云" ;;
  45|48) WEATHER="🌫️ 雾" ;;
  51|53|55) WEATHER="🌧️ 毛毛雨" ;;
  61|63|65) WEATHER="🌧️ 雨" ;;
  71|73|75) WEATHER="❄️ 雪" ;;
  77) WEATHER="🌨️ 阵雪" ;;
  80|81|82) WEATHER="🌦️ 阵雨" ;;
  95|96|99) WEATHER="⛈️ 雷雨" ;;
  *) WEATHER="🌤️ 多云" ;;
esac

# 格式化日期
DISPLAY_DATE=$(echo "$TOMORROW_DATE" | cut -d'-' -f2,3)

# 构建消息内容
MESSAGE="🌤️ **太原·明日天气**
📅 ${DISPLAY_DATE}
${WEATHER}
🌡️ ${TEMP_MIN}°C ~ ${TEMP_MAX}°C
💧 降水概率：${PRECIP}%"

log "✅ 天气数据：${TOMORROW_DATE}, ${WEATHER}, ${TEMP_MIN}~${TEMP_MAX}°C"

# 发送到飞书群
log "📤 发送消息到飞书群..."
openclaw message send --channel feishu --target "chat:${FEISHU_CHAT_ID}" --message "$MESSAGE" 2>&1 | tee -a "$WEATHER_LOG"

log "=== 任务完成 ==="
