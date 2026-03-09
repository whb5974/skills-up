# 📄 PDF 下载指南

PDF 下载服务器已完善，现在可以正常下载文件了！

---

## ✅ 服务器状态

- **状态：** 运行中
- **端口：** 3456
- **网页界面：** http://localhost:3456/
- **文件目录：** `/home/ghost/.openclaw/workspace/pdf-output/`

---

## 📥 下载方式

### 方式 1：网页界面（推荐！）

在浏览器中打开：

```
http://localhost:3456/
```

你会看到一个漂亮的下载页面，列出所有可用的 PDF 文件，点击"下载"按钮即可。

### 方式 2：直接下载链接

**当前可用文件：**

| 文件名 | 大小 | 下载链接 |
|--------|------|----------|
| magic-pencil-story.pdf | 4.7KB | http://localhost:3456/download/magic-pencil-story.pdf |
| test-report.pdf | 1.6KB | http://localhost:3456/download/test-report.pdf |

**点击下载《小明的神奇铅笔》故事：**
```
http://localhost:3456/download/magic-pencil-story.pdf
```

### 方式 3：命令行下载

```bash
# 下载指定文件
curl -O http://localhost:3456/download/magic-pencil-story.pdf

# 或下载到指定位置
curl -o ~/Downloads/story.pdf http://localhost:3456/download/magic-pencil-story.pdf
```

### 方式 4：查看文件列表

```bash
# JSON 格式
curl http://localhost:3456/list

# 或在浏览器中打开
http://localhost:3456/list
```

---

## 🆕 生成新 PDF

### 通过 API

```bash
curl -X POST http://localhost:3456/generate \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# 标题\n\n内容...",
    "filename": "mydoc.pdf"
  }'
```

### 对我说

直接告诉我：
- "把这段文字转成 PDF：[内容]"
- "生成投资日报 PDF"
- "创建一个故事 PDF"

---

## 🔧 故障排除

### 问题：下载链接打不开

**检查服务器是否运行：**
```bash
curl http://localhost:3456/health
```

如果返回 `{"status":"ok",...}` 说明服务器正常。

### 问题：404 错误

**可能原因：**
1. 文件名有误 - 检查 `/list` 确认文件名
2. 文件被删除 - 检查 `pdf-output/` 目录

**解决：**
```bash
# 查看可用文件
curl http://localhost:3456/list

# 检查目录
ls -la /home/ghost/.openclaw/workspace/pdf-output/
```

### 问题：服务器未运行

**重启服务器：**
```bash
cd /home/ghost/.openclaw/workspace/tools
node pdf-downloader.js &
```

---

## 📁 文件管理

### 查看已生成的 PDF

```bash
ls -lh /home/ghost/.openclaw/workspace/pdf-output/*.pdf
```

### 清理旧文件

```bash
# 删除所有 PDF
rm /home/ghost/.openclaw/workspace/pdf-output/*.pdf

# 删除指定文件
rm /home/ghost/.openclaw/workspace/pdf-output/old-file.pdf
```

---

## 🎯 立即试试

**在浏览器中打开下载页面：**
```
http://localhost:3456/
```

**或直接下载故事 PDF：**
```
http://localhost:3456/download/magic-pencil-story.pdf
```

---

**🎉 下载功能已完善，祝你使用愉快！**
