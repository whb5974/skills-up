# GitHub 手动推送指南

## 📋 配置说明

已配置为**手动控制上传内容**，不会自动推送。

---

## 🔧 忽略规则 (`.gitignore`)

以下文件**不会**被 Git 跟踪：

### 自动排除
- 📝 日志文件 (`*.log`, `logs/`)
- 🗑️ 缓存 (`__pycache__/`, `*.pyc`)
- 🔧 虚拟环境 (`venv/`, `env/`)
- 🎵 音频文件 (`audio/`, `*.opus`)
- 📄 PDF 输出 (`pdf-output/`, `*.pdf`)
- 💾 数据库 (`*.db`, `*.sqlite`)
- 📦 大型文件 (`*.zip`, `qbot.zip`)
- 📊 数据目录 (`investment-plan/data/`, `i-moutai-helper/data/`)
- 📈 扫描结果 (`nmap-scans/`)

---

## 📤 推送方法

### 方法 1: 使用推送脚本（推荐）

```bash
cd /home/ghost/.openclaw/workspace
./scripts/manual-git-push.sh
```

脚本会引导你：
1. 查看当前修改
2. 选择要添加的文件
3. 输入提交信息
4. 推送到 GitHub

---

### 方法 2: 手动命令

```bash
cd /home/ghost/.openclaw/workspace

# 1. 查看状态
git status

# 2. 添加指定文件
git add path/to/file.md

# 3. 提交
git commit -m "描述你的更改"

# 4. 推送
git push origin master
```

---

### 方法 3: 批量添加特定类型文件

```bash
# 只添加 Markdown 文档
git add *.md

# 只添加 Python 脚本
git add **/*.py

# 只添加配置文件
git add config/*.json
```

---

## 📊 常用命令

```bash
# 查看未跟踪的文件
git status --short

# 查看已暂存的更改
git diff --staged

# 撤销添加
git reset HEAD <file>

# 丢弃本地修改
git checkout -- <file>

# 查看提交历史
git log --oneline -10

# 拉取远程更新
git pull origin master
```

---

## ⚠️ 注意事项

1. **敏感信息**: 不要提交 Token、密码、API 密钥
2. **大文件**: 单个文件 >50MB 会被 GitHub 拒绝
3. **日志文件**: 已自动忽略，避免提交敏感日志
4. **数据库**: 已自动忽略，避免提交大量数据

---

## 🔐 如需提交敏感配置

使用环境变量或示例文件：

```bash
# 提交示例配置
cp config.yaml config.yaml.example
git add config.yaml.example
git commit -m "Add config example"

# 实际配置保存在本地，不提交
echo "config.yaml" >> .gitignore
```

---

## 📁 推荐提交的内容

✅ **应该提交**:
- 源代码 (`.py`, `.js`, `.sh`)
- 配置文件示例 (`.yaml.example`)
- 文档 (`.md`)
- 脚本工具

❌ **不应提交**:
- 日志文件
- 数据库
- 音频/视频
- 虚拟环境
- 敏感配置
- 大型数据文件

---

## 🆘 遇到问题

### 推送被拒绝
```bash
# 先拉取远程更新
git pull origin master

# 解决冲突后重新推送
git push origin master
```

### 误提交了大文件
```bash
# 撤销最后一次提交（保留本地修改）
git reset --soft HEAD~1

# 从历史中移除大文件
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/large-file" \
  --prune-empty --tag-name-filter cat -- --all

# 强制推送
git push --force origin master
```

---

**最后更新**: 2026-03-09
