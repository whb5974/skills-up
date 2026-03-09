# 语音优化配置文档

## 🎙️ 语音人性化优化

### 优化内容

#### 1. 语音文本优化
根据天气情况使用不同的语气和表达方式：

| 天气 | 语音风格 | 示例 |
|------|----------|------|
| ☀️ 晴天 | 轻松愉快 | "哈喽～太原明天是个好天气哦，晴天，适合出门活动。" |
| 🌧️ 雨天 | 关怀提醒 | "注意啦～太原明天要下雨哦，记得带伞。" |
| ❄️ 雪天 | 温暖关心 | "太原明天要下雪啦，出门记得多穿衣服，注意保暖哦。" |
| 🥶 低温 | 贴心提醒 | "太原明天比较冷哦，一定要穿厚衣服，注意防寒保暖。" |
| 🌤️ 普通 | 友好祝福 | "祝您有愉快的一天！" |

#### 2. 语音参数优化

```python
communicate = edge_tts.Communicate(
    TEXT, 
    "zh-CN-XiaoxiaoNeural",  # 温柔女声
    rate="+0%",               # 正常语速 (不急不慢)
    pitch="+5Hz",             # 稍微提高音调 (更活泼)
    volume="+0%"              # 正常音量
)
```

**参数说明：**
- **rate**: 语速调整
  - `+0%` = 正常 (默认)
  - `+10%` = 稍快
  - `-10%` = 稍慢 (更稳重)
  
- **pitch**: 音调调整
  - `+5Hz` = 稍高 (更活泼)
  - `-5Hz` = 稍低 (更稳重)
  - `+0Hz` = 默认
  
- **volume**: 音量调整
  - `+0%` = 正常
  - `+10%` = 更大声
  - `-10%` = 更轻柔

#### 3. 可用语音库

| 语音 ID | 性别 | 风格 | 适用场景 |
|---------|------|------|----------|
| `zh-CN-XiaoxiaoNeural` | 女 | 温柔亲切 | 默认推荐 ⭐ |
| `zh-CN-YunxiNeural` | 男 | 温暖稳重 | 正式场合 |
| `zh-CN-YunjianNeural` | 男 | 激情解说 | 体育/活动 |
| `zh-CN-XiaoyiNeural` | 女 | 温柔甜美 | 儿童内容 |
| `zh-CN-XiaochenNeural` | 女 | 知性优雅 | 新闻播报 |

### 测试结果

**最新测试** (2026-03-07 16:45):
```
✅ 语音文件大小：64KB
✅ 语音时长：约 12 秒
✅ 语音风格：温柔女声，带关怀语气
✅ 文本内容："太原明天比较冷哦，多云，最低气温 -2.6 度，最高气温 10.8 度，一定要穿厚衣服，注意防寒保暖。"
```

### 对比

#### 优化前
```
文本："太原明天天气，多云，最低气温 -2.6 度，最高气温 10.8 度，降水概率 10%。"
风格：机械播报，无感情
```

#### 优化后
```
文本："太原明天比较冷哦，多云，最低气温 -2.6 度，最高气温 10.8 度，一定要穿厚衣服，注意防寒保暖。"
风格：温柔关怀，有人情味 ✨
```

## 🎛️ 自定义配置

### 修改语音风格

编辑脚本 `/home/ghost/.openclaw/workspace/scripts/weather-voice-push.sh`：

```bash
# 更活泼的版本
rate="+10%"      # 稍快
pitch="+10Hz"    # 更高

# 更稳重的版本
rate="-5%"       # 稍慢
pitch="-5Hz"     # 更低

# 更温柔的版本
rate="-10%"      # 更慢
pitch="+0Hz"     # 正常
```

### 更换语音

```bash
# 男声版本
communicate = edge_tts.Communicate(TEXT, "zh-CN-YunxiNeural", ...)

# 更甜美的女声
communicate = edge_tts.Communicate(TEXT, "zh-CN-XiaoyiNeural", ...)
```

### 添加更多人性化表达

在脚本中添加更多场景：

```bash
# 大风天气
if [[ "$WEATHER_CODE" =~ ^(51|52|53)$ ]]; then
  VOICE_TEXT="太原明天风比较大哦，气温${TEMP_MIN}到${TEMP_MAX}度，出门记得戴帽子，小心吹乱发型～"
fi

# 高温天气
if [[ "$TEMP_MAX_INT" -gt 35 ]]; then
  VOICE_TEXT="太原明天很热哦，最高气温${TEMP_MAX}度，注意防暑降温，多喝水，避免中暑。"
fi
```

## 📊 语音参数参考

### 语速 (rate)
| 值 | 效果 | 适用场景 |
|-----|------|----------|
| `-20%` | 很慢 | 冥想、放松 |
| `-10%` | 稍慢 | 严肃内容、老年人 |
| `0%` | 正常 | 日常对话 ⭐ |
| `+10%` | 稍快 | 活力内容 |
| `+20%` | 很快 | 紧急通知 |

### 音调 (pitch)
| 值 | 效果 | 适用场景 |
|-----|------|----------|
| `-10Hz` | 低沉 | 严肃、权威 |
| `-5Hz` | 稍低 | 稳重 |
| `0Hz` | 正常 | 默认 |
| `+5Hz` | 稍高 | 活泼、友好 ⭐ |
| `+10Hz` | 更高 | 兴奋、激动 |

### 音量 (volume)
| 值 | 效果 | 适用场景 |
|-----|------|----------|
| `-20%` | 轻柔 | 睡前故事 |
| `-10%` | 稍轻 | 私密对话 |
| `0%` | 正常 | 日常 ⭐ |
| `+10%` | 响亮 | 公告 |
| `+20%` | 很大 | 紧急 |

## 🎯 最佳实践

### 天气预报推荐配置
```python
# 温柔女声，友好关怀风格
voice = "zh-CN-XiaoxiaoNeural"
rate = "+0%"      # 正常语速
pitch = "+5Hz"    # 稍活泼
volume = "+0%"    # 正常音量
```

### 紧急通知推荐配置
```python
# 清晰男声，严肃稳重风格
voice = "zh-CN-YunxiNeural"
rate = "-5%"      # 稍慢，确保听清
pitch = "-5Hz"    # 稍低，更严肃
volume = "+10%"   # 更大声
```

### 儿童内容推荐配置
```python
# 甜美女声，活泼可爱风格
voice = "zh-CN-XiaoyiNeural"
rate = "+10%"     # 稍快，更有活力
pitch = "+10Hz"   # 更高，更可爱
volume = "+5%"    # 稍大
```

## 📝 文本优化技巧

### 使用语气词
- ❌ "明天下雨"
- ✅ "明天要下雨哦"

### 添加关怀
- ❌ "气温 5 度"
- ✅ "气温 5 度，注意保暖"

### 使用表情符号 (文本中)
- ❌ "太原明天晴天"
- ✅ "哈喽～太原明天是个好天气哦☀️"

### 提供建议
- ❌ "降水概率 80%"
- ✅ "降水概率 80%，记得带伞"

## 🔧 测试工具

### 试听语音
```bash
# 生成测试语音
python3 << PYTHON
import asyncio
import edge_tts

TEXT = "哈喽～这是一个测试语音，听听效果怎么样！"
OUTPUT = "/tmp/test-voice.opus"

async def generate():
    communicate = edge_tts.Communicate(
        TEXT, 
        "zh-CN-XiaoxiaoNeural",
        rate="+0%",
        pitch="+5Hz",
        volume="+0%"
    )
    await communicate.save(OUTPUT)
    print(f"✅ 语音已生成：{OUTPUT}")

asyncio.run(generate())
PYTHON

# 播放语音 (需要安装 opus 播放器)
ffplay /tmp/test-voice.opus
```

### 批量测试不同语音
```bash
for voice in zh-CN-XiaoxiaoNeural zh-CN-YunxiNeural zh-CN-XiaoyiNeural; do
  echo "Testing $voice..."
  python3 << PYTHON
import asyncio
import edge_tts
async def gen():
    c = edge_tts.Communicate("测试语音", "$voice")
    await c.save("/tmp/test-$voice.opus")
asyncio.run(gen())
PYTHON
done
```

## 📖 参考资料

- [Edge TTS 文档](https://github.com/rany2/edge-tts)
- [Microsoft Azure TTS 语音列表](https://speech.microsoft.com/portal/voicegallery)
- [OPUS 音频格式](https://opus-codec.org/)
