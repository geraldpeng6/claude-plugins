#!/bin/bash
# 将 Markdown 转换为其他格式
set -e

INPUT_FILE="$1"
FORMAT="$2"

if [ -z "$INPUT_FILE" ] || [ -z "$FORMAT" ]; then
    echo "用法: convert-from-md.sh <markdown文件> <目标格式>"
    echo "支持: docx, pptx, pdf, html, odt, latex"
    exit 1
fi

if ! command -v pandoc &> /dev/null; then
    echo "错误: 未安装 pandoc"
    echo "安装: brew install pandoc"
    exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
    echo "错误: 文件不存在 - $INPUT_FILE"
    exit 1
fi

case "$FORMAT" in
    docx|pptx|html|odt) ;;
    latex|tex) FORMAT="latex" ;;
    pdf)
        if ! command -v pdflatex &> /dev/null; then
            echo "⚠️  警告: PDF 转换需要 LaTeX"
            echo "安装: brew install --cask mactex-no-gui"
            echo "或先转 HTML 再打印为 PDF"
            exit 1
        fi
        ;;
    *)
        echo "错误: 不支持的格式 - $FORMAT"
        echo "支持: docx, pptx, pdf, html, odt, latex"
        exit 1
        ;;
esac

INPUT_DIR=$(dirname "$INPUT_FILE")
INPUT_NAME=$(basename "$INPUT_FILE" .md)
EXT="$FORMAT"
[ "$FORMAT" = "latex" ] && EXT="tex"
OUTPUT_FILE="${INPUT_DIR}/${INPUT_NAME}.${EXT}"

echo "转换中: $INPUT_FILE -> $OUTPUT_FILE"
if [ "$FORMAT" = "pdf" ]; then
    # 使用 xelatex 支持中文
    pandoc "$INPUT_FILE" -s -o "$OUTPUT_FILE" --pdf-engine=xelatex -V CJKmainfont="PingFang SC"
else
    pandoc "$INPUT_FILE" -s -o "$OUTPUT_FILE"
fi
echo "已保存到: $OUTPUT_FILE"
