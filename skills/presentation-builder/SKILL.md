---
name: presentation-builder
description: Create PowerPoint presentations programmatically using python-pptx. Generate slides with text, images, charts, and formatting.
---

# Presentation Builder Skill

## Capabilities

- Create PowerPoint presentations from scratch
- Add slides with various layouts
- Insert text with formatting
- Add images and graphics
- Create charts and tables
- Apply themes and templates
- Export to PPTX format

## Tools Used

- `python-pptx` - PowerPoint generation library
- `pillow` - Image processing (optional)

## Installation

```bash
pip install python-pptx pillow
```

## Usage

When the user asks to create a presentation:

1. Determine the presentation structure (title, sections, slides)
2. Create presentation object
3. Add slides with appropriate layouts
4. Add content (text, images, charts)
5. Save the PPTX file

## Example Commands

```python
from pptx import Presentation
from pptx.util import Inches, Pt

# Create presentation
prs = Presentation()

# Title slide
title_slide = prs.slide_layouts[0]
slide = prs.slides.add_slide(title_slide)
title = slide.shapes.title
subtitle = slide.placeholders[1]
title.text = "Presentation Title"
subtitle.text = "Subtitle Here"

# Content slide
bullet_slide = prs.slide_layouts[1]
slide = prs.slides.add_slide(bullet_slide)
title = slide.shapes.title
content = slide.placeholders[1]
title.text = "Key Points"
content.text = "• Point 1\n• Point 2\n• Point 3"

# Save
prs.save('output.pptx')
```

## Slide Layouts

- 0: Title Slide
- 1: Title and Content
- 2: Section Header
- 3: Two Content
- 4: Comparison
- 5: Title Only
- 6: Blank

## Notes

- Use appropriate slide layouts for content type
- Keep text concise on slides
- Include speaker notes when needed
