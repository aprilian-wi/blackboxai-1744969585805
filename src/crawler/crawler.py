import time
import requests
from typing import Optional, Dict
from loguru import logger
from requests.exceptions import RequestException
from ..config import USER_AGENT, REQUEST_TIMEOUT, MAX_RETRIES, DELAY_BETWEEN_REQUESTS

class Crawler:
    """Base crawler class for fetching web pages"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })

    def get_page(self, url: str, retry_count: int = 0) -> Optional[str]:
        """
        Fetch a web page with retry mechanism
        
        Args:
            url (str): URL to fetch
            retry_count (int): Current retry attempt number
        
        Returns:
            Optional[str]: HTML content of the page if successful, None otherwise
        """
        try:
            # Add delay between requests to be polite
            time.sleep(DELAY_BETWEEN_REQUESTS)
            
            response = self.session.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            return response.text

        except RequestException as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            
            if retry_count < MAX_RETRIES:
                logger.info(f"Retrying {url} (attempt {retry_count + 1}/{MAX_RETRIES})")
                # Exponential backoff
                time.sleep(DELAY_BETWEEN_REQUESTS * (2 ** retry_count))
                return self.get_page(url, retry_count + 1)
            
            return None

    def get_contact_page(self, base_url: str) -> Optional[str]:
        """
        Try to find and fetch the contact page of a website
        
        Args:
            base_url (str): Base URL of the website
        
        Returns:
            Optional[str]: HTML content of the contact page if found, None otherwise
        """
        # Common contact page paths
        contact_paths = [
            '/contact',
            '/kontak',
            '/kontak-kami',
            '/contact-us',
            '/hubungi-kami',
            '/about',
            '/tentang-kami'
        ]
        
        # Remove trailing slash from base_url
        base_url = base_url.rstrip('/')
        
        # Try each contact path
        for path in contact_paths:
            contact_url = f"{base_url}{path}"
            content = self.get_page(contact_url)
            
            if content:
                logger.info(f"Found contact page at {contact_url}")
                return content
        
        logger.warning(f"No contact page found for {base_url}")
        return None

    def extract_base_url(self, url: str) -> str:
        """
        Extract base URL from a full URL
        
        Args:
            url (str): Full URL
            
        Returns:
            str: Base URL
        """
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"

    def close(self):
        """Close the session"""
        self.session.close()
