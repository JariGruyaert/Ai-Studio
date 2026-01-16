# Skills

Custom skills that agents can use to perform specific tasks. Skills are reusable, composable capabilities.

## What is a Skill?

A skill is a discrete capability that:
- Performs a specific function
- Has clear inputs and outputs
- Can be used by multiple agents
- Is testable independently

Think of skills as tools in an agent's toolbox.

## Skill Structure

```python
# Basic skill template
{
  "name": "skill_name",
  "description": "What this skill does",
  "input_schema": {
    "param1": "type",
    "param2": "type"
  },
  "output_schema": {
    "result": "type"
  },
  "implementation": "path/to/code"
}
```

## Skill Categories

### 1. Data Processing Skills
Transform, clean, or enrich data.

**Examples:**
- Text extraction
- Data validation
- Format conversion
- Normalization

### 2. Analysis Skills
Examine data and generate insights.

**Examples:**
- Sentiment analysis
- Entity extraction
- Pattern recognition
- Anomaly detection

### 3. Integration Skills
Connect to external systems.

**Examples:**
- API calls
- Database queries
- File system operations
- Web scraping

### 4. Generation Skills
Create new content.

**Examples:**
- Text generation
- Code generation
- Report creation
- Summary generation

## Creating a Skill

### Step 1: Define the Skill

```yaml
# text-extractor.yaml
name: text_extractor
version: 1.0.0
description: Extract text from various document formats

inputs:
  file_path:
    type: string
    required: true
    description: Path to the document

  format:
    type: string
    enum: [pdf, docx, txt, html]
    required: true

outputs:
  text:
    type: string
    description: Extracted text content

  metadata:
    type: object
    description: Document metadata (pages, author, etc.)

dependencies:
  - pypdf2
  - python-docx
  - beautifulsoup4
```

### Step 2: Implement the Skill

```python
# text-extractor.py
from typing import Dict, Any
import PyPDF2
from docx import Document
from bs4 import BeautifulSoup

class TextExtractor:
    """Extract text from various document formats"""

    def __init__(self):
        self.supported_formats = ['pdf', 'docx', 'txt', 'html']

    def execute(self, file_path: str, format: str) -> Dict[str, Any]:
        """
        Extract text from document

        Args:
            file_path: Path to document
            format: Document format (pdf, docx, txt, html)

        Returns:
            Dict with 'text' and 'metadata' keys
        """
        if format not in self.supported_formats:
            raise ValueError(f"Unsupported format: {format}")

        extractor = getattr(self, f"_extract_{format}")
        return extractor(file_path)

    def _extract_pdf(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()

            return {
                "text": text,
                "metadata": {
                    "pages": len(reader.pages),
                    "format": "pdf"
                }
            }

    def _extract_docx(self, file_path: str) -> Dict[str, Any]:
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])

        return {
            "text": text,
            "metadata": {
                "paragraphs": len(doc.paragraphs),
                "format": "docx"
            }
        }

    def _extract_txt(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        return {
            "text": text,
            "metadata": {
                "format": "txt"
            }
        }

    def _extract_html(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
            text = soup.get_text()

        return {
            "text": text,
            "metadata": {
                "format": "html"
            }
        }

# Usage
if __name__ == "__main__":
    extractor = TextExtractor()
    result = extractor.execute("document.pdf", "pdf")
    print(result["text"])
```

### Step 3: Test the Skill

```python
# test_text_extractor.py
import pytest
from text_extractor import TextExtractor

def test_pdf_extraction():
    extractor = TextExtractor()
    result = extractor.execute("test.pdf", "pdf")

    assert "text" in result
    assert "metadata" in result
    assert result["metadata"]["format"] == "pdf"
    assert isinstance(result["text"], str)

def test_unsupported_format():
    extractor = TextExtractor()

    with pytest.raises(ValueError):
        extractor.execute("test.xyz", "xyz")
```

## Skill Templates

### Template: Data Transformer

```python
# template-data-transformer.py
from typing import Dict, Any

class DataTransformer:
    """Transform data from one format to another"""

    def execute(self, data: Any, target_format: str) -> Dict[str, Any]:
        """
        Transform data to target format

        Args:
            data: Input data
            target_format: Desired output format

        Returns:
            Transformed data
        """
        transformer = self._get_transformer(target_format)

        return {
            "data": transformer(data),
            "format": target_format,
            "success": True
        }

    def _get_transformer(self, format: str):
        transformers = {
            "json": self._to_json,
            "csv": self._to_csv,
            "xml": self._to_xml
        }

        if format not in transformers:
            raise ValueError(f"Unsupported format: {format}")

        return transformers[format]

    def _to_json(self, data):
        import json
        return json.dumps(data, indent=2)

    def _to_csv(self, data):
        import csv
        import io

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()

    def _to_xml(self, data):
        # Implementation here
        pass
```

### Template: API Integration

```python
# template-api-integration.py
from typing import Dict, Any
import requests

class APIIntegration:
    """Generic API integration skill"""

    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()

        if api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {api_key}"
            })

    def execute(self, endpoint: str, method: str = "GET",
                data: Dict = None) -> Dict[str, Any]:
        """
        Make API request

        Args:
            endpoint: API endpoint
            method: HTTP method
            data: Request payload

        Returns:
            API response
        """
        url = f"{self.base_url}/{endpoint}"

        response = self.session.request(
            method=method,
            url=url,
            json=data
        )

        response.raise_for_status()

        return {
            "data": response.json(),
            "status_code": response.status_code,
            "success": True
        }
```

### Template: Validator

```python
# template-validator.py
from typing import Dict, Any, List

class Validator:
    """Validate data against a schema"""

    def __init__(self, schema: Dict[str, Any]):
        self.schema = schema

    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate data against schema

        Args:
            data: Data to validate

        Returns:
            Validation result with errors if any
        """
        errors = []

        for field, rules in self.schema.items():
            # Check required fields
            if rules.get("required") and field not in data:
                errors.append(f"Missing required field: {field}")
                continue

            if field not in data:
                continue

            # Check type
            expected_type = rules.get("type")
            if expected_type and not isinstance(data[field],
                                               self._get_type(expected_type)):
                errors.append(f"Invalid type for {field}: expected {expected_type}")

            # Check enum values
            if "enum" in rules and data[field] not in rules["enum"]:
                errors.append(f"Invalid value for {field}: must be one of {rules['enum']}")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "data": data if len(errors) == 0 else None
        }

    def _get_type(self, type_name: str):
        type_map = {
            "string": str,
            "number": (int, float),
            "boolean": bool,
            "object": dict,
            "array": list
        }
        return type_map.get(type_name, str)
```

## Skill Composition

Skills can be combined to create more complex capabilities:

```python
# Skill composition example
class DocumentProcessor:
    """Composite skill using multiple skills"""

    def __init__(self):
        self.extractor = TextExtractor()
        self.transformer = DataTransformer()
        self.validator = Validator(schema={
            "text": {"type": "string", "required": True},
            "format": {"type": "string", "required": True}
        })

    def execute(self, file_path: str, format: str) -> Dict[str, Any]:
        # Step 1: Extract
        extracted = self.extractor.execute(file_path, format)

        # Step 2: Validate
        validated = self.validator.execute(extracted)

        if not validated["valid"]:
            return {"success": False, "errors": validated["errors"]}

        # Step 3: Transform
        transformed = self.transformer.execute(
            validated["data"],
            "json"
        )

        return {
            "success": True,
            "result": transformed
        }
```

## Best Practices

### 1. Single Responsibility
Each skill should do one thing well.

❌ `process_and_analyze_and_store_data`
✅ `process_data`, `analyze_data`, `store_data`

### 2. Clear Interfaces
Define explicit input and output schemas.

```python
# Good: Clear schema
def execute(self, text: str, language: str) -> Dict[str, Any]:
    """
    Args:
        text: Input text to analyze
        language: Language code (en, es, fr, etc.)

    Returns:
        {
            "sentiment": float,  # -1.0 to 1.0
            "confidence": float, # 0.0 to 1.0
            "language": str
        }
    """
```

### 3. Error Handling
Gracefully handle errors and provide useful messages.

```python
try:
    result = process(data)
except ValidationError as e:
    return {
        "success": False,
        "error": str(e),
        "error_type": "validation"
    }
except Exception as e:
    return {
        "success": False,
        "error": "Unexpected error occurred",
        "error_type": "internal"
    }
```

### 4. Testability
Write skills that are easy to test.

```python
# Good: Testable skill
class Skill:
    def __init__(self, config: Dict = None):
        self.config = config or {}

    def execute(self, input_data):
        # No hidden dependencies, easy to mock
        return self._process(input_data)
```

### 5. Documentation
Document purpose, inputs, outputs, and examples.

## Skill Registry

Consider maintaining a registry of available skills:

```yaml
# skill-registry.yaml
skills:
  - name: text_extractor
    version: 1.0.0
    category: data_processing
    path: ./text-extractor.py

  - name: sentiment_analyzer
    version: 1.0.0
    category: analysis
    path: ./sentiment-analyzer.py

  - name: json_transformer
    version: 1.0.0
    category: transformation
    path: ./json-transformer.py
```

## Next Steps

1. Start with a simple skill (e.g., text extractor)
2. Test it independently
3. Integrate it into an agent (see `../configs/`)
4. Document patterns that work in `../../knowledge/patterns/`
5. Build more complex skills by composing simpler ones

## References

- [Claude Tool Use](https://docs.anthropic.com/claude/docs/tool-use)
- [Building Custom Tools](https://docs.anthropic.com/claude/docs/building-tools)
- Parent: [../README.md](../README.md)
