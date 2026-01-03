#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = ["yt-dlp", "curl_cffi", "imageio-ffmpeg"]
# ///
"""
video-dl: Video download tool.

Usage:
    Download video: ./video-dl.py https://www.youtube.com/watch?v=xxx
    Subtitles only: ./video-dl.py -s https://www.youtube.com/watch?v=xxx
    Output dir: ./video-dl.py -o ~/Videos https://www.youtube.com/watch?v=xxx
"""

import argparse
import sys
from pathlib import Path

import imageio_ffmpeg  # type: ignore[import-untyped]
import yt_dlp  # type: ignore[import-untyped]

# Get ffmpeg path (using imageio-ffmpeg bundled ffmpeg)
FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()


def download_subs_only(url: str, output_dir: Path, langs: str) -> int:
    """Download subtitles only."""
    opts = {
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": langs.split(","),
        "ignoreerrors": True,
        "outtmpl": str(output_dir / "%(title)s.%(ext)s"),
        "ffmpeg_location": FFMPEG_PATH,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:  # type: ignore[arg-type]
        ydl.download([url])
    return 0


def download_video(url: str, output_dir: Path, langs: str) -> int:
    """Download video and subtitles."""
    opts = {
        "format": "bestvideo+bestaudio/best",
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": langs.split(","),
        "ignoreerrors": True,
        "outtmpl": str(output_dir / "%(title)s_%(height)sp.%(ext)s"),
        "ffmpeg_location": FFMPEG_PATH,
        "merge_output_format": "mp4",
        "postprocessors": [{"key": "FFmpegEmbedSubtitle"}],
    }
    with yt_dlp.YoutubeDL(opts) as ydl:  # type: ignore[arg-type]
        ydl.download([url])
    return 0


def main() -> int:
    """Entry point for video download CLI."""
    parser = argparse.ArgumentParser(
        description="Video download tool (yt-dlp)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s URL                    # Download video (best quality)
  %(prog)s -s URL                 # Subtitles only
  %(prog)s -o ~/Videos URL        # Output directory
  %(prog)s -l en,ja URL           # Subtitle languages
        """,
    )
    parser.add_argument("url", help="视频URL")
    parser.add_argument("-o", "--output", type=Path, default=Path.home() / "Downloads",
                        help="输出目录 (默认: ~/Downloads)")
    parser.add_argument("-s", "--subs", action="store_true",
                        help="仅下载字幕 (不下载视频)")
    parser.add_argument("-l", "--lang", default="zh-Hans,zh,en",
                        help="字幕语言 (逗号分隔, 默认: zh-Hans,zh,en)")

    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    if args.subs:
        return download_subs_only(args.url, args.output, args.lang)
    else:
        return download_video(args.url, args.output, args.lang)


if __name__ == "__main__":
    sys.exit(main())
