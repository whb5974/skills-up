#!/bin/bash
# i 茅台申购辅助工具 - 安装脚本

set -e

echo "🍶 i 茅台申购辅助工具 - 安装脚本"
echo "================================"

# 检查 Python 版本
echo ""
echo "📌 检查 Python 版本..."
python3 --version || {
    echo "❌ 未找到 Python 3，请先安装 Python 3.10+"
    exit 1
}

# 创建虚拟环境
echo ""
echo "📦 创建虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 安装依赖
echo ""
echo "📥 安装依赖..."
pip install --upgrade pip
pip install -r requirements.txt

# 复制配置文件
echo ""
echo "⚙️  配置初始化..."
if [ ! -f config.yaml ]; then
    cp config.yaml.example config.yaml
    echo "✅ 已创建 config.yaml，请编辑配置"
else
    echo "✅ config.yaml 已存在"
fi

# 创建数据目录
echo ""
echo "📁 创建数据目录..."
mkdir -p data/logs data/backup

# 测试运行
echo ""
echo "🧪 测试运行..."
python main.py --help

echo ""
echo "================================"
echo "✅ 安装完成！"
echo ""
echo "📝 下一步："
echo "1. 编辑 config.yaml 配置参数"
echo "2. 运行 python main.py start 启动服务"
echo ""
echo "📚 使用说明：python main.py --help"
echo ""
