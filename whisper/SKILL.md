---
name: whisper
description: 音视频转文字工具。使用 mlx-whisper 将音频或视频文件转录为文字，支持翻译到英语。视频文件会自动提取音频后处理。适用于 Apple Silicon Mac。
---

# 音视频转录

使用 mlx-whisper 将音频或视频文件转录为文字。

## 使用方法

**运行脚本前先查看帮助**：
```bash
uv run --script scripts/whisper.py --help
```

## 基本用法

```bash
# 转录音频
uv run --script scripts/whisper.py audio.mp3

# 转录视频（自动提取音频）
uv run --script scripts/whisper.py video.mp4

# 翻译到英语
uv run --script scripts/whisper.py -t audio.mp3

# 指定源语言
uv run --script scripts/whisper.py -l zh audio.mp3
```

## 支持的格式

**音频**: mp3, wav, m4a, flac, ogg 等
**视频**: mp4, mkv, mov, avi, webm 等（需要 ffmpeg）

## 依赖

- mlx-whisper（uv run 自动安装）
- ffmpeg（视频处理需要，`brew install ffmpeg`）
