#!/bin/bash

# WhatsApp 快速配置脚本

echo "📱 WhatsApp 配置脚本"
echo "===================="
echo ""

CONFIG_FILE="$HOME/.openclaw/openclaw.json"
BACKUP_FILE="$CONFIG_FILE.bak.whatsapp"

# 备份原配置
if [ -f "$CONFIG_FILE" ]; then
    cp "$CONFIG_FILE" "$BACKUP_FILE"
    echo "✅ 配置已备份：$BACKUP_FILE"
fi

# 使用 Python 添加 WhatsApp 配置
python3 << 'PYTHON_EOF'
import json
import sys

config_file = "/home/ghost/.openclaw/openclaw.json"

try:
    # 读取配置
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 添加 WhatsApp 配置
    if 'channels' not in config:
        config['channels'] = {}
    
    config['channels']['whatsapp'] = {
        "enabled": True,
        "provider": "whatsapp-web",
        "name": "My WhatsApp",
        "autoReconnect": True,
        "auth": {
            "method": "qr",
            "sessionDir": "~/.openclaw/channels/whatsapp"
        }
    }
    
    # 保存配置
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✅ WhatsApp 配置已添加到 openclaw.json")
    
except Exception as e:
    print(f"❌ 配置失败：{e}")
    sys.exit(1)

PYTHON_EOF

echo ""
echo "===================="
echo "下一步操作:"
echo ""
echo "1. 启动 WhatsApp 连接:"
echo "   openclaw channels login --channel whatsapp"
echo ""
echo "2. 或重启 Gateway:"
echo "   openclaw gateway restart"
echo ""
echo "3. 查看配置:"
echo "   cat ~/.openclaw/openclaw.json | python3 -m json.tool | grep -A 10 whatsapp"
echo ""
echo "📖 详细文档：cat WHATSAPP-SETUP.md"
echo ""
