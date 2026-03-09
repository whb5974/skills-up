# 小红书配置指南

## 📋 配置需求

| 组件 | 状态 | 说明 |
|------|------|------|
| **Docker** | ❌ 需要安装 | 运行小红书 MCP 服务 |
| **小红书 MCP** | ❌ 需要配置 | Docker 容器 |
| **Cookie** | ❌ 需要获取 | 登录凭证 |
| **mcporter** | ✅ 已安装 | 管理工具 |

---

## 🔧 配置步骤

### 步骤 1: 安装 Docker

**方法一：使用脚本（需要 sudo 密码）**
```bash
curl -fsSL https://get.docker.com | sudo sh -
```

**方法二：手动安装（Ubuntu/Debian）**
```bash
# 1. 更新包索引
sudo apt update

# 2. 安装依赖
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release

# 3. 添加 Docker GPG 密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# 4. 添加仓库
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. 安装 Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# 6. 启动 Docker
sudo systemctl start docker
sudo systemctl enable docker

# 7. 验证安装
docker --version
```

**方法三：使用 Snap**
```bash
sudo snap install docker
```

**安装后配置（免 sudo 使用 Docker）**
```bash
sudo usermod -aG docker $USER
# 然后重新登录或运行：newgrp docker
```

---

### 步骤 2: 启动小红书 MCP 服务

```bash
# 创建数据目录
mkdir -p ~/.agent-reach/xiaohongshu

# 启动 Docker 容器
docker run -d \
  --name xiaohongshu-mcp \
  -p 18060:18060 \
  -v ~/.agent-reach/xiaohongshu:/app/data \
  xpzouying/xiaohongshu-mcp

# 查看日志
docker logs xiaohongshu-mcp

# 检查服务状态
curl http://localhost:18060/health
```

**预期输出:**
```json
{"status":"ok"}
```

---

### 步骤 3: 获取小红书 Cookie

**方法一：使用 Cookie-Editor（推荐 ⭐）**

1. **安装插件**
   - Chrome/Edge: [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)

2. **登录小红书**
   - 访问：https://www.xiaohongshu.com
   - 使用手机扫码或账号密码登录

3. **导出 Cookie**
   - 点击 Cookie-Editor 图标
   - 点击 **Export** 按钮
   - 选择 **Header String** 格式
   - 复制导出的字符串

4. **保存 Cookie**
   ```bash
   # 创建目录
   mkdir -p ~/.agent-reach/xiaohongshu
   
   # 保存 Cookie（替换 YOUR_COOKIE）
   echo "YOUR_COOKIE_STRING" > ~/.agent-reach/xiaohongshu/cookies.txt
   ```

**方法二：浏览器开发者工具**

1. 打开浏览器开发者工具 (F12)
2. 访问 https://www.xiaohongshu.com 并登录
3. 切换到 **Network** 标签页
4. 刷新页面
5. 点击任意请求
6. 在 **Headers** 中找到 **Request Headers**
7. 复制 `Cookie:` 后面的完整字符串

**Cookie 格式示例:**
```
Cookie: a1=1234567890; b2=abcdef; web_session=xyz123; ...
```

---

### 步骤 4: 注册到 mcporter

```bash
# 添加小红书 MCP 服务器
mcporter config add xiaohongshu http://localhost:18060/mcp

# 验证配置
mcporter list

# 测试连接
mcporter call 'xiaohongshu.search_feeds(query="美食")'
```

---

### 步骤 5: 测试功能

**搜索笔记:**
```bash
mcporter call 'xiaohongshu.search_feeds(query="旅行攻略")'
```

**获取笔记详情:**
```bash
mcporter call 'xiaohongshu.get_note_detail(note_id="65f1234567890abcdef")'
```

**获取用户信息:**
```bash
mcporter call 'xiaohongshu.get_user_profile(user_id="5f1234567890abcdef")'
```

**搜索用户:**
```bash
mcporter call 'xiaohongshu.search_users(query="美食博主")'
```

---

## 🛠️ 管理命令

### Docker 容器管理

```bash
# 查看状态
docker ps | grep xiaohongshu

# 查看日志
docker logs xiaohongshu-mcp --tail 50

# 重启容器
docker restart xiaohongshu-mcp

# 停止容器
docker stop xiaohongshu-mcp

# 启动容器
docker start xiaohongshu-mcp

# 删除容器（重新安装）
docker rm -f xiaohongshu-mcp
```

### mcporter 配置管理

```bash
# 列出所有服务器
mcporter list

# 查看小红书配置
mcporter config show xiaohongshu

# 移除配置
mcporter config remove xiaohongshu

# 重新添加
mcporter config add xiaohongshu http://localhost:18060/mcp
```

---

## ⚠️ 注意事项

### 1. Cookie 有效期
- 小红书 Cookie 通常有效期为 **7-30 天**
- Cookie 过期后需要重新获取
- 建议每 2 周检查一次

### 2. 代理配置（中国大陆用户）
如果在中国大陆，建议配置代理避免 IP 限制：

```bash
docker run -d \
  --name xiaohongshu-mcp \
  -p 18060:18060 \
  -e XHS_PROXY=http://user:pass@ip:port \
  -v ~/.agent-reach/xiaohongshu:/app/data \
  xpzouying/xiaohongshu-mcp
```

### 3. 端口占用
如果 18060 端口被占用，可以更改：

```bash
docker run -d \
  --name xiaohongshu-mcp \
  -p 18061:18060 \
  ...
  
# 然后注册时使用新端口
mcporter config add xiaohongshu http://localhost:18061/mcp
```

### 4. 安全提示
- ⚠️ **不要分享 Cookie** - Cookie 包含登录凭证
- ⚠️ **使用备用账号** - 建议用次要账号，降低风险
- ⚠️ **定期更新** - Cookie 过期后及时更新

---

## 🔍 故障排查

### 问题 1: Docker 未安装
```bash
# 检查 Docker
docker --version

# 如果未安装，参考步骤 1 安装
```

### 问题 2: 容器启动失败
```bash
# 查看详细日志
docker logs xiaohongshu-mcp --tail 100

# 检查端口是否被占用
sudo lsof -i :18060

# 删除旧容器重新创建
docker rm -f xiaohongshu-mcp
docker run -d --name xiaohongshu-mcp -p 18060:18060 -v ~/.agent-reach/xiaohongshu:/app/data xpzouying/xiaohongshu-mcp
```

### 问题 3: Cookie 无效
```bash
# 检查 Cookie 文件
cat ~/.agent-reach/xiaohongshu/cookies.txt

# 重新获取 Cookie（见步骤 3）
# 确保格式正确，包含完整的 Cookie 字符串
```

### 问题 4: mcporter 连接失败
```bash
# 检查服务是否运行
curl http://localhost:18060/health

# 检查 mcporter 配置
mcporter config show xiaohongshu

# 重新添加配置
mcporter config remove xiaohongshu
mcporter config add xiaohongshu http://localhost:18060/mcp
```

### 问题 5: 搜索结果为空
- 可能是 Cookie 过期 → 重新获取
- 可能是关键词问题 → 尝试其他关键词
- 可能是 IP 限制 → 配置代理

---

## 📖 参考资料

- **小红书 MCP 仓库**: https://github.com/xpzouying/xiaohongshu-mcp
- **Docker 安装**: https://docs.docker.com/engine/install/
- **Cookie-Editor**: https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm

---

## ✅ 配置检查清单

- [ ] Docker 已安装并运行
- [ ] 小红书 MCP 容器已启动 (`docker ps` 可见)
- [ ] 健康检查通过 (`curl http://localhost:18060/health`)
- [ ] Cookie 已获取并保存到 `~/.agent-reach/xiaohongshu/cookies.txt`
- [ ] mcporter 配置已添加
- [ ] 测试搜索功能正常
- [ ] 了解如何更新 Cookie

---

## 🎯 快速配置脚本

如果已安装 Docker，可以一键配置：

```bash
#!/bin/bash
# 小红书快速配置脚本

echo "=== 小红书 MCP 配置脚本 ==="

# 1. 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi
echo "✅ Docker 已安装"

# 2. 启动容器
echo "🚀 启动小红书 MCP 容器..."
docker run -d --name xiaohongshu-mcp -p 18060:18060 -v ~/.agent-reach/xiaohongshu:/app/data xpzouying/xiaohongshu-mcp

# 3. 创建目录
mkdir -p ~/.agent-reach/xiaohongshu

# 4. 提示用户输入 Cookie
echo ""
echo "📝 请获取小红书 Cookie:"
echo "1. 访问 https://www.xiaohongshu.com 并登录"
echo "2. 使用 Cookie-Editor 插件导出 Header String"
echo "3. 粘贴到下方"
echo ""
read -p "Cookie: " COOKIE

# 5. 保存 Cookie
echo "$COOKIE" > ~/.agent-reach/xiaohongshu/cookies.txt
echo "✅ Cookie 已保存"

# 6. 等待服务启动
echo "⏳ 等待服务启动..."
sleep 5

# 7. 注册到 mcporter
mcporter config add xiaohongshu http://localhost:18060/mcp
echo "✅ 已注册到 mcporter"

# 8. 测试
echo "🧪 测试搜索功能..."
mcporter call 'xiaohongshu.search_feeds(query="美食")'

echo ""
echo "✅ 配置完成！"
```

保存为 `setup-xiaohongshu.sh`，然后运行：
```bash
chmod +x setup-xiaohongshu.sh
./setup-xiaohongshu.sh
```

---

## 💡 下一步

1. **安装 Docker**（如果未安装）
2. **获取 Cookie**（使用 Cookie-Editor）
3. **运行配置脚本** 或手动执行上述步骤
4. **测试功能**

配置完成后，您就可以使用小红书的所有功能了！
