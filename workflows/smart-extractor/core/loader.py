"""
Resource Loader Component

Loads and validates resources from JSON input files.
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class ResourceLoader:
    """Loads and validates resource data from JSON files"""

    def __init__(self):
        self.resources = []
        self.stats = {
            'total': 0,
            'valid': 0,
            'invalid': 0,
            'duplicates': 0
        }

    def load_resources(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Load resources from JSON file

        Args:
            file_path: Path to resources JSON file

        Returns:
            List of resource dictionaries

        Raises:
            FileNotFoundError: If file doesn't exist
            json.JSONDecodeError: If JSON is invalid
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Resource file not found: {file_path}")

        logger.info(f"Loading resources from: {file_path}")

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Try to parse as single JSON object or array
        try:
            data = json.loads(content)

            # Handle different JSON structures
            if isinstance(data, list):
                self.resources = data
            elif isinstance(data, dict):
                # Might be wrapped in an object
                self.resources = [data]
            else:
                raise ValueError("Unexpected JSON structure")

        except json.JSONDecodeError as e:
            # Try to parse as multiple JSON arrays (current format issue)
            logger.warning("Standard JSON parsing failed, attempting multi-array parse")
            self.resources = self._parse_multi_array(content)

        self.stats['total'] = len(self.resources)
        logger.info(f"Loaded {self.stats['total']} resources")

        return self.resources

    def _parse_multi_array(self, content: str) -> List[Dict[str, Any]]:
        """
        Parse JSON file with multiple separate arrays

        Args:
            content: Raw file content

        Returns:
            Combined list of resources
        """
        resources = []

        # Split on ']' to get separate arrays
        parts = content.split(']')

        for part in parts:
            part = part.strip()
            if not part:
                continue

            # Add back the closing bracket
            if not part.endswith(']'):
                part = part + ']'

            # Remove leading '[' if not present
            if not part.startswith('['):
                part = '[' + part

            try:
                # Try to parse as JSON array
                data = json.loads(part)
                if isinstance(data, list):
                    resources.extend(data)
                elif isinstance(data, dict):
                    resources.append(data)
            except json.JSONDecodeError:
                # Try parsing just the object part
                try:
                    # Remove brackets and try as object
                    obj_part = part.strip('[]').strip()
                    if obj_part:
                        data = json.loads(obj_part)
                        if isinstance(data, dict):
                            resources.append(data)
                except:
                    continue

        return resources

    def validate_resources(self) -> List[Dict[str, Any]]:
        """
        Validate loaded resources

        Returns:
            List of valid resources
        """
        valid_resources = []

        for resource in self.resources:
            if self.validate_resource(resource):
                valid_resources.append(resource)
                self.stats['valid'] += 1
            else:
                self.stats['invalid'] += 1

        logger.info(f"Validation: {self.stats['valid']} valid, {self.stats['invalid']} invalid")

        return valid_resources

    def validate_resource(self, resource: Dict[str, Any]) -> bool:
        """
        Validate a single resource

        Args:
            resource: Resource dictionary to validate

        Returns:
            True if valid, False otherwise
        """
        # Required fields
        required_fields = ['url']

        for field in required_fields:
            if field not in resource:
                logger.warning(f"Resource missing required field '{field}': {resource}")
                return False

            if not resource[field] or not str(resource[field]).strip():
                logger.warning(f"Resource has empty '{field}': {resource}")
                return False

        # Validate URL format
        url = str(resource['url']).strip()
        if not url.startswith(('http://', 'https://')):
            logger.warning(f"Invalid URL format: {url}")
            return False

        return True

    def deduplicate_resources(self, resources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Remove duplicate resources based on URL

        Args:
            resources: List of resources

        Returns:
            Deduplicated list of resources
        """
        seen_urls = set()
        unique_resources = []

        for resource in resources:
            url = resource.get('url', '').strip().lower()

            if url not in seen_urls:
                seen_urls.add(url)
                unique_resources.append(resource)
            else:
                self.stats['duplicates'] += 1
                logger.debug(f"Duplicate URL found: {url}")

        if self.stats['duplicates'] > 0:
            logger.info(f"Removed {self.stats['duplicates']} duplicate resources")

        return unique_resources

    def load_and_validate(self, file_path: str, deduplicate: bool = True) -> List[Dict[str, Any]]:
        """
        Load, validate, and optionally deduplicate resources

        Args:
            file_path: Path to resources JSON file
            deduplicate: Whether to remove duplicates

        Returns:
            List of valid, unique resources
        """
        # Load
        self.load_resources(file_path)

        # Validate
        valid_resources = self.validate_resources()

        # Deduplicate
        if deduplicate:
            valid_resources = self.deduplicate_resources(valid_resources)

        logger.info(f"Final resource count: {len(valid_resources)}")

        return valid_resources

    def get_stats(self) -> Dict[str, int]:
        """Get loading statistics"""
        return self.stats.copy()
