# 📄 文字转 PDF 工具

将文字/Markdown 内容转换为 PDF 文件，并提供下载功能。

---

## 🚀 快速开始

### 1. 启动下载服务器

```bash
cd /home/ghost/.openclaw/workspace/tools
node pdf-downloader.js &
```

服务器将在 `http://localhost:3456` 运行。

### 2. 生成 PDF

#### 方法 A：直接转换文件

```bash
node text-to-pdf.js input.md output.pdf
```

#### 方法 B：通过 API 生成

```bash
curl -X POST http://localhost:3456/generate \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# 我的报告\n\n这是一份测试报告。\n\n- 项目 1\n- 项目 2\n- 项目 3",
    "filename": "report.pdf"
  }'
```

响应：
```json
{
  "success": true,
  "file": "report.pdf",
  "downloadUrl": "http://localhost:3456/download/report.pdf"
}
```

#### 方法 C：下载 PDF

```bash
curl -O http://localhost:3456/download/report.pdf
```

或在浏览器中打开下载链接。

---

## 📋 API 接口

| 端点 | 方法 | 说明 |
|------|------|------|
| `/generate` | POST | 生成 PDF |
| `/download/<filename>` | GET | 下载 PDF |
| `/list` | GET | 列出所有 PDF |
| `/health` | GET | 健康检查 |

### POST /generate

**请求体：**
```json
{
  "content": "# 标题\n\n内容...",
  "filename": "myfile.pdf"
}
```

**响应：**
```json
{
  "success": true,
  "file": "myfile.pdf",
  "downloadUrl": "http://localhost:3456/download/myfile.pdf",
  "path": "/path/to/myfile.pdf"
}
```

### GET /list

**响应：**
```json
{
  "files": [
    {
      "name": "report.pdf",
      "url": "http://localhost:3456/download/report.pdf",
      "size": 12345
    }
  ]
}
```

---

## 📝 Markdown 语法支持

| 语法 | 示例 | 效果 |
|------|------|------|
| 标题 1 | `# 标题` | 大标题 |
| 标题 2 | `## 标题` | 中标题 |
| 标题 3 | `### 标题` | 小标题 |
| 列表 | `- 项目` | 无序列表 |
| 代码 | `\`\`\`code\`\`\`` | 代码块 |
| 文本 | 普通文字 | 正文 |

---

## 🛠️ 命令行工具

### text-to-pdf.js

```bash
# 显示帮助
node text-to-pdf.js --help

# 转换文件
node text-to-pdf.js input.md output.pdf

# 从 stdin 读取
cat input.md | node text-to-pdf.js - output.pdf

# 指定页面大小
node text-to-pdf.js input.md output.pdf --size Letter
```

**选项：**
- `--size <A4|Letter>` - 页面大小（默认：A4）

---

## 📁 文件结构

```
tools/
├── text-to-pdf.js        # PDF 生成器
├── pdf-downloader.js     # 下载服务器
├── README-PDF.md         # 本文档
└── ../pdf-output/        # PDF 输出目录（自动生成）
```

---

## 💡 使用示例

### 生成投资日报 PDF

```bash
# 创建 Markdown 内容
cat > /tmp/daily-report.md << 'EOF'
# 投资日报 - 2026 年 2 月 26 日

## 总体情况
- 总资产：100,000 元
- 总收益：+0.00 元 (0.00%)
- 风险状态：正常

## 持仓明细
- 贵州茅台：36,000 元 (36.0%)
- 国债 ETF：15,000 元 (15.0%)
- 沪深 300ETF：11,400 元 (11.4%)

## 操作建议
- 继续持有
- 无需调仓
EOF

# 转换为 PDF
node text-to-pdf.js /tmp/daily-report.pdf /home/ghost/.openclaw/workspace/pdf-output/daily-report.pdf
```

### 通过 API 批量生成

```javascript
const reports = [
    { title: '周报', content: '# 周报\n\n内容...' },
    { title: '月报', content: '# 月报\n\n内容...' }
];

for (const report of reports) {
    const response = await fetch('http://localhost:3456/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            content: report.content,
            filename: `${report.title}.pdf`
        })
    });
    const result = await response.json();
    console.log(`生成：${result.downloadUrl}`);
}
```

---

## ⚙️ 配置

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `PDF_PORT` | 3456 | 服务器端口 |

### 修改端口

```bash
PDF_PORT=8080 node pdf-downloader.js
```

---

## 🐛 故障排除

### 问题：端口已被占用

**解决：** 使用不同端口
```bash
PDF_PORT=3457 node pdf-downloader.js
```

### 问题：PDF 生成失败

**检查：**
1. 确保 pdfkit 已安装：`npm list -g pdfkit`
2. 检查输入文件格式
3. 查看错误信息

### 问题：无法下载

**检查：**
1. 服务器是否运行：`curl http://localhost:3456/health`
2. 文件是否存在：`curl http://localhost:3456/list`
3. 文件名是否正确

---

## 📞 需要帮助？

告诉我你想生成什么 PDF，我可以帮你：
- 📊 投资报告
- 📝 会议记录
- 📈 数据分析
- 📋 任何文字内容

只需说："把这段文字转成 PDF" 或 "生成投资日报 PDF"
