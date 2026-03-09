# 🍶 i 茅台申购辅助工具 - 可行性计划与方案 (方案一)

**版本：** v1.0  
**制定日期：** 2026-03-07  
**执行周期：** 10 个工作日  
**风险等级：** 🟢 低风险 (合规安全)

---

## 📋 项目概述

### 项目目标

开发一款**合法合规的 i 茅台申购辅助工具**，帮助用户：
- ⏰ 不错过申购时间
- 📍 快速找到合适门店
- 📊 了解中签率情况
- 🔔 第一时间获知中签结果

### 核心原则

| 原则 | 说明 |
|------|------|
| ✅ **完全合规** | 不触碰 i 茅台 APP，所有操作由用户手动完成 |
| ✅ **零封号风险** | 不模拟点击、不自动提交、不绕过验证 |
| ✅ **用户主导** | 工具仅提供提醒和辅助，决策由用户控制 |
| ✅ **长期可用** | 不依赖 APP 版本，维护成本低 |

---

## 🎯 功能需求分析

### 核心功能模块

```
┌─────────────────────────────────────────────────────────┐
│              i 茅台申购辅助工具 v1.0                      │
├─────────────────────────────────────────────────────────┤
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐│
│  │  ⏰ 时间提醒  │  │  📍 门店查询  │  │  📊 中签统计  ││
│  │   模块        │  │   模块        │  │   模块        ││
│  └───────────────┘  └───────────────┘  └───────────────┘│
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐│
│  │  📝 申购助手  │  │  🔔 结果推送  │  │  📈 数据看板  ││
│  │   模块        │  │   模块        │  │   模块        ││
│  └───────────────┘  └───────────────┘  └───────────────┘│
└─────────────────────────────────────────────────────────┘
```

### 功能详细说明

#### 1️⃣ 时间提醒模块

| 功能 | 说明 | 实现方式 |
|------|------|----------|
| 申购开始提醒 | 每日 08:55 推送提醒 | 定时任务 + 飞书推送 |
| 申购截止提醒 | 每日 20:30 推送提醒 | 定时任务 + 飞书推送 |
| 抽签结果提醒 | 每日 22:00 推送提醒 | 定时任务 + 飞书推送 |
| 自定义提醒 | 用户可配置提醒时间 | 配置文件 |

**提醒内容示例：**
```
🍶 i 茅台申购提醒

⏰ 申购时间：09:00-21:00
📍 推荐门店：XX 专卖店 (竞争较小)
📊 昨日中签率：约 15%

👉 点击打开 i 茅台 APP
[快捷链接]

---
祝您好运！🍀
```

---

#### 2️⃣ 门店查询模块

| 功能 | 说明 | 数据来源 |
|------|------|----------|
| 附近门店 | 根据位置查找周边门店 | 高德/百度地图 API |
| 门店详情 | 地址、电话、营业时间 | 高德/百度地图 API |
| 竞争分析 | 估算各门店竞争程度 | 用户上报 + 统计 |
| 库存监控 | 显示可申购产品 | 需手动更新/用户上报 |

**门店数据结构：**
```python
{
    "store_id": "store_001",
    "name": "茅台专卖店 (XX 店)",
    "address": "XX 市 XX 区 XX 路 XX 号",
    "phone": "010-12345678",
    "distance": 2.5,  # 距离 (公里)
    "latitude": 39.9042,
    "longitude": 116.4074,
    "products": ["飞天 500ml", "飞天 375ml×2", "茅台 1935"],
    "competition_level": "中",  # 低/中/高
    "historical_rate": 0.15,  # 历史中签率
}
```

---

#### 3️⃣ 中签统计模块

| 功能 | 说明 | 实现方式 |
|------|------|----------|
| 个人统计 | 记录个人申购/中签历史 | 本地数据库 |
| 门店统计 | 各门店历史中签率 | 用户上报聚合 |
| 产品统计 | 各产品中签难度 | 用户上报聚合 |
| 趋势分析 | 中签率变化趋势 | 数据统计 |

**统计维度：**
```
个人统计：
├── 累计申购次数
├── 累计中签次数
├── 综合中签率
├── 各产品中签情况
└── 各门店中签情况

门店统计：
├── 门店名称
├── 参与人数 (估算)
├── 投放量 (估算)
├── 历史中签率
└── 竞争等级
```

---

#### 4️⃣ 申购助手模块

| 功能 | 说明 | 实现方式 |
|------|------|----------|
| 信息预填 | 提前准备申购信息 | 剪贴板/表单填充 |
| 快速入口 | 一键打开申购页面 | 深度链接/快捷方式 |
| 申购清单 | 显示今日可申购产品 | 本地配置 |
| 申购记录 | 记录每次申购 | 本地数据库 |

**申购流程辅助：**
```
1. 用户点击提醒通知
   ↓
2. 工具打开 i 茅台 APP
   ↓
3. 工具显示预填信息 (手机号、门店等)
   ↓
4. 用户手动填写并提交
   ↓
5. 工具记录申购信息
```

---

#### 5️⃣ 结果推送模块

| 功能 | 说明 | 实现方式 |
|------|------|----------|
| 飞书推送 | 推送到飞书群/个人 | 飞书开放 API |
| 微信推送 | 推送到微信 (可选) | 企业微信/Server 酱 |
| 短信推送 | 短信通知 (可选) | 阿里云短信 |
| 推送模板 | 可自定义推送内容 | 配置文件 |

**推送内容示例：**
```
🎉 i 茅台中签通知！

📦 中签产品：53%vol 500ml 贵州茅台酒 (飞天)
🏪 提货门店：XX 专卖店
⏰ 支付截止：2026-03-08 22:00
📍 门店地址：XX 市 XX 区 XX 路 XX 号

⚠️ 请在 24 小时内完成支付，7 天内提货！

祝您好运！🍀
```

---

#### 6️⃣ 数据看板模块

| 功能 | 说明 | 展示形式 |
|------|------|----------|
| 申购日历 | 显示每日申购情况 | 日历视图 |
| 中签趋势 | 中签率变化曲线 | 折线图 |
| 门店对比 | 各门店中签率对比 | 柱状图 |
| 数据导出 | 导出 Excel/CSV | 文件下载 |

---

## 🏗️ 技术架构设计

### 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                      用户界面层                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │  命令行界面  │  │  Web 界面    │  │  飞书机器人  │      │
│  └─────────────┘  └─────────────┘  └─────────────┘      │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                      业务逻辑层                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │  提醒服务    │  │  门店服务    │  │  统计服务    │      │
│  └─────────────┘  └─────────────┘  └─────────────┘      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │  推送服务    │  │  数据服务    │  │  配置服务    │      │
│  └─────────────┘  └─────────────┘  └─────────────┘      │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                      数据持久层                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │  SQLite     │  │  配置文件    │  │  日志文件    │      │
│  └─────────────┘  └─────────────┘  └─────────────┘      │
└─────────────────────────────────────────────────────────┘
```

### 技术栈选型

| 层级 | 技术 | 说明 |
|------|------|------|
| **开发语言** | Python 3.10+ | 跨平台、生态丰富 |
| **数据库** | SQLite | 轻量级、无需配置 |
| **定时任务** | APScheduler | Python 定时任务库 |
| **Web 框架** | FastAPI (可选) | 轻量级 API 框架 |
| **推送服务** | 飞书开放 API | 已配置，可直接使用 |
| **地图 API** | 高德地图 API | 门店位置查询 |
| **图表库** | Plotly/Matplotlib | 数据可视化 |
| **打包工具** | PyInstaller | 打包为可执行文件 |

### 目录结构

```
i-moutai-helper/
├── README.md                    # 项目说明
├── requirements.txt             # 依赖列表
├── config.yaml                  # 配置文件
├── main.py                      # 主程序入口
│
├── src/
│   ├── __init__.py
│   ├── reminder/                # 提醒模块
│   │   ├── __init__.py
│   │   ├── scheduler.py         # 定时任务
│   │   └── notifier.py          # 通知推送
│   │
│   ├── store/                   # 门店模块
│   │   ├── __init__.py
│   │   ├── finder.py            # 门店查询
│   │   └── analyzer.py          # 竞争分析
│   │
│   ├── stats/                   # 统计模块
│   │   ├── __init__.py
│   │   ├── tracker.py           # 申购追踪
│   │   └── analyzer.py          # 数据分析
│   │
│   ├── dashboard/               # 看板模块
│   │   ├── __init__.py
│   │   └── visualizer.py        # 数据可视化
│   │
│   └── utils/                   # 工具模块
│       ├── __init__.py
│       ├── database.py          # 数据库操作
│       ├── config.py            # 配置管理
│       └── feishu.py            # 飞书 API
│
├── data/
│   ├── moutai.db                # SQLite 数据库
│   ├── stores.json              # 门店数据
│   └── logs/                    # 日志目录
│
├── web/                         # Web 界面 (可选)
│   ├── index.html
│   ├── static/
│   └── templates/
│
└── tests/                       # 测试用例
    ├── __init__.py
    ├── test_reminder.py
    ├── test_store.py
    └── test_stats.py
```

---

## 📅 开发计划

### 总体时间线

```
Week 1 (Day 1-5)          Week 2 (Day 6-10)
├─ Day 1: 环境搭建         ├─ Day 6: 门店模块
├─ Day 2: 配置模块         ├─ Day 7: 统计模块
├─ Day 3: 数据库模块       ├─ Day 8: 看板模块
├─ Day 4: 飞书推送模块     ├─ Day 9: 整合测试
└─ Day 5: 提醒模块         └─ Day 10: 文档与发布
```

### 详细任务分解

#### Week 1: 基础框架

| 日期 | 任务 | 产出 | 工时 |
|------|------|------|------|
| **Day 1** | 环境搭建与项目初始化 | 项目框架 | 4h |
| - 创建项目目录 | - i-moutai-helper/ | | |
| - 配置 Python 虚拟环境 | - venv/ | | |
| - 初始化 Git 仓库 | - .gitignore | | |
| - 编写 requirements.txt | - requirements.txt | | |
| **Day 2** | 配置模块开发 | config.py | 4h |
| - YAML 配置解析 | - 配置加载/保存 | | |
| - 用户配置模板 | - config.yaml 模板 | | |
| - 配置验证 | - 配置校验逻辑 | | |
| **Day 3** | 数据库模块开发 | database.py | 6h |
| - SQLite 表结构设计 | - 用户表/申购表/中签表 | | |
| - CRUD 操作封装 | - 增删改查方法 | | |
| - 数据迁移脚本 | - init_db.sql | | |
| **Day 4** | 飞书推送模块开发 | feishu.py | 4h |
| - 飞书 API 封装 | - send_message() | | |
| - 消息模板配置 | - 多种消息模板 | | |
| - 推送测试 | - 测试脚本 | | |
| **Day 5** | 提醒模块开发 | reminder.py | 6h |
| - 定时任务配置 | - APScheduler 集成 | | |
| - 提醒逻辑实现 | - 申购/截止/结果提醒 | | |
| - 提醒测试 | - 手动触发测试 | | |

#### Week 2: 核心功能

| 日期 | 任务 | 产出 | 工时 |
|------|------|------|------|
| **Day 6** | 门店查询模块开发 | store_finder.py | 6h |
| - 高德地图 API 对接 | - 附近门店查询 | | |
| - 门店数据缓存 | - stores.json | | |
| - 竞争等级算法 | - 竞争度评估 | | |
| **Day 7** | 统计模块开发 | stats.py | 6h |
| - 申购记录追踪 | - 申购/中签记录 | | |
| - 中签率计算 | - 个人/门店统计 | | |
| - 数据导出功能 | - CSV/Excel导出 | | |
| **Day 8** | 看板模块开发 | dashboard.py | 6h |
| - 数据可视化 | - 折线图/柱状图 | | |
| - Web 界面 (可选) | - 简单 HTML 页面 | | |
| - 报表生成 | - PDF/图片报表 | | |
| **Day 9** | 整合测试 | 测试报告 | 8h |
| - 模块集成测试 | - 端到端测试 | | |
| - Bug 修复 | - 问题修复 | | |
| - 性能优化 | - 响应速度优化 | | |
| **Day 10** | 文档与发布 | README.md | 4h |
| - 用户文档编写 | - 使用说明 | | |
| - 打包发布 | - PyInstaller打包 | | |
| - 项目总结 | - 总结报告 | | |

---

## 💾 数据库设计

### 表结构

#### 用户表 (users)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| phone | TEXT | 手机号 |
| name | TEXT | 姓名 |
| created_at | DATETIME | 创建时间 |

#### 门店表 (stores)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | TEXT | 门店 ID (主键) |
| name | TEXT | 门店名称 |
| address | TEXT | 详细地址 |
| phone | TEXT | 联系电话 |
| latitude | REAL | 纬度 |
| longitude | REAL | 经度 |
| competition_level | TEXT | 竞争等级 (低/中/高) |
| updated_at | DATETIME | 更新时间 |

#### 申购记录表 (reservations)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| user_id | INTEGER | 用户 ID (外键) |
| store_id | TEXT | 门店 ID (外键) |
| product_name | TEXT | 产品名称 |
| reservation_date | DATE | 申购日期 |
| status | TEXT | 状态 (待抽签/中签/未中签) |
| created_at | DATETIME | 创建时间 |

#### 中签记录表 (lottery_results)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| reservation_id | INTEGER | 申购记录 ID (外键) |
| result | TEXT | 结果 (success/failed) |
| notify_time | DATETIME | 通知时间 |
| paid | BOOLEAN | 是否支付 |
| picked_up | BOOLEAN | 是否提货 |
| created_at | DATETIME | 创建时间 |

### SQL 初始化脚本

```sql
-- data/init_db.sql

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone TEXT UNIQUE NOT NULL,
    name TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS stores (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT,
    phone TEXT,
    latitude REAL,
    longitude REAL,
    competition_level TEXT DEFAULT '中',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    store_id TEXT NOT NULL,
    product_name TEXT NOT NULL,
    reservation_date DATE NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (store_id) REFERENCES stores(id)
);

CREATE TABLE IF NOT EXISTS lottery_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reservation_id INTEGER NOT NULL,
    result TEXT NOT NULL,
    notify_time DATETIME,
    paid BOOLEAN DEFAULT FALSE,
    picked_up BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reservation_id) REFERENCES reservations(id)
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_reservations_date ON reservations(reservation_date);
CREATE INDEX IF NOT EXISTS idx_reservations_user ON reservations(user_id);
CREATE INDEX IF NOT EXISTS idx_results_reservation ON lottery_results(reservation_id);
```

---

## 🔧 配置文件示例

```yaml
# config.yaml

# 用户配置
user:
  phone: "13800138000"
  name: "张三"
  location:
    city: "北京市"
    district: "朝阳区"
    latitude: 39.9042
    longitude: 116.4074

# 提醒配置
reminder:
  enabled: true
  purchase_start: "08:55"    # 申购开始提醒
  purchase_end: "20:30"      # 申购截止提醒
  result_notify: "22:00"     # 结果通知提醒
  timezone: "Asia/Shanghai"

# 门店配置
store:
  max_distance: 10.0         # 最大距离 (公里)
  competition_threshold:     # 竞争等级阈值
    low: 0.2                 # 中签率>20% 为低竞争
    medium: 0.1              # 中签率 10-20% 为中竞争
    high: 0.0                # 中签率<10% 为高竞争

# 推送配置
notification:
  feishu:
    enabled: true
    chat_id: "oc_61223fa3823a1a7373a10b6974358342"
    app_id: "cli_a92910c88bf89bb3"
    app_secret: "O6WuZwPyHpkZbFW4fZkk8cMsQg4RwzfN"
  wechat:
    enabled: false
    key: ""                  # Server 酱 key
  sms:
    enabled: false
    provider: "aliyun"
    access_key: ""
    secret_key: ""

# 产品配置
products:
  - name: "53%vol 500ml 贵州茅台酒 (飞天)"
    price: 1499
    enabled: true
  - name: "53%vol 375ml×2 贵州茅台酒 (飞天)"
    price: 2999
    enabled: true
  - name: "53%vol 500ml 茅台 1935"
    price: 1188
    enabled: true
  - name: "53%vol 500ml 珍品茅台酒"
    price: 3999
    enabled: false

# 数据库配置
database:
  path: "data/moutai.db"
  
# 日志配置
logging:
  level: "INFO"
  path: "data/logs/"
  max_size: "10MB"
  backup_count: 5
```

---

## 📊 数据看板设计

### 个人申购看板

```
┌─────────────────────────────────────────────────────────┐
│              🍶 我的申购看板 - 2026 年 3 月                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  📈 本月统计                                             │
│  ┌─────────────┬─────────────┬─────────────┐           │
│  │  申购次数    │  中签次数    │  中签率      │           │
│  ├─────────────┼─────────────┼─────────────┤           │
│  │     7       │     1       │   14.3%     │           │
│  └─────────────┴─────────────┴─────────────┘           │
│                                                         │
│  📦 产品中签情况                                         │
│  ┌───────────────────────────────────────────┐         │
│  │ 飞天 500ml    ████████░░  2/10 (20%)      │         │
│  │ 飞天 375ml×2  ████░░░░░░  1/5  (20%)      │         │
│  │ 茅台 1935     ██░░░░░░░░  1/8  (12.5%)    │         │
│  └───────────────────────────────────────────┘         │
│                                                         │
│  🏪 门店中签情况                                         │
│  ┌───────────────────────────────────────────┐         │
│  │ XX 专卖店 (朝阳)  ████████░░  1/3 (33%)   │         │
│  │ XX 专卖店 (海淀)  ████░░░░░░  1/4 (25%)   │         │
│  │ XX 专卖店 (东城)  ██░░░░░░░░  0/2 (0%)    │         │
│  └───────────────────────────────────────────┘         │
│                                                         │
│  📅 申购日历                                             │
│  ┌───────────────────────────────────────────┐         │
│  │  一   二   三   四   五   六   日          │         │
│  │     [1]  [2]  [3]  [4]  [5]  [6]          │         │
│  │  [7]  [8]  [9] [10] [11] [12] [13]        │         │
│  │ [14] [15] [16] [17] [18] [19] [20]        │         │
│  │ [21] [22] [23] [24] [25] [26] [27]        │         │
│  │ [28] [29] [30] [31]                       │         │
│  │  🟢 已申购  🟡 待抽签  🔴 已中签           │         │
│  └───────────────────────────────────────────┘         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🧪 测试计划

### 测试用例

| 模块 | 测试项 | 预期结果 |
|------|--------|----------|
| 提醒模块 | 定时提醒触发 | 准时推送提醒消息 |
| 提醒模块 | 配置修改生效 | 修改后立即生效 |
| 门店模块 | 附近门店查询 | 返回正确门店列表 |
| 门店模块 | 竞争等级计算 | 根据数据正确评估 |
| 统计模块 | 申购记录保存 | 记录正确保存 |
| 统计模块 | 中签率计算 | 计算结果准确 |
| 推送模块 | 飞书消息发送 | 消息成功发送 |
| 推送模块 | 消息模板渲染 | 模板正确填充 |

### 测试环境

```bash
# 创建测试环境
python3 -m venv test-venv
source test-venv/bin/activate
pip install -r requirements.txt
pip install pytest pytest-cov

# 运行测试
pytest tests/ -v --cov=src
```

---

## 📦 部署方案

### 部署方式一：本地运行 (推荐)

```bash
# 1. 克隆项目
git clone <repo>
cd i-moutai-helper

# 2. 配置环境
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. 配置参数
cp config.yaml.example config.yaml
# 编辑 config.yaml

# 4. 运行程序
python main.py

# 5. 后台运行 (可选)
nohup python main.py > output.log 2>&1 &
```

### 部署方式二：Docker 容器

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "main.py"]
```

```bash
# 构建和运行
docker build -t i-moutai-helper .
docker run -d \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/config.yaml:/app/config.yaml \
  i-moutai-helper
```

### 部署方式三：系统服务 (Linux)

```ini
# /etc/systemd/system/i-moutai-helper.service
[Unit]
Description=i-Moutai Helper Service
After=network.target

[Service]
Type=simple
User=ghost
WorkingDirectory=/home/ghost/.openclaw/workspace/i-moutai-helper
ExecStart=/home/ghost/.openclaw/workspace/i-moutai-helper/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 启用服务
sudo systemctl enable i-moutai-helper
sudo systemctl start i-moutai-helper
sudo systemctl status i-moutai-helper
```

---

## ⚠️ 风险与应对

### 风险评估

| 风险 | 等级 | 可能性 | 影响 | 应对措施 |
|------|------|--------|------|----------|
| 飞书 API 限流 | 🟡 中 | 低 | 中 | 添加重试机制 |
| 地图 API 配额 | 🟡 中 | 中 | 低 | 缓存门店数据 |
| 数据丢失 | 🟡 中 | 低 | 中 | 定期备份数据库 |
| 配置错误 | 🟢 低 | 中 | 低 | 配置验证 |
| 定时任务失效 | 🟡 中 | 低 | 中 | 健康检查 |

### 应对措施

```python
# 1. API 重试机制
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential())
def send_feishu_message(content):
    # 发送消息
    pass

# 2. 数据备份
import shutil
from datetime import datetime

def backup_database():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"data/backup/moutai_{timestamp}.db"
    shutil.copy("data/moutai.db", backup_path)

# 3. 健康检查
def health_check():
    checks = {
        "database": check_database(),
        "feishu_api": check_feishu_api(),
        "config": check_config(),
    }
    return all(checks.values())
```

---

## 📈 后续迭代计划

### v1.1 (申购季优化)

- [ ] 多账号支持
- [ ] 申购自动记录 (辅助功能)
- [ ] 门店库存预警

### v1.2 (数据分析)

- [ ] 中签率预测模型
- [ ] 最佳申购时间推荐
- [ ] 门店竞争趋势分析

### v2.0 (Web 界面)

- [ ] 完整 Web 管理界面
- [ ] 移动端适配
- [ ] 数据同步功能

---

## ✅ 验收标准

### 功能验收

| 功能 | 验收标准 | 状态 |
|------|----------|------|
| 时间提醒 | 每日准时推送 3 次提醒 | ⬜ |
| 门店查询 | 能查询附近 10 公里内门店 | ⬜ |
| 中签统计 | 正确记录申购/中签数据 | ⬜ |
| 结果推送 | 中签后及时推送通知 | ⬜ |
| 数据看板 | 显示个人统计数据 | ⬜ |

### 性能验收

| 指标 | 目标 | 状态 |
|------|------|------|
| 提醒延迟 | < 1 分钟 | ⬜ |
| 推送延迟 | < 5 秒 | ⬜ |
| 查询响应 | < 2 秒 | ⬜ |
| 系统稳定性 | 7x24 小时运行 | ⬜ |

### 文档验收

- [ ] README.md 完整
- [ ] 配置说明清晰
- [ ] 常见问题解答
- [ ] 部署文档完整

---

## 📝 下一步行动

### 立即可做

- [ ] 确认配置文件内容
- [ ] 申请高德地图 API Key (如需门店查询)
- [ ] 确认飞书推送配置

### 本周目标 (Day 1-5)

- [ ] 完成项目初始化
- [ ] 完成基础模块开发
- [ ] 完成提醒和推送功能

### 下周目标 (Day 6-10)

- [ ] 完成门店和统计模块
- [ ] 完成数据看板
- [ ] 整合测试与发布

---

## 💬 需要确认的事项

1. **部署方式？** 本地运行 / Docker / 系统服务
2. **是否需要 Web 界面？** v1.0 仅命令行 + 飞书推送
3. **高德地图 API Key？** 用于门店查询 (可自行申请)
4. **多账号需求？** v1.0 支持单账号，v1.1 支持多账号

---

**🎯 项目启动时间：** 确认可立即开始  
**📅 预计完成时间：** 10 个工作日  
**👨‍💻 开发负责人：** AI Investment Assistant

---

*Generated by AI Investment Assistant*  
*最后更新：2026-03-07*
