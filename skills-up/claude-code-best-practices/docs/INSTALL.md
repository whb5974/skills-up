# 安装指南

> 📦 如何安装和配置 Claude Code 最佳实践技能包

---

## 📋 前置要求

- OpenClaw 框架
- Claude Code 访问权限
- Bash 环境（用于 Hooks）
- Node.js 或 Python（用于语法检查）

---

## 🚀 安装步骤

### 步骤 1: 克隆仓库

```bash
git clone https://github.com/whb5974/skills-up.git
cd skills-up/claude-code-best-practices
```

### 步骤 2: 复制文件

```bash
# 假设你的 OpenClaw 工作区在 ~/.openclaw/workspace

# 复制 Skills
cp -r skills ~/.openclaw/workspace/.claude/

# 复制 Hooks
cp -r hooks ~/.openclaw/workspace/.claude/

# 复制配置文件
cp settings.json ~/.openclaw/workspace/.claude/

# 复制项目指令
cp CLAUDE.md ~/.openclaw/workspace/
```

### 步骤 3: 设置权限

```bash
# 确保 Hooks 可执行
chmod +x ~/.openclaw/workspace/.claude/hooks/*.sh

# 验证权限
ls -la ~/.openclaw/workspace/.claude/hooks/
```

### 步骤 4: 验证安装

```bash
# 检查文件结构
tree ~/.openclaw/workspace/.claude/

# 应该看到:
# .claude/
# ├── skills/
# │   ├── project-status.md
# │   ├── code-review.md
# │   └── test-gen.md
# ├── hooks/
# │   ├── on-file-edit.sh
# │   └── on-task-complete.sh
# └── settings.json
```

---

## 🔧 配置说明

### settings.json

编辑 `~/.openclaw/workspace/.claude/settings.json` 根据你的需求调整：

```json
{
  "permissions": {
    "fs": {
      "read": ["**/*"],
      "write": ["**/*"],
      "deny": ["**/.env*", "**/*.key", "**/secrets/**"]
    }
  }
}
```

### CLAUDE.md

编辑 `~/.openclaw/workspace/CLAUDE.md` 调整项目规范：

```markdown
## 编码规范
- **语言**: 优先使用 JavaScript/TypeScript 和 Python
- **风格**: 简洁、高效、可读性强
```

---

## ✅ 测试安装

### 测试 Skills

在 Claude Code 会话中：

```bash
# 测试项目状态
/skill project-status

# 测试代码审查（选择一个现有文件）
/skill code-review CLAUDE.md

# 测试测试生成
/skill test-gen <某个文件>
```

### 测试 Hooks

```bash
# 编辑一个文件
echo "test" >> test.js

# 应该触发 on-file-edit.sh，显示语法检查

# 完成一个任务后
# 应该触发 on-task-complete.sh，显示 git 变更
```

---

## 🔍 故障排除

### Skills 不工作

**问题:** `/skill` 命令无响应

**解决:**
```bash
# 检查技能文件是否存在
ls -la ~/.openclaw/workspace/.claude/skills/

# 检查文件格式
cat ~/.openclaw/workspace/.claude/skills/project-status.md

# 重启 Claude Code 会话
```

### Hooks 不触发

**问题:** 编辑文件后没有语法检查

**解决:**
```bash
# 检查 Hooks 是否可执行
chmod +x ~/.openclaw/workspace/.claude/hooks/*.sh

# 测试 Hook 脚本
~/.openclaw/workspace/.claude/hooks/on-file-edit.sh test.js

# 检查 Claude Code 配置
cat ~/.openclaw/workspace/.claude/settings.json
```

### 权限问题

**问题:** 无法执行某些命令

**解决:**
```bash
# 检查 settings.json 中的 exec.allow 列表
cat ~/.openclaw/workspace/.claude/settings.json | grep -A 20 '"allow"'

# 添加需要的命令
```

---

## 📦 卸载

```bash
# 删除 Skills
rm -rf ~/.openclaw/workspace/.claude/skills/

# 删除 Hooks
rm -rf ~/.openclaw/workspace/.claude/hooks/

# 删除配置
rm ~/.openclaw/workspace/.claude/settings.json
rm ~/.openclaw/workspace/CLAUDE.md
```

---

## 🆘 获取帮助

1. 查看 [使用示例](USAGE.md)
2. 查看 [配置详解](CONFIG.md)
3. 提交 [Issue](https://github.com/whb5974/skills-up/issues)

---

**最后更新:** 2026-03-10
