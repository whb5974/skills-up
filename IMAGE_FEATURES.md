# 图片分析处理功能

OpenClaw 已配置完整的图片分析处理功能，支持：

## 📸 图片识别与分析

### 支持的模型
- **主模型**: `bailian/qwen3.5-plus` (支持 text+image 输入，1M 上下文)
- **备用模型**: `bailian/kimi-k2.5` (支持 text+image 输入，256k 上下文)

### 功能
1. **OCR 文字识别** - 识别图片中的文字内容
2. **图形识别** - 识别图表、图形、表格等
3. **内容理解** - 理解图片场景、物体、人物、动作等
4. **详细描述** - 生成图片的详细文字描述

### 使用方法
直接在对话中发送图片，然后提问：
- "这张图片里有什么？"
- "请识别图中的文字"
- "分析这个图表的数据"
- "描述这张图片的内容"

## 🎨 图片生成

### 配置
图片生成功能使用 OpenAI Images API，支持以下模型：

| 模型 | 说明 | 支持尺寸 | 特点 |
|------|------|----------|------|
| `dall-e-3` | DALL-E 3 | 1024x1024, 1792x1024, 1024x1792 | 高质量，每次生成 1 张 |
| `dall-e-2` | DALL-E 2 | 256x256, 512x512, 1024x1024 | 快速，可批量生成 |
| `gpt-image-1` | GPT Image | 1024x1024, 1536x1024, 1024x1536 | 支持透明背景 |

### 配置 API Key
在 `~/.openclaw/openclaw.json` 中配置：
```json
{
  "skills": {
    "entries": {
      "openai-image-gen": {
        "apiKey": "你的 OpenAI API Key"
      }
    }
  }
}
```

### 使用方法
使用命令生成图片：
```bash
# 生成 1 张图片
python3 ~/.npm-global/lib/node_modules/openclaw/skills/openai-image-gen/scripts/gen.py --prompt "一只可爱的猫咪" --model dall-e-3

# 批量生成 4 张
python3 ~/.npm-global/lib/node_modules/openclaw/skills/openai-image-gen/scripts/gen.py --prompt "风景画" --count 4 --model dall-e-2

# 高清生成
python3 ~/.npm-global/lib/node_modules/openclaw/skills/openai-image-gen/scripts/gen.py --prompt "工作室摄影" --quality hd --model dall-e-3
```

### 输出
- 生成的图片保存在 `~/tmp/openai-image-gen-*/` 目录
- 包含 `index.html` 缩略图画廊
- 包含 `prompts.json` 提示词映射

## 🔧 高级配置

### 图片分析配置
```json
{
  "agents": {
    "defaults": {
      "imageAnalysisModel": {
        "primary": "bailian/qwen3.5-plus",
        "fallbacks": ["bailian/kimi-k2.5"]
      },
      "imageMaxDimensionPx": 4096,
      "imageMaxBytes": 20971520
    }
  }
}
```

### 图片生成配置
```json
{
  "skills": {
    "entries": {
      "openai-image-gen": {
        "apiKey": "sk-xxx",
        "defaultModel": "dall-e-3",
        "defaultCount": 1,
        "defaultSize": "1024x1024",
        "defaultQuality": "standard"
      }
    }
  }
}
```

## 📝 使用示例

### 图片分析示例
```
用户：[发送图片]
用户：这张图片里写了什么？
助手：图片中的文字是："Hello World"

用户：[发送图表图片]
用户：分析这个图表的趋势
助手：这是一个折线图，显示了...
```

### 图片生成示例
```
用户：生成一张夕阳下的海滩图片
助手：正在为您生成图片...
[生成完成后发送图片]
```

## ⚠️ 注意事项

1. **图片大小限制**: 最大 20MB，最大边长 4096px
2. **API 费用**: 图片生成使用 OpenAI API，会产生费用
3. **生成时间**: DALL-E 3 生成一张图片约需 10-30 秒
4. **内容政策**: 请遵守内容生成政策，不要生成违规内容
