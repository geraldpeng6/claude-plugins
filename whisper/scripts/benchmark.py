#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10,<3.13"
# dependencies = [
#     "imageio-ffmpeg",
#     "pywhispercpp",
#     "mlx-whisper>=0.4",
# ]
# ///
"""Benchmark mlx-whisper vs whisper.cpp (pywhispercpp)."""

import subprocess
import sys
import tempfile
import time
from pathlib import Path

import imageio_ffmpeg  # type: ignore[import-untyped]

FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()


def extract_audio(video_path: str, output_path: str) -> bool:
    """Extract audio from video."""
    cmd = [FFMPEG_PATH, "-y", "-i", video_path, "-vn", "-acodec", "pcm_s16le",
           "-ar", "16000", "-ac", "1", output_path]
    return subprocess.run(cmd, capture_output=True).returncode == 0


def benchmark_mlx(audio_path: str) -> tuple[str, float]:
    """Benchmark mlx-whisper."""
    import mlx_whisper  # type: ignore[import-untyped]
    
    start = time.time()
    result = mlx_whisper.transcribe(
        audio_path,
        path_or_hf_repo="mlx-community/whisper-large-v3-mlx"
    )
    elapsed = time.time() - start
    return result["text"].strip(), elapsed


def benchmark_whispercpp(audio_path: str) -> tuple[str, float]:
    """Benchmark whisper.cpp via pywhispercpp."""
    from pywhispercpp.model import Model  # type: ignore[import-untyped]
    
    start = time.time()
    model = Model("large-v3", n_threads=8)
    segments = model.transcribe(audio_path)
    text = "".join(seg.text for seg in segments).strip()
    elapsed = time.time() - start
    return text, elapsed


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: benchmark.py <audio_or_video_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    
    # Extract audio if video
    if Path(input_file).suffix.lower() in {'.mp4', '.mkv', '.mov', '.avi', '.webm'}:
        print(f"Extracting audio from {input_file}...")
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            audio_path = f.name
        extract_audio(input_file, audio_path)
    else:
        audio_path = input_file

    print(f"\n=== Benchmarking: {input_file} ===\n")

    # MLX-Whisper
    print("Testing mlx-whisper (Apple Silicon)...")
    mlx_text, mlx_time = benchmark_mlx(audio_path)
    print(f"  Time: {mlx_time:.2f}s")
    print(f"  Text: {mlx_text[:100]}...")

    print()

    # whisper.cpp
    print("Testing whisper.cpp (CPU/Vulkan)...")
    cpp_text, cpp_time = benchmark_whispercpp(audio_path)
    print(f"  Time: {cpp_time:.2f}s")
    print(f"  Text: {cpp_text[:100]}...")

    print(f"\n=== Results ===")
    print(f"mlx-whisper:  {mlx_time:.2f}s")
    print(f"whisper.cpp:  {cpp_time:.2f}s")
    if mlx_time < cpp_time:
        print(f"Speedup: {cpp_time/mlx_time:.2f}x (mlx is faster)")
    else:
        print(f"Speedup: {mlx_time/cpp_time:.2f}x (whisper.cpp is faster)")


if __name__ == "__main__":
    main()
