# mitm-analyzer

使用 mitmproxy 捕获流量并生成 OpenAPI 文档，用于逆向分析网站 API。

## 安装 uv

首先安装 uv (Python 包管理器)：

### macOS / Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## 安装依赖

所有平台统一使用 uv：

```bash
# 安装 mitmproxy 和 mitmproxy2swagger
uv tool install mitmproxy --python 3.12
uv tool install mitmproxy2swagger --python 3.12

# 安装 jq (可选，用于 JSON 处理)
# macOS: brew install jq
# Linux: sudo apt install jq
# Windows: scoop install jq
```

## 证书安装

首次使用运行命令自动安装：
```bash
/mitm-analyzer:install-cert
```

或手动安装：
- **macOS**: `sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain ~/.mitmproxy/mitmproxy-ca-cert.pem`
- **Linux**: `sudo cp ~/.mitmproxy/mitmproxy-ca-cert.pem /usr/local/share/ca-certificates/mitmproxy.crt && sudo update-ca-certificates`
- **Windows**: 双击 `%USERPROFILE%\.mitmproxy\mitmproxy-ca-cert.p12` 导入到"受信任的根证书颁发机构"

## 使用方法

```bash
# 1. 安装证书
/mitm-analyzer:install-cert

# 2. 启动捕获
/mitm-analyzer:capture

# 3. 配置代理 127.0.0.1:8080，访问目标网站

# 4. Ctrl+C 停止，然后转换
/mitm-analyzer:convert ./captures/flow_xxx https://api.example.com
```

## 命令

| 命令 | 说明 |
|------|------|
| `install-cert` | 安装 CA 证书 |
| `capture` | 启动流量捕获 |
| `convert` | 转换为 OpenAPI |

## License

MIT
