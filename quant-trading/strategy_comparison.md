# 📊 Qbot 策略对比报告

**生成日期：** 2026-03-08  
**测试周期：** 252 个交易日 (1 年)  
**初始资金：** 100,000 元

---

## 🎯 测试策略

| 策略 | 类型 | 参数 | 适用市场 |
|------|------|------|----------|
| 双均线 (MA5/MA20) | 趋势跟踪 | MA5, MA20 | 趋势市场 |
| MACD (12/26/9) | 趋势 + 动量 | EMA12, EMA26, Signal9 | 震荡 + 趋势 |
| 布林带 (20,2) | 均值回归 | Window20, Std2 | 震荡市场 |

---

## 📈 回测结果对比

### 核心指标

| 指标 | 双均线 | MACD | 布林带 | 最优 |
|------|--------|------|--------|------|
| **总收益率** | - | - | - | - |
| **年化收益率** | - | - | - | - |
| **胜率** | - | - | - | - |
| **最大回撤** | - | - | - | - |
| **夏普比率** | - | - | - | - |
| **交易次数** | - | - | - | - |

> 注：实际数据需要安装 pandas 后运行测试

---

## 🔍 策略特点分析

### 双均线策略

**优点：**
- ✅ 逻辑简单，易于理解
- ✅ 趋势市场表现优秀
- ✅ 交易信号明确

**缺点：**
- ❌ 震荡市场频繁止损
- ❌ 信号滞后
- ❌ 参数敏感

**适用场景：**
- 明显趋势行情
- 长线投资

---

### MACD 策略

**优点：**
- ✅ 兼顾趋势和动量
- ✅ 零轴过滤假信号
- ✅ 强势信号识别

**缺点：**
- ❌ 震荡市场表现一般
- ❌ 参数复杂
- ❌ 计算量较大

**适用场景：**
- 震荡 + 趋势混合市场
- 中线投资

---

### 布林带策略

**优点：**
- ✅ 震荡市场表现优秀
- ✅ %B 指标直观
- ✅ 极度信号准确

**缺点：**
- ❌ 趋势市场容易失效
- ❌ 触及轨道不一定反转
- ❌ 需要配合其他指标

**适用场景：**
- 震荡市场
- 短线交易

---

## 💡 策略组合建议

### 保守型

- **主策略：** 双均线 (MA20/MA60)
- **辅助：** MACD 过滤
- **仓位：** 50%

### 平衡型

- **主策略：** MACD
- **辅助：** 布林带超买超卖
- **仓位：** 70%

### 激进型

- **主策略：** 布林带
- **辅助：** RSI 确认
- **仓位：** 90%

---

## 🎯 下一步计划

### Day 11-14

- [ ] RSI 策略实现
- [ ] 参数优化测试
- [ ] 多策略组合回测
- [ ] 实盘模拟测试

### 环境配置

- [ ] 安装 pandas, numpy
- [ ] 安装 matplotlib (可视化)
- [ ] 安装 loguru (日志)
- [ ] 创建虚拟环境

---

## 📝 测试代码

```python
# 统一回测框架
from strategy.dual_ma_strategy import DualMAStrategy
from strategy.macd_strategy import MACDStrategy
from strategy.bollinger_strategy import BollingerStrategy

# 创建策略
dual_ma = DualMAStrategy(short_window=5, long_window=20)
macd = MACDStrategy(fast_period=12, slow_period=26, signal_period=9)
bollinger = BollingerStrategy(window=20, num_std=2)

# 回测
dual_ma_result = dual_ma.backtest(df)
macd_result = macd.backtest(df)
bollinger_result = bollinger.backtest(df)

# 对比
print(f"双均线收益率：{dual_ma_result['total_return_pct']}")
print(f"MACD 收益率：{macd_result['total_return_pct']}")
print(f"布林带收益率：{bollinger_result['total_return_pct']}")
```

---

**报告生成：** AI Investment Assistant  
**下次更新：** 2026-03-09 (RSI 策略完成后)
