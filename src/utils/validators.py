import re
import validators

def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email (str): Email address to validate
    
    Returns:
        bool: True if email is valid, False otherwise
    """
    return bool(validators.email(email))

def validate_phone(phone: str) -> bool:
    """
    Validate Indonesian phone number format
    
    Args:
        phone (str): Phone number to validate
    
    Returns:
        bool: True if phone number is valid, False otherwise
    """
    # Remove all non-numeric characters
    phone = re.sub(r'\D', '', phone)
    
    # Indonesian phone number patterns:
    # - Starts with 0 or +62
    # - Followed by 8-12 digits
    pattern = r'^(?:0|62)\d{8,12}$'
    
    return bool(re.match(pattern, phone))

def validate_url(url: str) -> bool:
    """
    Validate URL format
    
    Args:
        url (str): URL to validate
    
    Returns:
        bool: True if URL is valid, False otherwise
    """
    return bool(validators.url(url))

def clean_phone_number(phone: str) -> str:
    """
    Clean and standardize phone number format
    
    Args:
        phone (str): Phone number to clean
    
    Returns:
        str: Cleaned phone number
    """
    # Remove all non-numeric characters
    phone = re.sub(r'\D', '', phone)
    
    # Convert leading 0 to 62
    if phone.startswith('0'):
        phone = '62' + phone[1:]
    
    return phone

def clean_email(email: str) -> str:
    """
    Clean and standardize email format
    
    Args:
        email (str): Email to clean
    
    Returns:
        str: Cleaned email
    """
    return email.strip().lower()
