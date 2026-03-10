#!/bin/bash
# Hook: 任务完成时执行
# 触发条件：当 Claude 完成一个任务后

echo "✅ 任务完成"
echo "📅 完成时间：$(date '+%Y-%m-%d %H:%M:%S')"

# 如果有 git 仓库，显示变更摘要
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "\n📊 Git 变更摘要:"
    git status --short
    echo -e "\n📝 未暂存的变更:"
    git diff --stat
fi

echo -e "\n---"
