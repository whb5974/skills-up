#!/bin/bash
# 太原天气预报定时任务 - 每天 17:50 执行
# 获取次日天气预报并发送到飞书群

# 设置 PATH (cron 环境中可能缺少 npm global bin 路径)
export PATH="$HOME/.npm-global/bin:$PATH"

# 获取太原天气数据 (Open-Meteo API)
# 坐标：太原 37.8706°N, 112.5489°E
RESPONSE=$(curl -s --max-time 10 "https://api.open-meteo.com/v1/forecast?latitude=37.8706&longitude=112.5489&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=Asia%2FShanghai&forecast_days=2")

# 解析天气数据
TOMORROW_DATE=$(echo "$RESPONSE" | grep -o '"time":\["[^"]*","[^"]*"' | cut -d'"' -f4)
WEATHER_CODE=$(echo "$RESPONSE" | grep -o '"weather_code":\[[0-9]*,[0-9]*\]' | cut -d'[' -f2 | cut -d',' -f2)
TEMP_MAX=$(echo "$RESPONSE" | grep -o '"temperature_2m_max":\[[0-9.]*,[0-9.]*\]' | cut -d'[' -f2 | cut -d',' -f2)
TEMP_MIN=$(echo "$RESPONSE" | grep -o '"temperature_2m_min":\[[0-9.-]*,[0-9.-]*\]' | cut -d'[' -f2 | cut -d',' -f2)
PRECIP=$(echo "$RESPONSE" | grep -o '"precipitation_probability_max":\[[0-9]*,[0-9]*\]' | cut -d'[' -f2 | cut -d',' -f2)

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

# 格式化日期 (只显示月 - 日)
DISPLAY_DATE=$(echo "$TOMORROW_DATE" | cut -d'-' -f2,3)

# 构建消息内容
MESSAGE="🌤️ **太原·明日天气**
📅 ${DISPLAY_DATE}
${WEATHER}
🌡️ ${TEMP_MIN}°C ~ ${TEMP_MAX}°C
💧 降水概率：${PRECIP}%"

# 发送到飞书群 (使用 openclaw message 命令)
openclaw message send --channel feishu --target "chat:oc_61223fa3823a1a7373a10b6974358342" --message "$MESSAGE"

echo "天气推送完成：$TOMORROW_DATE"
