#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Extract URL to Knowledge
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon 📚
# @raycast.argument1 { "type": "text", "placeholder": "URL" }
# @raycast.argument2 { "type": "text", "placeholder": "Category (optional)", "optional": true }
# @raycast.packageName Knowledge Extraction

# Documentation:
# @raycast.description Extract content from URL and save to knowledge base
# @raycast.author Your Name

# Configuration
SCRIPT_PATH="$HOME/Ai-Studio/automation/scripts/extract-to-knowledge.py"
PYTHON_BIN="python3"

# Get arguments
URL="$1"
CATEGORY="${2:-}"

# Validate URL
if [ -z "$URL" ]; then
    echo "❌ Error: URL is required"
    echo ""
    echo "Usage: Extract URL to Knowledge <url> [category]"
    exit 1
fi

# Check if script exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "❌ Error: Extraction script not found"
    echo "Expected: $SCRIPT_PATH"
    exit 1
fi

# Run extraction
echo "📚 Extracting content from URL..."
echo "🔗 $URL"
echo ""

if [ -n "$CATEGORY" ]; then
    echo "📁 Category: $CATEGORY"
    echo ""
    "$PYTHON_BIN" "$SCRIPT_PATH" "$URL" --category "$CATEGORY" --verbose
else
    "$PYTHON_BIN" "$SCRIPT_PATH" "$URL" --verbose
fi

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✅ Extraction complete!"
else
    echo ""
    echo "❌ Extraction failed"
fi

exit $EXIT_CODE
