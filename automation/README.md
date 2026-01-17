# Automation

Daily workflow tools: scripts, Raycast AI presets, and terminal commands for productivity.

## 🚀 Quick Start: Knowledge Extraction Workflow

**New!** Extract web content to your knowledge base with one command.

```bash
# Via command line
python3 scripts/extract-to-knowledge.py "https://docs.anthropic.com/api" --category claude-docs

# Via Raycast (after setup)
# Cmd+Space → "Extract URL to Knowledge" → Enter URL
```

**See:** [WORKFLOW.md](./WORKFLOW.md) for complete documentation and setup instructions.

This workflow demonstrates the modular pipeline pattern used throughout the AI Infrastructure:
- **Extract** raw content without modification
- **Process** into clean, structured markdown
- **Save** to organized knowledge base with metadata

---

## Overview

This directory contains automation tools for:
- **scripts/** - Python/Bash scripts for repetitive tasks
- **raycast/** - Raycast AI presets, commands, and workflows
- **terminal/** - Shell aliases, functions, and commands

## Directory Structure

```
automation/
├── scripts/       # General automation scripts
├── raycast/       # Raycast AI presets and commands
└── terminal/      # Terminal aliases and functions
```

## Philosophy

Automate tasks you do more than twice. Make the computer work for you.

### When to Automate
✅ Repetitive data processing
✅ Common file operations
✅ Frequent API calls
✅ Standard text transformations
❌ One-time tasks
❌ Already-automated workflows

## Scripts

General-purpose automation scripts.

### Script Categories

**Data Processing**
- Text extraction and transformation
- File format conversion
- Batch processing

**API Integration**
- Claude API interactions
- External service integrations
- Data fetching

**Development Tools**
- Code generation
- Documentation generation
- Project setup

### Example: Text Processor

```python
# scripts/process_text.py
#!/usr/bin/env python3
"""
Process text files with various transformations
Usage: python process_text.py <input_file> <operation>
"""

import sys
from pathlib import Path

def clean_text(text: str) -> str:
    """Remove extra whitespace and normalize"""
    lines = [line.strip() for line in text.split('\n')]
    return '\n'.join(line for line in lines if line)

def extract_code_blocks(text: str) -> list:
    """Extract markdown code blocks"""
    blocks = []
    in_block = False
    current_block = []

    for line in text.split('\n'):
        if line.startswith('```'):
            if in_block:
                blocks.append('\n'.join(current_block))
                current_block = []
            in_block = not in_block
        elif in_block:
            current_block.append(line)

    return blocks

def summarize(text: str, max_lines: int = 10) -> str:
    """Create a summary of the text"""
    lines = text.split('\n')
    return '\n'.join(lines[:max_lines]) + f"\n... ({len(lines)} total lines)"

OPERATIONS = {
    'clean': clean_text,
    'extract-code': lambda t: '\n\n'.join(extract_code_blocks(t)),
    'summarize': summarize,
}

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: process_text.py <file> <operation>")
        print(f"Operations: {', '.join(OPERATIONS.keys())}")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    operation = sys.argv[2]

    if operation not in OPERATIONS:
        print(f"Unknown operation: {operation}")
        sys.exit(1)

    text = file_path.read_text()
    result = OPERATIONS[operation](text)
    print(result)
```

### Example: Claude API Script

```python
# scripts/claude_api.py
#!/usr/bin/env python3
"""
Quick Claude API interactions
Usage: python claude_api.py <prompt>
"""

import os
import sys
from anthropic import Anthropic

def query_claude(prompt: str, system: str = None) -> str:
    """Send prompt to Claude and return response"""
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    messages = [{"role": "user", "content": prompt}]

    kwargs = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 2000,
        "messages": messages
    }

    if system:
        kwargs["system"] = system

    response = client.messages.create(**kwargs)
    return response.content[0].text

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: claude_api.py <prompt> [system_prompt]")
        sys.exit(1)

    prompt = sys.argv[1]
    system = sys.argv[2] if len(sys.argv) > 2 else None

    response = query_claude(prompt, system)
    print(response)
```

### Script Template

```python
#!/usr/bin/env python3
"""
[Script Description]
Usage: python script_name.py [args]
"""

import argparse
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main(args):
    """Main script logic"""
    logger.info(f"Processing: {args.input}")

    try:
        # Your logic here
        result = process(args.input)
        logger.info(f"Success: {result}")
        return 0
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script description')
    parser.add_argument('input', help='Input file or data')
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    exit(main(args))
```

## Raycast Integration

Raycast AI presets and custom commands for quick access.

### AI Presets Structure

```
raycast/
├── presets/
│   ├── code-review.json
│   ├── summarize.json
│   ├── explain-code.json
│   └── generate-tests.json
├── commands/
│   ├── quick-search.sh
│   └── process-clipboard.sh
└── workflows/
    └── document-flow.json
```

### Example: Code Review Preset

```json
{
  "name": "Code Review",
  "description": "Review code for security, performance, and best practices",
  "prompt": "Review the following code:\n\n{selection}\n\nFocus on:\n- Security vulnerabilities\n- Performance issues\n- Best practices\n- Potential bugs\n\nProvide specific, actionable feedback.",
  "creativity": "medium",
  "model": "claude-3-5-sonnet"
}
```

### Example: Summarize Preset

```json
{
  "name": "Summarize Document",
  "description": "Create concise summary with key points",
  "prompt": "Summarize the following content:\n\n{selection}\n\nProvide:\n- 3-5 key points\n- Main conclusions\n- Action items (if any)\n\nBe concise and focus on what's most important.",
  "creativity": "low",
  "model": "claude-3-5-sonnet"
}
```

### Example: Explain Code Preset

```json
{
  "name": "Explain Code",
  "description": "Explain code in simple terms",
  "prompt": "Explain this code in simple terms:\n\n{selection}\n\nInclude:\n- What it does (high level)\n- How it works (key logic)\n- Important details\n- Potential gotchas\n\nUse clear, beginner-friendly language.",
  "creativity": "low",
  "model": "claude-3-5-sonnet"
}
```

### Raycast Script Command

```bash
#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Process Clipboard
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon 📋
# @raycast.argument1 { "type": "text", "placeholder": "Operation" }

# Documentation:
# @raycast.description Process clipboard content with various operations
# @raycast.author Your Name

# Get clipboard content
clipboard=$(pbpaste)

# Process based on operation
case "$1" in
  "clean")
    echo "$clipboard" | sed 's/[[:space:]]*$//' | sed '/^$/d'
    ;;
  "upper")
    echo "$clipboard" | tr '[:lower:]' '[:upper:]'
    ;;
  "lower")
    echo "$clipboard" | tr '[:upper:]' '[:lower:]'
    ;;
  *)
    echo "Unknown operation: $1"
    echo "Available: clean, upper, lower"
    ;;
esac
```

## Terminal Automation

Shell aliases, functions, and commands for efficiency.

### Bash/Zsh Aliases

```bash
# terminal/aliases.sh
# Source this file in your .bashrc or .zshrc

# Navigation
alias ai='cd ~/Ai-Studio'
alias prompts='cd ~/Ai-Studio/prompts'
alias agents='cd ~/Ai-Studio/agents'
alias pipes='cd ~/Ai-Studio/pipelines'

# Quick edits
alias edit-prompt='code ~/Ai-Studio/prompts'
alias edit-agent='code ~/Ai-Studio/agents'

# Git shortcuts
alias gs='git status'
alias ga='git add'
alias gc='git commit -m'
alias gp='git push'

# Python virtual env
alias venv='source venv/bin/activate'
alias venvc='python -m venv venv'

# Quick Claude API
alias claude='python ~/Ai-Studio/automation/scripts/claude_api.py'

# Pipeline shortcuts
alias extract='python ~/Ai-Studio/pipelines/extraction/run.py'
alias process='python ~/Ai-Studio/pipelines/processing/run.py'
```

### Bash Functions

```bash
# terminal/functions.sh
# Source this file in your .bashrc or .zshrc

# Quick note taking
note() {
    local note_file="$HOME/Ai-Studio/knowledge/quick-notes.md"
    echo "## $(date '+%Y-%m-%d %H:%M')" >> "$note_file"
    echo "$@" >> "$note_file"
    echo "" >> "$note_file"
    echo "Note saved to $note_file"
}

# Process files with Claude
process_with_claude() {
    if [ -z "$1" ]; then
        echo "Usage: process_with_claude <file> <instruction>"
        return 1
    fi

    local file="$1"
    local instruction="${2:-Summarize this content}"

    local content=$(cat "$file")
    local prompt="$instruction\n\n$content"

    python ~/Ai-Studio/automation/scripts/claude_api.py "$prompt"
}

# Quick search in knowledge base
ksearch() {
    if [ -z "$1" ]; then
        echo "Usage: ksearch <query>"
        return 1
    fi

    grep -r "$1" ~/Ai-Studio/knowledge/ \
        --include="*.md" \
        --color=always \
        -n \
        -C 2
}

# Create new agent
new_agent() {
    local name="$1"
    if [ -z "$name" ]; then
        echo "Usage: new_agent <agent-name>"
        return 1
    fi

    local config_file="$HOME/Ai-Studio/agents/configs/${name}.yaml"

    cat > "$config_file" << EOF
name: $name
description: Description of $name agent
created: $(date '+%Y-%m-%d')

system_prompt: |
  You are ${name}.
  Your role is to...

skills:
  - skill1
  - skill2

tools:
  - tool1

constraints:
  timeout: 300
  max_tokens: 4000
EOF

    echo "Created agent config: $config_file"
    code "$config_file"
}

# Run pipeline
run_pipeline() {
    local pipeline="${1:-document-pipeline}"
    python ~/Ai-Studio/pipelines/orchestrator.py \
        --config "~/Ai-Studio/pipelines/${pipeline}.yaml"
}

# Export notes to markdown
export_notes() {
    local output="${1:-notes-export.md}"
    local knowledge_dir="$HOME/Ai-Studio/knowledge"

    echo "# Knowledge Export" > "$output"
    echo "Generated: $(date)" >> "$output"
    echo "" >> "$output"

    find "$knowledge_dir" -name "*.md" -type f | while read file; do
        echo "## $(basename "$file" .md)" >> "$output"
        cat "$file" >> "$output"
        echo "" >> "$output"
        echo "---" >> "$output"
        echo "" >> "$output"
    done

    echo "Exported to $output"
}
```

### Terminal Workflow Examples

**Daily Startup**
```bash
# terminal/startup.sh
#!/bin/bash
# Run this at the start of each session

cd ~/Ai-Studio
echo "AI Studio - $(date)"
echo ""

# Show recent changes
echo "Recent changes:"
git log --oneline -5
echo ""

# Show pending tasks
if [ -f "tasks.md" ]; then
    echo "Pending tasks:"
    grep "- \[ \]" tasks.md
fi
```

**Batch Processing**
```bash
# terminal/batch_process.sh
#!/bin/bash
# Process multiple files

source_dir="${1:-./sources}"
output_dir="${2:-./output}"

mkdir -p "$output_dir"

for file in "$source_dir"/*; do
    echo "Processing: $(basename "$file")"
    python scripts/process_text.py "$file" clean > "$output_dir/$(basename "$file")"
done

echo "Processed $(ls -1 "$source_dir" | wc -l) files"
```

## Workflow Patterns

### Pattern: Quick Text Processing

1. Copy text to clipboard
2. Run Raycast command with preset
3. Get instant result
4. Paste or save

### Pattern: Document Pipeline

1. Drop documents in `pipelines/sources/`
2. Run: `run_pipeline document-pipeline`
3. Query results with vector search
4. Export findings

### Pattern: Knowledge Capture

1. Learn something new
2. Run: `note "Quick insight about..."`
3. Later: Expand in proper documentation
4. Cross-reference with `ksearch`

## Best Practices

### Scripts
- Make scripts executable: `chmod +x script.sh`
- Use shebangs: `#!/usr/bin/env python3`
- Add usage documentation
- Handle errors gracefully
- Log important steps

### Raycast Presets
- Name presets clearly
- Optimize creativity level per task
- Use consistent prompt structure
- Test before saving

### Terminal Functions
- Keep functions focused
- Provide usage help
- Use meaningful names
- Source from shell config

## Installation

### Setup Scripts

```bash
# terminal/setup.sh
#!/bin/bash
# Setup automation tools

echo "Setting up automation..."

# Make scripts executable
chmod +x scripts/*.py
chmod +x scripts/*.sh

# Source aliases and functions
cat >> ~/.zshrc << 'EOF'

# AI Studio Automation
source ~/Ai-Studio/automation/terminal/aliases.sh
source ~/Ai-Studio/automation/terminal/functions.sh
EOF

echo "Setup complete! Restart your terminal or run: source ~/.zshrc"
```

## Next Steps

1. Create your first automation script
2. Set up Raycast AI presets for common tasks
3. Add terminal aliases for frequent commands
4. Build workflows that combine multiple tools
5. Document what works in `../knowledge/best-practices/`

## References

- [Raycast Documentation](https://developers.raycast.com/)
- [Bash Scripting Guide](https://www.gnu.org/software/bash/manual/)
- [Python argparse](https://docs.python.org/3/library/argparse.html)
- Parent: [../README.md](../README.md)
