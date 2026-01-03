#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "mlx-whisper>=0.4",
# ]
# ///
"""
whisper: 音视频转文字工具

用法:
    单次运行: ./whisper.py audio.mp3
    视频文件: ./whisper.py video.mp4
    翻译模式: ./whisper.py -t audio.mp3
    服务模式: ./whisper.py --serve
"""

import sys
import argparse
import json
import subprocess
import tempfile
from pathlib import Path

# 视频文件扩展名
VIDEO_EXTENSIONS = {'.mp4', '.mkv', '.mov', '.avi', '.webm', '.flv', '.wmv', '.m4v'}


def is_video_file(path: str) -> bool:
    """判断是否为视频文件"""
    return Path(path).suffix.lower() in VIDEO_EXTENSIONS


def extract_audio(video_path: str, output_path: str) -> bool:
    """使用 ffmpeg 提取音频"""
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vn", "-acodec", "pcm_s16le",
        "-ar", "16000", "-ac", "1",
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True)
    return result.returncode == 0


def check_ffmpeg() -> bool:
    """检查 ffmpeg 是否可用"""
    return subprocess.run(["which", "ffmpeg"], capture_output=True).returncode == 0


def transcribe(audio_path: str, translate: bool = False, language: str = None, 
               model: str = "mlx-community/whisper-large-v3-mlx") -> str:
    """转录或翻译音频文件"""
    import mlx_whisper
    
    task = "translate" if translate else "transcribe"
    kwargs = {"path_or_hf_repo": model, "task": task}
    if language:
        kwargs["language"] = language
    result = mlx_whisper.transcribe(audio_path, **kwargs)
    return result["text"].strip()


def process_file(file_path: str, translate: bool = False, language: str = None,
                 model: str = "mlx-community/whisper-large-v3-mlx") -> str:
    """处理音频或视频文件"""
    if is_video_file(file_path):
        if not check_ffmpeg():
            print("错误: 需要安装 ffmpeg", file=sys.stderr)
            sys.exit(1)
        
        print(f"检测到视频文件，提取音频: {file_path}", file=sys.stderr)
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


def serve(host: str = "127.0.0.1", port: int = 8765, model: str = "mlx-community/whisper-large-v3-mlx"):
    """启动HTTP服务"""
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import mlx_whisper
    from mlx_whisper import load_models
    
    # 预加载模型
    print(f"加载模型: {model}", file=sys.stderr)
    load_models.load_model(model)
    print(f"服务启动: http://{host}:{port}", file=sys.stderr)
    
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            pass
        
        def do_POST(self):
            content_length = int(self.headers.get('Content-Length', 0))
            translate = self.headers.get('X-Translate', 'false').lower() == 'true'
            language = self.headers.get('X-Language', None)
            
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                f.write(self.rfile.read(content_length))
                temp_path = f.name
            
            try:
                task = "translate" if translate else "transcribe"
                kwargs = {"path_or_hf_repo": model, "task": task}
                if language:
                    kwargs["language"] = language
                result = mlx_whisper.transcribe(temp_path, **kwargs)
                text = result["text"].strip()
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"text": text}).encode())
            finally:
                Path(temp_path).unlink(missing_ok=True)
    
    HTTPServer((host, port), Handler).serve_forever()


def main():
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
    parser.add_argument("-m", "--model", default="mlx-community/whisper-large-v3-mlx")
    parser.add_argument("--serve", action="store_true", help="启动HTTP服务")
    parser.add_argument("--host", default="127.0.0.1", help="服务地址")
    parser.add_argument("--port", type=int, default=8765, help="服务端口")
    
    args = parser.parse_args()
    
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
