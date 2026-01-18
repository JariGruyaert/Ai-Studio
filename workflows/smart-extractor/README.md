# Smart Content Extractor

Intelligently extract, process, and store content from a curated list of URLs with type-specific extraction.

## Status: Phase 1 Complete ✓

**Current Features:**
- ✅ Load and validate resources from JSON
- ✅ Detect resource types (GitHub, YouTube, Blog, Article)
- ✅ Extract content from web pages
- ✅ Save as organized markdown files
- ✅ Track processing status

**Coming in Future Phases:**
- ⏳ Type-specific extractors (GitHub, YouTube, Blog)
- ⏳ AI enrichment (summaries, tags, key points)
- ⏳ Configuration file support
- ⏳ Checkpoint/resume capability

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
# Process resources with default settings
python workflows/smart-extractor/main.py

# With custom input/output paths
python workflows/smart-extractor/main.py \
  --input data/resources-raw/resources-raw.json \
  --output knowledge

# With verbose logging
python workflows/smart-extractor/main.py --verbose

# Custom timeout
python workflows/smart-extractor/main.py --timeout 60
```

### Command-Line Options

```
-i, --input    Input JSON file with resources (default: data/resources-raw/resources-raw.json)
-o, --output   Output directory (default: knowledge)
-t, --timeout  HTTP timeout in seconds (default: 30)
-v, --verbose  Enable verbose logging
```

## Input Format

The input JSON should contain an array of resource objects:

```json
[
  {
    "url": "https://github.com/example/repo",
    "title": "Example Repository",
    "type": "GitHub Repo",
    "date": "2026-01-17",
    "device": "iPhone"
  }
]
```

Required fields:
- `url`: The resource URL (must start with http:// or https://)

Optional fields:
- `title`: Resource title
- `type`: Resource type hint
- All other fields are preserved but not used

## Output Structure

Extracted content is organized by type:

```
knowledge/
├── github-repos/
│   └── example-repository.md
├── youtube-videos/
│   └── video-title.md
├── blog-posts/
│   └── article-title.md
├── articles/
│   └── another-article.md
└── _processing-log.json
```

Each markdown file includes:
- YAML frontmatter with metadata
- Title and description
- Extracted content
- Metadata section with source info

## Processing Log

The `_processing-log.json` file tracks all processing attempts:

```json
{
  "last_updated": "2026-01-18T12:00:00",
  "total_processed": 20,
  "successful": 18,
  "failed": 2,
  "resources": [
    {
      "url": "https://example.com",
      "status": "completed",
      "processed_at": "2026-01-18T12:00:00",
      "output_file": "knowledge/articles/example.md",
      "error": null
    }
  ]
}
```

## Architecture

### Components

1. **ResourceLoader** (`core/loader.py`)
   - Loads resources from JSON
   - Validates structure
   - Removes duplicates

2. **TypeDetector** (`core/detector.py`)
   - Detects resource type from URL
   - Parses GitHub/YouTube URLs
   - Extracts metadata

3. **FallbackExtractor** (`extractors/fallback.py`)
   - Generic HTML extraction
   - BeautifulSoup-based parsing
   - Content cleaning

4. **StorageManager** (`core/storage.py`)
   - Generates filenames
   - Creates markdown files
   - Maintains processing log

5. **SmartExtractor** (`main.py`)
   - Orchestrates the workflow
   - Coordinates components
   - Handles errors and logging

### Data Flow

```
Input JSON
    ↓
ResourceLoader (load & validate)
    ↓
For each resource:
    ↓
TypeDetector (identify type)
    ↓
FallbackExtractor (extract content)
    ↓
StorageManager (save markdown)
    ↓
Processing Log (track status)
```

## Error Handling

The extractor handles various error conditions:

- **Invalid JSON**: Attempts multi-array parsing
- **Network errors**: Logs and continues with next resource
- **Missing content**: Validation fails, resource skipped
- **Duplicate URLs**: Removed during loading
- **Invalid URLs**: Validation fails, resource skipped

Failed resources are logged with error details in `_processing-log.json`.

## Development

### Project Structure

```
smart-extractor/
├── core/
│   ├── loader.py         # Resource loading & validation
│   ├── detector.py       # Type detection
│   └── storage.py        # Storage management
├── extractors/
│   ├── base.py           # Base extractor class
│   └── fallback.py       # Generic HTML extractor
├── utils/
│   └── ...               # Utility functions
├── tests/
│   └── ...               # Unit tests
├── main.py               # Main entry point
├── requirements.txt      # Dependencies
└── README.md             # This file
```

### Running Tests

```bash
# Run all tests
pytest workflows/smart-extractor/tests/

# With coverage
pytest --cov=workflows/smart-extractor workflows/smart-extractor/tests/
```

## Roadmap

### Phase 2: Type-Specific Extractors
- GitHub extractor with API integration
- YouTube metadata extraction
- Blog/article extraction with trafilatura
- Better content quality

### Phase 3: AI Enrichment
- Claude API integration
- Auto-generated summaries
- Key point extraction
- Automatic tagging

### Phase 4: Production Features
- Configuration file support
- Checkpoint/resume capability
- Incremental updates
- Better error recovery

## License

Part of the Ai-Studio project.
