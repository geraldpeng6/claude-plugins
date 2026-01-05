---
name: md
description: 双向文档转换 - PDF/DOCX/XLSX/PPTX/HTML/LaTeX ↔ Markdown
---

# 文档转换

使用 markitdown 将各种文档格式转换为 Markdown，或使用 Pandoc 将 Markdown 转换为其他格式。

## 转换为 Markdown

### 基本用法（Python 代码）

```python
from markitdown import MarkItDown
from pathlib import Path

# 转换文件
md = MarkItDown()
input_file = Path("/absolute/path/to/document.pdf")
result = md.convert(str(input_file))

# 输出到输入文件同目录
output_file = input_file.with_suffix('.md')
output_file.write_text(result.text_content, encoding='utf-8')
print(f"已保存到: {output_file}")
```

**支持格式**: PDF, DOCX, XLSX, PPTX, HTML, LaTeX, 图片, 音频

### 高级用法（脚本）

脚本支持 YouTube 字幕提取、OpenAI 图片描述等高级功能。

```bash
# 使用 uv 运行（自动管理依赖）
uv run --script scripts/to-md.py ~/Documents/document.pdf

# YouTube 视频 URL
uv run --script scripts/to-md.py "https://www.youtube.com/watch?v=xxx"
```

**输出**: Markdown 文件输出到**输入文件相同的目录**

例如：`~/Documents/report.pdf` → `~/Documents/report.md`

## 从 Markdown 转换

使用 Pandoc 将 Markdown 转换为其他格式：

```bash
pandoc input.md -o output.pdf
pandoc input.md -o output.docx
pandoc input.md -o output.html
```

**支持格式**: PDF, DOCX, PPTX, HTML, ODT, LaTeX

### 中文 PDF 支持

```bash
pandoc input.md -o output.pdf --pdf-engine=xelatex -V CJKmainfont="PingFang SC"
```

## 配置

可选配置文件 `config.yaml` 用于 OpenAI API（图片描述功能）：
```bash
cp config.example.yaml config.yaml
# 编辑 config.yaml 添加你的 API 密钥
```
