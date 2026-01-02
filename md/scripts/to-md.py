#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "markitdown",
#     "openai",
#     "pyyaml",
#     "pydub",
#     "SpeechRecognition",
#     "youtube-transcript-api",
# ]
# ///
"""
将文件转换为 Markdown 格式
支持: PDF, DOCX, XLSX, PPTX, HTML, LaTeX, 图片, 音频 等
"""

import sys
from pathlib import Path
import yaml


def load_config():
    """加载配置文件"""
    script_dir = Path(__file__).parent.parent
    config_path = script_dir / "config.yaml"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}


def main():
    if len(sys.argv) < 2:
        print("用法: convert-to-md.py <文件路径或URL> [输出路径]")
        print("支持: PDF, DOCX, XLSX, PPTX, HTML, 音频, YouTube URL 等")
        sys.exit(1)

    input_source = sys.argv[1]
    is_url = input_source.startswith(('http://', 'https://'))
    
    if is_url:
        # URL 输入
        if len(sys.argv) >= 3:
            output_file = Path(sys.argv[2]).resolve()
        else:
            output_file = Path('./output.md').resolve()
    else:
        # 文件输入
        input_file = Path(input_source).resolve()
        if not input_file.exists():
            print(f"错误: 文件不存在 - {input_file}")
            sys.exit(1)
        if len(sys.argv) >= 3:
            output_file = Path(sys.argv[2]).resolve()
        else:
            output_file = input_file.with_suffix('.md')

    # LaTeX 文件使用 pandoc
    if not is_url and input_file.suffix.lower() in ['.tex', '.latex']:
        import subprocess
        result = subprocess.run(
            ['pandoc', str(input_file), '-o', str(output_file)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"错误: {result.stderr}")
            sys.exit(1)
    else:
        from markitdown import MarkItDown
        config = load_config()
        openai_config = config.get('openai', {})
        
        # 如果配置了 OpenAI，启用图片描述
        if openai_config.get('api_key'):
            from openai import OpenAI
            client = OpenAI(
                api_key=openai_config['api_key'],
                base_url=openai_config.get('base_url', 'https://api.openai.com/v1')
            )
            md = MarkItDown(
                llm_client=client,
                llm_model=openai_config.get('model', 'gpt-4o')
            )
        else:
            md = MarkItDown()
        
        # 获取自定义 prompt
        llm_prompt = openai_config.get('image_prompt')
        result = md.convert(input_source, llm_prompt=llm_prompt)
        output_file.write_text(result.text_content, encoding='utf-8')

    print(f"已保存到: {output_file}")


if __name__ == "__main__":
    main()
