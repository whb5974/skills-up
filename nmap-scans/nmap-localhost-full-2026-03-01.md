# Nmap 完整端口扫描报告

**扫描时间：** 2026-03-01 17:49 CST  
**扫描目标：** localhost (127.0.0.1)  
**扫描类型：** 全端口 + 服务版本检测 (-sV -p-)  
**Nmap 版本：** 7.94SVN

---

## 📊 开放端口汇总

| 端口 | 状态 | 服务 | 版本/详情 | 风险等级 |
|------|------|------|-----------|----------|
| 22/tcp | open | ssh | OpenSSH 9.6p1 Ubuntu 3ubuntu13.14 | 🟡 中 |
| 631/tcp | open | ipp | CUPS 2.4 | 🟢 低 |
| 3389/tcp | open | ms-wbt-server | xrdp | 🟠 较高 |
| 3456/tcp | open | vat? | PDF 下载中心 (Node.js) | 🟡 中 |
| 18789/tcp | open | unknown | OpenClaw Control UI | 🟢 低 |
| 18791/tcp | open | http | Node.js Express | 🟢 低 |
| 18792/tcp | open | unknown | OpenClaw Gateway | 🟢 低 |

**扫描统计：** 65535 端口中 7 个开放，65528 个关闭

---

## 🔍 详细分析

### 🟢 低风险端口 (本地服务)

#### 端口 631 - CUPS 打印服务
- **服务：** CUPS 2.4
- **说明：** Linux 标准打印服务
- **建议：** ✅ 正常，仅本地访问

#### 端口 18789/18791/18792 - OpenClaw Gateway
- **18789:** OpenClaw Control UI (Web 界面)
- **18791:** Node.js Express (内部 API)
- **18792:** OpenClaw Gateway (健康检查/内部通信)
- **说明：** OpenClaw 核心服务
- **建议：** ✅ 正常，仅本地监听

---

### 🟡 中风险端口

#### 端口 22 - SSH
- **服务：** OpenSSH 9.6p1 Ubuntu 3ubuntu13.14
- **协议：** SSH 2.0
- **说明：** 远程登录服务
- **建议：** 
  - ✅ 确保使用密钥认证
  - ✅ 禁用 root 登录
  - ✅ 考虑修改默认端口

#### 端口 3456 - PDF 下载中心
- **服务：** Node.js HTTP 服务
- **说明：** PDF 下载管理应用
- **详情：** 
  - Access-Control-Allow-Origin: *
  - Content-Type: text/html; charset=utf-8
- **建议：** 
  - ⚠️ 确认是否需要对外暴露
  - ⚠️ 检查是否有认证机制

---

### 🟠 较高风险端口

#### 端口 3389 - XRDP 远程桌面
- **服务：** xrdp (Microsoft RDP 兼容)
- **说明：** 远程桌面协议服务
- **风险：**
  - 🔴 可能被暴力破解
  - 🔴 历史上有多个 RDP 漏洞
  - 🔴 不建议暴露在公网
- **建议：**
  - ⚠️ 如不需要请关闭
  - ⚠️ 如需要，限制访问 IP
  - ⚠️ 启用 NLA (网络级认证)
  - ⚠️ 使用强密码或证书

---

## 📈 安全评估

### 整体风险等级：🟡 中等

**积极方面：**
- ✅ 大部分服务仅本地监听
- ✅ OpenClaw 配置了安全头 (CSP, X-Frame-Options 等)
- ✅ SSH 版本较新 (9.6p1)

**需关注：**
- ⚠️ XRDP (3389) 暴露 - 建议关闭或限制
- ⚠️ PDF 下载中心 (3456) - 需确认访问控制
- ⚠️ 未知服务识别 - 3 个服务未完全识别

---

## 🔧 安全建议

### 立即执行

1. **评估 XRDP 必要性**
   ```bash
   # 查看 xrdp 状态
   sudo systemctl status xrdp
   
   # 如不需要，停止并禁用
   sudo systemctl stop xrdp
   sudo systemctl disable xrdp
   ```

2. **检查 PDF 下载中心**
   ```bash
   # 查看是什么进程
   ps aux | grep 3456
   # 或
   sudo ss -ltnp | grep 3456
   ```

3. **SSH 加固**
   ```bash
   # 编辑 SSH 配置
   sudo nano /etc/ssh/sshd_config
   
   # 确保以下设置：
   PermitRootLogin no
   PasswordAuthentication no
   PubkeyAuthentication yes
   ```

### 建议执行

4. **配置防火墙**
   ```bash
   # 启用 UFW
   sudo ufw enable
   
   # 允许 SSH
   sudo ufw allow 22/tcp
   
   # 拒绝 XRDP (如不需要)
   sudo ufw deny 3389/tcp
   
   # 查看状态
   sudo ufw status
   ```

5. **定期扫描**
   ```bash
   # 每周扫描一次
   nmap -sV localhost
   ```

---

## 📄 原始扫描输出

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-03-01 17:49 CST
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000091s latency).
Not shown: 65528 closed tcp ports (conn-refused)
PORT      STATE SERVICE       VERSION
22/tcp    open  ssh           OpenSSH 9.6p1 Ubuntu 3ubuntu13.14 (Ubuntu Linux; protocol 2.0)
631/tcp   open  ipp           CUPS 2.4
3389/tcp  open  ms-wbt-server xrdp
3456/tcp  open  vat?
18789/tcp open  unknown
18791/tcp open  http          Node.js Express framework
18792/tcp open  unknown
```

---

**扫描工具：** Nmap 7.94SVN  
**报告生成：** AI Security Assistant  
**原始数据：** `/home/ghost/.openclaw/workspace/nmap-scans/nmap-localhost-full-2026-03-01.txt`

---

*⚠️ 注意：此报告基于本地扫描结果。生产环境建议进行更全面的安全审计。*
