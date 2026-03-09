# 本地端口扫描报告

**扫描时间：** 2026-03-01 17:39 GMT+8  
**扫描目标：** 本机 (localhost)  
**扫描方式：** ss -ltnp (系统端口检测)  
**备注：** nmap 尚未安装，使用系统命令替代

---

## 📊 开放端口列表

| 端口 | 协议 | 监听地址 | 服务/进程 | 风险等级 |
|------|------|----------|-----------|----------|
| 22 | TCP | 0.0.0.0 / ::: | SSH | 🟡 中 |
| 53 | TCP | 127.0.0.54 / 127.0.0.53 | DNS (systemd-resolved) | 🟢 低 |
| 631 | TCP | 127.0.0.1 / ::1 | CUPS (打印机服务) | 🟢 低 |
| 3350 | TCP | ::1 | 未知服务 | 🟡 中 |
| 3389 | TCP | * | RDP (远程桌面) | 🟠 较高 |
| 3456 | TCP | * | Node.js 应用 | 🟡 中 |
| 18789 | TCP | 127.0.0.1 / ::1 | OpenClaw Gateway | 🟢 低 |
| 18791 | TCP | 127.0.0.1 | OpenClaw Gateway | 🟢 低 |
| 18792 | TCP | 127.0.0.1 | OpenClaw Gateway | 🟢 低 |

---

## 🔍 详细分析

### 🟢 低风险端口 (本地监听)

| 端口 | 服务 | 说明 |
|------|------|------|
| 53 | DNS | systemd-resolved 本地 DNS 解析 |
| 631 | CUPS | Linux 打印服务，仅本地访问 |
| 18789 | OpenClaw | OpenClaw Gateway 主端口 |
| 18791 | OpenClaw | OpenClaw Gateway 内部端口 |
| 18792 | OpenClaw | OpenClaw Gateway 内部端口 |

### 🟡 中风险端口

| 端口 | 服务 | 建议 |
|------|------|------|
| 22 | SSH | ✅ 正常，确保使用密钥认证 |
| 3456 | Node.js | 检查是否为预期应用 |
| 3350 | 未知 | 建议调查此服务 |

### 🟠 较高风险端口

| 端口 | 服务 | 建议 |
|------|------|------|
| 3389 | RDP | ⚠️ 如不需要请关闭，或限制访问 IP |

---

## 📈 安全建议

### 立即检查

1. **端口 3389 (RDP)** - 确认是否需要远程桌面服务
   ```bash
   # 查看是什么进程在监听
   sudo ss -ltnp | grep 3389
   ```

2. **端口 3350 (未知)** - 调查此服务
   ```bash
   # 查看进程信息
   sudo ss -ltnp | grep 3350
   ```

3. **端口 3456 (Node.js)** - 确认是否为预期应用
   ```bash
   # 查看进程详情
   ps aux | grep 129731
   ```

### 常规建议

- ✅ SSH (22) - 确保禁用 root 登录，使用密钥认证
- ✅ OpenClaw 端口 - 仅本地监听，配置正确
- ⚠️ RDP (3389) - 如不需要建议关闭
- ⚠️ 未知服务 - 建议识别并评估必要性

---

## 🔧 后续操作

### 安装 Nmap 进行更详细扫描

```bash
sudo apt-get update
sudo apt-get install -y nmap

# 完整端口扫描
nmap -p- -sV localhost

# 服务版本检测
nmap -sV localhost

# 漏洞扫描
nmap --script vuln localhost
```

### 防火墙配置建议

```bash
# 查看防火墙状态
sudo ufw status

# 如未启用，考虑开启
sudo ufw enable

# 允许 SSH
sudo ufw allow 22/tcp

# 拒绝不必要的端口
sudo ufw deny 3389/tcp
```

---

**扫描工具：** ss (netstat 替代)  
**报告生成：** AI Investment Assistant  
**下次扫描：** 建议安装 nmap 后进行更详细扫描

---

*⚠️ 注意：此扫描仅检测 TCP 监听端口，未进行 UDP 扫描或漏洞检测*
