#!/bin/bash
# Test script for knowledge extraction workflow

echo "🧪 Testing Knowledge Extraction Workflow"
echo "=========================================="
echo ""

# Check dependencies
echo "Checking dependencies..."
if ! python3 -c "import requests; import bs4" 2>/dev/null; then
    echo "❌ Missing dependencies"
    echo ""
    echo "Install with:"
    echo "  pip install -r requirements.txt"
    exit 1
fi
echo "✓ Dependencies installed"
echo ""

# Test with a simple example URL (using example.com as it's reliable)
echo "Testing extraction..."
echo "URL: http://example.com"
echo ""

python3 extract-to-knowledge.py \
    "http://example.com" \
    --category test \
    --verbose

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ Test passed!"
    echo ""
    echo "Check the output in: knowledge/test/"
    echo ""
    echo "Next steps:"
    echo "1. Try with a real documentation URL"
    echo "2. Install Raycast command for quick access"
    echo "3. Customize processing rules as needed"
else
    echo ""
    echo "=========================================="
    echo "❌ Test failed"
    echo ""
    echo "Check error messages above"
fi

exit $EXIT_CODE
