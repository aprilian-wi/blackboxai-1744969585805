from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Organizer:
    """
    Data class representing a Haji & Umroh organizer
    """
    name: str
    website_url: str
    address: Optional[str] = None
    phone_numbers: List[str] = None
    emails: List[str] = None
    created_at: datetime = None
    
    def __post_init__(self):
        self.phone_numbers = self.phone_numbers or []
        self.emails = self.emails or []
        self.created_at = self.created_at or datetime.now()
    
    def to_dict(self):
        """Convert the organizer object to a dictionary"""
        return {
            'name': self.name,
            'website_url': self.website_url,
            'address': self.address,
            'phone_numbers': ','.join(self.phone_numbers) if self.phone_numbers else '',
            'emails': ','.join(self.emails) if self.emails else '',
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create an Organizer instance from a dictionary"""
        return cls(
            name=data['name'],
            website_url=data['website_url'],
            address=data.get('address'),
            phone_numbers=data.get('phone_numbers', '').split(',') if data.get('phone_numbers') else [],
            emails=data.get('emails', '').split(',') if data.get('emails') else [],
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None
        )
