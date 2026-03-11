# Claude Code 技能

## 概述

Claude Code 是 Anthropic 开发的代理编码工具，可以读取代码库、编辑文件、运行命令，并与开发工具集成。

## 核心能力

### 1. 代码理解与编辑
- 读取和分析整个代码库
- 智能文件编辑和重构
- 自动修复 bug
- 生成测试代码

### 2. 命令行集成
- 在终端中直接运行
- 执行 shell 命令
- Git 操作集成
- 项目管理

### 3. 多平台支持
- **终端**: CLI 工具
- **VS Code**: 扩展程序
- **JetBrains IDEs**: IntelliJ, PyCharm, WebStorm 等
- **Chrome 扩展**: 网页应用测试和调试
- **Desktop 应用**: 独立桌面客户端
- **Web 版**: claude.ai/code

### 4. 高级功能

#### Subagents (子代理)
- 创建专门的 AI 子代理处理特定任务
- 改进上下文管理
- 并行任务处理

#### Skills (技能)
- 创建自定义命令
- 打包和分享技能
- 扩展 Claude 能力

#### MCP (Model Context Protocol)
- 连接外部工具和服务
- 标准化集成协议

#### Hooks (钩子)
- 文件编辑时自动触发
- 任务完成时执行命令
- 自动化工作流

#### Plugins (插件)
- 创建自定义插件
- 从市场安装插件
- 扩展功能

## 使用场景

### 日常开发
- 代码探索和导航
- Bug 修复
- 功能开发
- 代码审查

### 项目维护
- 重构代码
- 更新依赖
- 文档生成
- 测试编写

### 自动化
- CI/CD 集成 (GitHub Actions, GitLab CI/CD)
- Slack 集成
- 远程协作

## 配置要点

### 设置文件
- 全局设置
- 项目级设置 (`CLAUDE.md`)
- 环境变量

### 权限控制
- 细粒度权限规则
- 沙箱隔离
- 安全策略

### 记忆系统
- CLAUDE.md 文件存储持久指令
- 自动记忆积累学习

## 最佳实践

1. **上下文管理**: 合理使用子代理处理大项目
2. **权限设置**: 根据项目敏感度配置权限
3. **成本控制**: 监控 token 使用，选择合适模型
4. **钩子自动化**: 设置代码格式化、测试运行等自动化

## 相关资源

- 官方文档：https://code.claude.com/docs/
- GitHub: https://github.com/anthropics/claude-code
- 更新日志：https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
