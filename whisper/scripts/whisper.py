#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10,<3.13"
# dependencies = [
#     "imageio-ffmpeg",
#     "pywhispercpp",
# ]
# ///
"""
whisper: Audio/video transcription tool.

Backend: whisper.cpp via pywhispercpp
- Apple Silicon: Metal GPU acceleration
- AMD/Intel: Vulkan GPU acceleration
- All platforms: Optimized CPU fallback

Usage:
    Single run: ./whisper.py audio.mp3
    Video file: ./whisper.py video.mp4
    Translate: ./whisper.py -t audio.mp3
    Server mode: ./whisper.py --serve
"""

import argparse
import json
import platform
import subprocess
import sys
import tempfile
from pathlib import Path

import imageio_ffmpeg  # type: ignore[import-untyped]

# Get ffmpeg path (using imageio-ffmpeg bundled ffmpeg)
FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()

# 视频文件扩展名
VIDEO_EXTENSIONS = {'.mp4', '.mkv', '.mov', '.avi', '.webm', '.flv', '.wmv', '.m4v'}


def is_video_file(path: str) -> bool:
    """Check if file is a video file."""
    return Path(path).suffix.lower() in VIDEO_EXTENSIONS


def extract_audio(video_path: str, output_path: str) -> bool:
    """Extract audio from video using ffmpeg."""
    cmd = [
        FFMPEG_PATH, "-y", "-i", video_path,
        "-vn", "-acodec", "pcm_s16le",
        "-ar", "16000", "-ac", "1",
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True)
    return result.returncode == 0


def transcribe(
    audio_path: str,
    translate: bool = False,
    language: str | None = None,
    model: str | None = None,
) -> str:
    """Transcribe or translate audio file using whisper.cpp."""
    from pywhispercpp.model import Model  # type: ignore[import-untyped]

    model_name = model or "large-v3"
    whisper_model = Model(model_name, n_threads=8)
    segments = whisper_model.transcribe(
        audio_path,
        language=language if language else "",
    )
    return "".join(seg.text for seg in segments).strip()


def process_file(
    file_path: str,
    translate: bool = False,
    language: str | None = None,
    model: str | None = None,
) -> str:
    """Process audio or video file."""
    if is_video_file(file_path):
        print(f"检测到视频文件, 提取音频: {file_path}", file=sys.stderr)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            temp_audio = f.name

        if not extract_audio(file_path, temp_audio):
            print("错误: 音频提取失败", file=sys.stderr)
            sys.exit(1)

        try:
            return transcribe(temp_audio, translate, language, model)
        finally:
            Path(temp_audio).unlink(missing_ok=True)
    else:
        return transcribe(file_path, translate, language, model)


def serve(
    host: str = "127.0.0.1",
    port: int = 8765,
    model: str | None = None,
) -> None:
    """Start HTTP server for transcription."""
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from pywhispercpp.model import Model  # type: ignore[import-untyped]

    model_name = model or "large-v3"
    print(f"加载模型: {model_name} (whisper.cpp)", file=sys.stderr)
    whisper_model = Model(model_name, n_threads=8)
    print(f"服务启动: http://{host}:{port}", file=sys.stderr)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args: object) -> None:
            pass

        def do_POST(self) -> None:
            content_length = int(self.headers.get('Content-Length', 0))
            language = self.headers.get('X-Language', None)

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                f.write(self.rfile.read(content_length))
                temp_path = f.name

            try:
                segments = whisper_model.transcribe(
                    temp_path,
                    language=language if language else "",
                )
                text = "".join(seg.text for seg in segments).strip()

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"text": text}).encode())
            finally:
                Path(temp_path).unlink(missing_ok=True)

    HTTPServer((host, port), Handler).serve_forever()


def main() -> None:
    """Entry point for whisper CLI."""
    parser = argparse.ArgumentParser(
        description="音视频转文字 (whisper.cpp)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s audio.mp3              # 转录音频
  %(prog)s video.mp4              # 转录视频
  %(prog)s -l zh audio.mp3        # 指定语言
  %(prog)s --serve                # 启动服务
        """
    )
    parser.add_argument("file", nargs="?", help="音频或视频文件路径")
    parser.add_argument("-l", "--language", help="源语言代码 (如: zh, ja, en)")
    parser.add_argument("-m", "--model", default="large-v3", help="模型名称")
    parser.add_argument("--serve", action="store_true", help="启动HTTP服务")
    parser.add_argument("--host", default="127.0.0.1", help="服务地址")
    parser.add_argument("--port", type=int, default=8765, help="服务端口")

    args = parser.parse_args()

    # Show platform info
    print(f"使用 whisper.cpp ({platform.system()})", file=sys.stderr)

    if args.serve:
        serve(args.host, args.port, args.model)
    elif args.file:
        if not Path(args.file).exists():
            print(f"错误: 文件不存在: {args.file}", file=sys.stderr)
            sys.exit(1)
        print(process_file(args.file, False, args.language, args.model))
    else:
        if sys.stdin.isatty():
            parser.print_help()
            sys.exit(1)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(sys.stdin.buffer.read())
            temp_path = f.name
        try:
            print(transcribe(temp_path, False, args.language, args.model))
        finally:
            Path(temp_path).unlink(missing_ok=True)


if __name__ == "__main__":
    main()
