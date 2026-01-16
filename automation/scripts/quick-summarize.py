#!/usr/bin/env python3
"""
Quick Summarize Script
Summarize text files or clipboard content using Claude

Usage:
    # Summarize a file
    python quick-summarize.py document.txt

    # Summarize from stdin
    cat document.txt | python quick-summarize.py

    # With custom instructions
    python quick-summarize.py document.txt --instruction "Extract key findings"
"""

import os
import sys
import argparse
from pathlib import Path

try:
    from anthropic import Anthropic
except ImportError:
    print("Error: anthropic package not installed")
    print("Install it with: pip install anthropic")
    sys.exit(1)


def summarize_text(text: str, instruction: str = None) -> str:
    """
    Summarize text using Claude

    Args:
        text: Text to summarize
        instruction: Optional custom instruction

    Returns:
        Summary text
    """
    api_key = os.getenv('ANTHROPIC_API_KEY')

    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY not found in environment. "
            "Please add it to config/settings/.env"
        )

    client = Anthropic(api_key=api_key)

    # Build prompt
    if instruction:
        prompt = f"{instruction}\n\n{text}"
    else:
        prompt = f"""
Summarize the following text concisely:

<text>
{text}
</text>

Provide:
- 3-5 key points
- Main conclusions
- Any action items

Be concise and focus on what's most important.
"""

    # Call Claude
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.content[0].text


def main():
    """Main script logic"""
    parser = argparse.ArgumentParser(
        description='Summarize text using Claude'
    )
    parser.add_argument(
        'file',
        nargs='?',
        help='File to summarize (optional, reads from stdin if not provided)'
    )
    parser.add_argument(
        '-i', '--instruction',
        help='Custom instruction for summarization'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file (prints to stdout if not provided)'
    )

    args = parser.parse_args()

    # Read input
    if args.file:
        # Read from file
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {args.file}")
            sys.exit(1)

        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        # Read from stdin
        if sys.stdin.isatty():
            print("Error: No input provided")
            print("Usage: quick-summarize.py <file> or pipe text to stdin")
            sys.exit(1)

        text = sys.stdin.read()

    # Check if text is empty
    if not text.strip():
        print("Error: Input text is empty")
        sys.exit(1)

    try:
        # Summarize
        print("Summarizing...", file=sys.stderr)
        summary = summarize_text(text, args.instruction)

        # Output
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(summary)
            print(f"Summary written to {args.output}", file=sys.stderr)
        else:
            print(summary)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
