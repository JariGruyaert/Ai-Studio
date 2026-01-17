# Knowledge Extraction Workflow

Simple, modular workflow for extracting web content into your knowledge base.

## Overview

**Trigger:** Raycast → **Extract:** Raw Text → **Process:** Clean & Format → **Save:** Knowledge Base

This workflow demonstrates the core pipeline pattern that will be used for all knowledge extraction.

## Components

### 1. Extract-to-Knowledge Script
**Location:** `scripts/extract-to-knowledge.py`

Two-stage pipeline:
1. **Stage 1: Raw Extraction** - Get content without modifications
2. **Stage 2: Processing** - Clean, structure, and format

**Features:**
- Extracts raw text from web URLs
- Cleans HTML artifacts
- Structures headings
- Adds YAML frontmatter with metadata
- Auto-generates filenames and directories
- Saves to knowledge base

### 2. Raycast Command
**Location:** `raycast/extract-url-to-knowledge.sh`

Raycast integration for quick access:
- Trigger from anywhere
- Pass URL and optional category
- View progress in real-time
- Get instant feedback

## Installation

### 1. Install Python Dependencies

```bash
cd ~/Ai-Studio/automation/scripts
pip install -r requirements.txt
```

Or install individually:
```bash
pip install requests beautifulsoup4
```

### 2. Install Raycast Command

**Option A: Import via Raycast**
1. Open Raycast
2. Go to Extensions → Script Commands
3. Click "+" → Add Script Directory
4. Select: `~/Ai-Studio/automation/raycast/`

**Option B: Manual Setup**
```bash
# Raycast will auto-discover scripts in this location
mkdir -p ~/.config/raycast/script-commands
ln -s ~/Ai-Studio/automation/raycast/extract-url-to-knowledge.sh \
      ~/.config/raycast/script-commands/
```

### 3. Verify Installation

Test the script directly:
```bash
cd ~/Ai-Studio
python3 automation/scripts/extract-to-knowledge.py \
  "https://docs.anthropic.com/en/api/getting-started" \
  --category claude-docs \
  --verbose
```

## Usage

### Via Raycast (Recommended)

1. Trigger Raycast (Cmd+Space or your hotkey)
2. Type: "Extract URL to Knowledge"
3. Enter URL
4. Optionally enter category
5. Press Enter
6. View progress and result

**Example:**
```
URL: https://docs.anthropic.com/en/api/messages
Category: claude-docs
```

Result: Saved to `knowledge/claude-docs/messages-api.md`

### Via Command Line

**Basic usage:**
```bash
python3 automation/scripts/extract-to-knowledge.py <url>
```

**With category:**
```bash
python3 automation/scripts/extract-to-knowledge.py \
  "https://example.com/article" \
  --category python-guides
```

**With custom filename:**
```bash
python3 automation/scripts/extract-to-knowledge.py \
  "https://example.com/article" \
  --category guides \
  --output custom-name.md
```

**Verbose output:**
```bash
python3 automation/scripts/extract-to-knowledge.py \
  "https://example.com/article" \
  --verbose
```

## How It Works

### Stage 1: Raw Extraction

```python
# Fetch URL
extractor = RawTextExtractor(url)
extractor.fetch()

# Extract raw text (no modifications)
raw_text = extractor.extract_raw()
```

**What happens:**
- Fetches HTML from URL
- Removes script, style, nav elements
- Extracts title and meta description
- Gets raw text while preserving structure
- Stores metadata (source, date, etc.)

### Stage 2: Processing & Formatting

```python
# Process and format
processor = MarkdownProcessor(raw_text, metadata)
markdown = processor.process()
```

**What happens:**
1. **Clean HTML artifacts**
   - Normalize whitespace
   - Fix HTML entities
   - Remove excessive line breaks

2. **Structure headings**
   - Detect potential headings
   - Apply markdown heading syntax
   - Maintain hierarchy

3. **Add metadata header**
   - YAML frontmatter
   - Title, source, date
   - Description and domain

### Output Format

```markdown
---
title: Getting Started with Claude API
source: https://docs.anthropic.com/api/getting-started
domain: docs.anthropic.com
extracted: 2024-01-17T10:30:00
description: Learn how to use the Claude API
---

# Getting Started with Claude API

[Content with structured headings and cleaned formatting...]
```

## Directory Structure

Extracted content is organized automatically:

```
knowledge/
├── claude-docs/           # Category: claude-docs
│   ├── getting-started.md
│   ├── messages-api.md
│   └── tool-use.md
├── python-guides/         # Category: python-guides
│   └── async-patterns.md
└── docs-anthropic-com/    # Auto-generated from domain
    └── content.md
```

**Rules:**
- If category specified → `knowledge/{category}/`
- If no category → `knowledge/{domain}/`
- Filenames auto-generated from title
- Duplicates get numeric suffix: `-1`, `-2`, etc.

## Examples

### Example 1: Claude Documentation

```bash
# Extract Claude API docs
python3 automation/scripts/extract-to-knowledge.py \
  "https://docs.anthropic.com/en/api/messages" \
  --category claude-docs \
  --verbose
```

**Output:**
```
[Stage 1] Extracting raw text...
  ✓ Extracted 12,450 characters
  ✓ Title: Messages API - Claude

[Stage 2] Processing and formatting...
  ✓ Cleaned HTML artifacts
  ✓ Structured headings
  ✓ Added metadata header

✓ Saved to: knowledge/claude-docs/messages-api-claude.md
  Title: Messages API - Claude
  Size: 13,200 characters
```

### Example 2: Python Tutorial

```bash
# Extract Python guide
python3 automation/scripts/extract-to-knowledge.py \
  "https://realpython.com/async-io-python/" \
  --category python-guides
```

Saved to: `knowledge/python-guides/async-io-python.md`

### Example 3: Research Article

```bash
# Extract article (no category)
python3 automation/scripts/extract-to-knowledge.py \
  "https://example.com/ai-research-2024"
```

Saved to: `knowledge/example-com/ai-research-2024.md`

## Customization

### Modify Processing Rules

Edit `scripts/extract-to-knowledge.py`:

```python
class MarkdownProcessor:
    def process(self) -> str:
        """Add your custom processing steps here"""
        cleaned = self.clean_html_artifacts()
        structured = self.structure_headings(cleaned)

        # Add custom processing:
        # structured = self.extract_code_blocks(structured)
        # structured = self.add_table_of_contents(structured)

        with_metadata = self.add_metadata_header(structured)
        return with_metadata
```

### Change Output Location

Modify `generate_filename()` function:

```python
# Change base path
base_path = Path.home() / "Documents" / "Knowledge"  # Instead of Ai-Studio
```

### Add Custom Metadata

Modify `add_metadata_header()`:

```python
frontmatter = f"""---
title: {self.metadata.get('title')}
source: {self.metadata['source_url']}
author: {self.metadata.get('author', 'Unknown')}
tags: {self.metadata.get('tags', [])}
---
"""
```

## Troubleshooting

### "Module not found: bs4"

Install dependencies:
```bash
pip install requests beautifulsoup4
```

### "Permission denied"

Make scripts executable:
```bash
chmod +x automation/scripts/extract-to-knowledge.py
chmod +x automation/raycast/extract-url-to-knowledge.sh
```

### "Raycast command not appearing"

1. Check script has correct metadata (see `@raycast.*` comments)
2. Restart Raycast
3. Check Raycast preferences → Extensions → Script Commands

### "SSL certificate error"

Add SSL verification bypass (not recommended for production):
```python
response = requests.get(url, verify=False)
```

## Next Steps

This simple workflow demonstrates the pipeline pattern. Future enhancements:

1. **Add more extractors**
   - PDF extractor
   - GitHub repository extractor
   - YouTube transcript extractor

2. **Enhanced processing**
   - Code block extraction
   - Table of contents generation
   - Link validation
   - Image downloading

3. **Enrichment**
   - Claude-powered summarization
   - Automatic tagging
   - Embedding generation
   - Relationship detection

4. **Integration**
   - Vector database storage
   - Search interface
   - Batch processing
   - Scheduled extraction

## Architecture Notes

This workflow validates the modular pipeline pattern:

```
Source → Parse → Process → Enrich → Store → Query
   ↓        ↓        ↓         ↓        ↓       ↓
WebFetch  HTML   Clean+    Metadata  Files  Search
         Parser  Format
```

**Key insights:**
- Clear separation of concerns (extract vs. process)
- Modular stages can be swapped/extended
- Configuration-driven (via CLI args now, YAML later)
- Metadata preserved throughout pipeline
- Output format is standardized (markdown + frontmatter)

This foundation supports building more complex pipelines while maintaining simplicity and debuggability.

## Related

- [Automation README](./README.md) - Full automation documentation
- [Scripts](./scripts/) - All automation scripts
- [Raycast Commands](./raycast/) - Raycast integrations
