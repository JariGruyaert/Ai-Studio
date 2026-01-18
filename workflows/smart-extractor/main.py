#!/usr/bin/env python3
"""
Smart Content Extractor - Main Entry Point

Intelligently extract, process, and store content from URLs.
"""

import argparse
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from core import ResourceLoader, TypeDetector, StorageManager
from extractors import FallbackExtractor


class SmartExtractor:
    """Main orchestrator for smart content extraction"""

    def __init__(
        self,
        input_file: str,
        output_dir: str = "knowledge",
        timeout: int = 30,
        verbose: bool = False
    ):
        """
        Initialize Smart Extractor

        Args:
            input_file: Path to resources JSON file
            output_dir: Output directory for extracted content
            timeout: HTTP request timeout
            verbose: Enable verbose logging
        """
        self.input_file = input_file
        self.output_dir = output_dir
        self.timeout = timeout

        # Setup logging
        self._setup_logging(verbose)

        # Initialize components
        self.loader = ResourceLoader()
        self.detector = TypeDetector()
        self.storage = StorageManager(base_path=output_dir)
        self.extractor = FallbackExtractor(timeout=timeout)

        # Stats
        self.stats = {
            'total': 0,
            'successful': 0,
            'failed': 0,
            'start_time': None,
            'end_time': None
        }

        self.logger = logging.getLogger(__name__)

    def _setup_logging(self, verbose: bool):
        """Setup logging configuration"""
        level = logging.DEBUG if verbose else logging.INFO

        logging.basicConfig(
            level=level,
            format='%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def process_all(self) -> Dict[str, Any]:
        """
        Process all resources from input file

        Returns:
            Processing statistics
        """
        self.logger.info("=" * 60)
        self.logger.info("Smart Content Extractor v1.0")
        self.logger.info("=" * 60)

        self.stats['start_time'] = datetime.now()

        # Load resources
        self.logger.info(f"\nLoading resources from: {self.input_file}")
        try:
            resources = self.loader.load_and_validate(self.input_file, deduplicate=True)
        except Exception as e:
            self.logger.error(f"Failed to load resources: {e}")
            return self.stats

        self.stats['total'] = len(resources)

        if not resources:
            self.logger.warning("No valid resources found to process")
            return self.stats

        loader_stats = self.loader.get_stats()
        self.logger.info(f"✓ Loaded {loader_stats['total']} resources")
        self.logger.info(f"✓ Valid: {loader_stats['valid']}, Invalid: {loader_stats['invalid']}, Duplicates: {loader_stats['duplicates']}")

        # Process each resource
        self.logger.info(f"\nProcessing {len(resources)} resources:\n")

        for idx, resource in enumerate(resources, 1):
            self._process_resource(resource, idx, len(resources))

        # Finalize
        self.stats['end_time'] = datetime.now()
        self._print_summary()

        # Save processing log
        self.storage.save_processing_log()

        return self.stats

    def _process_resource(self, resource: Dict[str, Any], index: int, total: int):
        """
        Process a single resource

        Args:
            resource: Resource dictionary
            index: Current index
            total: Total number of resources
        """
        url = resource.get('url', '').strip()

        self.logger.info(f"[{index}/{total}] {url}")

        try:
            # Detect type
            resource_type, type_metadata = self.detector.detect_type(url)
            self.logger.info(f"  └─ Type: {resource_type}")

            # Extract content
            self.logger.info(f"  └─ Extracting...")
            extracted_data = self.extractor.extract(url, type_metadata)

            # Save content
            self.logger.info(f"  └─ Saving...")
            output_file = self.storage.save_content(extracted_data, resource_type, url)

            if output_file:
                self.logger.info(f"  └─ ✓ Saved to: {output_file}")
                self.stats['successful'] += 1
            else:
                self.logger.warning(f"  └─ ✗ Failed to save")
                self.stats['failed'] += 1

        except Exception as e:
            self.logger.error(f"  └─ ✗ Error: {str(e)}")
            self.stats['failed'] += 1

        self.logger.info("")  # Blank line for readability

    def _print_summary(self):
        """Print processing summary"""
        duration = self.stats['end_time'] - self.stats['start_time']
        duration_str = str(duration).split('.')[0]  # Remove microseconds

        self.logger.info("=" * 60)
        self.logger.info("SUMMARY")
        self.logger.info("=" * 60)
        self.logger.info(f"✓ Successfully processed: {self.stats['successful']}")
        self.logger.info(f"✗ Failed: {self.stats['failed']}")
        self.logger.info(f"⏱  Time elapsed: {duration_str}")
        self.logger.info(f"📁 Output directory: {self.output_dir}/")
        self.logger.info(f"📋 Processing log: {self.storage.processing_log_path}")
        self.logger.info("=" * 60)

        # Component stats
        detector_stats = self.detector.get_stats()
        storage_stats = self.storage.get_stats()

        self.logger.info("\nDetection Statistics:")
        for resource_type, count in detector_stats.items():
            if count > 0:
                self.logger.info(f"  {resource_type}: {count}")

        self.logger.info(f"\nStorage Statistics:")
        self.logger.info(f"  Files saved: {storage_stats['saved']}")
        self.logger.info(f"  Total size: {storage_stats['total_bytes']:,} bytes")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Smart Content Extractor - Intelligently extract and store web content',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '-i', '--input',
        default='data/resources-raw/resources-raw.json',
        help='Input JSON file with resources (default: data/resources-raw/resources-raw.json)'
    )

    parser.add_argument(
        '-o', '--output',
        default='knowledge',
        help='Output directory for extracted content (default: knowledge)'
    )

    parser.add_argument(
        '-t', '--timeout',
        type=int,
        default=30,
        help='HTTP request timeout in seconds (default: 30)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    # Run extractor
    extractor = SmartExtractor(
        input_file=args.input,
        output_dir=args.output,
        timeout=args.timeout,
        verbose=args.verbose
    )

    stats = extractor.process_all()

    # Exit with appropriate code
    if stats['failed'] > 0 and stats['successful'] == 0:
        sys.exit(1)  # All failed
    elif stats['failed'] > 0:
        sys.exit(2)  # Some failed
    else:
        sys.exit(0)  # All successful


if __name__ == '__main__':
    main()
