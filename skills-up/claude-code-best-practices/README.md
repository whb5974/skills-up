# Claude Code 最佳实践技能包

> 🎯 为 OpenClaw 和类似 AI 助手框架设计的 Claude Code 集成技能包

---

## 📦 包含内容

### Skills (3 个核心技能)
| 技能 | 功能 | 使用方式 |
|------|------|----------|
| `project-status` | 查看项目状态（git、文件、提交） | `/skill project-status` |
| `code-review` | 代码审查（语法/安全/性能/规范） | `/skill code-review <文件>` |
| `test-gen` | 为函数/模块生成测试用例 | `/skill test-gen <文件/函数>` |

### Hooks (2 个自动化钩子)
| Hook | 触发条件 | 功能 |
|------|----------|------|
| `on-file-edit.sh` | 文件编辑后 | 自动语法检查（JS/TS/Python/MD） |
| `on-task-complete.sh` | 任务完成后 | 显示 git 变更摘要 |

### 配置文件
- `settings.json` - 权限和安全配置
- `CLAUDE.md` - 项目持久指令模板

### 文档
- `SKILL.md` - 技能使用说明
- `docs/INSTALL.md` - 安装指南
- `docs/USAGE.md` - 使用示例
- `docs/CONFIG.md` - 配置详解

---

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/whb5974/skills-up.git
cd skills-up/claude-code-best-practices

# 复制到工作区
cp -r skills /your/workspace/.claude/
cp -r hooks /your/workspace/.claude/
cp settings.json /your/workspace/.claude/
cp CLAUDE.md /your/workspace/
```

### 使用技能

在 Claude Code 会话中：

```bash
# 查看项目状态
/skill project-status

# 代码审查
/skill code-review src/main.js

# 生成测试
/skill test-gen src/utils.js
```

### 自动 Hooks

Hooks 会自动触发，无需手动调用：

- 编辑文件后 → 自动语法检查
- 任务完成后 → 显示变更摘要

---

## 📋 详细文档

- [安装指南](docs/INSTALL.md)
- [使用示例](docs/USAGE.md)
- [配置详解](docs/CONFIG.md)
- [技能开发](docs/SKILL-DEV.md)

---

## 🔧 配置说明

### 权限配置 (settings.json)

```json
{
  "permissions": {
    "fs": {
      "read": ["**/*"],
      "write": ["**/*"],
      "deny": ["**/.env*", "**/*.key", "**/secrets/**"]
    },
    "exec": {
      "allow": ["git *", "npm *", "node *", "python*", ...],
      "deny": ["rm -rf *", "sudo *", "curl * | sh", ...]
    }
  }
}
```

### 项目指令 (CLAUDE.md)

包含：
- 编码规范
- 工作流程
- 安全规则
- 测试要求
- 沟通风格

---

## 🎯 技能详解

### 1. project-status

**功能:** 快速查看项目状态

**输出:**
```
=== Git 状态 ===
 M src/main.js
?? new-file.js

=== 最近提交 ===
abc123 修复登录 bug
def456 添加用户管理
ghi789 初始提交

=== 工作区文件 ===
./README.md
./src/main.js
./package.json
```

### 2. code-review

**功能:** 全面代码审查

**审查要点:**
- ✅ 语法检查
- ✅ 错误处理
- ✅ 安全检查
- ✅ 性能问题
- ✅ 代码规范
- ✅ 边界条件

**输出格式:**
```
## 审查结果：src/main.js

### ✅ 优点
- 代码结构清晰
- 注释充分

### ⚠️ 需要注意
- 缺少输入验证

### ❌ 问题
- [严重] 硬编码密码
- [一般] 未处理空值

### 建议修改
[具体代码修改建议]
```

### 3. test-gen

**功能:** 自动生成测试用例

**覆盖场景:**
- 正常输入
- 边界条件
- 错误输入
- 空值/null 处理

**输出格式:**
```javascript
// 测试文件：xxx.test.js
describe('函数名', () => {
  it('应该处理正常情况', () => {
    // ...
  });
  
  it('应该处理边界条件', () => {
    // ...
  });
  
  it('应该处理错误输入', () => {
    // ...
  });
});
```

---

## 🛠️ 开发自己的技能

参考 `docs/SKILL-DEV.md` 学习如何：
- 创建新的 skill
- 编写 hook 脚本
- 配置权限
- 测试和调试

---

## 📊 测试结果

**坦克大战项目实战测试:**
```
📊 测试结果：22 通过，0 失败
🎉 所有测试通过！
```

**技能包已实战验证，可放心使用。**

---

## 🔐 安全承诺

- ✅ 不提交敏感信息（.env, *.key）
- ✅ 不执行危险命令（rm -rf, sudo）
- ✅ 不下载执行远程脚本（curl | sh）
- ✅ 使用 trash 而非 rm 删除文件

---

## 📝 更新日志

### v1.0.0 (2026-03-10)
- ✅ 初始发布
- ✅ 3 个核心 skills
- ✅ 2 个自动化 hooks
- ✅ 完整文档
- ✅ 实战验证

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

**贡献指南:**
1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 📞 支持

遇到问题？
1. 查看 [文档](docs/)
2. 提交 [Issue](https://github.com/whb5974/skills-up/issues)
3. 查看 [示例](examples/)

---

**Made with 🖤 by 墨灵 (MoLing)**
