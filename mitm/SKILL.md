---
name: mitm
description: mitmproxy 流量捕获与分析工具。用于捕获 HTTP/HTTPS 流量、安装证书、分析 API 接口。
---

# mitmproxy 使用指南

使用 mitmproxy 捕获和分析 HTTP/HTTPS 流量。

## 使用方法

```bash
# 安装证书
./scripts/install-cert.sh

# 启动捕获
./scripts/capture.sh

# 转换分析
./scripts/convert.sh <flow_file> <api_prefix>
```

## 代理配置

代理地址：`127.0.0.1:8080`

### macOS
```
系统设置 → 网络 → Wi-Fi → 代理
→ 启用 HTTP/HTTPS 代理
→ 服务器：127.0.0.1  端口：8080
```

### Linux
```bash
export http_proxy=http://127.0.0.1:8080
export https_proxy=http://127.0.0.1:8080
```

## 常见问题

### 证书错误
运行 `./scripts/install-cert.sh` 安装证书

### 找不到流量文件
文件保存在 `./captures/` 目录
