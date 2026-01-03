#!/bin/bash
# 启动 mitmproxy 捕获流量 (支持 macOS/Linux/Windows)

set -e

# ===== 系统检测 =====
detect_os() {
    case "$(uname -s)" in
        Darwin*) echo "macos" ;;
        Linux*)  echo "linux" ;;
        MINGW*|MSYS*|CYGWIN*) echo "windows" ;;
        *) echo "unknown" ;;
    esac
}

OS=$(detect_os)

# ===== 前置检查 =====
check_prerequisites() {
    echo "=== 环境检查 ==="

    # 检查 mitmproxy 是否安装
    if ! command -v mitmweb &> /dev/null; then
        echo "❌ mitmproxy 未安装"
        echo "   安装方法："
        case "$OS" in
            macos)   echo "   brew install mitmproxy" ;;
            linux)   echo "   pip install mitmproxy 或 apt install mitmproxy" ;;
            windows) echo "   pip install mitmproxy 或下载安装包" ;;
        esac
        exit 1
    fi
    echo "✓ mitmproxy 已安装"

    # 检查证书是否存在
    CERT_FILE="$HOME/.mitmproxy/mitmproxy-ca-cert.pem"
    if [ ! -f "$CERT_FILE" ]; then
        echo "⚠ CA 证书未生成，首次运行将自动生成"
    else
        echo "✓ CA 证书已存在"
    fi

    # 检查端口是否被占用
    if lsof -i :8080 &> /dev/null 2>&1 || netstat -an 2>/dev/null | grep -q ":8080.*LISTEN"; then
        echo "⚠ 端口 8080 可能被占用"
    else
        echo "✓ 端口 8080 可用"
    fi

    echo ""
}

# ===== 显示代理配置提示 =====
show_proxy_hint() {
    echo "=== 代理配置提示 ($OS) ==="
    case "$OS" in
        macos)
            echo "系统设置 → 网络 → Wi-Fi → 详细信息 → 代理"
            echo "→ 启用 HTTP/HTTPS 代理：127.0.0.1:8080"
            ;;
        linux)
            echo "设置环境变量："
            echo "  export http_proxy=http://127.0.0.1:8080"
            echo "  export https_proxy=http://127.0.0.1:8080"
            ;;
        windows)
            echo "设置 → 网络和 Internet → 代理 → 手动设置"
            echo "→ 地址：127.0.0.1  端口：8080"
            ;;
    esac
    echo ""
}

# ===== 主流程 =====
check_prerequisites
show_proxy_hint

OUTPUT_DIR="./captures"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="${1:-$OUTPUT_DIR/flow_$TIMESTAMP}"

mkdir -p "$OUTPUT_DIR"

echo "=== MitmProxy 流量捕获 ==="
echo "输出文件: $OUTPUT_FILE"
echo "Web界面: http://127.0.0.1:8081"
echo "代理地址: 127.0.0.1:8080"
echo "按 Ctrl+C 停止"
echo ""

mitmweb --save-stream-file "$OUTPUT_FILE"
