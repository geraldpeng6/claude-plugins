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

**默认行为**: 转录结果自动保存到输入文件同目录，文件名为 `输入文件名.txt`

例如：`video.mp4` → `video.txt`（保存在同一目录）

```bash
# 默认保存到同目录
uv run --script scripts/whisper.py video.mp4
# 输出: video.txt

# 指定输出路径
uv run --script scripts/whisper.py -o ~/output.txt video.mp4

# 输出到终端（不保存文件）
uv run --script scripts/whisper.py --stdout video.mp4
```

## 基本用法

```bash
# 转录音频（保存到 audio.txt）
uv run --script scripts/whisper.py audio.mp3

# 转录视频（保存到 video.txt）
uv run --script scripts/whisper.py video.mp4

# 指定源语言
uv run --script scripts/whisper.py -l zh audio.mp3

# 指定输出文件
uv run --script scripts/whisper.py -o result.txt video.mp4
```

## 支持的格式

**音频**: mp3, wav, m4a, flac, ogg 等
**视频**: mp4, mkv, mov, avi, webm 等