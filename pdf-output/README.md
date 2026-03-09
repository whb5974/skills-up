# 📄 PDF 输出目录

所有生成的 PDF 文件都保存在这里。

---

## 📥 下载方式

### 1. 通过浏览器下载

访问：`http://localhost:3456/list`

点击任意文件的下载链接。

### 2. 通过命令行下载

```bash
# 查看可用文件
curl http://localhost:3456/list

# 下载指定文件
curl -O http://localhost:3456/download/<文件名.pdf>
```

### 3. 直接访问文件

```bash
ls -lh /home/ghost/.openclaw/workspace/pdf-output/
```

---

## 📋 当前文件

运行以下命令查看最新文件列表：

```bash
curl http://localhost:3456/list
```

---

## 🧹 清理旧文件

```bash
# 删除所有 PDF
rm /home/ghost/.openclaw/workspace/pdf-output/*.pdf

# 删除指定文件
rm /home/ghost/.openclaw/workspace/pdf-output/old-report.pdf
```
