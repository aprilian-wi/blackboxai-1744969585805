# Haji & Umroh Organizer Contact Scraper

A Python-based web scraper that automatically collects contact information from Haji and Umroh travel organizers in Indonesia.

## Features

- 🔍 Automated Google search for travel agency websites
- 📋 Extracts contact information including:
  - Organization name
  - Website URL
  - Full address
  - Phone numbers
  - Email addresses
- 🧹 Data cleaning and validation
- 📊 CSV export functionality
- 📝 Detailed logging

## Requirements

- Python 3.8+
- Required Python packages (see `requirements.txt`)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/haji-umroh-scraper.git
cd haji-umroh-scraper
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the scraper with default settings:

```bash
python -m src.main
```

The scraper will:
1. Search for travel agency websites
2. Filter valid websites
3. Extract contact information
4. Clean and deduplicate data
5. Export results to CSV

Results will be saved in the `exports` directory with a timestamp in the filename.

### Project Structure

```
haji-umroh-scraper/
├── src/
│   ├── crawler/
│   │   ├── crawler.py        # Base web crawler
│   │   └── google_search.py  # Google search functionality
│   ├── scraper/
│   │   └── scraper.py        # Contact information extraction
│   ├── models/
│   │   └── organizer.py      # Data models
│   ├── utils/
│   │   ├── data_cleaner.py   # Data cleaning utilities
│   │   └── validators.py     # Data validation
│   ├── export/
│   │   └── exporter.py       # CSV export functionality
│   └── main.py               # Main application entry
├── requirements.txt
└── README.md
```

## Configuration

Key settings can be modified in `config.py`:

- Search keywords
- Request delays
- User agent
- Export settings

## Output Format

The CSV output includes the following columns:

- Name: Organization name
- Website URL: Homepage URL
- Address: Physical address
- Phone Numbers: Semicolon-separated list of phone numbers
- Emails: Semicolon-separated list of email addresses
- Created At: Timestamp of when the record was created

## Error Handling

The scraper includes comprehensive error handling:

- Retries for failed requests
- Validation of extracted data
- Detailed logging to both console and file
- Graceful handling of network issues

Logs are saved to `scraper.log` for debugging and monitoring.

## Best Practices

1. Respect robots.txt and website terms of service
2. Use appropriate delays between requests
3. Only collect publicly available information
4. Validate and clean collected data
5. Handle errors gracefully

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is intended for legitimate business purposes only. Users are responsible for ensuring compliance with all applicable laws and regulations regarding web scraping and data collection.
