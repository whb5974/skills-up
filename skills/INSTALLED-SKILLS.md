# 已安装 Skills 清单

**安装日期**: 2026-03-09  
**总数**: 7 个新技能

---

## 📦 新安装的技能

| 技能名称 | 描述 | 状态 |
|---------|------|------|
| **data-analysis** | 使用 Python (pandas, numpy) 进行数据分析、统计和可视化 | ✅ 已安装 |
| **presentation-builder** | 使用 python-pptx 创建 PowerPoint 演示文稿 | ✅ 已安装 |
| **pdf-deep-reader** | 深度 PDF 分析，包括文本提取、表格提取、结构分析 | ✅ 已安装 |
| **postgres-admin** | PostgreSQL 数据库管理和查询执行 | ✅ 已安装 |
| **brand-voice-guard** | 品牌语音/风格一致性检查 | ✅ 已安装 |
| **anthropics-skills** | Anthropic 官方技能集合（子模块） | ✅ 已克隆 |
| **nmap-scanner** | 网络扫描和安全评估（之前已安装） | ✅ 已存在 |

---

## 📁 技能目录结构

```
skills/
├── anthropics-skills/          # Anthropic 官方技能集合
│   ├── pdf/                    # PDF 处理技能
│   ├── xlsx/                   # Excel 处理技能
│   ├── pptx/                   # PowerPoint 技能
│   ├── docx/                   # Word 文档技能
│   └── ...                     # 更多技能
├── data-analysis/              # 数据分析技能
│   └── SKILL.md
├── presentation-builder/       # 演示文稿创建技能
│   └── SKILL.md
├── pdf-deep-reader/            # PDF 深度阅读技能
│   └── SKILL.md
├── postgres-admin/             # PostgreSQL 管理技能
│   └── SKILL.md
├── brand-voice-guard/          # 品牌语音检查技能
│   └── SKILL.md
└── nmap-scanner/               # 网络扫描技能（已有）
    └── SKILL.md
```

---

## 🔧 技能依赖安装

### 数据分析技能
```bash
pip install pandas numpy matplotlib seaborn plotly
```

### 演示文稿技能
```bash
pip install python-pptx pillow
```

### PDF 深度阅读技能
```bash
pip install pymupdf pdfplumber PyPDF2 pytesseract
```

### PostgreSQL 管理技能
```bash
pip install psycopg2-binary
```

### 品牌语音检查技能
```bash
pip install textblob nltk  # 可选，用于情感分析
```

---

## 📝 使用说明

### 激活技能

在 OpenClaw 配置中启用技能：

```json
{
  "skills": {
    "entries": {
      "data-analysis": { "enabled": true },
      "presentation-builder": { "enabled": true },
      "pdf-deep-reader": { "enabled": true },
      "postgres-admin": { "enabled": true },
      "brand-voice-guard": { "enabled": true }
    }
  }
}
```

### 使用示例

**数据分析**:
> "帮我分析这个 CSV 文件，生成统计摘要和可视化图表"

**演示文稿**:
> "创建一个 10 页的产品介绍 PPT，包含标题页、功能介绍、市场分析"

**PDF 阅读**:
> "阅读这个 PDF 文档，提取所有表格并总结主要内容"

**PostgreSQL**:
> "连接到数据库，查询活跃用户列表并导出为 CSV"

**品牌语音**:
> "检查这篇文档是否符合我们的品牌语音指南"

---

## ⚠️ 注意事项

1. **anthropics-skills** 是作为 git 子模块克隆的，需要单独管理
2. 某些技能需要额外的 Python 依赖，请在使用前安装
3. PostgreSQL 技能需要有效的数据库连接信息
4. PDF OCR 功能需要安装 `tesseract-ocr` 系统包

---

## 🔄 更新技能

```bash
# 更新所有技能
clawhub update --all

# 更新特定技能
clawhub update data-analysis

# 更新 anthropics 子模块
cd skills/anthropics-skills && git pull
```

---

**最后更新**: 2026-03-09
