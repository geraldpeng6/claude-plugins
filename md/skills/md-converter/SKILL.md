# 文档转换指南

当用户需要将文档转换为 Markdown 或从 Markdown 转换为其他格式时，加载此技能。

## 快速开始

1. 转换为 MD：`/md:to-md <file_path>`
2. 从 MD 转换：`/md:from-md <file_path> <format>`

## 支持的格式

### 转换为 Markdown
- PDF → MD
- DOCX → MD
- XLSX → MD
- PPTX → MD
- HTML → MD
- LaTeX → MD
- YouTube 字幕 → MD
- 音频转录 → MD
- 图片描述 → MD (Groq Vision)
- OCR → MD

### 从 Markdown 转换
- MD → PDF
- MD → DOCX
- MD → HTML
- MD → LaTeX

## 使用示例

### 转换 PDF 到 Markdown
```
/md:to-md ./document.pdf
```

### 转换 Markdown 到 DOCX
```
/md:from-md ./document.md docx
```

### YouTube 字幕提取
```
/md:to-md https://youtube.com/watch?v=xxx
```

### 图片描述（需要 Groq API）
```
/md:to-md ./image.png --mode vision
```

## 配置

复制 `config.example.yaml` 为 `config.yaml` 并配置：
- `groq_api_key`: Groq API 密钥（用于图片描述和音频转录）

## 常见问题

### 缺少依赖
运行 `pip install markitdown` 安装核心依赖

### Groq API 错误
检查 config.yaml 中的 API 密钥是否正确
