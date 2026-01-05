# 文档转换 - 详细文档

本文档提供文档转换功能的详细说明和高级用法。

## 前置要求

### 必需工具

- **[uv](https://github.com/astral-sh/uv)** - Python 包管理器
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

- **[Pandoc](https://pandoc.org/)** - 文档转换工具
  ```bash
  brew install pandoc
  ```

### 可选工具

- **LaTeX** (PDF 输出)
  ```bash
  brew install --cask mactex-no-gui
  ```

- **ffmpeg** (音频转录)
  ```bash
  brew install ffmpeg
  ```

## 转换为 Markdown

### 脚本功能

`scripts/to-md.py` 支持以下功能：

- **文档格式**: PDF, DOCX, XLSX, PPTX, HTML, LaTeX
- **图片**: PNG, JPG 等（支持 LLM 描述）
- **音频**: MP3, WAV 等（语音转文字）
- **YouTube URL**: 自动提取字幕

### 配置选项

创建 `config.yaml` 文件（可选）：

```bash
cp config.example.yaml config.yaml
```

**配置示例**：

```yaml
# OpenAI API（用于图片描述）
openai:
  api_key: "sk-xxx"
  model: "gpt-4o"
  base_url: "https://api.openai.com/v1"

# 音频转录设置
audio:
  language: "zh"  # 自动检测语言，或指定如 'zh', 'en'

# PDF 输出设置（从 markdown 转换时）
pdf:
  engine: "xelatex"
  cjk_font: "PingFang SC"
```

### 高级用法

#### 1. YouTube 字幕提取

```bash
uv run scripts/to-md.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

自动提取视频字幕并保存为 Markdown。

#### 2. 图片 LLM 描述

配置 OpenAI API 后，图片会自动生成详细描述：

```bash
uv run scripts/to-md.py screenshot.png
```

输出示例：

```markdown
![Screenshot](screenshot.png)

*图片描述：一个显示代码编辑器的屏幕截图，深色主题，左侧是文件浏览器，右侧是代码编辑区域...*
```

#### 3. 音频转录

```bash
uv run scripts/to-md.py recording.mp3
```

自动将音频转换为文字并保存为 Markdown。

## 从 Markdown 转换

### 支持的输出格式

| 格式 | 说明 |
|------|------|
| `docx` | Word 文档 |
| `pptx` | PowerPoint 演示文稿 |
| `pdf` | PDF 文档 |
| `html` | HTML 网页 |
| `odt` | OpenDocument 文本 |
| `latex` | LaTeX 源码 |

### 基本用法

```bash
uv run scripts/from-md.sh input.md docx
```

输出文件保存在输入文件同目录，扩展名自动更改。

### 中文 PDF 支持

使用 XeLaTeX 引擎和中文字体：

```bash
uv run scripts/from-md.sh paper.md pdf
```

脚本会自动使用 `xelatex` 和 `PingFang SC` 字体处理中文。

如需自定义字体，编辑 `scripts/from-md.sh`：

```bash
pandoc "$input" -o "$output" \
  --pdf-engine=xelatex \
  -V CJKmainfont="你的字体名称"
```

### Pandoc 高级选项

直接使用 Pandoc 获得更多控制：

```bash
# 自定义 PDF 样式
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V CJKmainfont="PingFang SC" \
  -V geometry:margin=2cm \
  --toc \
  --number-sections

# HTML 自定义样式
pandoc input.md -o output.html \
  --standalone \
  --css=style.css \
  --toc

# PPTX 自定义主题
pandoc input.md -o output.pptx \
  --reference-doc=theme.pptx
```

## 常见问题

### Q: 为什么不直接在 SKILL.md 中使用 Python 代码？

A: SKILL.md 是技能的入口文档，应该简洁明了。嵌入可执行的 Python 代码会导致 Claude 尝试直接运行 Python，而跳过 uv 的依赖管理。使用 `uv run scripts/to-md.py` 可以确保依赖正确安装。

### Q: 转换后的 Markdown 保存在哪里？

A: 默认保存在输入文件同目录，文件名相同但扩展名为 `.md`。例如：
- `~/Documents/report.pdf` → `~/Documents/report.md`

### Q: 如何批量转换多个文件？

A: 使用 shell 循环：

```bash
for file in ~/Documents/*.pdf; do
  uv run scripts/to-md.py "$file"
done
```

### Q: YouTube 字幕提取支持哪些语言？

A: 支持所有 YouTube 支持的自动字幕和手动字幕语言。

### Q: 图片描述功能必须用 OpenAI 吗？

A: 是的，目前仅支持 OpenAI API。你可以在 `config.yaml` 中配置自定义的 `base_url` 使用兼容的 API 服务。
