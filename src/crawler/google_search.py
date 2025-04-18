from typing import List, Set
from loguru import logger
from googlesearch import search
from .crawler import Crawler
from ..config import SEARCH_KEYWORDS, DELAY_BETWEEN_REQUESTS
import time

class GoogleSearchCrawler:
    """
    Class for searching Google to find travel agency websites
    """
    
    def __init__(self):
        self.crawler = Crawler()
        self.found_urls: Set[str] = set()

    def search_travel_agencies(self, num_results: int = 10) -> List[str]:
        """
        Search for travel agency websites using predefined keywords
        
        Args:
            num_results (int): Number of results to fetch per keyword
            
        Returns:
            List[str]: List of unique website URLs found
        """
        try:
            for keyword in SEARCH_KEYWORDS:
                logger.info(f"Searching for: {keyword}")
                
                # Add 'Indonesia' to make search more specific
                search_query = f"{keyword} Indonesia"
                
                try:
                    # Use googlesearch-python to get results
                    search_results = search(
                        query=search_query,
                        num_results=num_results,
                        lang="id"  # Indonesian results
                    )
                    
                    # Process each result
                    for url in search_results:
                        try:
                            # Extract base URL to avoid duplicate subpages
                            base_url = self.crawler.extract_base_url(url)
                            
                            # Add to found URLs if new
                            if base_url not in self.found_urls:
                                logger.info(f"Found new website: {base_url}")
                                self.found_urls.add(base_url)
                                
                            # Add delay between searches
                            time.sleep(DELAY_BETWEEN_REQUESTS)
                            
                        except Exception as e:
                            logger.error(f"Error processing URL {url}: {str(e)}")
                            continue
                    
                except Exception as e:
                    logger.error(f"Error during search for keyword '{keyword}': {str(e)}")
                    continue
                
                # Add delay between keywords
                time.sleep(DELAY_BETWEEN_REQUESTS * 2)
            
            return list(self.found_urls)
            
        except Exception as e:
            logger.error(f"Fatal error in search_travel_agencies: {str(e)}")
            return list(self.found_urls)  # Return any URLs found before error
        
        finally:
            self.crawler.close()

    def validate_travel_website(self, url: str) -> bool:
        """
        Basic validation to check if a website is likely a travel agency
        
        Args:
            url (str): Website URL to validate
            
        Returns:
            bool: True if website appears to be a travel agency
        """
        try:
            # Get homepage content
            content = self.crawler.get_page(url)
            if not content:
                return False
            
            # Convert to lowercase for case-insensitive matching
            content_lower = content.lower()
            
            # Keywords that suggest this is a travel agency website
            travel_keywords = [
                'umroh',
                'umrah',
                'haji',
                'hajj',
                'travel',
                'wisata',
                'ziarah',
                'mekkah',
                'madinah',
                'saudi',
                'paket'
            ]
            
            # Check if at least 3 keywords are present
            keyword_count = sum(1 for keyword in travel_keywords if keyword in content_lower)
            
            return keyword_count >= 3
            
        except Exception as e:
            logger.error(f"Error validating website {url}: {str(e)}")
            return False

    def filter_valid_websites(self, urls: List[str]) -> List[str]:
        """
        Filter list of URLs to only include valid travel agency websites
        
        Args:
            urls (List[str]): List of URLs to filter
            
        Returns:
            List[str]: Filtered list of valid travel agency URLs
        """
        valid_urls = []
        
        for url in urls:
            try:
                if self.validate_travel_website(url):
                    logger.info(f"Validated travel website: {url}")
                    valid_urls.append(url)
                else:
                    logger.info(f"Skipping non-travel website: {url}")
                    
                # Add delay between validations
                time.sleep(DELAY_BETWEEN_REQUESTS)
                
            except Exception as e:
                logger.error(f"Error filtering website {url}: {str(e)}")
                continue
        
        return valid_urls
