# 🤖 投资助手配置指南

> 让你的 AI 助手 24/7 跟踪投资、提供建议、提醒重要事项

---

## 📋 助手能力清单

| 能力 | 频率 | 说明 |
|------|------|------|
| 📊 持仓跟踪 | 每日 | 自动计算盈亏、生成日报 |
| ⚠️ 风险预警 | 实时 | 触及止损线立即提醒 |
| 🔄 调仓建议 | 每周/每月 | 资产配置再平衡建议 |
| 💰 估值分析 | 每周 | 判断持仓是否高估/低估 |
| 📈 市场解读 | 重大事件 | 市场波动时提供分析 |
| 📚 学习提醒 | 每周 | 投资知识学习建议 |
| 📅 定投提醒 | 每月 15 日 | 基金定投提醒 |
| 📝 复盘提醒 | 每月/每季 | 定期复盘提醒 |

---

## 🔧 配置方法

### 方法 1：OpenClaw 定时任务（推荐）

如果你有 OpenClaw 的 cron 功能，可以设置定时检查：

```bash
# 编辑 crontab
crontab -e

# 添加以下任务：

# 每日 9:00 生成投资日报
0 9 * * 1-5 cd /home/ghost/.openclaw/workspace/investment-plan && python3 analyze.py --quick >> logs/cron_daily.log 2>&1

# 每周五 17:00 周复盘
0 17 * * 5 cd /home/ghost/.openclaw/workspace/investment-plan && python3 analyze.py --full >> logs/cron_weekly.log 2>&1

# 每月 15 日 定投提醒
0 9 15 * * echo "💰 今天是基金定投日！建议定投 2000 元" >> logs/cron_monthly.log 2>&1

# 每月最后一天 22:00 月复盘
0 22 28-31 * * [ "$(date +\%d -d tomorrow)" = "01" ] && cd /home/ghost/.openclaw/workspace/investment-plan && python3 analyze.py --rebalance >> logs/cron_monthly.log 2>&1

# 每季度最后一天 季度复盘
0 20 28-31 3,6,9,12 * * [ "$(date +\%m -d tomorrow)" = "01" ] && cd /home/ghost/.openclaw/workspace/investment-plan && python3 analyze.py --full >> logs/cron_quarterly.log 2>&1
```

### 方法 2：直接对话（最简单）

随时在聊天中问我：

```
• "今天投资情况怎么样？"
• "帮我分析一下持仓"
• "需要调仓吗？"
• "贵州茅台现在估值如何？"
• "生成投资日报"
• "本月定投提醒"
```

我会立即运行分析工具，给你最新报告！

### 方法 3：消息推送（高级）

如果你配置了 Telegram/微信等，可以设置消息推送：

```bash
# 示例：Telegram 推送
python3 analyze.py --quick | telegram-send --stdin
```

---

## 📱 日常使用流程

### 每日检查（1 分钟）

```
你：今天投资情况？
我：📊 投资日报
   • 总资产：XXX 元
   • 今日盈亏：+/-XX 元
   • 风险状态：正常/关注/警惕
```

### 每周复盘（5 分钟）

```
你：周复盘
我：📈 周度分析
   • 本周收益：+/-X%
   • 持仓变化：买入/卖出 X 只
   • 调仓建议：需要/不需要
   • 下周策略：...
```

### 每月复盘（15 分钟）

```
你：月复盘
我：📊 月度分析
   • 本月收益：+/-X%
   • 累计收益：+/-X%
   • 资产配置：对比目标
   • 调仓计划：具体操作
   • 下月策略：...
```

---

## ⚙️ 个性化配置

### 修改投资目标

编辑 `2026-investment-plan.md` 中的配置：

```markdown
预期年化收益：12% - 18%  → 改成你的目标
最大可承受回撤：-20%     → 改成你的风险承受能力
```

### 修改持仓数据

编辑 `data/portfolio.json`：

```json
{
  "positions": {
    "600519": {
      "name": "贵州茅台",
      "shares": 20,           // 改成你的持仓
      "cost_basis": 1800.00,  // 改成你的成本
      "current_price": 1800.00 // 每日更新
    }
  }
}
```

### 修改提醒频率

编辑 `cron-tasks.sh` 中的定时任务时间。

---

## 🎯 助手工作模式

### 主动模式（推荐）

我定期检查，主动提醒你：
- ⏰ 每日早上 9 点：投资日报
- ⏰ 每周五下午：周复盘
- ⏰ 每月 15 日：定投提醒
- ⏰ 每月最后一天：月复盘
- ⚠️ 触及止损：立即预警

### 被动模式

你随时问我，我立即回答：
- "今天盈亏如何？"
- "需要调仓吗？"
- "帮我分析贵州茅台"
- "生成月报"

---

## 📊 我能提供的分析

### 1. 持仓分析
```bash
python3 analyze.py --quick
```
- 总资产、总收益
- 各持仓盈亏
- 风险状态

### 2. 估值分析
```bash
python3 analyze.py --valuation
```
- PE/PB/PEG 估值
- 低估/高估判断
- 操作建议

### 3. 调仓建议
```bash
python3 analyze.py --rebalance
```
- 配置偏离分析
- 调仓金额计算
- 具体操作建议

### 4. 股票筛选
```bash
python3 analyze.py --screen 价值股
python3 analyze.py --screen 成长股
python3 analyze.py --screen 高股息
```
- 按条件筛选
- 推荐标的列表

### 5. 可视化
```bash
python3 analyze.py --charts
```
- 资产配置图
- 盈亏分布图
- 风险等级图

### 6. 完整分析
```bash
python3 analyze.py
```
- 以上所有功能一次性运行

---

## 💡 使用技巧

### 快捷命令

| 你说 | 我执行 |
|------|--------|
| "今天怎么样" | `analyze.py --quick` |
| "分析持仓" | `analyze.py --valuation` |
| "需要调仓吗" | `analyze.py --rebalance` |
| "推荐股票" | `analyze.py --screen 价值股` |
| "看图" | `analyze.py --charts` |
| "完整报告" | `analyze.py` |

### 更新价格

```bash
# 方法 1：手动编辑 data/portfolio.json
# 方法 2：使用跟踪器
python3 portfolio-tracker.py --update
```

### 添加新持仓

```bash
python3 portfolio-tracker.py --add
# 按提示输入股票信息
```

### 查看历史交易

```bash
cat data/transactions.csv
```

---

## ⚠️ 重要提醒

### 助手能做的
✅ 记录持仓、计算盈亏  
✅ 分析估值、风险评估  
✅ 生成报告、提供建议  
✅ 定时提醒、主动预警  
✅ 解答投资问题  

### 助手不能做的
❌ 代替你做交易决策  
❌ 保证投资收益  
❌ 预测市场走势  
❌ 接入实时行情（需手动更新价格）  
❌ 承担投资损失  

### 你需要做的
1. **每日/每周更新价格** - 从行情软件获取最新价格
2. **审核建议** - 我的建议仅供参考，决策在你
3. **执行交易** - 实际买卖操作需要你自己完成
4. **风险自负** - 投资有风险，请独立判断

---

## 🎁 额外功能

### 学习提醒
我可以定期提醒你学习投资知识：
- 📚 每周推荐一本书
- 📖 解读投资概念
- 📊 分析经典案例

### 市场解读
重大市场事件发生时，问我：
- "今天大盘为什么跌？"
- "美联储加息有什么影响？"
- "这个政策对 A 股有什么影响？"

### 投资心理
投资心态波动时，找我聊聊：
- "最近市场波动大，怎么办？"
- "持仓跌了 20%，要止损吗？"
- "牛市来了，要加仓吗？"

---

## 🚀 立即开始

### 第一步：确认配置
```bash
cd /home/ghost/.openclaw/workspace/investment-plan
cat TASK-CHECKLIST.md
```

### 第二步：运行一次完整分析
```bash
python3 analyze.py
```

### 第三步：设置提醒（可选）
```bash
bash cron-tasks.sh
# 按提示配置 crontab
```

### 第四步：随时找我
```
"今天投资情况怎么样？"
```

---

## 📞 联系方式

随时在聊天中找我，我会立即响应！

**推荐对话开场白：**
- "今天投资情况怎么样？"
- "帮我生成投资日报"
- "需要调仓吗？"
- "分析一下贵州茅台"
- "推荐几只低估值的股票"
- "本月定投提醒"

---

**🤖 我随时待命，做你的 24/7 投资助手！**

> 投资是场马拉松，我会一直陪着你，提供数据、分析、建议，但最终的决策在你手中。
> 让我们一起，理性投资，长期致胜！📈
