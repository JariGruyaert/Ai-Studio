"""
Type Detector Component

Identifies resource type from URL patterns.
"""

import logging
import re
from urllib.parse import urlparse
from typing import Dict, Tuple, Optional

logger = logging.getLogger(__name__)


class TypeDetector:
    """Detects resource type based on URL patterns"""

    # Resource type constants
    TYPE_GITHUB = "github-repo"
    TYPE_YOUTUBE = "youtube-video"
    TYPE_BLOG = "blog-post"
    TYPE_ARTICLE = "article"
    TYPE_UNKNOWN = "unknown"

    def __init__(self):
        self.detection_stats = {
            self.TYPE_GITHUB: 0,
            self.TYPE_YOUTUBE: 0,
            self.TYPE_BLOG: 0,
            self.TYPE_ARTICLE: 0,
            self.TYPE_UNKNOWN: 0
        }

    def detect_type(self, url: str) -> Tuple[str, Dict[str, str]]:
        """
        Detect resource type from URL

        Args:
            url: URL to analyze

        Returns:
            Tuple of (resource_type, metadata_dict)
        """
        url = url.strip()
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        path = parsed.path.lower()

        # GitHub detection
        if self.is_github(domain, path):
            resource_type = self.TYPE_GITHUB
            metadata = self.parse_github_url(url)

        # YouTube detection
        elif self.is_youtube(domain, path):
            resource_type = self.TYPE_YOUTUBE
            metadata = self.parse_youtube_url(url)

        # Blog detection
        elif self.is_blog(domain, path):
            resource_type = self.TYPE_BLOG
            metadata = {'domain': domain}

        # Default to article
        else:
            resource_type = self.TYPE_ARTICLE
            metadata = {'domain': domain}

        self.detection_stats[resource_type] += 1
        logger.debug(f"Detected type '{resource_type}' for: {url}")

        return resource_type, metadata

    def is_github(self, domain: str, path: str) -> bool:
        """Check if URL is a GitHub repository"""
        return 'github.com' in domain and path.count('/') >= 2

    def is_youtube(self, domain: str, path: str) -> bool:
        """Check if URL is a YouTube video"""
        return (
            ('youtube.com' in domain and '/watch' in path) or
            'youtu.be' in domain
        )

    def is_blog(self, domain: str, path: str) -> bool:
        """Heuristic check for blog posts"""
        blog_indicators = [
            'medium.com',
            'dev.to',
            'substack.com',
            'hashnode',
            'blog.',
            'blogs.',
            '/blog/',
            '/post/',
            '/article/'
        ]

        return any(indicator in domain or indicator in path for indicator in blog_indicators)

    def parse_github_url(self, url: str) -> Dict[str, str]:
        """
        Parse GitHub URL to extract owner and repo

        Args:
            url: GitHub repository URL

        Returns:
            Dictionary with owner, repo, and full_name
        """
        parsed = urlparse(url)
        path_parts = [p for p in parsed.path.split('/') if p]

        metadata = {'domain': 'github.com'}

        if len(path_parts) >= 2:
            owner = path_parts[0]
            repo = path_parts[1]

            metadata.update({
                'owner': owner,
                'repo': repo,
                'full_name': f"{owner}/{repo}"
            })

        return metadata

    def parse_youtube_url(self, url: str) -> Dict[str, str]:
        """
        Parse YouTube URL to extract video ID

        Args:
            url: YouTube video URL

        Returns:
            Dictionary with video_id
        """
        parsed = urlparse(url)
        metadata = {'domain': 'youtube.com'}

        # youtube.com/watch?v=VIDEO_ID
        if 'youtube.com' in parsed.netloc:
            match = re.search(r'[?&]v=([^&]+)', url)
            if match:
                metadata['video_id'] = match.group(1)

        # youtu.be/VIDEO_ID
        elif 'youtu.be' in parsed.netloc:
            path_parts = [p for p in parsed.path.split('/') if p]
            if path_parts:
                metadata['video_id'] = path_parts[0]

        return metadata

    def get_stats(self) -> Dict[str, int]:
        """Get detection statistics"""
        return self.detection_stats.copy()
