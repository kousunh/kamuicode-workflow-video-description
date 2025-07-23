#!/usr/bin/env python3
"""
Generic Gemini Analyzer for Videos and Images
Flexible tool for analyzing media files with custom prompts
"""

import os
import sys
import json
import base64
import mimetypes
import argparse
from pathlib import Path
import google.generativeai as genai

# Supported file types
VIDEO_EXTENSIONS = ('.mp4', '.avi', '.mov', '.mkv', '.webm')
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')

def get_file_size_mb(file_path):
    """Get file size in MB"""
    return os.path.getsize(file_path) / (1024 * 1024)

def encode_file_for_gemini(file_path):
    """Encode file (video or image) for Gemini API"""
    with open(file_path, 'rb') as file:
        file_data = file.read()
    return base64.b64encode(file_data).decode('utf-8')

def get_mime_type(file_path):
    """Get MIME type for file"""
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        ext = Path(file_path).suffix.lower()
        if ext in VIDEO_EXTENSIONS:
            mime_type = 'video/mp4'
        elif ext in IMAGE_EXTENSIONS:
            mime_type = 'image/jpeg'
        else:
            mime_type = 'application/octet-stream'
    return mime_type

def parse_gemini_response(response_text, output_format='json'):
    """Parse Gemini response based on expected format"""
    if output_format == 'json':
        try:
            # JSONブロックを探す
            if '```json' in response_text:
                start = response_text.find('```json') + 7
                end = response_text.find('```', start)
                json_str = response_text[start:end].strip()
            else:
                # JSON形式の部分を抽出
                start = response_text.find('{')
                if start == -1:
                    start = response_text.find('[')
                end = response_text.rfind('}')
                if end == -1:
                    end = response_text.rfind(']')
                end = end + 1
                json_str = response_text[start:end]
            
            return json.loads(json_str)
        except Exception as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Response text: {response_text[:500]}...")
            return None
    else:
        return response_text.strip()

def write_output(output_path, data, output_format='json'):
    """Write data to output file"""
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    
    if output_format == 'json' and not isinstance(data, str):
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    else:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(str(data))

def main():
    parser = argparse.ArgumentParser(
        description='Analyze videos or images using Google Gemini API',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('input', help='Input video or image file path')
    parser.add_argument('output', help='Output file path')
    parser.add_argument('api_key', help='Google Gemini API key')
    parser.add_argument('--prompt', help='Analysis prompt (direct text)')
    parser.add_argument('--prompt-file', help='File containing the analysis prompt')
    parser.add_argument('--format', choices=['json', 'text', 'markdown'], default='json',
                      help='Output format (default: json)')
    parser.add_argument('--model', default='gemini-1.5-flash',
                      help='Gemini model to use (default: gemini-1.5-flash)')
    
    args = parser.parse_args()
    
    # Get prompt
    if args.prompt:
        prompt = args.prompt
    elif args.prompt_file:
        if not os.path.exists(args.prompt_file):
            print(f"Error: Prompt file not found: {args.prompt_file}")
            sys.exit(1)
        with open(args.prompt_file, 'r', encoding='utf-8') as f:
            prompt = f.read().strip()
    else:
        print("Error: Either --prompt or --prompt-file must be specified")
        parser.print_help()
        sys.exit(1)
    
    # Check input file
    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)
    
    file_size_mb = get_file_size_mb(args.input)
    print(f"=== Gemini Analyzer ===")
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    print(f"Format: {args.format}")
    print(f"File size: {file_size_mb:.2f} MB")
    
    # Determine file type
    ext = Path(args.input).suffix.lower()
    is_video = ext in VIDEO_EXTENSIONS
    is_image = ext in IMAGE_EXTENSIONS
    
    if not (is_video or is_image):
        print(f"Error: Unsupported file type: {ext}")
        sys.exit(1)
    
    # Configure Gemini
    genai.configure(api_key=args.api_key)
    model = genai.GenerativeModel(args.model)
    
    # Encode media
    print(f"Encoding {'video' if is_video else 'image'} for analysis...")
    encoded_media = encode_file_for_gemini(args.input)
    mime_type = get_mime_type(args.input)
    
    # Generate content
    print("Sending request to Gemini API...")
    try:
        response = model.generate_content([
            {"mime_type": mime_type, "data": encoded_media},
            prompt
        ])
        
        # Parse response
        result = parse_gemini_response(response.text, args.format)
        if result is None and args.format == 'json':
            print("Warning: Failed to parse JSON, saving raw response")
            result = response.text
        
        # Write output
        write_output(args.output, result, args.format)
        print(f"✅ Analysis complete! Results saved to: {args.output}")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        
        # Write error information
        error_data = {
            "error": str(e),
            "status": "failed",
            "input": args.input,
            "prompt": prompt[:200] + "..." if len(prompt) > 200 else prompt
        }
        
        if args.format == 'json':
            write_output(args.output, error_data, args.format)
        else:
            write_output(args.output, f"Error: {e}", args.format)
        
        sys.exit(1)

if __name__ == "__main__":
    main()