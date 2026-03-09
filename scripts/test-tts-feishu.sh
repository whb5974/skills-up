#!/bin/bash
# 测试 TTS 语音生成并发送到飞书

set -e

export PATH="$HOME/.npm-global/bin:$PATH"
export HOME="/home/ghost"

# 测试文本
TEXT="大家好，这是天气预报语音测试。太原明天天气晴朗，气温 5 到 18 度。"

# 生成语音文件 (opus 格式，飞书支持)
AUDIO_FILE="/tmp/weather-test-$(date +%Y%m%d%H%M%S).opus"

echo "生成 TTS 语音..."
# 使用 edge-tts 直接生成 opus 文件
edge-tts --voice zh-CN-XiaoxiaoNeural --text "$TEXT" --write-media "$AUDIO_FILE" 2>&1 || {
    echo "edge-tts 不可用，尝试使用 openclaw tts..."
    # 如果 edge-tts 不可用，使用 openclaw 的 tts 功能
    openclaw tts --text "$TEXT" 2>&1
    exit 1
}

if [ -f "$AUDIO_FILE" ]; then
    echo "✅ 语音文件已生成：$AUDIO_FILE ($(du -h "$AUDIO_FILE" | cut -f1))"
    
    # 发送到飞书群
    FEISHU_CHAT_ID="oc_61223fa3823a1a7373a10b6974358342"
    echo "📤 发送语音到飞书群..."
    
    # 使用 openclaw message send 发送音频文件
    openclaw message send \
        --channel feishu \
        --target "chat:${FEISHU_CHAT_ID}" \
        --message "🔊 语音测试：${TEXT}" \
        --media "$AUDIO_FILE" 2>&1
    
    echo "✅ 发送完成"
else
    echo "❌ 语音文件生成失败"
    exit 1
fi
