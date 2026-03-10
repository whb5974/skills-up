#!/bin/bash
# Hook: 文件编辑后自动执行
# 触发条件：当 Claude 编辑文件后

# 获取修改的文件路径
FILE_PATH="$1"

echo "📝 文件已修改：$FILE_PATH"

# 如果是 JavaScript/TypeScript 文件，检查语法
if [[ "$FILE_PATH" == *.js || "$FILE_PATH" == *.ts ]]; then
    if command -v node &> /dev/null; then
        echo "🔍 检查语法..."
        node --check "$FILE_PATH" 2>&1 || echo "⚠️ 语法检查失败"
    fi
fi

# 如果是 Python 文件，检查语法
if [[ "$FILE_PATH" == *.py ]]; then
    if command -v python3 &> /dev/null; then
        echo "🔍 检查 Python 语法..."
        python3 -m py_compile "$FILE_PATH" 2>&1 || echo "⚠️ 语法检查失败"
    fi
fi

# 如果是 Markdown 文件，检查格式
if [[ "$FILE_PATH" == *.md ]]; then
    echo "✅ Markdown 文件已更新"
fi

echo "---"
