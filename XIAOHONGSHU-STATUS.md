# 小红书配置状态报告

**更新时间**: 2026-03-07 17:40

---

## ✅ 已完成

| 步骤 | 状态 | 说明 |
|------|------|------|
| Docker 安装 | ✅ 完成 | Docker 28.2.2 已安装并运行 |
| 用户组配置 | ✅ 完成 | 用户已添加到 docker 组 |
| 目录创建 | ✅ 完成 | `~/.agent-reach/xiaohongshu/` 已创建 |

---

## ⚠️ 遇到的问题

### 问题：无法拉取 Docker 镜像

**错误信息:**
```
Error response from daemon: Get "https://registry-1.docker.io/v2/": 
net/http: request canceled while waiting for connection (Client.Timeout exceeded)
```

**原因:**
- 网络连接问题，无法访问 Docker Hub
- 可能需要配置代理或使用国内镜像

---

## 🔧 解决方案

### 方案一：配置 Docker 代理（推荐）

如果您有代理服务器，配置后重试：

```bash
# 创建 Docker 配置目录
sudo mkdir -p /etc/systemd/system/docker.service.d

# 创建代理配置
sudo tee /etc/systemd/system/docker.service.d/http-proxy.conf << EOF
[Service]
Environment="HTTP_PROXY=http://user:pass@ip:port"
Environment="HTTPS_PROXY=http://user:pass@ip:port"
Environment="NO_PROXY=localhost,127.0.0.1,.local"
EOF

# 重启 Docker
sudo systemctl daemon-reload
sudo systemctl restart docker

# 验证代理
sudo docker info | grep -i proxy

# 拉取镜像
sudo docker pull xpzouying/xiaohongshu-mcp:latest
```

### 方案二：使用国内镜像源

修改 Docker 配置使用国内镜像：

```bash
# 创建 Docker 配置
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json << EOF
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://docker.1panel.live",
    "https://hub.rat.dev"
  ]
}
EOF

# 重启 Docker
sudo systemctl daemon-reload
sudo systemctl restart docker

# 拉取镜像
sudo docker pull xpzouying/xiaohongshu-mcp:latest
```

### 方案三：手动下载镜像（离线安装）

1. **在有网络的机器上下载:**
   ```bash
   docker pull xpzouying/xiaohongshu-mcp:latest
   docker save -o xiaohongshu-mcp.tar xpzouying/xiaohongshu-mcp:latest
   ```

2. **传输到目标机器:**
   ```bash
   scp xiaohongshu-mcp.tar user@target:/tmp/
   ```

3. **加载镜像:**
   ```bash
   sudo docker load -i /tmp/xiaohongshu-mcp.tar
   ```

### 方案四：使用替代方案（无需 Docker）

如果 Docker 镜像无法使用，可以考虑：

1. **使用 Jina Reader 读取小红书网页**
   ```bash
   curl "https://r.jina.ai/https://www.xiaohongshu.com/explore/xxx"
   ```

2. **使用第三方 API**（需要 API Key）
   - 一些服务商提供小红书数据 API

---

## 📝 后续步骤

### 如果镜像拉取成功

1. **启动容器:**
   ```bash
   sudo docker run -d \
     --name xiaohongshu-mcp \
     -p 18060:18060 \
     -v ~/.agent-reach/xiaohongshu:/app/data \
     xpzouying/xiaohongshu-mcp
   ```

2. **验证服务:**
   ```bash
   curl http://localhost:18060/health
   ```

3. **获取 Cookie:**
   - 访问 https://www.xiaohongshu.com 并登录
   - 使用 Cookie-Editor 导出 Cookie (Header String 格式)
   - 保存到 `~/.agent-reach/xiaohongshu/cookies.txt`

4. **注册到 mcporter:**
   ```bash
   mcporter config add xiaohongshu http://localhost:18060/mcp
   ```

5. **测试:**
   ```bash
   mcporter call 'xiaohongshu.search_feeds(query="美食")'
   ```

---

## 🛠️ Docker 管理命令

```bash
# 查看 Docker 状态
sudo systemctl status docker

# 查看 Docker 版本
docker --version

# 查看运行的容器
sudo docker ps

# 查看所有容器
sudo docker ps -a

# 查看镜像
sudo docker images

# 重启 Docker
sudo systemctl restart docker

# 查看 Docker 日志
sudo journalctl -u docker -f
```

---

## 📖 参考资料

- **小红书 MCP**: https://github.com/xpzouying/xiaohongshu-mcp
- **Docker 代理配置**: https://docs.docker.com/config/daemon/http-proxy/
- **国内 Docker 镜像**: https://gist.github.com/y0ngb1n/7e8f16af3242c7815e7ca2f0833d3ea6

---

## ✅ 当前可用渠道

虽然小红书暂时无法配置，Agent Reach 仍有 **9 个渠道可用**:

- ✅ Twitter/X
- ✅ YouTube
- ✅ B 站
- ✅ RSS
- ✅ Exa 搜索
- ✅ Jina Reader
- ✅ 微信公众号
- ✅ 抖音 (已配置)
- ✅ LinkedIn (已安装，需登录)

---

## 💡 建议

1. **先使用现有渠道** - 9 个渠道已能满足大部分需求
2. **配置网络代理** - 解决 Docker 镜像拉取问题
3. **稍后配置小红书** - 网络问题解决后再继续

如需帮助配置代理，请提供代理服务器信息。
