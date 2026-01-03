#!/bin/bash
# 将流量文件转换为 OpenAPI 规范

FLOW_FILE="$1"
API_PREFIX="$2"
OUTPUT_FILE="${3:-./output/swagger.yaml}"

if [ -z "$FLOW_FILE" ] || [ -z "$API_PREFIX" ]; then
    echo "用法: convert.sh <flow_file> <api_prefix> [output_file]"
    exit 1
fi

mkdir -p "$(dirname "$OUTPUT_FILE")"

echo "转换中..."
mitmproxy2swagger -i "$FLOW_FILE" -o "$OUTPUT_FILE" -p "$API_PREFIX" --examples

echo "完成: $OUTPUT_FILE"
