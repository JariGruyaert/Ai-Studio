"""
Storage Manager Component

Handles saving extracted content to markdown files and tracking processing status.
"""

import json
import logging
import re
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class StorageManager:
    """Manages storage of extracted content"""

    def __init__(self, base_path: str = "knowledge", create_categories: bool = True):
        """
        Initialize storage manager

        Args:
            base_path: Base directory for storing content
            create_categories: Whether to create category subdirectories
        """
        self.base_path = Path(base_path)
        self.create_categories = create_categories
        self.processing_log_path = self.base_path / "_processing-log.json"

        # Ensure base directory exists
        self.base_path.mkdir(parents=True, exist_ok=True)

        # Load or create processing log
        self.processing_log = self._load_processing_log()

        # Stats
        self.stats = {
            'saved': 0,
            'failed': 0,
            'total_bytes': 0
        }

    def save_content(
        self,
        extracted_data: Dict[str, Any],
        resource_type: str,
        original_url: str
    ) -> Optional[Path]:
        """
        Save extracted content to markdown file

        Args:
            extracted_data: Extracted content dictionary
            resource_type: Type of resource
            original_url: Original URL

        Returns:
            Path to saved file, or None if failed
        """
        try:
            # Determine category and filename
            category = self._determine_category(resource_type)
            filename = self._generate_filename(extracted_data.get('title', 'untitled'), resource_type)

            # Create category directory
            category_path = self.base_path / category
            if self.create_categories:
                category_path.mkdir(parents=True, exist_ok=True)

            # Full file path
            file_path = category_path / filename

            # Generate markdown content
            markdown = self._format_markdown(extracted_data, resource_type, original_url)

            # Write to file
            file_path.write_text(markdown, encoding='utf-8')

            # Update stats
            self.stats['saved'] += 1
            self.stats['total_bytes'] += len(markdown)

            # Update processing log
            self._update_processing_log(original_url, 'completed', str(file_path), None)

            logger.info(f"Saved to: {file_path}")

            return file_path

        except Exception as e:
            logger.error(f"Failed to save content for {original_url}: {str(e)}")
            self.stats['failed'] += 1
            self._update_processing_log(original_url, 'failed', None, str(e))
            return None

    def _determine_category(self, resource_type: str) -> str:
        """
        Determine storage category based on resource type

        Args:
            resource_type: Type of resource

        Returns:
            Category directory name
        """
        category_map = {
            'github-repo': 'github-repos',
            'youtube-video': 'youtube-videos',
            'blog-post': 'blog-posts',
            'article': 'articles',
            'unknown': 'other'
        }

        return category_map.get(resource_type, 'other')

    def _generate_filename(self, title: str, resource_type: str, max_length: int = 50) -> str:
        """
        Generate filename from title

        Args:
            title: Resource title
            resource_type: Type of resource
            max_length: Maximum filename length

        Returns:
            Sanitized filename with .md extension
        """
        # Create slug from title
        slug = title.lower()

        # Remove special characters
        slug = re.sub(r'[^\w\s-]', '', slug)

        # Replace whitespace with hyphens
        slug = re.sub(r'[\s_-]+', '-', slug)

        # Remove leading/trailing hyphens
        slug = slug.strip('-')

        # Limit length
        if len(slug) > max_length:
            slug = slug[:max_length].rstrip('-')

        # Ensure slug is not empty
        if not slug:
            slug = 'untitled'

        # Add .md extension
        filename = f"{slug}.md"

        # Handle duplicates
        file_path = self.base_path / self._determine_category(resource_type) / filename
        counter = 2

        while file_path.exists():
            filename = f"{slug}-{counter}.md"
            file_path = self.base_path / self._determine_category(resource_type) / filename
            counter += 1

        return filename

    def _format_markdown(
        self,
        extracted_data: Dict[str, Any],
        resource_type: str,
        original_url: str
    ) -> str:
        """
        Format extracted data as markdown with frontmatter

        Args:
            extracted_data: Extracted content
            resource_type: Type of resource
            original_url: Original URL

        Returns:
            Formatted markdown content
        """
        title = extracted_data.get('title', 'Untitled')
        description = extracted_data.get('description', 'No description available')
        content = extracted_data.get('content', '')
        metadata = extracted_data.get('metadata', {})

        # Create YAML frontmatter
        frontmatter = f"""---
title: "{title}"
source: {original_url}
type: {resource_type}
extracted: {datetime.now().isoformat()}
domain: {metadata.get('domain', 'unknown')}
word_count: {metadata.get('word_count', 0)}
processing_status: completed
---

"""

        # Build markdown content
        markdown_content = f"""# {title}

## Description
{description}

## Content

{content}

---

## Metadata

**Source:** [{original_url}]({original_url})
**Type:** {resource_type}
**Extracted:** {metadata.get('extracted_at', datetime.now().isoformat())}
**Extractor:** {metadata.get('extractor', 'unknown')}
**Word Count:** {metadata.get('word_count', 0)}
"""

        return frontmatter + markdown_content

    def _load_processing_log(self) -> Dict[str, Any]:
        """
        Load processing log from file

        Returns:
            Processing log dictionary
        """
        if self.processing_log_path.exists():
            try:
                with open(self.processing_log_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load processing log: {e}")

        # Return new log structure
        return {
            'last_updated': datetime.now().isoformat(),
            'total_processed': 0,
            'successful': 0,
            'failed': 0,
            'resources': []
        }

    def _update_processing_log(
        self,
        url: str,
        status: str,
        output_file: Optional[str],
        error: Optional[str]
    ):
        """
        Update processing log

        Args:
            url: Resource URL
            status: Processing status (completed, failed, etc.)
            output_file: Path to output file if successful
            error: Error message if failed
        """
        # Create log entry
        log_entry = {
            'url': url,
            'status': status,
            'processed_at': datetime.now().isoformat(),
            'output_file': output_file,
            'error': error
        }

        # Update log
        self.processing_log['resources'].append(log_entry)
        self.processing_log['total_processed'] = len(self.processing_log['resources'])
        self.processing_log['successful'] = sum(1 for r in self.processing_log['resources'] if r['status'] == 'completed')
        self.processing_log['failed'] = sum(1 for r in self.processing_log['resources'] if r['status'] == 'failed')
        self.processing_log['last_updated'] = datetime.now().isoformat()

    def save_processing_log(self):
        """Save processing log to file"""
        try:
            with open(self.processing_log_path, 'w', encoding='utf-8') as f:
                json.dump(self.processing_log, f, indent=2, ensure_ascii=False)
            logger.info(f"Processing log saved to: {self.processing_log_path}")
        except Exception as e:
            logger.error(f"Failed to save processing log: {e}")

    def get_stats(self) -> Dict[str, int]:
        """Get storage statistics"""
        return self.stats.copy()

    def get_processing_summary(self) -> Dict[str, Any]:
        """Get processing summary"""
        return {
            'total_processed': self.processing_log['total_processed'],
            'successful': self.processing_log['successful'],
            'failed': self.processing_log['failed'],
            'last_updated': self.processing_log['last_updated']
        }
