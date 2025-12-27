#!/bin/bash
# 检查并安装 mitmproxy CA 证书 (支持 macOS/Linux)

CERT_DIR="$HOME/.mitmproxy"
CERT_FILE="$CERT_DIR/mitmproxy-ca-cert.pem"

# 检测操作系统
detect_os() {
    case "$(uname -s)" in
        Darwin*) echo "macos" ;;
        Linux*)  echo "linux" ;;
        MINGW*|MSYS*|CYGWIN*) echo "windows" ;;
        *) echo "unknown" ;;
    esac
}

OS=$(detect_os)

# 确保证书存在
if [ ! -f "$CERT_FILE" ]; then
    echo "生成 CA 证书..."
    mitmproxy --help > /dev/null 2>&1
    if [ ! -f "$CERT_FILE" ]; then
        echo "错误: 无法生成证书，请确保 mitmproxy 已安装"
        exit 1
    fi
fi

echo "检测到系统: $OS"

# macOS 安装
install_macos() {
    if security find-certificate -c "mitmproxy" /Library/Keychains/System.keychain > /dev/null 2>&1 || \
       security find-certificate -c "mitmproxy" ~/Library/Keychains/login.keychain-db > /dev/null 2>&1; then
        echo "证书已安装"
        return 0
    fi
    echo "安装证书 (需要管理员密码)..."
    sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain "$CERT_FILE"
}

# Linux 安装
install_linux() {
    if [ -f /usr/local/share/ca-certificates/mitmproxy.crt ]; then
        echo "证书已安装"
        return 0
    fi
    echo "安装证书 (需要 sudo)..."
    sudo cp "$CERT_FILE" /usr/local/share/ca-certificates/mitmproxy.crt
    sudo update-ca-certificates
}

# Windows 提示
install_windows() {
    echo "Windows 请手动安装:"
    echo "  1. 双击 $CERT_DIR/mitmproxy-ca-cert.p12"
    echo "  2. 导入到'受信任的根证书颁发机构'"
}

# 执行安装
case "$OS" in
    macos)   install_macos ;;
    linux)   install_linux ;;
    windows) install_windows ;;
    *)       echo "未知系统，请手动安装证书: $CERT_FILE" ;;
esac

echo "完成"
