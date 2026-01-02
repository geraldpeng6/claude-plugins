# Doc Converter Plugin

通用文档格式转换插件，支持双向转换。

## 功能

### 转换为 Markdown (→ MD)
- PDF, DOCX, XLSX, PPTX, HTML
- 图片 (支持 LLM 描述)
- 音频 (语音转文字)
- YouTube URL (提取字幕)
- LaTeX

### 从 Markdown 转换 (MD →)
- DOCX, PPTX, PDF, HTML, ODT, LaTeX

## 前置要求

- [uv](https://github.com/astral-sh/uv) - Python 包管理器
- [Pandoc](https://pandoc.org/) - `brew install pandoc`
- LaTeX (PDF 输出) - `brew install --cask mactex-no-gui`
- ffmpeg (音频) - `brew install ffmpeg`

## 命令

```bash
# 转换为 Markdown
/convert-to-md <文件或URL>

# 从 Markdown 转换
/convert-from-md <文件> <格式>
```

## 示例

```bash
# 文档转换
/convert-to-md ./report.pdf
/convert-to-md ./data.xlsx

# YouTube 字幕
/convert-to-md "https://www.youtube.com/watch?v=xxx"

# 导出格式
/convert-from-md ./doc.md docx
/convert-from-md ./slides.md pptx
/convert-from-md ./paper.md pdf
```
