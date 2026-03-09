#!/bin/bash

# PDF 工具快速启动脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PDF_DIR="$(dirname "$SCRIPT_DIR")/pdf-output"

echo "📄 PDF 工具启动器"
echo "================"

# 创建输出目录
mkdir -p "$PDF_DIR"
echo "✅ 输出目录：$PDF_DIR"

# 检查依赖
if ! node -e "require('pdfkit')" 2>/dev/null; then
    echo "❌ pdfkit 未安装，正在安装..."
    npm install -g pdfkit --quiet
fi

# 启动服务器
echo "🚀 启动 PDF 下载服务器..."
cd "$SCRIPT_DIR"
node pdf-downloader.js &
SERVER_PID=$!

echo "✅ 服务器已启动 (PID: $SERVER_PID)"
echo ""
echo "📋 快速使用:"
echo "   生成 PDF: curl -X POST http://localhost:3456/generate -H 'Content-Type: application/json' -d '{\"content\":\"# 测试\",\"filename\":\"test.pdf\"}'"
echo "   下载 PDF: curl -O http://localhost:3456/download/test.pdf"
echo "   查看列表：curl http://localhost:3456/list"
echo ""
echo "按 Ctrl+C 停止服务器"

# 等待服务器
wait $SERVER_PID
