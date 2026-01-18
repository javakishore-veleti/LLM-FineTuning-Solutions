#!/usr/bin/env python3
"""
AWS re:Invent 2025 Web Scraper

Scrapes the AWS re:Invent 2025 top announcements page and all linked pages,
extracts text content, and saves to ~/runtime_data/datasets/aws_reinvent_2025/latest-content/
"""

import os
import re
import sys
import json
import shutil
import hashlib
import logging
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin, urlparse
from typing import Set, Dict, List, Optional

import requests
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
ROOT_URL = "https://aws.amazon.com/blogs/aws/top-announcements-of-aws-reinvent-2025/"
AWS_BLOG_DOMAIN = "aws.amazon.com"
OUTPUT_DIR = Path.home() / "runtime_data" / "datasets" / "aws_reinvent_2025" / "latest-content"
METADATA_FILE = "scrape_metadata.json"

# Request headers to mimic a browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}


class AWSReInventScraper:
    """Scraper for AWS re:Invent 2025 announcements."""

    def __init__(self, output_dir: Path = OUTPUT_DIR, max_depth: int = 1):
        """
        Initialize the scraper.

        Args:
            output_dir: Directory to save scraped content
            max_depth: Maximum depth for following links (1 = only links from root page)
        """
        self.output_dir = Path(output_dir)
        self.max_depth = max_depth
        self.visited_urls: Set[str] = set()
        self.scraped_data: List[Dict] = []
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def clean_text(self, soup: BeautifulSoup) -> str:
        """
        Extract and clean text content from HTML.

        Args:
            soup: BeautifulSoup object

        Returns:
            Cleaned text content
        """
        # Remove script and style elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'noscript']):
            element.decompose()

        # Remove comments
        for comment in soup.find_all(string=lambda text: isinstance(text, str) and text.strip().startswith('<!--')):
            comment.extract()

        # Get text
        text = soup.get_text(separator='\n')

        # Clean up whitespace
        lines = []
        for line in text.split('\n'):
            line = line.strip()
            if line:
                lines.append(line)

        # Join lines and remove excessive whitespace
        text = '\n'.join(lines)
        text = re.sub(r'\n{3,}', '\n\n', text)

        return text.strip()

    def extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title from HTML."""
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text().strip()

        h1_tag = soup.find('h1')
        if h1_tag:
            return h1_tag.get_text().strip()

        return "Untitled"

    def extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """
        Extract relevant links from the page.

        Args:
            soup: BeautifulSoup object
            base_url: Base URL for resolving relative links

        Returns:
            List of absolute URLs
        """
        links = []

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']

            # Skip anchors, javascript, and mailto links
            if href.startswith(('#', 'javascript:', 'mailto:', 'tel:')):
                continue

            # Resolve relative URLs
            absolute_url = urljoin(base_url, href)

            # Parse URL
            parsed = urlparse(absolute_url)

            # Only follow AWS blog links
            if AWS_BLOG_DOMAIN in parsed.netloc and '/blogs/' in parsed.path:
                # Remove fragments and query strings for comparison
                clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                if clean_url not in self.visited_urls:
                    links.append(clean_url)

        return list(set(links))

    def generate_filename(self, url: str, title: str) -> str:
        """
        Generate a safe filename for the scraped content.

        Args:
            url: Page URL
            title: Page title

        Returns:
            Safe filename
        """
        # Create a hash of the URL for uniqueness
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]

        # Clean the title for use as filename
        safe_title = re.sub(r'[^\w\s-]', '', title)
        safe_title = re.sub(r'[-\s]+', '_', safe_title)
        safe_title = safe_title[:50]  # Limit length

        return f"{safe_title}_{url_hash}.txt"

    def scrape_page(self, url: str, depth: int = 0) -> Optional[Dict]:
        """
        Scrape a single page.

        Args:
            url: URL to scrape
            depth: Current recursion depth

        Returns:
            Dictionary with scraped data or None if failed
        """
        if url in self.visited_urls:
            return None

        self.visited_urls.add(url)
        logger.info(f"Scraping: {url} (depth: {depth})")

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract content
        title = self.extract_title(soup)
        text_content = self.clean_text(soup)

        # Generate filename
        filename = self.generate_filename(url, title)

        # Prepare data
        data = {
            'url': url,
            'title': title,
            'filename': filename,
            'scraped_at': datetime.now().isoformat(),
            'depth': depth,
            'content_length': len(text_content)
        }

        # Save content to file
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"URL: {url}\n")
            f.write(f"Title: {title}\n")
            f.write(f"Scraped: {data['scraped_at']}\n")
            f.write("=" * 80 + "\n\n")
            f.write(text_content)

        logger.info(f"Saved: {filename} ({len(text_content)} chars)")

        self.scraped_data.append(data)

        # Extract and follow links if not at max depth
        if depth < self.max_depth:
            links = self.extract_links(soup, url)
            logger.info(f"Found {len(links)} new links to follow")

            for link in links:
                self.scrape_page(link, depth + 1)

        return data

    def clear_output_directory(self):
        """Clear the output directory before scraping."""
        if self.output_dir.exists():
            logger.info(f"Clearing existing content in {self.output_dir}")
            shutil.rmtree(self.output_dir)

        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created output directory: {self.output_dir}")

    def save_metadata(self):
        """Save scraping metadata to JSON file."""
        metadata = {
            'root_url': ROOT_URL,
            'scraped_at': datetime.now().isoformat(),
            'total_pages': len(self.scraped_data),
            'max_depth': self.max_depth,
            'output_directory': str(self.output_dir),
            'pages': self.scraped_data
        }

        metadata_path = self.output_dir / METADATA_FILE
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)

        logger.info(f"Saved metadata to {metadata_path}")

    def run(self, clear_existing: bool = True) -> Dict:
        """
        Run the scraper.

        Args:
            clear_existing: Whether to clear existing content before scraping

        Returns:
            Dictionary with scraping results
        """
        logger.info("=" * 60)
        logger.info("AWS re:Invent 2025 Web Scraper")
        logger.info("=" * 60)

        if clear_existing:
            self.clear_output_directory()
        else:
            self.output_dir.mkdir(parents=True, exist_ok=True)

        # Reset state
        self.visited_urls.clear()
        self.scraped_data.clear()

        # Start scraping from root URL
        logger.info(f"Starting from: {ROOT_URL}")
        self.scrape_page(ROOT_URL, depth=0)

        # Save metadata
        self.save_metadata()

        # Summary
        logger.info("=" * 60)
        logger.info(f"Scraping complete!")
        logger.info(f"Total pages scraped: {len(self.scraped_data)}")
        logger.info(f"Output directory: {self.output_dir}")
        logger.info("=" * 60)

        return {
            'success': True,
            'total_pages': len(self.scraped_data),
            'output_directory': str(self.output_dir),
            'pages': self.scraped_data
        }


def main():
    """Main entry point for the scraper."""
    import argparse

    parser = argparse.ArgumentParser(description='AWS re:Invent 2025 Web Scraper')
    parser.add_argument('--refresh', action='store_true',
                        help='Clear existing content and re-scrape')
    parser.add_argument('--max-depth', type=int, default=1,
                        help='Maximum depth for following links (default: 1)')
    parser.add_argument('--output-dir', type=str, default=str(OUTPUT_DIR),
                        help=f'Output directory (default: {OUTPUT_DIR})')

    args = parser.parse_args()

    scraper = AWSReInventScraper(
        output_dir=Path(args.output_dir),
        max_depth=args.max_depth
    )

    result = scraper.run(clear_existing=args.refresh or not Path(args.output_dir).exists())

    if result['success']:
        print(f"\n✅ Successfully scraped {result['total_pages']} pages")
        print(f"📁 Output directory: {result['output_directory']}")
    else:
        print("\n❌ Scraping failed")
        sys.exit(1)


if __name__ == '__main__':
    main()

