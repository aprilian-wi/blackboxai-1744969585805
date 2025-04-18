import re
from typing import List, Optional, Tuple
from bs4 import BeautifulSoup
from loguru import logger
from ..models.organizer import Organizer
from ..utils.validators import validate_email, validate_phone, validate_url
from ..crawler.crawler import Crawler

class Scraper:
    """Class for scraping contact information from travel agency websites"""
    
    def __init__(self):
        self.crawler = Crawler()

    def extract_phones(self, text: str) -> List[str]:
        """
        Extract phone numbers from text
        
        Args:
            text (str): Text to extract from
            
        Returns:
            List[str]: List of phone numbers found
        """
        # Patterns for Indonesian phone numbers
        patterns = [
            r'\+62[0-9\-\s]{8,}',  # +62 format
            r'0[0-9\-\s]{8,}',     # 0 format
            r'62[0-9\-\s]{8,}',    # 62 format
            r'[\(\s]0[0-9\-\s\)]{8,}'  # (0xx) format
        ]
        
        phones = []
        for pattern in patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                # Clean up the phone number
                phone = match.group()
                phone = re.sub(r'[\s\(\)\-]', '', phone)  # Remove spaces, parentheses, hyphens
                
                if validate_phone(phone):
                    phones.append(phone)
        
        return list(set(phones))  # Remove duplicates

    def extract_emails(self, text: str) -> List[str]:
        """
        Extract email addresses from text
        
        Args:
            text (str): Text to extract from
            
        Returns:
            List[str]: List of email addresses found
        """
        # Basic email pattern
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        
        emails = []
        matches = re.finditer(pattern, text)
        for match in matches:
            email = match.group().lower()
            if validate_email(email):
                emails.append(email)
        
        return list(set(emails))  # Remove duplicates

    def extract_address(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extract address from HTML
        
        Args:
            soup (BeautifulSoup): Parsed HTML
            
        Returns:
            Optional[str]: Address if found, None otherwise
        """
        # Common address indicators
        address_keywords = ['alamat', 'address', 'location', 'lokasi']
        
        # Try to find address in elements with these keywords
        for keyword in address_keywords:
            # Look for elements containing the keyword
            elements = soup.find_all(lambda tag: keyword.lower() in tag.get_text().lower())
            
            for element in elements:
                # Get the parent element to capture the full address
                parent = element.parent
                if parent:
                    text = parent.get_text().strip()
                    
                    # Basic address validation (length and common words)
                    if len(text) > 10 and any(word in text.lower() for word in ['jl', 'jalan', 'street']):
                        # Clean up the text
                        lines = text.split('\n')
                        # Take lines that look like address
                        address_lines = [line.strip() for line in lines 
                                      if any(word in line.lower() for word in ['jl', 'jalan', 'street', 'no', 'rt', 'rw'])]
                        
                        if address_lines:
                            return ' '.join(address_lines)
        
        return None

    def extract_name(self, soup: BeautifulSoup, url: str) -> str:
        """
        Extract organization name from HTML
        
        Args:
            soup (BeautifulSoup): Parsed HTML
            url (str): Website URL
            
        Returns:
            str: Organization name
        """
        # Try to find name in title
        title = soup.title.string if soup.title else ''
        if title:
            # Remove common suffixes
            title = re.sub(r'[-|].*$', '', title).strip()
            return title
        
        # Try to find name in header/logo
        header = soup.find('header')
        if header:
            logo = header.find('img', alt=True)
            if logo and logo.get('alt'):
                return logo['alt'].strip()
        
        # Fallback to domain name
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        domain = re.sub(r'^www\.', '', domain)
        domain = domain.split('.')[0].replace('-', ' ').title()
        
        return domain

    def scrape_page(self, url: str) -> Optional[Organizer]:
        """
        Scrape contact information from a website
        
        Args:
            url (str): Website URL to scrape
            
        Returns:
            Optional[Organizer]: Organizer instance if successful, None otherwise
        """
        try:
            # Validate URL
            if not validate_url(url):
                logger.warning(f"Invalid URL: {url}")
                return None
            
            # Get homepage content
            content = self.crawler.get_page(url)
            if not content:
                return None
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract initial information from homepage
            name = self.extract_name(soup, url)
            phones = self.extract_phones(content)
            emails = self.extract_emails(content)
            address = self.extract_address(soup)
            
            # Try to get additional information from contact page
            contact_content = self.crawler.get_contact_page(url)
            if contact_content:
                contact_soup = BeautifulSoup(contact_content, 'html.parser')
                
                # Extract additional contact information
                phones.extend(self.extract_phones(contact_content))
                emails.extend(self.extract_emails(contact_content))
                
                # Update address if not found on homepage
                if not address:
                    address = self.extract_address(contact_soup)
            
            # Create Organizer instance
            organizer = Organizer(
                name=name,
                website_url=url,
                address=address,
                phone_numbers=list(set(phones)),  # Remove duplicates
                emails=list(set(emails))  # Remove duplicates
            )
            
            return organizer
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return None
        
    def close(self):
        """Close the crawler session"""
        self.crawler.close()
