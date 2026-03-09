#!/bin/bash
# 太原天气预报定时任务 - 语音推送版本
# 每天 17:50 执行，获取次日天气预报，生成语音并推送到飞书群

set -e

# 设置 PATH
export PATH="$HOME/.npm-global/bin:$PATH"
export HOME="/home/ghost"

# 配置
WEATHER_LOG="/home/ghost/.openclaw/logs/weather.log"
FEISHU_CHAT_ID="oc_61223fa3823a1a7373a10b6974358342"
AUDIO_DIR="/home/ghost/.openclaw/workspace/audio"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$WEATHER_LOG"
}

log "=== 天气语音推送任务开始 ==="

# 创建音频目录
mkdir -p "$AUDIO_DIR"

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

# 天气代码转中文描述和语音文本
case $WEATHER_CODE in
  0) WEATHER="☀️ 晴"; VOICE_WEATHER="晴天" ;;
  1|2|3) WEATHER="⛅ 多云"; VOICE_WEATHER="多云" ;;
  45|48) WEATHER="🌫️ 雾"; VOICE_WEATHER="有雾" ;;
  51|53|55) WEATHER="🌧️ 毛毛雨"; VOICE_WEATHER="毛毛雨" ;;
  61|63|65) WEATHER="🌧️ 雨"; VOICE_WEATHER="下雨" ;;
  71|73|75) WEATHER="❄️ 雪"; VOICE_WEATHER="下雪" ;;
  77) WEATHER="🌨️ 阵雪"; VOICE_WEATHER="阵雪" ;;
  80|81|82) WEATHER="🌦️ 阵雨"; VOICE_WEATHER="阵雨" ;;
  95|96|99) WEATHER="⛈️ 雷雨"; VOICE_WEATHER="雷雨" ;;
  *) WEATHER="🌤️ 多云"; VOICE_WEATHER="多云" ;;
esac

# 格式化日期
DISPLAY_DATE=$(echo "$TOMORROW_DATE" | cut -d'-' -f2,3)

# 构建文字消息内容
TEXT_MESSAGE="🌤️ **太原·明日天气**
📅 ${DISPLAY_DATE}
${WEATHER}
🌡️ ${TEMP_MIN}°C ~ ${TEMP_MAX}°C
💧 降水概率：${PRECIP}%"

# 构建语音文本 (更人性化的表达)
# 根据天气情况调整语气
TEMP_MIN_INT=$(echo "$TEMP_MIN" | cut -d'.' -f1)
if [[ "$WEATHER_CODE" == "0" ]]; then
  VOICE_TEXT="哈喽～太原明天是个好天气哦，晴天，适合出门活动。气温在${TEMP_MIN}度到${TEMP_MAX}度之间，体感舒适。"
elif [[ "$WEATHER_CODE" =~ ^(61|63|65|80|81|82)$ ]]; then
  VOICE_TEXT="注意啦～太原明天要下雨哦，记得带伞。气温${TEMP_MIN}到${TEMP_MAX}度，降水概率${PRECIP}%，出门要小心路滑。"
elif [[ "$WEATHER_CODE" =~ ^(71|73|75|77)$ ]]; then
  VOICE_TEXT="太原明天要下雪啦，气温${TEMP_MIN}到${TEMP_MAX}度，出门记得多穿衣服，注意保暖哦。"
elif [[ "$TEMP_MIN_INT" -lt 0 ]]; then
  VOICE_TEXT="太原明天比较冷哦，${VOICE_WEATHER}，最低气温${TEMP_MIN}度，最高气温${TEMP_MAX}度，一定要穿厚衣服，注意防寒保暖。"
else
  VOICE_TEXT="太原明天${VOICE_WEATHER}，气温${TEMP_MIN}到${TEMP_MAX}度，降水概率${PRECIP}%。祝您有愉快的一天！"
fi

log "✅ 天气数据：${TOMORROW_DATE}, ${WEATHER}, ${TEMP_MIN}~${TEMP_MAX}°C"

# 发送文字消息到飞书群
log "📤 发送文字消息..."
openclaw message send --channel feishu --target "chat:${FEISHU_CHAT_ID}" --message "$TEXT_MESSAGE" 2>&1 | tee -a "$WEATHER_LOG"

# 生成语音并发送
log "🔊 生成并发送语音..."
AUDIO_FILE="${AUDIO_DIR}/weather-$(date +%Y%m%d).opus"

# 使用 Python edge-tts 生成语音 (opus 格式，调整语速和音调使其更自然)
python3 << PYTHON_SCRIPT
import asyncio
import edge_tts

TEXT = "${VOICE_TEXT}"
OUTPUT = "${AUDIO_FILE}"

async def generate():
    # 使用更温柔的语音，调整语速稍慢 (+10% 语速会让声音更友好)
    # 使用 XiaoxiaoNeural (温柔女声) 或 YunxiNeural (温暖男声)
    communicate = edge_tts.Communicate(
        TEXT, 
        "zh-CN-XiaoxiaoNeural",
        rate="+0%",      # 正常语速，稍微放慢更亲切
        pitch="+5Hz",    # 稍微提高音调，更活泼
        volume="+0%"     # 正常音量
    )
    await communicate.save(OUTPUT)

asyncio.run(generate())
PYTHON_SCRIPT

if [ -f "$AUDIO_FILE" ]; then
    log "✅ 语音文件已生成：$AUDIO_FILE ($(du -h "$AUDIO_FILE" | cut -f1))"
    
    # 发送语音到飞书群 (飞书支持 opus 格式的音频消息)
    log "📤 发送语音消息..."
    openclaw message send \
        --channel feishu \
        --target "chat:${FEISHU_CHAT_ID}" \
        --message "🔊 语音播报：太原明天天气，${VOICE_WEATHER}，最低气温${TEMP_MIN}度，最高气温${TEMP_MAX}度。" \
        --media "$AUDIO_FILE" 2>&1 | tee -a "$WEATHER_LOG"
    
    log "✅ 语音发送成功"
else
    log "⚠️ 语音文件生成失败，已发送文字版本"
fi

log "=== 任务完成 ==="
