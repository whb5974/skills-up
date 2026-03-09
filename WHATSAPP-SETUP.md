# 📱 WhatsApp 对接配置指南

## 🎯 对接方式

OpenClaw 支持 **WhatsApp Web** 方式连接你的个人 WhatsApp 账号。

---

## ⚙️ 配置步骤

### 方式 1：使用 openclaw configure 向导（推荐）

```bash
openclaw configure --section channels
```

然后选择 WhatsApp，按提示完成配置。

---

### 方式 2：手动配置

#### 步骤 1：创建配置目录

```bash
mkdir -p ~/.openclaw/channels/whatsapp
```

#### 步骤 2：编辑配置文件

```bash
nano ~/.openclaw/openclaw.json
```

添加 WhatsApp 配置：

```json
{
  "channels": {
    "whatsapp": {
      "enabled": true,
      "provider": "whatsapp-web",
      "name": "My WhatsApp",
      "auth": {
        "method": "qr"
      }
    }
  }
}
```

#### 步骤 3：启动 WhatsApp 连接

```bash
openclaw channels login --channel whatsapp
```

系统会显示二维码，用手机 WhatsApp 扫描即可连接。

---

### 方式 3：使用 Twilio WhatsApp API（企业账号）

如果你有企业 WhatsApp 账号：

```bash
openclaw channels add \
  --channel whatsapp \
  --name "Business WhatsApp" \
  --token "YOUR_TWILIO_TOKEN"
```

---

## 📋 连接流程

### WhatsApp Web 方式

1. **运行连接命令**
   ```bash
   openclaw channels login --channel whatsapp
   ```

2. **显示二维码**
   - 终端会显示 QR 二维码
   - 或提供二维码图片路径

3. **手机扫码**
   - 打开 WhatsApp 手机应用
   - 设置 → 已连接设备 → 连接设备
   - 扫描二维码

4. **连接成功**
   - 显示 "Connected" 消息
   - 可以开始接收/发送消息

---

## 🔍 验证连接

### 查看已配置的渠道

```bash
openclaw channels list
```

### 查看连接状态

```bash
openclaw channels status --probe
```

### 测试发送消息

```bash
openclaw message send \
  --channel whatsapp \
  --target "+8613800138000" \
  --message "测试消息"
```

---

## 📁 文件位置

| 文件/目录 | 说明 |
|-----------|------|
| `~/.openclaw/channels/whatsapp/` | WhatsApp 认证数据 |
| `~/.openclaw/openclaw.json` | 主配置文件 |
| `~/.openclaw/logs/` | 日志文件 |

---

## 🛠️ 故障排除

### 问题 1：Unknown channel: whatsapp

**原因：** WhatsApp 插件未安装

**解决：**
```bash
# 检查可用渠道
openclaw channels list

# 重新配置
openclaw configure --section channels
```

### 问题 2：二维码不显示

**原因：** 终端不支持或浏览器问题

**解决：**
```bash
# 查看日志
tail -f ~/.openclaw/logs/gateway.log

# 检查浏览器依赖
openclaw browser status
```

### 问题 3：连接后掉线

**原因：** 会话过期

**解决：**
```bash
# 重新登录
openclaw channels logout --channel whatsapp
openclaw channels login --channel whatsapp
```

---

## 💡 使用示例

### 发送消息

```bash
# 发送给个人
openclaw message send \
  --channel whatsapp \
  --target "+8613800138000" \
  --message "你好！"

# 发送给群组
openclaw message send \
  --channel whatsapp \
  --target "群组名称" \
  --message "群消息"
```

### 接收消息

配置后自动接收，消息会路由到 OpenClaw Agent。

### 查看最近消息

```bash
openclaw message list --channel whatsapp --limit 10
```

---

## 🔐 安全提示

1. **不要分享二维码** - 等同于账号密码
2. **定期检查连接设备** - WhatsApp → 已连接设备
3. **使用专用账号** - 建议用工作号而非个人主号
4. **备份认证数据** - `~/.openclaw/channels/whatsapp/`

---

## 📊 功能对比

| 功能 | WhatsApp Web | Twilio API |
|------|-------------|-----------|
| 成本 | 免费 | 收费 |
| 难度 | 简单 | 中等 |
| 稳定性 | 中等 | 高 |
| 适用 | 个人/小团队 | 企业 |
| 限制 | 需保持在线 | 无限制 |

---

## 🚀 快速开始

**最简单的方式：**

```bash
# 1. 运行配置向导
openclaw configure --section channels

# 2. 选择 WhatsApp

# 3. 扫码连接

# 4. 测试
openclaw message send \
  --channel whatsapp \
  --target "+8613800138000" \
  --message "WhatsApp 已连接！"
```

---

## 📞 需要帮助？

遇到问题时：

1. **查看日志**
   ```bash
   tail -100 ~/.openclaw/logs/gateway.log
   ```

2. **检查状态**
   ```bash
   openclaw doctor
   ```

3. **重新配置**
   ```bash
   openclaw channels remove --channel whatsapp
   openclaw channels login --channel whatsapp
   ```

---

**准备好开始了吗？** 运行：

```bash
openclaw configure --section channels
```

或告诉我你的需求，我帮你一步步配置！😊
