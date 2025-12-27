# mitmproxy 使用指南

当用户询问如何使用 mitmproxy、配置代理、安装证书或分析 API 流量时，加载此技能。

## 快速开始

1. 安装证书：`/mitm-analyzer:install-cert`
2. 启动捕获：`/mitm-analyzer:capture`
3. 配置代理：127.0.0.1:8080
4. 访问目标网站
5. 停止捕获：Ctrl+C
6. 转换分析：`/mitm-analyzer:convert <flow_file> <api_prefix>`

## 代理配置

代理地址：`127.0.0.1:8080`

### macOS 系统代理
```
系统设置 → 网络 → Wi-Fi/以太网 → 详细信息 → 代理
→ 启用 "Web 代理 (HTTP)" 和 "安全 Web 代理 (HTTPS)"
→ 服务器：127.0.0.1  端口：8080
```

### Windows 系统代理
```
设置 → 网络和 Internet → 代理 → 手动设置代理
→ 使用代理服务器：开
→ 地址：127.0.0.1  端口：8080
```
或命令行临时设置：
```powershell
set HTTP_PROXY=http://127.0.0.1:8080
set HTTPS_PROXY=http://127.0.0.1:8080
```

### Linux 系统代理
环境变量方式（推荐）：
```bash
export http_proxy=http://127.0.0.1:8080
export https_proxy=http://127.0.0.1:8080
```
GNOME 桌面：设置 → 网络 → 网络代理 → 手动

### 浏览器代理（跨平台）
- **Firefox**：设置 → 网络设置 → 手动代理配置
- **Chrome**：使用系统代理，或安装 SwitchyOmega 扩展

## 常见问题

### 证书错误
运行 `/mitm-analyzer:install-cert` 安装证书

### 找不到流量文件
文件保存在 `./captures/` 目录

### API 前缀是什么
从捕获的请求 URL 中提取域名部分，如 `https://api.example.com`
