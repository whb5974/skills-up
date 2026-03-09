# 定时任务配置文档 - 天气语音推送

## 功能说明

每天 17:50 自动获取太原次日天气预报，并通过以下方式推送到飞书群：
- 📝 **文字消息**（Markdown 格式，包含天气图标）
- 🔊 **语音消息**（OPUS 格式音频，飞书原生支持，可点击播放）

## ✅ 测试状态

**最新测试结果** (2026-03-07 16:41):
```
✅ 文字消息发送成功 (Message ID: om_x100b558a024168a8b3378e00f50d67e)
✅ 语音消息发送成功 (Message ID: om_x100b558a03ae0ca8b26b08f4738c290)
✅ 语音文件大小：60KB
✅ 语音格式：OPUS (飞书原生支持)
```

## 配置文件

### 1. Systemd Timer
- **位置**: `~/.config/systemd/user/weather-voice-push.timer`
- **执行时间**: 每天 17:50 (Asia/Shanghai 时区)
- **状态**: ✅ 已启用

### 2. Systemd Service
- **位置**: `~/.config/systemd/user/weather-voice-push.service`
- **脚本**: `/home/ghost/.openclaw/workspace/scripts/weather-voice-push.sh`

### 3. 天气脚本
- **位置**: `/home/ghost/.openclaw/workspace/scripts/weather-voice-push.sh`
- **日志**: `/home/ghost/.openclaw/logs/weather.log`
- **音频目录**: `/home/ghost/.openclaw/workspace/audio/`

### 4. 依赖
- ✅ Python edge-tts (已安装)
- ✅ OpenClaw Gateway (运行中)
- ✅ 飞书插件 (已启用)
- ✅ curl (已安装)

## 管理命令

```bash
# 查看定时任务状态
systemctl --user status weather-voice-push.timer

# 查看下次执行时间
systemctl --user list-timers weather-voice-push.timer

# 手动执行一次
systemctl --user start weather-voice-push.service

# 查看执行日志
journalctl --user -u weather-voice-push.service -f

# 查看天气日志
tail -f /home/ghost/.openclaw/logs/weather.log

# 禁用定时任务
systemctl --user disable --now weather-voice-push.timer

# 启用定时任务
systemctl --user enable --now weather-voice-push.timer
```

## 消息示例

### 文字消息
```
🌤️ **太原·明日天气**
📅 03-08
🌤️ 多云
🌡️ -2.6°C ~ 10.8°C
💧 降水概率：10%
```

### 语音消息
```
🔊 语音播报：太原明天天气，多云，最低气温 -2.6 度，最高气温 10.8 度，降水概率 10%。
[OPUS 音频附件 - 点击播放]
```

## TTS 语音配置

使用 Microsoft Edge TTS 服务生成语音：
- **库**: Python edge-tts
- **语音**: zh-CN-XiaoxiaoNeural (女声，标准普通话)
- **格式**: OPUS (飞书原生支持)
- **费用**: 免费 (Microsoft 公开服务)

### 更换语音
编辑脚本中的语音配置：
```python
communicate = edge_tts.Communicate(TEXT, "zh-CN-XiaoxiaoNeural")
```

可用语音：
- `zh-CN-XiaoxiaoNeural` - 女声 (默认)
- `zh-CN-YunxiNeural` - 男声
- `zh-CN-YunjianNeural` - 男声 (体育解说风格)
- `zh-CN-XiaoyiNeural` - 女声 (温柔)

## 添加其他城市

复制脚本并修改坐标：
```bash
cp weather-voice-push.sh weather-beijing.sh
# 编辑脚本，修改纬度/经度
```

### 城市坐标
| 城市 | 纬度 | 经度 |
|------|------|------|
| 太原 | 37.8706 | 112.5489 |
| 北京 | 39.9042 | 116.4074 |
| 上海 | 31.2304 | 121.4737 |
| 深圳 | 22.5431 | 114.0579 |
| 广州 | 23.1291 | 113.2644 |

## 修改执行时间

编辑 timer 文件：
```bash
nano ~/.config/systemd/user/weather-voice-push.timer
```

修改 `OnCalendar` 字段：
- `0 8 * * *` - 每天早上 8:00
- `0 7,19 * * *` - 每天早上 7:00 和晚上 19:00
- `0 9 * * 1-5` - 工作日早上 9:00
- `30 17 * * *` - 每天下午 17:30

格式：`分钟 小时 日 月 星期`

## 故障排查

### 1. 检查服务状态
```bash
systemctl --user status weather-voice-push.service
```

### 2. 查看最近执行日志
```bash
journalctl --user -u weather-voice-push.service --since "1 hour ago"
```

### 3. 测试脚本
```bash
/home/ghost/.openclaw/workspace/scripts/weather-voice-push.sh
```

### 4. 检查飞书连接
```bash
openclaw status
```

### 5. 检查 edge-tts
```bash
python3 -c "import edge_tts; print('OK')"
```

### 6. 重新安装 edge-tts
```bash
pip3 install --break-system-packages --upgrade edge-tts
```

## 音频文件管理

音频文件保存在：`/home/ghost/.openclaw/workspace/audio/`

### 清理旧音频
```bash
# 删除 7 天前的音频文件
find /home/ghost/.openclaw/workspace/audio/ -name "*.opus" -mtime +7 -delete

# 添加到 cron 定期清理
0 3 * * * find /home/ghost/.openclaw/workspace/audio/ -name "*.opus" -mtime +7 -delete
```

## 飞书群配置

- **群聊 ID**: `oc_61223fa3823a1a7373a10b6974358342`
- **消息类型**: 文字 + 音频文件
- **自动播放**: 飞书支持点击音频消息播放

### 修改目标群
编辑脚本中的 `FEISHU_CHAT_ID` 变量。

## 日志示例

```
[2026-03-07 16:41:36] === 天气语音推送任务开始 ===
[2026-03-07 16:41:36] 获取天气数据...
[2026-03-07 16:41:37] ✅ 天气数据：2026-03-07, 🌤️ 多云，-2.6~10.8°C
[2026-03-07 16:41:37] 📤 发送文字消息...
[2026-03-07 16:41:45] 🔊 生成并发送语音...
[2026-03-07 16:41:50] ✅ 语音文件已生成：/home/ghost/.openclaw/workspace/audio/weather-20260307.opus (60K)
[2026-03-07 16:41:58] ✅ 语音发送成功
[2026-03-07 16:41:58] === 任务完成 ===
```

## 依赖服务

- ✅ OpenClaw Gateway (必须运行)
- ✅ 飞书插件 (已启用)
- ✅ Python edge-tts (已安装)
- ✅ Systemd Timer (已配置)

## 更新历史

- **2026-03-07**: 初始版本，支持文字 + 语音推送
- **2026-03-07**: 修复音频路径权限问题
- **2026-03-07**: 测试成功，语音消息已发送到飞书群
