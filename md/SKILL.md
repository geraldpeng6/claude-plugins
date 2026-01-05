---
name: md
description: 双向文档转换 - PDF/DOCX/XLSX/PPTX/HTML/LaTeX ↔ Markdown
---

# 文档转换

使用 markitdown 将各种文档格式转换为 Markdown，或使用 Pandoc 将 Markdown 转换为其他格式。

## 快速开始

### 转换为 Markdown

```bash
uv run scripts/to-md.py <文件或URL>
```

**输入格式**: PDF, DOCX, XLSX, PPTX, HTML, LaTeX, 图片, 音频, YouTube URL

**输出**: Markdown 文件保存在输入文件同目录

**示例**:
```bash
uv run scripts/to-md.py ~/Documents/report.pdf
uv run scripts/to-md.py "https://www.youtube.com/watch?v=xxx"
```

### 从 Markdown 转换

```bash
uv run scripts/from-md.sh <文件.md> <格式>
```

**输出格式**: docx, pptx, pdf, html, odt, latex

**示例**:
```bash
uv run scripts/from-md.sh ~/Documents/doc.md docx
uv run scripts/from-md.sh ~/Documents/slides.md pptx
uv run scripts/from-md.sh ~/Documents/paper.md pdf
```

## 详细文档

参见 [reference.md](reference.md) 了解：
- 完整配置选项（OpenAI API、音频转写）
- 高级用法（YouTube 字幕、图片描述）
- 中文 PDF 支持
- Pandoc 高级选项
