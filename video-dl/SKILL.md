---
name: video-dl
description: 视频下载工具。从 YouTube、Bilibili 等网站下载视频和字幕。支持自动合并最佳画质视频和音频，嵌入字幕。
---

# 视频下载

使用 yt-dlp 从 YouTube、Bilibili 等网站下载视频。

## 使用方法

**运行脚本前先查看帮助**：
```bash
uv run --script scripts/video-dl.py --help
```

## 基本用法

```bash
# 下载视频（最佳画质）
uv run --script scripts/video-dl.py https://www.youtube.com/watch?v=xxx

# 仅下载字幕
uv run --script scripts/video-dl.py -s https://www.youtube.com/watch?v=xxx

# 指定输出目录
uv run --script scripts/video-dl.py -o ~/Videos https://www.youtube.com/watch?v=xxx

# 指定字幕语言
uv run --script scripts/video-dl.py -l en,ja https://www.youtube.com/watch?v=xxx
```

## 支持的网站

| 网站 | 类型 | 备注 |
|------|------|------|
| YouTube | 视频 | ✅ 完全支持 |
| Bilibili | 视频 | ✅ 支持（4K/字幕需登录） |
| Twitter/X | 视频 | ✅ 支持 |
| Vimeo | 视频 | 部分需要登录 |
| TikTok | 短视频 | ✅ 支持 |
| Instagram | 视频/Reels | 需要登录 |
| Facebook | 视频 | 需要登录 |
| Twitch | 直播/VOD | ✅ 支持 |
| NicoNico | 视频 | 需要登录 |
| Dailymotion | 视频 | ✅ 支持 |

完整列表: [1800+ 网站](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)

## 依赖

- yt-dlp（uv run 自动安装）
- imageio-ffmpeg（uv run 自动安装，内置 ffmpeg 二进制）

**无需手动安装 ffmpeg**，脚本使用 `imageio-ffmpeg` 内置的 ffmpeg。
