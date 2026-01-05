---
name: whisper
description: 音视频转文字工具。使用 whisper.cpp 将音频或视频文件转录为文字。支持 Apple Silicon (Metal)、AMD/Intel (Vulkan) GPU 加速。
---

# 音视频转录

使用 whisper.cpp 将音频或视频文件转录为文字。

## 使用方法

**运行脚本前先查看帮助**：
```bash
uv run --script scripts/whisper.py --help
```

## 输出说明

**⚠️ 重要**: 转录结果直接输出到终端（stdout），不会自动保存文件。

如需保存结果，请使用重定向：
```bash
uv run --script scripts/whisper.py video.mp4 > output.txt
```

## 基本用法

```bash
# 转录音频（输出到终端）
uv run --script scripts/whisper.py audio.mp3

# 转录视频（自动提取音频）
uv run --script scripts/whisper.py video.mp4

# 指定源语言
uv run --script scripts/whisper.py -l zh audio.mp3

# 保存结果到文件
uv run --script scripts/whisper.py video.mp4 > transcript.txt
```

## 支持的格式

**音频**: mp3, wav, m4a, flac, ogg 等
**视频**: mp4, mkv, mov, avi, webm 等