---
description: 将 Markdown 转换为其他格式 (docx/pptx/pdf/html/odt/latex)
argument-hint: "<markdown文件> <目标格式>"
allowed-tools: ["Bash", "Read", "Write"]
---

# 转换 Markdown 为其他格式

使用 Pandoc 将 Markdown 文件转换为指定格式。

## 步骤

### 1. 验证文件和格式
```bash
ls -la "$ARGUMENTS"
```

### 2. 执行转换
```bash
./scripts/from-md.sh $ARGUMENTS
```

### 3. 输出结果
显示生成的文件路径。
