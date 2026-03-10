#!/bin/bash
# Claude Code 技能包推送脚本

echo "🚀 推送 Claude Code 最佳实践技能包到 GitHub..."
echo ""

cd /home/ghost/.openclaw/workspace/skills-up/claude-code-best-practices

echo "📊 当前状态:"
git status --short
echo ""

echo "📝 最近提交:"
git log --oneline -3
echo ""

echo "📤 推送到 skills-up 仓库..."
git push skills-up master

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 推送成功！"
    echo ""
    echo "📦 技能包已上传到:"
    echo "   https://github.com/whb5974/skills-up/tree/main/claude-code-best-practices"
    echo ""
    echo "📋 包含内容:"
    echo "   - 3 个核心 skills (project-status, code-review, test-gen)"
    echo "   - 2 个自动化 hooks (on-file-edit, on-task-complete)"
    echo "   - 完整文档 (README, INSTALL, USAGE)"
    echo "   - 配置文件 (settings.json, CLAUDE.md)"
    echo ""
else
    echo ""
    echo "❌ 推送失败，请检查网络连接或 GitHub 凭证"
    echo ""
    echo "手动推送命令:"
    echo "  cd /home/ghost/.openclaw/workspace/skills-up"
    echo "  git push skills-up master"
    echo ""
fi
