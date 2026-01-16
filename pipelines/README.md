# Pipelines

Data pipelines for text extraction and knowledge creation. Transform raw sources into structured knowledge.

## Overview

This directory contains pipelines for:
- Extracting text from various sources (PDFs, websites, APIs)
- Processing and enriching extracted data
- Ingesting into knowledge bases
- Managing source materials

## Pipeline Architecture

```
sources/ → extraction/ → processing/ → ingestion/ → Knowledge Base
   ↓           ↓            ↓             ↓
  Raw      Extracted    Structured    Stored &
  Data       Text         Data       Searchable
```

## Directory Structure

```
pipelines/
├── extraction/      # Pull text from PDFs, websites, APIs
├── processing/      # Clean, chunk, embed, enrich
├── ingestion/       # Load into vector DBs, knowledge graphs
└── sources/         # Raw input data/documents
```

## Core Pipeline Pattern

### 1. Source → Extract
Get text from raw materials:
- PDFs → text + metadata
- Websites → content + links
- APIs → structured data
- Documents → extracted content

### 2. Extract → Process
Transform and enrich:
- Clean and normalize
- Chunk into manageable pieces
- Generate embeddings
- Extract entities and relationships
- Add metadata

### 3. Process → Ingest
Store for retrieval:
- Vector databases (semantic search)
- Knowledge graphs (relationships)
- Traditional databases (structured queries)
- File systems (versioned storage)

## Example Pipeline: Document Knowledge Base

### Pipeline Definition

```yaml
# pipelines/extraction/document-pipeline.yaml
name: document-knowledge-pipeline
description: Extract and process documents into searchable knowledge base

stages:
  - name: extract
    input: sources/
    output: extraction/output/
    config:
      formats: [pdf, docx, html, md]
      preserve_structure: true
      extract_metadata: true

  - name: process
    input: extraction/output/
    output: processing/output/
    config:
      chunk_size: 1000
      overlap: 200
      embedding_model: text-embedding-3-small
      extract_entities: true

  - name: ingest
    input: processing/output/
    output: vector_db
    config:
      db_type: chromadb
      collection: documents
      metadata_fields: [source, date, author, tags]
```

### Implementation

```python
# pipelines/extraction/document_pipeline.py
from pathlib import Path
from typing import List, Dict, Any
import chromadb

class DocumentKnowledgePipeline:
    """End-to-end pipeline for document knowledge extraction"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.extractor = DocumentExtractor()
        self.processor = TextProcessor()
        self.ingestor = VectorDBIngestor()

    def run(self, source_dir: str) -> Dict[str, Any]:
        """
        Run complete pipeline

        Args:
            source_dir: Directory containing source documents

        Returns:
            Pipeline results and statistics
        """
        results = {
            "extracted": 0,
            "processed": 0,
            "ingested": 0,
            "errors": []
        }

        # Stage 1: Extract
        documents = self.extract_documents(source_dir)
        results["extracted"] = len(documents)

        # Stage 2: Process
        chunks = self.process_documents(documents)
        results["processed"] = len(chunks)

        # Stage 3: Ingest
        ingested = self.ingest_chunks(chunks)
        results["ingested"] = ingested

        return results

    def extract_documents(self, source_dir: str) -> List[Dict]:
        """Extract text from all documents in directory"""
        documents = []
        source_path = Path(source_dir)

        for file_path in source_path.rglob("*"):
            if file_path.suffix in ['.pdf', '.docx', '.html', '.md']:
                try:
                    doc = self.extractor.extract(file_path)
                    documents.append(doc)
                except Exception as e:
                    print(f"Error extracting {file_path}: {e}")

        return documents

    def process_documents(self, documents: List[Dict]) -> List[Dict]:
        """Process documents into chunks with embeddings"""
        chunks = []

        for doc in documents:
            try:
                doc_chunks = self.processor.process(
                    text=doc["text"],
                    metadata=doc["metadata"],
                    chunk_size=self.config.get("chunk_size", 1000),
                    overlap=self.config.get("overlap", 200)
                )
                chunks.extend(doc_chunks)
            except Exception as e:
                print(f"Error processing document: {e}")

        return chunks

    def ingest_chunks(self, chunks: List[Dict]) -> int:
        """Ingest chunks into vector database"""
        return self.ingestor.ingest(
            chunks=chunks,
            collection=self.config.get("collection", "documents")
        )
```

## Extraction Patterns

### PDF Extraction

```python
# pipelines/extraction/pdf_extractor.py
import PyPDF2
from pathlib import Path

class PDFExtractor:
    """Extract text and metadata from PDFs"""

    def extract(self, file_path: Path) -> dict:
        """
        Extract content from PDF

        Returns:
            {
                "text": "extracted text",
                "metadata": {
                    "pages": 10,
                    "author": "...",
                    "title": "...",
                    "created_date": "..."
                }
            }
        """
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)

            # Extract text
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"

            # Extract metadata
            metadata = {
                "pages": len(reader.pages),
                "source_file": str(file_path),
                "format": "pdf"
            }

            # Add PDF metadata if available
            if reader.metadata:
                metadata.update({
                    "author": reader.metadata.get('/Author', ''),
                    "title": reader.metadata.get('/Title', ''),
                    "created_date": reader.metadata.get('/CreationDate', '')
                })

            return {
                "text": text,
                "metadata": metadata
            }
```

### Web Extraction

```python
# pipelines/extraction/web_extractor.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class WebExtractor:
    """Extract content from web pages"""

    def extract(self, url: str) -> dict:
        """
        Extract content from URL

        Returns:
            {
                "text": "page content",
                "metadata": {
                    "url": "...",
                    "title": "...",
                    "links": [...]
                }
            }
        """
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract main content
        # Remove scripts, styles, etc.
        for tag in soup(['script', 'style', 'nav', 'footer']):
            tag.decompose()

        text = soup.get_text(separator='\n', strip=True)

        # Extract links
        links = [
            urljoin(url, a['href'])
            for a in soup.find_all('a', href=True)
        ]

        # Extract metadata
        title = soup.find('title')
        title_text = title.string if title else ''

        return {
            "text": text,
            "metadata": {
                "url": url,
                "title": title_text,
                "links": links,
                "format": "html"
            }
        }
```

## Processing Patterns

### Text Chunking

```python
# pipelines/processing/chunker.py
from typing import List, Dict

class TextChunker:
    """Split text into overlapping chunks"""

    def chunk(self, text: str, chunk_size: int = 1000,
              overlap: int = 200) -> List[str]:
        """
        Split text into chunks with overlap

        Args:
            text: Text to chunk
            chunk_size: Target size of each chunk
            overlap: Overlap between chunks

        Returns:
            List of text chunks
        """
        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]

            # Try to break at sentence boundary
            if end < len(text):
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)

                if break_point > chunk_size * 0.8:  # If we found a good break
                    chunk = text[start:start + break_point + 1]
                    end = start + break_point + 1

            chunks.append(chunk.strip())
            start = end - overlap

        return chunks
```

### Entity Extraction

```python
# pipelines/processing/entity_extractor.py
from anthropic import Anthropic

class EntityExtractor:
    """Extract entities and relationships from text"""

    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)

    def extract(self, text: str) -> Dict:
        """
        Extract entities from text

        Returns:
            {
                "entities": [
                    {"text": "...", "type": "PERSON", "relevance": 0.9}
                ],
                "relationships": [
                    {"source": "...", "target": "...", "type": "..."}
                ]
            }
        """
        prompt = f"""
Extract entities and relationships from the following text.

<text>
{text}
</text>

Return a JSON object with:
- entities: list of {{text, type, relevance}}
- relationships: list of {{source, target, type}}

Entity types: PERSON, ORGANIZATION, LOCATION, DATE, CONCEPT, TECHNOLOGY

<output_format>
{{
  "entities": [...],
  "relationships": [...]
}}
</output_format>
"""

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        import json
        return json.loads(response.content[0].text)
```

### Embedding Generation

```python
# pipelines/processing/embedder.py
import openai
from typing import List

class Embedder:
    """Generate embeddings for text chunks"""

    def __init__(self, api_key: str, model: str = "text-embedding-3-small"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for text chunks

        Args:
            texts: List of text chunks

        Returns:
            List of embedding vectors
        """
        response = self.client.embeddings.create(
            input=texts,
            model=self.model
        )

        return [item.embedding for item in response.data]

    def embed_with_metadata(self, chunks: List[Dict]) -> List[Dict]:
        """
        Add embeddings to chunks with metadata

        Args:
            chunks: List of {text, metadata} dicts

        Returns:
            List of {text, metadata, embedding} dicts
        """
        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.embed(texts)

        for chunk, embedding in zip(chunks, embeddings):
            chunk["embedding"] = embedding

        return chunks
```

## Ingestion Patterns

### Vector Database

```python
# pipelines/ingestion/vector_db.py
import chromadb
from typing import List, Dict

class VectorDBIngestor:
    """Ingest chunks into vector database"""

    def __init__(self, db_path: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=db_path)

    def ingest(self, chunks: List[Dict], collection: str = "documents") -> int:
        """
        Ingest chunks into collection

        Args:
            chunks: List of {text, metadata, embedding} dicts
            collection: Collection name

        Returns:
            Number of chunks ingested
        """
        coll = self.client.get_or_create_collection(name=collection)

        # Prepare data
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        documents = [chunk["text"] for chunk in chunks]
        embeddings = [chunk["embedding"] for chunk in chunks]
        metadatas = [chunk["metadata"] for chunk in chunks]

        # Add to collection
        coll.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

        return len(chunks)

    def query(self, query_embedding: List[float],
              collection: str = "documents",
              n_results: int = 5) -> List[Dict]:
        """Query vector database"""
        coll = self.client.get_collection(name=collection)

        results = coll.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        return results
```

## Pipeline Orchestration

```python
# pipelines/orchestrator.py
from typing import Dict, Any
import yaml

class PipelineOrchestrator:
    """Orchestrate multi-stage pipelines"""

    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

    def run(self) -> Dict[str, Any]:
        """Run pipeline stages in sequence"""
        results = {}

        for stage in self.config['stages']:
            print(f"Running stage: {stage['name']}")

            stage_func = getattr(self, f"run_{stage['name']}")
            stage_results = stage_func(stage)

            results[stage['name']] = stage_results

        return results

    # Implement stage runners
    def run_extract(self, stage_config):
        # Extract implementation
        pass

    def run_process(self, stage_config):
        # Process implementation
        pass

    def run_ingest(self, stage_config):
        # Ingest implementation
        pass
```

## Best Practices

### 1. Idempotency
Pipelines should produce the same output given the same input.

### 2. Resumability
Track progress and allow pipelines to resume from failures.

### 3. Monitoring
Log key metrics:
- Documents processed
- Errors encountered
- Processing time
- Data quality metrics

### 4. Error Handling
Gracefully handle failures without stopping the entire pipeline.

```python
# Continue on error pattern
for item in items:
    try:
        process(item)
    except Exception as e:
        log_error(e, item)
        continue  # Don't stop pipeline
```

### 5. Testing
Test each stage independently before integration.

## Source Management

### Organizing Sources

```
sources/
├── documents/
│   ├── pdfs/
│   ├── word/
│   └── markdown/
├── web/
│   ├── scraped/
│   └── apis/
└── metadata/
    └── source-registry.yaml
```

### Source Registry

```yaml
# sources/metadata/source-registry.yaml
sources:
  - id: source_001
    type: pdf
    path: documents/pdfs/report-2024.pdf
    added: 2026-01-16
    status: processed
    tags: [report, 2024]

  - id: source_002
    type: url
    url: https://example.com/article
    added: 2026-01-16
    status: pending
    tags: [article, reference]
```

## Next Steps

1. Start with a simple extraction script (PDF → text)
2. Add processing (chunking → embeddings)
3. Implement ingestion (vector DB)
4. Build orchestration to connect stages
5. Monitor and refine

## References

- [Text Extraction Techniques](https://docs.anthropic.com/)
- [Vector Databases Guide](https://www.pinecone.io/learn/)
- Parent: [../README.md](../README.md)
