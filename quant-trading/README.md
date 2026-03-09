# 量化交易分析框架

## 📊 配置的 API

| API | 状态 | Key 位置 |
|-----|------|----------|
| Tushare | 待配置 | `.env` |
| 聚宽 JoinQuant | 待配置 | `.env` |
| 新浪财经 | ✅ 无需 Key | - |
| Alpha Vantage | 待配置 | `.env` |
| Yahoo Finance | ✅ 无需 Key | - |

## 🚀 快速开始

### 1. 安装依赖
```bash
cd quant-trading
pip install -r requirements.txt
```

### 2. 配置 API Key
```bash
cp .env.example .env
# 编辑 .env 填入你的 API Key
```

### 3. 运行分析
```bash
python main.py
```

## 📁 项目结构

```
quant-trading/
├── README.md           # 本文件
├── requirements.txt    # Python 依赖
├── .env.example        # 环境变量模板
├── .env                # 实际配置（自行创建）
├── main.py             # 主程序入口
├── config.py           # 配置管理
├── data/               # 数据存储
│   ├── raw/           # 原始数据
│   └── processed/     # 处理后数据
├── src/
│   ├── api/           # API 接口封装
│   │   ├── tushare_api.py
│   │   ├── joinquant_api.py
│   │   ├── sina_api.py
│   │   ├── alphavantage_api.py
│   │   └── yahoo_api.py
│   ├── analysis/      # 分析模块
│   │   ├── technical.py    # 技术分析
│   │   ├── fundamental.py  # 基本面分析
│   │   └── risk.py         # 风险分析
│   ├── strategy/      # 交易策略
│   │   ├── momentum.py     # 动量策略
│   │   ├── mean_reversion.py # 均值回归
│   │   └── ml_strategy.py  # 机器学习策略
│   └── utils/         # 工具函数
└── notebooks/         # Jupyter 笔记本
    └── analysis.ipynb
```

## ⚠️ 风险提示

- 量化交易有风险，入市需谨慎
- 历史表现不代表未来收益
- 建议先用模拟盘测试策略
- 不要投入超过你能承受损失的资金

## 📚 学习资源

- [聚宽量化教程](https://www.joinquant.com/help)
- [Tushare 文档](https://tushare.pro/document/2)
- [量化交易入门](https://github.com/quantitative-trading)
