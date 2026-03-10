# Skill: project-status

## 描述
快速查看项目状态，包括 git 状态、文件变更、最近提交等。

## 命令
```bash
#!/bin/bash
echo "=== Git 状态 ==="
git status --short 2>/dev/null || echo "不是 git 仓库"

echo -e "\n=== 最近提交 ==="
git log --oneline -5 2>/dev/null || echo "无提交历史"

echo -e "\n=== 工作区文件 ==="
find . -maxdepth 2 -type f -name "*.md" -o -name "*.js" -o -name "*.ts" -o -name "*.py" 2>/dev/null | head -20
```

## 使用方式
在 Claude Code 中输入：`/skill project-status`
