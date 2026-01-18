"""Core components for Smart Content Extractor"""

from .loader import ResourceLoader
from .detector import TypeDetector
from .storage import StorageManager

__all__ = ['ResourceLoader', 'TypeDetector', 'StorageManager']
