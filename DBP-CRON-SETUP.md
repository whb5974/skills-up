# 等保测评自动化项目 - 定时任务配置

## 概述

配置每天上午 10 点自动推送项目执行报告到飞书群。

---

## Cron 任务配置

### 任务信息

| 字段 | 值 |
|------|-----|
| **任务 ID** | `1c3d24f2-e170-4382-822d-38461bfa6ad7` |
| **任务名称** | 等保测评项目日报 |
| **执行时间** | 每天上午 10:00 (Asia/Shanghai) |
| **Cron 表达式** | `0 10 * * *` |
| **目标频道** | 飞书群 `oc_79169c8c6daa7864f85ad4404de3be22` |
| **状态** | ✅ 已启用 |

### 任务内容

每天上午 10 点自动执行：

1. ✅ 生成项目日报（包含项目状态、执行情况、下一步计划）
2. ✅ 发送报告到飞书群
3. ✅ 检查 GitHub 推送状态，网络恢复时自动重试

---

## 相关文件

| 文件 | 路径 | 说明 |
|------|------|------|
| 日报生成脚本 | `/home/ghost/.openclaw/workspace/tools/dbp-daily-report.py` | 生成项目日报内容 |
| GitHub 推送脚本 | `/home/ghost/.openclaw/workspace/tools/github-push-retry.py` | 检查网络并推送 GitHub |
| 项目文档 | `/home/ghost/.openclaw/workspace/dbp-automation/docs/` | 7 份项目方案文档 |

---

## 管理命令

### 查看任务状态

```bash
openclaw cron list
```

### 查看任务详情

```bash
openclaw cron status 1c3d24f2-e170-4382-822d-38461bfa6ad7
```

### 手动执行任务（测试）

```bash
openclaw cron run 1c3d24f2-e170-4382-822d-38461bfa6ad7
```

### 禁用任务

```bash
openclaw cron disable 1c3d24f2-e170-4382-822d-38461bfa6ad7
```

### 启用任务

```bash
openclaw cron enable 1c3d24f2-e170-4382-822d-38461bfa6ad7
```

### 删除任务

```bash
openclaw cron rm 1c3d24f2-e170-4382-822d-38461bfa6ad7
```

---

## 报告内容

每日报告包含：

### 📊 项目状态
- 项目阶段
- 整体进度
- 下一里程碑
- 里程碑日期
- 项目健康度

### 📝 今日执行情况
- 检测脚本开发进度
- 项目文档归档状态
- GitHub 推送状态

### 📋 下一步行动计划
- 项目立项审批
- 组建项目团队
- 召开项目启动会
- 启动需求分析
- 搭建开发环境

### 💾 代码管理状态
- 最后提交信息
- GitHub 同步状态
- 仓库地址

### 📂 项目文档清单
- 细化工作方案 v2.0
- 完整方案 v3.0
- 交付成果汇总
- 测评项设计
- 研讨记录
- 学习报告
- 工作计划

---

## 下次执行时间

**下次运行：** 明天上午 10:00 (Asia/Shanghai)

---

## 注意事项

1. **GitHub 推送**：由于网络连接问题，GitHub 推送可能失败。脚本会在每次执行时检查网络状态，网络恢复后自动重试。

2. **飞书群变更**：如需更改推送的飞书群，请更新 cron 任务的 `--channel` 参数。

3. **报告内容定制**：如需修改报告内容，请编辑 `/home/ghost/.openclaw/workspace/tools/dbp-daily-report.py`。

4. **时区设置**：任务使用 `Asia/Shanghai` 时区（北京时间）。

---

**配置日期：** 2026-03-07  
**配置人：** AI 助手
