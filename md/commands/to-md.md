---
description: 将文件转换为 Markdown 格式
argument-hint: "<文件路径>"
allowed-tools: ["Bash", "Read", "Write"]
---

# 转换文件为 Markdown

使用 markitdown 或 pandoc 将指定文件转换为 Markdown 格式。

## 步骤

### 1. 验证文件存在
```bash
ls -la "$ARGUMENTS"
```

### 2. 执行转换
```bash
./scripts/to-md.py "$ARGUMENTS"
```

### 3. 输出结果
显示生成的 Markdown 文件路径。
