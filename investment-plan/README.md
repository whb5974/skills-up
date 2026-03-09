# 📊 2026 年投资计划配套工具

## 文件说明

| 文件 | 用途 |
|------|------|
| `2026-investment-plan.md` | 完整投资计划文档 ⭐ |
| `portfolio-tracker.py` | 投资组合跟踪器 |
| `risk-calculator.py` | 风险分析计算器 |
| `data/` | 数据存储目录 (自动创建) |

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install pandas numpy loguru
```

### 2. 阅读投资计划

打开并阅读 `2026-investment-plan.md`，了解完整策略。

### 3. 初始化投资组合

```bash
cd investment-plan
python portfolio-tracker.py --init
```

输入初始资金 (如 100000 元)。

### 4. 添加持仓

```bash
python portfolio-tracker.py --add
```

按提示输入：
- 股票代码
- 股票名称
- 数量
- 价格
- 手续费
- 备注

### 5. 查看报告

```bash
python portfolio-tracker.py --report
```

---

## 📋 使用示例

### 建仓示例

```bash
# 初始化
python portfolio-tracker.py --init
# 输入：100000

# 买入贵州茅台
python portfolio-tracker.py --add
# 股票代码：600519
# 股票名称：贵州茅台
# 数量：50
# 价格：1800
# 手续费：10
# 备注：核心持仓

# 买入招商银行
python portfolio-tracker.py --add
# 股票代码：600036
# 股票名称：招商银行
# 数量：500
# 价格：35
# 手续费：5
# 备注：蓝筹配置

# 查看报告
python portfolio-tracker.py --report
```

### 更新价格

```bash
# 更新单只股票
python portfolio-tracker.py --update
# 股票代码：600519
# 当前价格：1950

# 或批量更新 (留空股票代码)
python portfolio-tracker.py --update
# 股票代码：(直接回车)
# 然后依次输入每只股票的当前价格
```

### 卖出股票

```bash
python portfolio-tracker.py --sell
# 股票代码：600036
# 数量：200
# 价格：38
# 手续费：5
# 备注：部分止盈
```

---

## 📊 风险分析

```bash
python risk-calculator.py
```

会输出：
- 整体风险评级
- 组合波动率
- 各持仓风险等级
- 投资建议

---

## 📁 数据文件

```
data/
├── portfolio.json        # 持仓数据
├── transactions.csv      # 交易记录
└── reports/              # 生成的报告
    └── report_20260226_143000.txt
```

---

## 🔄 日常使用流程

```
📅 每日:
   - 更新股票价格：python portfolio-tracker.py --update
   - 查看盈亏：python portfolio-tracker.py --report

📅 每周:
   - 运行风险分析：python risk-calculator.py
   - 检查是否触及止损/止盈线

📅 每月:
   - 导出交易记录：查看 data/transactions.csv
   - 月度复盘：对比投资计划
```

---

## ⚠️ 注意事项

1. **数据备份**: 定期备份 `data/` 目录
2. **价格更新**: 需要手动更新当前价格 (可从行情软件获取)
3. **风险提示**: 工具仅供参考，不构成投资建议
4. **止损纪律**: 严格执行投资计划中的止损策略

---

## 📚 扩展功能 (可自行开发)

- [ ] 接入实时行情 API 自动更新价格
- [ ] 添加图表可视化
- [ ] 支持基金持仓
- [ ] 导出 Excel 报表
- [ ] 设置价格预警
- [ ] 回测功能

---

## 💡 提示

投资计划的核心是**执行**和**纪律**：

✅ 按计划配置资产  
✅ 严格执行止损  
✅ 定期复盘调整  
✅ 保持学习心态  

祝投资顺利！📈
