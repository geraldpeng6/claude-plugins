---
description: 将流量文件(mitmproxy/HAR)转换为 OpenAPI 文档
argument-hint: "<flow_or_har_file> <api_prefix> [output_file]"
allowed-tools: ["Bash", "Read", "Glob", "Edit"]
---

# 转换流量为 OpenAPI

**重要：mitmproxy2swagger 可直接处理 HAR 文件和 mitmproxy flow 文件，无需任何转换脚本。**

## 步骤

### 1. 定位文件

如果用户未提供文件路径，搜索流量文件：
```bash
ls -la ./*.har ./captures/* ~/Downloads/*.har 2>/dev/null | head -20
```

### 2. 第一次转换

直接运行 mitmproxy2swagger：
```bash
mitmproxy2swagger -i <file> -o ./output/swagger.yaml -p <api_prefix>
```

### 3. 分析路径列表

读取生成的 yaml 文件的 `x-path-templates` 部分。

**分类展示给用户：**

| 类型 | 路径示例 | 建议 |
|------|----------|------|
| API端点 | `/api/...`, `/v1/...` | 文档化 |
| 静态资源 | `/_nuxt/...`, `/static/...` | 忽略 |

**询问用户**：哪些路径需要生成文档？

### 4. 编辑 yaml 文件

用 Edit 工具移除用户选择路径的 `ignore:` 前缀。

### 5. 第二次转换

```bash
mitmproxy2swagger -i <file> -o ./output/swagger.yaml -p <api_prefix> --examples
```

### 6. 输出 API 摘要

读取文档，输出端点列表、方法、数据结构。
