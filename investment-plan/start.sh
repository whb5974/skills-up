#!/bin/bash
# ===========================================
# 投资助手 - 快速启动脚本
# ===========================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║                                                      ║"
echo "║          🤖 投资助手 - 快速启动                      ║"
echo "║                                                      ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "请选择操作:"
echo ""
echo "  [1] 📊 今日投资日报（快速检查）"
echo "  [2] 📈 完整分析报告（估值 + 调仓 + 图表）"
echo "  [3] 💰 估值分析"
echo "  [4] 🔄 调仓建议"
echo "  [5] 🔍 股票筛选"
echo "  [6] 📊 可视化图表"
echo "  [7] 📚 查看配置指南"
echo "  [8] ⚙️ 配置定时任务"
echo "  [0] 退出"
echo ""
echo -n "请输入选项 [0-8]: "
read choice

case $choice in
    1)
        echo ""
        echo "════════════════════════════════════════"
        echo "  📊 生成投资日报..."
        echo "════════════════════════════════════════"
        python3 analyze.py --quick
        ;;
    2)
        echo ""
        echo "════════════════════════════════════════"
        echo "  📈 生成完整分析报告..."
        echo "════════════════════════════════════════"
        python3 analyze.py --full
        ;;
    3)
        echo ""
        echo "════════════════════════════════════════"
        echo "  💰 估值分析..."
        echo "════════════════════════════════════════"
        python3 analyze.py --valuation
        ;;
    4)
        echo ""
        echo "════════════════════════════════════════"
        echo "  🔄 调仓建议..."
        echo "════════════════════════════════════════"
        python3 analyze.py --rebalance
        ;;
    5)
        echo ""
        echo "════════════════════════════════════════"
        echo "  🔍 股票筛选..."
        echo "════════════════════════════════════════"
        echo ""
        echo "选择筛选条件:"
        echo "  [1] 价值股"
        echo "  [2] 成长股"
        echo "  [3] 蓝筹股"
        echo "  [4] 高股息"
        echo "  [5] 低估值"
        echo ""
        echo -n "请输入选项 [1-5]: "
        read screen_choice
        
        case $screen_choice in
            1) python3 analyze.py --screen 价值股 ;;
            2) python3 analyze.py --screen 成长股 ;;
            3) python3 analyze.py --screen 蓝筹股 ;;
            4) python3 analyze.py --screen 高股息 ;;
            5) python3 analyze.py --screen 低估值 ;;
            *) echo "无效选项" ;;
        esac
        ;;
    6)
        echo ""
        echo "════════════════════════════════════════"
        echo "  📊 生成可视化图表..."
        echo "════════════════════════════════════════"
        python3 analyze.py --charts
        echo ""
        echo "图表已保存至：charts/"
        echo ""
        ls -la charts/
        ;;
    7)
        echo ""
        echo "════════════════════════════════════════"
        echo "  📚 查看配置指南..."
        echo "════════════════════════════════════════"
        echo ""
        cat ASSISTANT-SETUP.md | head -100
        echo ""
        echo "...（更多内容请查看 ASSISTANT-SETUP.md）"
        ;;
    8)
        echo ""
        echo "════════════════════════════════════════"
        echo "  ⚙️ 配置定时任务..."
        echo "════════════════════════════════════════"
        bash cron-tasks.sh
        ;;
    0)
        echo ""
        echo "👋 再见！祝你投资顺利！📈"
        echo ""
        exit 0
        ;;
    *)
        echo ""
        echo "❌ 无效选项"
        exit 1
        ;;
esac

echo ""
echo "══════════════════════════════════════════════════════"
echo ""
echo "✅ 操作完成！"
echo ""
echo "💡 提示:"
echo "   • 随时运行 ./start.sh 启动助手"
echo "   • 或直接对我说：'今天投资情况怎么样？'"
echo "   • 查看详细报告：cat logs/daily_*.txt"
echo ""
echo "══════════════════════════════════════════════════════"
echo ""
