"""
Base Extractor

Abstract base class for all content extractors.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class BaseExtractor(ABC):
    """Base class for content extractors"""

    def __init__(self, timeout: int = 30):
        """
        Initialize extractor

        Args:
            timeout: HTTP request timeout in seconds
        """
        self.timeout = timeout
        self.extraction_count = 0

    @abstractmethod
    def extract(self, url: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Extract content from URL

        Args:
            url: URL to extract from
            metadata: Optional metadata about the resource

        Returns:
            Dictionary with extracted content:
            {
                'title': str,
                'description': str,
                'content': str,
                'metadata': dict
            }

        Raises:
            Exception: If extraction fails
        """
        pass

    def can_extract(self, url: str, resource_type: str) -> bool:
        """
        Check if this extractor can handle the given URL/type

        Args:
            url: URL to check
            resource_type: Detected resource type

        Returns:
            True if this extractor can handle it
        """
        return True

    def validate_extracted_data(self, data: Dict[str, Any]) -> bool:
        """
        Validate extracted data has required fields

        Args:
            data: Extracted data dictionary

        Returns:
            True if valid
        """
        required_fields = ['title', 'content']

        for field in required_fields:
            if field not in data:
                logger.warning(f"Extracted data missing '{field}'")
                return False

            if not data[field] or not str(data[field]).strip():
                logger.warning(f"Extracted data has empty '{field}'")
                return False

        return True

    def get_extraction_count(self) -> int:
        """Get number of successful extractions"""
        return self.extraction_count
