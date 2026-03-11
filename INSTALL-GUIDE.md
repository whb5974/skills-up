# Nmap Scanner Skill - 安装指南

## ✅ 技能已配置完成！

技能文件已创建并链接到 OpenClaw：
```
~/.npm-global/lib/node_modules/openclaw/skills/nmap-scanner
→ /home/ghost/.openclaw/workspace/skills/nmap-scanner
```

## ⚠️ 需要安装 Nmap

Nmap 尚未安装在系统上。请执行以下命令安装：

### Ubuntu/Debian（你的系统）

```bash
sudo apt-get update
sudo apt-get install -y nmap
```

### 验证安装

```bash
nmap --version
```

### 完成后

重启 OpenClaw Gateway：
```bash
openclaw gateway restart
```

---

## 📋 安装检查清单

- [x] 技能文件已创建
- [x] SKILL.md 已配置
- [x] nmap-scan.sh 工具脚本已创建
- [x] README.md 文档已创建
- [x] 技能已链接到 OpenClaw
- [ ] **待完成：安装 nmap**
- [ ] **待完成：重启 Gateway**

---

## 🚀 快速开始

安装 nmap 并重启后，你可以：

### 方式 1：通过对话使用

直接对我说：
```
"扫描我的网络 192.168.1.0/24"
"检查 192.168.1.1 有哪些端口开放"
"对我的服务器进行漏洞扫描"
```

### 方式 2：使用 CLI 工具

```bash
cd /home/ghost/.openclaw/workspace/skills/nmap-scanner

# 查看帮助
./nmap-scan.sh --help

# 基础扫描
./nmap-scan.sh basic 192.168.1.1

# 完整扫描
./nmap-scan.sh comprehensive 192.168.1.1

# 主机发现
./nmap-scan.sh discovery 192.168.1.0/24
```

---

## 📊 扫描类型

| 类型 | 说明 | 耗时 |
|------|------|------|
| discovery | 主机发现（Ping 扫描） | 快 |
| basic | 基础端口扫描（前 1000 端口） | 中 |
| fast | 快速扫描（前 100 端口） | 快 |
| full | 全端口扫描（65535 端口） | 慢 |
| service | 服务版本检测 | 中 |
| os | 操作系统检测（需 sudo） | 中 |
| comprehensive | 综合扫描（全端口 + 服务+OS） | 慢 |
| vuln | 漏洞扫描 | 很慢 |
| stealth | SYN 隐蔽扫描（需 sudo） | 中 |
| udp | UDP 扫描 | 很慢 |

---

## ⚠️ 法律警告

**仅扫描你拥有或已获得书面授权的网络！**

未经授权的网络扫描可能违反计算机犯罪法律。

---

## 📁 文件结构

```
/home/ghost/.openclaw/workspace/skills/nmap-scanner/
├── SKILL.md           # 技能配置（OpenClaw 使用）
├── README.md          # 使用文档
├── INSTALL-GUIDE.md   # 安装指南（本文件）
├── nmap-scan.sh       # CLI 工具脚本
├── install.sh         # 自动安装脚本
└── nmap-scans/        # 扫描结果输出目录
```

---

## 🔧 故障排除

### "command not found: nmap"
→ 执行上面的安装命令

### "permission denied"
→ 某些扫描需要 sudo：
```bash
sudo nmap -O <target>  # OS 检测
sudo nmap -sS <target> # SYN 扫描
```

### 技能未生效
→ 重启 Gateway：
```bash
openclaw gateway restart
```

---

## 📞 下一步

1. **安装 nmap**（需要 sudo 权限）
2. **重启 Gateway**
3. **测试扫描**

需要我帮你执行安装命令吗？或者你想自己手动安装？
