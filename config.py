import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Search Configuration
SEARCH_KEYWORDS = [
    "Paket Umroh",
    "Travel Haji dan Umroh",
    "Penyelenggara Umroh Resmi",
    "Biro Perjalanan Umroh",
    "Travel Umroh Terpercaya",
    "Agen Umroh Resmi"
]

# Crawler Configuration
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
REQUEST_TIMEOUT = 30  # seconds
MAX_RETRIES = 3
DELAY_BETWEEN_REQUESTS = 2  # seconds

# Export Configuration
EXPORT_DIRECTORY = 'exports'
CSV_FILENAME = 'haji_umroh_organizers.csv'

# Create export directory if it doesn't exist
os.makedirs(EXPORT_DIRECTORY, exist_ok=True)
