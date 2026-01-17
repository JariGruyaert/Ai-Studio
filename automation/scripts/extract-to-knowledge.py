#!/usr/bin/env python3
"""
Extract content from URL to knowledge base

Simple two-stage pipeline:
1. Extract raw text from URL (no modifications)
2. Process and format into clean markdown with metadata

Usage:
    python extract-to-knowledge.py <url>
    python extract-to-knowledge.py <url> --category claude-docs
    python extract-to-knowledge.py <url> --output custom-name.md
"""

import os
import sys
import argparse
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from typing import Optional

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: Required packages not installed")
    print("Install with: pip install requests beautifulsoup4")
    sys.exit(1)


class RawTextExtractor:
    """
    Stage 1: Extract raw text from URL
    Goal: Get the content with minimal modification
    """

    def __init__(self, url: str):
        self.url = url
        self.raw_html = None
        self.raw_text = None
        self.metadata = {}

    def fetch(self) -> bool:
        """Fetch raw HTML from URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; KnowledgeExtractor/1.0)'
            }
            response = requests.get(self.url, headers=headers, timeout=30)
            response.raise_for_status()

            self.raw_html = response.text
            self.metadata['fetch_date'] = datetime.now().isoformat()
            self.metadata['source_url'] = self.url
            self.metadata['status_code'] = response.status_code

            return True
        except requests.RequestException as e:
            print(f"Error fetching URL: {e}", file=sys.stderr)
            return False

    def extract_raw(self) -> str:
        """
        Extract raw text content without modifications
        Preserves structure but removes HTML tags
        """
        if not self.raw_html:
            raise ValueError("No HTML to extract from. Call fetch() first.")

        soup = BeautifulSoup(self.raw_html, 'html.parser')

        # Remove script, style, and navigation elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()

        # Extract title
        title_tag = soup.find('title')
        self.metadata['title'] = title_tag.get_text().strip() if title_tag else 'Untitled'

        # Extract meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            self.metadata['description'] = meta_desc['content']

        # Get raw text - preserve basic structure
        self.raw_text = soup.get_text(separator='\n', strip=False)

        return self.raw_text


class MarkdownProcessor:
    """
    Stage 2: Process and format into clean markdown
    Goal: Clean, structure, and format for readability
    """

    def __init__(self, raw_text: str, metadata: dict):
        self.raw_text = raw_text
        self.metadata = metadata
        self.processed_text = None

    def clean_html_artifacts(self) -> str:
        """Remove HTML artifacts and normalize whitespace"""
        text = self.raw_text

        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)

        # Remove leading/trailing whitespace from lines
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(lines)

        # Remove empty lines at start and end
        text = text.strip()

        # Fix common HTML entity issues
        replacements = {
            '&nbsp;': ' ',
            '&amp;': '&',
            '&lt;': '<',
            '&gt;': '>',
            '&quot;': '"',
            '&#39;': "'",
        }
        for entity, char in replacements.items():
            text = text.replace(entity, char)

        return text

    def structure_headings(self, text: str) -> str:
        """
        Detect and format headings based on context
        This is a simple heuristic-based approach
        """
        lines = text.split('\n')
        structured_lines = []

        for i, line in enumerate(lines):
            line_stripped = line.strip()

            # Skip empty lines
            if not line_stripped:
                structured_lines.append('')
                continue

            # Detect potential headings (short lines, capitalized, etc.)
            is_short = len(line_stripped) < 80
            is_title_case = line_stripped[0].isupper() if line_stripped else False
            next_line_empty = i + 1 < len(lines) and not lines[i + 1].strip()

            # Simple heuristic: short, capitalized lines followed by empty line
            if is_short and is_title_case and next_line_empty and not line_stripped.endswith('.'):
                # Check if it's already a heading
                if not line_stripped.startswith('#'):
                    # Determine heading level (this is basic - can be improved)
                    if len(line_stripped) < 40 and line_stripped.isupper():
                        structured_lines.append(f"# {line_stripped}")
                    else:
                        structured_lines.append(f"## {line_stripped}")
                else:
                    structured_lines.append(line_stripped)
            else:
                structured_lines.append(line_stripped)

        return '\n'.join(structured_lines)

    def add_metadata_header(self, text: str) -> str:
        """Add YAML frontmatter with metadata"""
        # Parse domain for category
        domain = urlparse(self.metadata['source_url']).netloc

        frontmatter = f"""---
title: {self.metadata.get('title', 'Untitled')}
source: {self.metadata['source_url']}
domain: {domain}
extracted: {self.metadata['fetch_date']}
description: {self.metadata.get('description', 'No description available')}
---

"""
        return frontmatter + text

    def process(self) -> str:
        """Run full processing pipeline"""
        # Stage 1: Clean HTML artifacts
        cleaned = self.clean_html_artifacts()

        # Stage 2: Structure headings
        structured = self.structure_headings(cleaned)

        # Stage 3: Add metadata
        with_metadata = self.add_metadata_header(structured)

        self.processed_text = with_metadata
        return self.processed_text


def generate_filename(url: str, title: str, category: Optional[str] = None) -> Path:
    """
    Generate a good filename from URL and title
    """
    # Create slug from title
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[\s_-]+', '-', slug)
    slug = slug[:50]  # Limit length

    # Get domain for context
    domain = urlparse(url).netloc.replace('www.', '')

    # Base path
    base_path = Path.home() / "Ai-Studio" / "knowledge"

    # Add category subdirectory if specified
    if category:
        base_path = base_path / category
    else:
        # Use domain as category
        domain_clean = domain.replace('.', '-')
        base_path = base_path / domain_clean

    # Create directory if it doesn't exist
    base_path.mkdir(parents=True, exist_ok=True)

    # Generate filename
    filename = f"{slug}.md"
    filepath = base_path / filename

    # Handle duplicates
    counter = 1
    while filepath.exists():
        filename = f"{slug}-{counter}.md"
        filepath = base_path / filename
        counter += 1

    return filepath


def main():
    """Main workflow"""
    parser = argparse.ArgumentParser(
        description='Extract web content to knowledge base'
    )
    parser.add_argument(
        'url',
        help='URL to extract content from'
    )
    parser.add_argument(
        '-c', '--category',
        help='Category subdirectory (e.g., claude-docs, python-guides)'
    )
    parser.add_argument(
        '-o', '--output',
        help='Custom output filename (optional)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        print(f"Error: Invalid URL. Must start with http:// or https://")
        sys.exit(1)

    if args.verbose:
        print(f"Extracting content from: {args.url}")

    # Stage 1: Extract raw text
    if args.verbose:
        print("\n[Stage 1] Extracting raw text...")

    extractor = RawTextExtractor(args.url)

    if not extractor.fetch():
        sys.exit(1)

    raw_text = extractor.extract_raw()

    if args.verbose:
        print(f"  ✓ Extracted {len(raw_text)} characters")
        print(f"  ✓ Title: {extractor.metadata['title']}")

    # Stage 2: Process and format
    if args.verbose:
        print("\n[Stage 2] Processing and formatting...")

    processor = MarkdownProcessor(raw_text, extractor.metadata)
    markdown = processor.process()

    if args.verbose:
        print(f"  ✓ Cleaned HTML artifacts")
        print(f"  ✓ Structured headings")
        print(f"  ✓ Added metadata header")

    # Generate filename and save
    if args.output:
        # Custom filename
        if args.category:
            base_path = Path.home() / "Ai-Studio" / "knowledge" / args.category
            base_path.mkdir(parents=True, exist_ok=True)
            filepath = base_path / args.output
        else:
            filepath = Path.home() / "Ai-Studio" / "knowledge" / args.output
    else:
        # Auto-generate filename
        filepath = generate_filename(
            args.url,
            extractor.metadata['title'],
            args.category
        )

    # Save to file
    try:
        filepath.write_text(markdown, encoding='utf-8')

        # Success message
        relative_path = filepath.relative_to(Path.home() / "Ai-Studio")
        print(f"\n✓ Saved to: {relative_path}")
        print(f"  Title: {extractor.metadata['title']}")
        print(f"  Size: {len(markdown)} characters")

        return 0

    except Exception as e:
        print(f"Error saving file: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
