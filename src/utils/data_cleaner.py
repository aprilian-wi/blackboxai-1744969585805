from typing import List, Dict
from ..models.organizer import Organizer
from .validators import clean_phone_number, clean_email, validate_phone, validate_email

class DataCleaner:
    """
    Class for cleaning and deduplicating organizer data
    """
    
    @staticmethod
    def clean_organizer(organizer: Organizer) -> Organizer:
        """
        Clean individual organizer data
        
        Args:
            organizer (Organizer): Organizer instance to clean
        
        Returns:
            Organizer: Cleaned organizer instance
        """
        # Clean phone numbers
        cleaned_phones = []
        for phone in organizer.phone_numbers:
            cleaned_phone = clean_phone_number(phone)
            if validate_phone(cleaned_phone) and cleaned_phone not in cleaned_phones:
                cleaned_phones.append(cleaned_phone)
        organizer.phone_numbers = cleaned_phones

        # Clean emails
        cleaned_emails = []
        for email in organizer.emails:
            cleaned_email = clean_email(email)
            if validate_email(cleaned_email) and cleaned_email not in cleaned_emails:
                cleaned_emails.append(cleaned_email)
        organizer.emails = cleaned_emails

        # Clean address (remove extra whitespace)
        if organizer.address:
            organizer.address = ' '.join(organizer.address.split())

        return organizer

    @staticmethod
    def remove_duplicates(organizers: List[Organizer]) -> List[Organizer]:
        """
        Remove duplicate organizers based on website URL and merge their information
        
        Args:
            organizers (List[Organizer]): List of organizers to deduplicate
        
        Returns:
            List[Organizer]: Deduplicated list of organizers
        """
        # Use dictionary to track unique organizers by website URL
        unique_organizers: Dict[str, Organizer] = {}
        
        for org in organizers:
            if org.website_url in unique_organizers:
                # Merge information with existing organizer
                existing = unique_organizers[org.website_url]
                
                # Merge phone numbers
                for phone in org.phone_numbers:
                    if phone not in existing.phone_numbers:
                        existing.phone_numbers.append(phone)
                
                # Merge emails
                for email in org.emails:
                    if email not in existing.emails:
                        existing.emails.append(email)
                
                # Update address if current one is empty
                if not existing.address and org.address:
                    existing.address = org.address
                
                # Keep the earliest created_at date
                if org.created_at and (not existing.created_at or org.created_at < existing.created_at):
                    existing.created_at = org.created_at
            else:
                # Add new organizer to unique list
                unique_organizers[org.website_url] = org
        
        return list(unique_organizers.values())

    @staticmethod
    def clean_dataset(organizers: List[Organizer]) -> List[Organizer]:
        """
        Clean entire dataset of organizers
        
        Args:
            organizers (List[Organizer]): List of organizers to clean
        
        Returns:
            List[Organizer]: Cleaned list of organizers
        """
        # Clean individual organizers
        cleaned_organizers = [DataCleaner.clean_organizer(org) for org in organizers]
        
        # Remove duplicates
        deduplicated_organizers = DataCleaner.remove_duplicates(cleaned_organizers)
        
        return deduplicated_organizers
