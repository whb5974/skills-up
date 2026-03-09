#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import os

# 创建图片
width, height = 1400, 1000
img = Image.new('RGB', (width, height), color='#f5f5f5')
draw = ImageDraw.Draw(img)

# 尝试加载中文字体
font_paths = [
    '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc',
    '/System/Library/Fonts/PingFang.ttc',
    'C:\\Windows\\Fonts\\msyh.ttc',
]
font = None
for fp in font_paths:
    if os.path.exists(fp):
        try:
            font = ImageFont.truetype(fp, 24)
            font_large = ImageFont.truetype(fp, 36)
            font_small = ImageFont.truetype(fp, 18)
            break
        except:
            pass

if font is None:
    font = ImageFont.load_default()
    font_large = font
    font_small = font

# 标题
draw.text((width//2, 30), "《卜算子·咏梅》对比分析", fill='#2c3e50', font=font_large, anchor='mm')
draw.text((width//2, 65), "毛泽东 vs 陆游", fill='#7f8c8d', font=font, anchor='mm')

# 中心节点
center_x, center_y = width//2, 150
draw.ellipse([center_x-70, center_y-70, center_x+70, center_y+70], fill='#667eea', outline='#5a67d8', width=3)
draw.text((center_x, center_y-10), "咏梅", fill='white', font=font_large, anchor='mm')
draw.text((center_x, center_y+15), "对比", fill='white', font=font, anchor='mm')

# 左侧 - 毛泽东
mao_x, mao_y = 350, 150
draw.line([(center_x-70, center_y), (mao_x+50, mao_y)], fill='#e74c3c', width=4)
draw.ellipse([mao_x-50, mao_y-50, mao_x+50, mao_y+50], fill='#e74c3c', outline='#c0392b', width=3)
draw.text((mao_x, mao_y-10), "毛泽东", fill='white', font=font_large, anchor='mm')
draw.text((mao_x, mao_y+15), "1961 年", fill='white', font=font_small, anchor='mm')

# 毛泽东子项
mao_items = [
    (200, 280, "乐观豪迈", "革命精神"),
    (350, 280, "花枝俏", "自信美丽"),
    (500, 280, "丛中笑", "与民同乐"),
]
for x, y, title, desc in mao_items:
    draw.line([(mao_x, mao_y+50), (x, y-20)], fill='#e74c3c', width=2)
    draw.rounded_rectangle([x-70, y-25, x+70, y+25], radius=10, fill='#ffeaa7', outline='#fdcb6e', width=2)
    draw.text((x, y-8), title, fill='#333', font=font, anchor='mm')
    draw.text((x, y+10), desc, fill='#666', font=font_small, anchor='mm')

# 右侧 - 陆游
lu_x, lu_y = 1050, 150
draw.line([(center_x+70, center_y), (lu_x-50, lu_y)], fill='#3498db', width=4)
draw.ellipse([lu_x-50, lu_y-50, lu_x+50, lu_y+50], fill='#3498db', outline='#2980b9', width=3)
draw.text((lu_x, lu_y-10), "陆游", fill='white', font=font_large, anchor='mm')
draw.text((lu_x, lu_y+15), "南宋", fill='white', font=font_small, anchor='mm')

# 陆游子项
lu_items = [
    (900, 280, "孤寂悲凉", "怀才不遇"),
    (1050, 280, "独自愁", "孤独无助"),
    (1200, 280, "香如故", "坚守节操"),
]
for x, y, title, desc in lu_items:
    draw.line([(lu_x, lu_y+50), (x, y-20)], fill='#3498db', width=2)
    draw.rounded_rectangle([x-70, y-25, x+70, y+25], radius=10, fill='#d5f5e3', outline='#58d68d', width=2)
    draw.text((x, y-8), title, fill='#333', font=font, anchor='mm')
    draw.text((x, y+10), desc, fill='#666', font=font_small, anchor='mm')

# 下方 - 相同点
common_y = 400
draw.line([(center_x, center_y+70), (center_x, common_y-30)], fill='#9b59b6', width=4)
draw.rounded_rectangle([center_x-150, common_y-30, center_x+150, common_y+30], radius=15, fill='#f5eef8', outline='#9b59b6', width=3)
draw.text((center_x, common_y-5), "相同点", fill='#8e44ad', font=font_large, anchor='mm')
draw.text((center_x, common_y+18), "词牌·咏物·不争春·傲雪", fill='#666', font=font_small, anchor='mm')

# 相同点子项
common_items = [
    (400, 520, "卜算子", "词牌相同"),
    (600, 520, "咏梅花", "托物言志"),
    (800, 520, "不争春", "高洁品格"),
    (1000, 520, "傲霜雪", "坚韧不拔"),
]
for x, y, title, desc in common_items:
    draw.line([(center_x, common_y+30), (x, y-25)], fill='#9b59b6', width=2)
    draw.rounded_rectangle([x-60, y-22, x+60, y+22], radius=8, fill='#f5eef8', outline='#9b59b6', width=2)
    draw.text((x, y-6), title, fill='#8e44ad', font=font, anchor='mm')
    draw.text((x, y+10), desc, fill='#666', font=font_small, anchor='mm')

# 诗词原文区域
poem_y = 620
draw.rounded_rectangle([50, poem_y, 650, poem_y+180], radius=15, fill='white', outline='#e74c3c', width=3)
draw.text((350, poem_y+25), "🔴 毛泽东《卜算子·咏梅》", fill='#c0392b', font=font_large, anchor='mm')
mao_poem = "风雨送春归，飞雪迎春到。\n已是悬崖百丈冰，犹有花枝俏。\n\n俏也不争春，只把春来报。\n待到山花烂漫时，她在丛中笑。"
draw.text((350, poem_y+70), mao_poem, fill='#333', font=font, anchor='mm', spacing=8)

draw.rounded_rectangle([750, poem_y, 1350, poem_y+180], radius=15, fill='white', outline='#3498db', width=3)
draw.text((1050, poem_y+25), "🔵 陆游《卜算子·咏梅》", fill='#2980b9', font=font_large, anchor='mm')
lu_poem = "驿外断桥边，寂寞开无主。\n已是黄昏独自愁，更著风和雨。\n\n无意苦争春，一任群芳妒。\n零落成泥碾作尘，只有香如故。"
draw.text((1050, poem_y+70), lu_poem, fill='#333', font=font, anchor='mm', spacing=8)

# 总结
summary_y = 830
draw.rounded_rectangle([100, summary_y, 1300, summary_y+140], radius=15, fill='#fef5e7', outline='#e67e22', width=3)
draw.text((width//2, summary_y+25), "💡 核心对比总结", fill='#d35400', font=font_large, anchor='mm')
summary_text = "毛泽东：革命乐观 · 集体主义 · 积极向上 → 困难时期的精神鼓舞\n\n陆  游：孤寂悲凉 · 个人节操 · 坚守本心 → 报国无门的无奈抒发\n\n📚 学习要点：知人论世 · 同一意象不同情感 · 对比阅读深化理解"
draw.text((width//2, summary_y+75), summary_text, fill='#666', font=font, anchor='mm', spacing=6)

# 保存图片
output_path = '/home/ghost/.openclaw/workspace/卜算子咏梅思维导图.png'
img.save(output_path, 'PNG')
print(f"图片已保存：{output_path}")
