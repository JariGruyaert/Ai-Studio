"""
Fallback Extractor

Generic HTML extractor for any web page.
Uses BeautifulSoup for basic content extraction.
"""

import logging
import re
from typing import Dict, Any, Optional
from datetime import datetime

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    raise ImportError("Required packages not installed. Run: pip install requests beautifulsoup4")

from .base import BaseExtractor

logger = logging.getLogger(__name__)


class FallbackExtractor(BaseExtractor):
    """Generic fallback extractor for web pages"""

    def __init__(self, timeout: int = 30):
        super().__init__(timeout)

    def extract(self, url: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Extract content from any web page

        Args:
            url: URL to extract from
            metadata: Optional metadata (domain, etc.)

        Returns:
            Extracted content dictionary
        """
        logger.info(f"Extracting content from: {url}")

        try:
            # Fetch HTML
            html = self._fetch_html(url)

            # Parse with BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')

            # Extract components
            title = self._extract_title(soup)
            description = self._extract_description(soup)
            content = self._extract_content(soup)

            # Build metadata
            extracted_metadata = {
                'url': url,
                'domain': metadata.get('domain', '') if metadata else '',
                'extracted_at': datetime.now().isoformat(),
                'extractor': 'fallback',
                'word_count': len(content.split()) if content else 0
            }

            result = {
                'title': title,
                'description': description,
                'content': content,
                'metadata': extracted_metadata
            }

            # Validate
            if self.validate_extracted_data(result):
                self.extraction_count += 1
                logger.info(f"Successfully extracted {extracted_metadata['word_count']} words from: {url}")
                return result
            else:
                raise ValueError("Extracted data validation failed")

        except Exception as e:
            logger.error(f"Failed to extract from {url}: {str(e)}")
            raise

    def _fetch_html(self, url: str) -> str:
        """
        Fetch HTML from URL

        Args:
            url: URL to fetch

        Returns:
            HTML content as string
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; SmartExtractor/1.0)'
        }

        response = requests.get(url, headers=headers, timeout=self.timeout)
        response.raise_for_status()

        return response.text

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """
        Extract page title

        Args:
            soup: BeautifulSoup object

        Returns:
            Page title
        """
        # Try <title> tag
        title_tag = soup.find('title')
        if title_tag and title_tag.get_text().strip():
            return title_tag.get_text().strip()

        # Try og:title meta tag
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            return og_title['content'].strip()

        # Try h1 tag
        h1_tag = soup.find('h1')
        if h1_tag and h1_tag.get_text().strip():
            return h1_tag.get_text().strip()

        return "Untitled"

    def _extract_description(self, soup: BeautifulSoup) -> str:
        """
        Extract page description

        Args:
            soup: BeautifulSoup object

        Returns:
            Page description
        """
        # Try meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc['content'].strip()

        # Try og:description
        og_desc = soup.find('meta', property='og:description')
        if og_desc and og_desc.get('content'):
            return og_desc['content'].strip()

        # Try first paragraph
        first_p = soup.find('p')
        if first_p and first_p.get_text().strip():
            text = first_p.get_text().strip()
            # Limit to ~200 characters
            if len(text) > 200:
                text = text[:197] + "..."
            return text

        return "No description available"

    def _extract_content(self, soup: BeautifulSoup) -> str:
        """
        Extract main content from page

        Args:
            soup: BeautifulSoup object

        Returns:
            Main content as text
        """
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            element.decompose()

        # Try to find main content area
        main_content = None

        # Try common content containers
        for selector in ['main', 'article', '[role="main"]', '.content', '#content']:
            main_content = soup.select_one(selector)
            if main_content:
                break

        # Fallback to body
        if not main_content:
            main_content = soup.find('body')

        if not main_content:
            return ""

        # Extract text
        text = main_content.get_text(separator='\n', strip=False)

        # Clean up text
        text = self._clean_text(text)

        return text

    def _clean_text(self, text: str) -> str:
        """
        Clean extracted text

        Args:
            text: Raw extracted text

        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)

        # Remove leading/trailing whitespace from lines
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(lines)

        # Remove empty lines at start and end
        text = text.strip()

        return text
