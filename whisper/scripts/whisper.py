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

Backends:
- Apple Silicon: mlx-whisper (GPU accelerated via Metal)
- Other platforms: whisper.cpp via pywhispercpp (Vulkan/CPU)

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

# Detect platform and choose whisper backend
IS_APPLE_SILICON = (
    platform.system() == "Darwin" and platform.machine() in ("arm64", "arm")
)

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


def check_ffmpeg() -> bool:
    """Check if ffmpeg is available (using imageio-ffmpeg bundled)."""
    return True


def transcribe(
    audio_path: str,
    translate: bool = False,
    language: str | None = None,
    model: str | None = None,
) -> str:
    """Transcribe or translate audio file."""
    if IS_APPLE_SILICON:
        # Use mlx-whisper on Apple Silicon (faster)
        import mlx_whisper  # type: ignore[import-untyped]

        model_name = model or "mlx-community/whisper-large-v3-mlx"
        task = "translate" if translate else "transcribe"
        kwargs = {"path_or_hf_repo": model_name, "task": task}
        if language:
            kwargs["language"] = language
        result = mlx_whisper.transcribe(audio_path, **kwargs)
        return result["text"].strip()
    else:
        # Use whisper.cpp via pywhispercpp (Vulkan/CPU, cross-platform)
        from pywhispercpp.model import Model  # type: ignore[import-untyped]

        model_name = model or "large-v3"
        whisper_model = Model(model_name, n_threads=4)
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
    from http.server import BaseHTTPRequestHandler
    from http.server import HTTPServer

    if IS_APPLE_SILICON:
        import mlx_whisper  # type: ignore[import-untyped]
        from mlx_whisper import load_models  # type: ignore[import-untyped]

        model_name = model or "mlx-community/whisper-large-v3-mlx"
        print(f"加载模型: {model_name}", file=sys.stderr)
        load_models.load_model(model_name)
    else:
        from pywhispercpp.model import Model  # type: ignore[import-untyped]

        model_name = model or "large-v3"
        print(f"加载模型: {model_name} (whisper.cpp)", file=sys.stderr)
        # Model will be loaded on first request

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args: object) -> None:
            pass

        def do_POST(self) -> None:
            content_length = int(self.headers.get('Content-Length', 0))
            translate = self.headers.get('X-Translate', 'false').lower() == 'true'
            language = self.headers.get('X-Language', None)

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                f.write(self.rfile.read(content_length))
                temp_path = f.name

            try:
                if IS_APPLE_SILICON:
                    import mlx_whisper  # type: ignore[import-untyped]

                    task = "translate" if translate else "transcribe"
                    kwargs = {"path_or_hf_repo": model, "task": task}
                    if language:
                        kwargs["language"] = language
                    result = mlx_whisper.transcribe(temp_path, **kwargs)
                    text = result["text"].strip()
                else:
                    from pywhispercpp.model import Model  # type: ignore[import-untyped]

                    model_name = model or "large-v3"
                    whisper_model = Model(model_name, n_threads=4)
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
        description="音视频转文字 (mlx-whisper)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s audio.mp3              # 转录音频
  %(prog)s video.mp4              # 转录视频
  %(prog)s -t audio.mp3           # 翻译到英语
  %(prog)s --serve                # 启动服务
        """
    )
    parser.add_argument("file", nargs="?", help="音频或视频文件路径")
    parser.add_argument("-t", "--translate", action="store_true", help="翻译到英语")
    parser.add_argument("-l", "--language", help="源语言代码 (如: zh, ja, en)")
    parser.add_argument("-m", "--model", help="模型名称 (默认: 自动选择)")
    parser.add_argument("--serve", action="store_true", help="启动HTTP服务")
    parser.add_argument("--host", default="127.0.0.1", help="服务地址")
    parser.add_argument("--port", type=int, default=8765, help="服务端口")

    args = parser.parse_args()

    # Show platform info
    if IS_APPLE_SILICON:
        print("使用 mlx-whisper (Apple Silicon GPU)", file=sys.stderr)
    else:
        print(f"使用 whisper.cpp ({platform.system()})", file=sys.stderr)

    if args.serve:
        serve(args.host, args.port, args.model)
    elif args.file:
        if not Path(args.file).exists():
            print(f"错误: 文件不存在: {args.file}", file=sys.stderr)
            sys.exit(1)
        print(process_file(args.file, args.translate, args.language, args.model))
    else:
        if sys.stdin.isatty():
            parser.print_help()
            sys.exit(1)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(sys.stdin.buffer.read())
            temp_path = f.name
        try:
            print(transcribe(temp_path, args.translate, args.language, args.model))
        finally:
            Path(temp_path).unlink(missing_ok=True)


if __name__ == "__main__":
    main()
