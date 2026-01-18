"""Content extractors for different resource types"""

from .base import BaseExtractor
from .fallback import FallbackExtractor

__all__ = ['BaseExtractor', 'FallbackExtractor']
