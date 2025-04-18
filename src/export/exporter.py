import csv
import os
from typing import List
from datetime import datetime
from loguru import logger
from ..models.organizer import Organizer
from ..config import EXPORT_DIRECTORY, CSV_FILENAME

class Exporter:
    """Class for exporting organizer data to various formats"""
    
    @staticmethod
    def to_csv(organizers: List[Organizer], filename: str = None) -> str:
        """
        Export organizers to CSV file
        
        Args:
            organizers (List[Organizer]): List of organizers to export
            filename (str, optional): Custom filename. If None, uses default from config
            
        Returns:
            str: Path to the created CSV file
        """
        try:
            # Use default filename if none provided
            if not filename:
                # Add timestamp to filename
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                base_name, ext = os.path.splitext(CSV_FILENAME)
                filename = f"{base_name}_{timestamp}{ext}"
            
            # Ensure export directory exists
            os.makedirs(EXPORT_DIRECTORY, exist_ok=True)
            
            # Full path for CSV file
            filepath = os.path.join(EXPORT_DIRECTORY, filename)
            
            # CSV headers
            headers = [
                'Name',
                'Website URL',
                'Address',
                'Phone Numbers',
                'Emails',
                'Created At'
            ]
            
            # Write to CSV
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write headers
                writer.writerow(headers)
                
                # Write data rows
                for org in organizers:
                    writer.writerow([
                        org.name,
                        org.website_url,
                        org.address or '',
                        '; '.join(org.phone_numbers) if org.phone_numbers else '',
                        '; '.join(org.emails) if org.emails else '',
                        org.created_at.isoformat() if org.created_at else ''
                    ])
            
            logger.info(f"Successfully exported {len(organizers)} organizers to {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error exporting to CSV: {str(e)}")
            raise

    @staticmethod
    def load_from_csv(filepath: str) -> List[Organizer]:
        """
        Load organizers from a CSV file
        
        Args:
            filepath (str): Path to CSV file
            
        Returns:
            List[Organizer]: List of organizers loaded from the file
        """
        try:
            organizers = []
            
            with open(filepath, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    # Create Organizer instance from row
                    organizer = Organizer(
                        name=row['Name'],
                        website_url=row['Website URL'],
                        address=row['Address'] if row['Address'] else None,
                        phone_numbers=row['Phone Numbers'].split('; ') if row['Phone Numbers'] else [],
                        emails=row['Emails'].split('; ') if row['Emails'] else [],
                        created_at=datetime.fromisoformat(row['Created At']) if row['Created At'] else None
                    )
                    organizers.append(organizer)
            
            logger.info(f"Successfully loaded {len(organizers)} organizers from {filepath}")
            return organizers
            
        except Exception as e:
            logger.error(f"Error loading from CSV: {str(e)}")
            raise
