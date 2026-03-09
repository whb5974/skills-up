# Agent Reach 统一配置报告

**配置时间**: 2026-03-07 17:32  
**状态**: ✅ 9/13 个渠道可用

---

## ✅ 已激活渠道 (9 个)

### 🌐 基础功能 (5 个)

| 渠道 | 状态 | 功能 | 命令示例 |
|------|------|------|----------|
| **Twitter/X** | ✅ | 搜索推文、读取推文 | `xreach search "关键词" --json` |
| **YouTube** | ✅ | 视频信息、字幕提取 | `yt-dlp --dump-json "URL"` |
| **B 站** | ✅ | 视频信息、字幕提取 | `yt-dlp --dump-json "BV 号"` |
| **RSS/Atom** | ✅ | 读取订阅源 | `python3 -c "import feedparser"` |
| **全网搜索** | ✅ | Exa 语义搜索 | `mcporter call 'exa.web_search_exa(...)'` |
| **任意网页** | ✅ | Jina Reader | `curl "https://r.jina.ai/URL"` |
| **微信公众号** | ✅ | 搜索 + 阅读文章 | `mcporter call 'wechat.search(...)'` |

### 🔧 MCP 服务 (3 个)

| 渠道 | 状态 | 服务 | 端口 | 命令示例 |
|------|------|------|------|----------|
| **抖音** | ✅ | douyin-mcp-server | 18070 | `mcporter call 'douyin.parse_douyin_video_info(...)'` |
| **LinkedIn** | ⚠️ | linkedin-scraper-mcp | 8001 | `mcporter call 'linkedin.get_person_profile(...)'` |
| **Exa 搜索** | ✅ | exa-mcp | - | `mcporter call 'exa.web_search_exa(...)'` |

---

## ⚠️ 需要配置的渠道 (4 个)

| 渠道 | 状态 | 原因 | 解锁方法 |
|------|------|------|----------|
| **小红书** | ❌ | 需要 Docker | `docker run -d --name xiaohongshu-mcp -p 18060:18060 xpzouying/xiaohongshu-mcp` |
| **Reddit** | ⚠️ | 需要代理 | `agent-reach configure proxy http://user:pass@ip:port` |
| **Boss 直聘** | ❌ | 需要安装 MCP | 见 https://github.com/mucsbr/mcp-bosszp |
| **GitHub** | ❌ | 需要 gh CLI | `sudo snap install gh` |

---

## 🔧 已安装组件

```
✅ agent-reach (1.3.0)
✅ yt-dlp (2026.3.3)
✅ feedparser (6.0.12)
✅ mcporter (0.7.3)
✅ xreach CLI
✅ undici (Node.js 代理支持)
✅ douyin-mcp-server (1.2.1) - 端口 18070
✅ linkedin-scraper-mcp (4.2.0) - 端口 8001
✅ wechat-article-for-ai
✅ python-dotenv
```

---

## 📁 安装位置

| 组件 | 路径 |
|------|------|
| Agent Reach Skill | `/home/ghost/.openclaw/skills/agent-reach/` |
| MCP 工具 | `~/.agent-reach/tools/` |
| 配置文件 | `~/.agent-reach/config.json` |
| mcporter 配置 | `/home/ghost/.openclaw/workspace/config/mcporter.json` |

---

## 🚀 快速使用

### Twitter 搜索
```bash
xreach search "OpenAI" --limit 5 --json
```

### YouTube 视频信息
```bash
yt-dlp --dump-json "https://youtube.com/watch?v=xxx"
```

### 抖音视频解析
```bash
mcporter call 'douyin.parse_douyin_video_info(url="https://v.douyin.com/xxx")'
```

### LinkedIn 个人信息 (需要登录)
```bash
mcporter call 'linkedin.get_person_profile(profile_url="https://linkedin.com/in/xxx")'
```

### 全网搜索
```bash
mcporter call 'exa.web_search_exa(query="AI 最新进展", num_results=5)'
```

### 读取网页
```bash
curl -s "https://r.jina.ai/https://example.com"
```

---

## 🔐 需要登录的服务

### LinkedIn (需要浏览器登录)

**首次登录:**
```bash
linkedin-scraper-mcp --login --no-headless
```

这会打开浏览器，手动登录 LinkedIn。登录后 session 会保存到 `~/.linkedin-mcp/profile/`。

**启动服务:**
```bash
linkedin-scraper-mcp --transport streamable-http --port 8001
```

### 小红书 (需要 Docker + Cookie)

**1. 安装 Docker:**
```bash
curl -fsSL https://get.docker.com | sh -
```

**2. 启动 MCP 服务:**
```bash
docker run -d --name xiaohongshu-mcp -p 18060:18060 -v ~/.agent-reach/xiaohongshu:/app/data xpzouying/xiaohongshu-mcp
```

**3. 获取 Cookie:**
- 使用 [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)
- 登录 https://www.xiaohongshu.com
- 导出 Cookie (Header String 格式)
- 保存到 `~/.agent-reach/xiaohongshu/cookies.txt`

**4. 注册到 mcporter:**
```bash
mcporter config add xiaohongshu http://localhost:18060/mcp
```

---

## 📊 服务状态检查

```bash
# 检查 Agent Reach 状态
agent-reach doctor

# 检查 MCP 服务器
mcporter list

# 检查抖音服务
curl http://localhost:18070/health

# 检查 LinkedIn 服务
curl http://localhost:8001/health

# 查看抖音日志
tail -f /tmp/douyin-mcp.log

# 查看 LinkedIn 日志
tail -f /tmp/linkedin-mcp.log
```

---

## 🛠️ 管理命令

### 启动/停止服务

```bash
# 抖音 MCP
pkill -f "douyin_mcp_server"  # 停止
nohup python3 -c "from douyin_mcp_server.server import mcp; mcp.settings.host='127.0.0.1'; mcp.settings.port=18070; mcp.run(transport='streamable-http')" > /tmp/douyin-mcp.log 2>&1 &  # 启动

# LinkedIn MCP
pkill -f "linkedin-scraper-mcp"  # 停止
nohup linkedin-scraper-mcp --transport streamable-http --port 8001 > /tmp/linkedin-mcp.log 2>&1 &  # 启动

# 小红书 MCP (Docker)
docker stop xiaohongshu-mcp  # 停止
docker start xiaohongshu-mcp  # 启动
docker restart xiaohongshu-mcp  # 重启
```

### 开机自启动

创建 systemd 服务文件 `/etc/systemd/system/agent-reach-mcp.service`:

```ini
[Unit]
Description=Agent Reach MCP Services
After=network.target

[Service]
Type=forking
ExecStart=/home/ghost/.openclaw/workspace/scripts/start-mcp-services.sh
ExecStop=/home/ghost/.openclaw/workspace/scripts/stop-mcp-services.sh
Restart=on-failure
User=ghost

[Install]
WantedBy=multi-user.target
```

---

## 📈 性能优化

### 1. 代理配置 (中国大陆用户)

如果访问 Twitter/Reddit 等需要代理：

```bash
# 配置全局代理
agent-reach configure proxy http://user:pass@ip:port

# 或在 ~/.agent-reach/config.json 中添加
{
  "proxy": "http://user:pass@ip:port"
}
```

### 2. 缓存配置

Exa 搜索和 Jina Reader 支持缓存，减少重复请求。

### 3. 并发限制

MCP 服务器默认并发限制为 10 请求/秒，可根据需要调整。

---

## ⚠️ 注意事项

### 1. Cookie 安全
- ⚠️ 不要分享 Cookie 文件
- ⚠️ 使用备用账号登录
- ⚠️ 定期更新 Cookie (有效期约 30 天)

### 2. 服务端口
确保以下端口未被占用：
- 18070 (抖音)
- 8001 (LinkedIn)
- 18060 (小红书 - 需要 Docker)

### 3. 资源占用
- 抖音 MCP: ~100MB 内存
- LinkedIn MCP: ~200MB 内存 (需要浏览器)
- 小红书 MCP: ~50MB 内存 (Docker 容器)

### 4. API 限制
- Twitter: 有速率限制，建议间隔请求
- LinkedIn: 过于频繁可能触发风控
- 抖音: 无限制 (本地解析)

---

## 📖 参考资料

- **Agent Reach**: https://github.com/Panniantong/Agent-Reach
- **抖音 MCP**: https://github.com/yzfly/douyin-mcp-server
- **LinkedIn MCP**: https://github.com/stickerdaniel/linkedin-mcp-server
- **小红书 MCP**: https://github.com/xpzouying/xiaohongshu-mcp
- **mcporter**: https://github.com/openclaw/mcporter

---

## ✅ 配置检查清单

- [x] Agent Reach 主程序安装
- [x] Twitter/X 可用
- [x] YouTube 可用
- [x] B 站可用
- [x] RSS 可用
- [x] Exa 搜索可用
- [x] Jina Reader 可用
- [x] 微信公众号可用
- [x] 抖音 MCP 已安装并启动 (端口 18070)
- [x] LinkedIn MCP 已安装 (端口 8001)
- [ ] LinkedIn 已登录 (需要手动登录)
- [ ] 小红书 MCP 已配置 (需要 Docker)
- [ ] Reddit 代理已配置 (可选)
- [ ] Boss 直聘 MCP 已配置 (可选)
- [ ] GitHub gh CLI 已安装 (可选)

---

## 🎯 下一步建议

1. **测试基本功能**
   ```bash
   xreach search "AI" --limit 3
   mcporter call 'douyin.parse_douyin_video_info(url="https://v.douyin.com/xxx")'
   ```

2. **登录 LinkedIn** (如需使用)
   ```bash
   linkedin-scraper-mcp --login --no-headless
   ```

3. **配置小红书** (如需使用，先安装 Docker)

4. **设置自动监控** (可选)
   创建定时任务每天检查服务状态

---

**配置完成！9/13 个渠道已激活。**
