---
description: 启动 mitmproxy 捕获网站流量
argument-hint: "[output_name]"
allowed-tools: ["Bash"]
---

# 启动流量捕获

运行捕获脚本：

```bash
$PLUGIN_DIR/scripts/capture.sh $ARGUMENTS
```

告知用户：
1. 代理地址：127.0.0.1:8080
2. Web界面：http://127.0.0.1:8081
3. 配置浏览器代理后访问目标网站
4. 完成后按 Ctrl+C 停止
