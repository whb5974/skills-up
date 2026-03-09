# Qbot 学习问题追踪

## 📋 问题列表

### 问题 001：GitHub 克隆失败

**发现日期：** 2026-02-26

**现象：**
```bash
git clone https://github.com/UFund-Me/Qbot.git
fatal: 无法访问 'https://github.com/UFund-Me/Qbot.git/'
GnuTLS recv error (-110): The TLS connection was non-properly terminated.
```

**原因分析：**
1. 网络连接不稳定
2. GitHub 在国内访问受限
3. TLS 连接被干扰

**解决方案：**

方案 1 - 使用代理：
```bash
# 配置代理后重试
export https_proxy=http://127.0.0.1:7890
git clone https://github.com/UFund-Me/Qbot.git
```

方案 2 - 使用镜像源：
```bash
# 使用国内镜像
git clone https://github.com.cnpmjs.org/UFund-Me/Qbot.git
```

方案 3 - 手动下载：
```bash
# 下载 ZIP 后解压
wget https://github.com/UFund-Me/Qbot/archive/refs/heads/main.zip
unzip main.zip
```

方案 4 - 先学习文档：
```bash
# 不依赖代码，先学习理论和文档
# 等网络好时再克隆
```

**当前状态：** ⚠️ 待解决（不影响理论学习）

**影响：** 延迟环境搭建，但不影响理论学习

---

## 📊 问题统计

| 状态 | 数量 |
|------|------|
| 🔴 未解决 | 1 |
| 🟡 部分解决 | 0 |
| 🟢 已解决 | 0 |
| **总计** | **1** |

---

## 📝 新增问题模板

### 问题 XXX：[问题标题]

**发现日期：** YYYY-MM-DD

**现象：**
```
错误信息或现象描述
```

**原因分析：**
1. 
2. 

**解决方案：**

方案 1 - 

方案 2 - 

**当前状态：** ⬜ 待解决 / ✅ 已解决

**影响：** 

---

### 问题 002：Python 环境缺少依赖包

**发现日期：** 2026-03-06

**现象：**
```bash
python3 src/strategy/dual_ma_strategy.py
ModuleNotFoundError: No module named 'pandas'
```

**原因分析：**
1. 系统 Python 未安装 pip
2. 无 sudo 权限安装系统包
3. 量化交易依赖 (pandas, numpy, loguru) 缺失

**解决方案：**

方案 1 - 申请 sudo 权限安装：
```bash
sudo apt install python3-pip
pip3 install pandas numpy loguru matplotlib
```

方案 2 - 使用虚拟环境 (需要 pip):
```bash
python3 -m venv qbot-env
source qbot-env/bin/activate
pip install pandas numpy loguru matplotlib
```

方案 3 - 使用 conda (如果可用):
```bash
conda create -n qbot python=3.10 pandas numpy
conda activate qbot
```

**当前状态：** ⚠️ 待解决

**影响：** 代码已完成，无法运行测试

---

**更新时间：** 2026-03-06

---

## ✅ 已修复问题

### 修复 001：飞书报告脚本解析错误

**发现日期：** 2026-03-06

**问题：**
- 学习阶段提取包含 markdown 格式残留 (`**`)
- 周次提取失败，显示 "第？周"

**修复内容：**
1. 修复 `send-qbot-feishu-report.py` 中的字符串解析逻辑
2. 添加 `strip('**')` 清理 markdown 格式
3. 使用正则表达式提取周次信息

**状态：** ✅ 已修复

---

### 修复 002：天气脚本命令未找到

**发现日期：** 2026-03-06

**问题：**
```
/home/ghost/.openclaw/workspace/scripts/taiyuan-weather.sh: 行 41: openclaw: 未找到命令
```

**原因：** cron 环境中 PATH 不包含 npm global bin 路径

**修复内容：**
在 `taiyuan-weather.sh` 开头添加 PATH 设置：
```bash
export PATH="$HOME/.npm-global/bin:$PATH"
```

**状态：** ✅ 已修复

---

**更新时间：** 2026-03-06
