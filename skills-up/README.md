# Skills-Up - OpenClaw 技能仓库

> 🎯 OpenClaw AI 助手技能集合 - 持续更新，自主进化

---

## 📦 技能包列表

### 🔥 最新技能包

#### Claude Code 最佳实践 (v1.0.0) 🆕
**位置:** `claude-code-best-practices/`

包含：
- ✅ 3 个核心 Skills: project-status, code-review, test-gen
- ✅ 2 个自动化 Hooks: on-file-edit, on-task-complete
- ✅ 完整文档：README, INSTALL, USAGE
- ✅ 实战验证：坦克大战项目 (22 测试通过)

**快速使用:**
```bash
git clone https://github.com/whb5974/skills-up.git
cd skills-up/claude-code-best-practices
cp -r skills ~/.openclaw/workspace/.claude/
cp -r hooks ~/.openclaw/workspace/.claude/
cp settings.json ~/.openclaw/workspace/.claude/
chmod +x ~/.openclaw/workspace/.claude/hooks/*.sh
```

[查看详细文档 →](claude-code-best-practices/README.md)

---

### 📚 其他技能包

#### Anthropic 官方技能集合
**位置:** `anthropics-skills/`

包含 15+ 个官方技能：
- **文档处理:** docx, xlsx, pptx, pdf
- **开发工具:** mcp-builder, skill-creator, claude-api
- **设计工具:** canvas-design, theme-factory, frontend-design
- **协作工具:** slack-gif-creator, doc-coauthoring

[查看技能列表 →](skills/anthropics-skills/README.md)

---

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/whb5974/skills-up.git
cd skills-up
```

### 2. 安装技能包

```bash
# 以 Claude Code 最佳实践为例
cd claude-code-best-practices

# 复制 Skills
cp -r skills ~/.openclaw/workspace/.claude/

# 复制 Hooks
cp -r hooks ~/.openclaw/workspace/.claude/

# 复制配置
cp settings.json ~/.openclaw/workspace/.claude/
cp CLAUDE.md ~/.openclaw/workspace/

# 设置权限
chmod +x ~/.openclaw/workspace/.claude/hooks/*.sh
```

### 3. 验证安装

在 Claude Code 中测试：
```bash
/skill project-status
/skill code-review <文件>
/skill test-gen <文件>
```

---

## 📋 技能包开发指南

### 创建新技能包

1. **创建目录结构**
```bash
mkdir -p my-skill/{skills,hooks,docs,examples}
```

2. **编写技能文件**
```markdown
# skills/my-skill.md
## 描述
技能功能描述

## 使用方式
/skill my-skill <参数>
```

3. **添加元数据**
```json
{
  "name": "my-skill",
  "version": "1.0.0",
  "description": "技能描述"
}
```

4. **提交到仓库**
```bash
git add .
git commit -m "feat: 添加新技能 my-skill"
git push
```

---

## 🔧 贡献指南

### 提交新技能包

1. Fork 仓库
2. 创建分支：`git checkout -b feature/my-skill`
3. 添加技能文件
4. 提交：`git commit -m "feat: 添加 my-skill 技能"`
5. 推送：`git push origin feature/my-skill`
6. 创建 Pull Request

### 技能包要求

- ✅ 包含 README.md 说明
- ✅ 包含使用示例
- ✅ 包含 META.json 元数据
- ✅ 经过实际测试
- ✅ 遵循 MIT 许可证

---

## 📊 统计

| 类别 | 数量 |
|------|------|
| 技能包总数 | 20+ |
| Claude Code Skills | 3 |
| Anthropic 官方技能 | 15+ |
| 自定义技能 | 5+ |
| Hooks | 2 |

---

## 📝 更新日志

### v1.0.0 (2026-03-10)
- 🆕 新增 `claude-code-best-practices` 技能包
  - 3 个核心 Skills
  - 2 个自动化 Hooks
  - 完整文档
  - 实战验证（坦克大战项目）

---

## 🤝 社区

- **问题反馈:** [GitHub Issues](https://github.com/whb5974/skills-up/issues)
- **讨论:** [GitHub Discussions](https://github.com/whb5974/skills-up/discussions)

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

**Made with 🖤 by 墨灵 (MoLing)**
