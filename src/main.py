import sys
from typing import List
from loguru import logger
from .crawler.google_search import GoogleSearchCrawler
from .scraper.scraper import Scraper
from .utils.data_cleaner import DataCleaner
from .export.exporter import Exporter
from .models.organizer import Organizer

class HajiUmrohScraper:
    """Main class for orchestrating the scraping process"""
    
    def __init__(self):
        # Configure logger
        logger.remove()  # Remove default handler
        logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
        logger.add("scraper.log", rotation="500 MB")

    def run(self, num_results_per_keyword: int = 10) -> str:
        """
        Run the complete scraping process
        
        Args:
            num_results_per_keyword (int): Number of results to fetch per search keyword
            
        Returns:
            str: Path to the exported CSV file
        """
        try:
            # Step 1: Search for travel agency websites
            logger.info("Starting website search...")
            google_crawler = GoogleSearchCrawler()
            websites = google_crawler.search_travel_agencies(num_results_per_keyword)
            logger.info(f"Found {len(websites)} potential websites")
            
            # Step 2: Filter valid travel websites
            valid_websites = google_crawler.filter_valid_websites(websites)
            logger.info(f"Filtered down to {len(valid_websites)} valid travel websites")
            
            # Step 3: Scrape contact information
            logger.info("Starting contact information scraping...")
            scraper = Scraper()
            organizers: List[Organizer] = []
            
            for url in valid_websites:
                try:
                    organizer = scraper.scrape_page(url)
                    if organizer:
                        organizers.append(organizer)
                except Exception as e:
                    logger.error(f"Error scraping {url}: {str(e)}")
                    continue
            
            logger.info(f"Successfully scraped {len(organizers)} organizers")
            
            # Step 4: Clean and deduplicate data
            logger.info("Cleaning and deduplicating data...")
            cleaner = DataCleaner()
            cleaned_organizers = cleaner.clean_dataset(organizers)
            logger.info(f"Data cleaned, {len(cleaned_organizers)} unique organizers remaining")
            
            # Step 5: Export to CSV
            logger.info("Exporting results to CSV...")
            csv_path = Exporter.to_csv(cleaned_organizers)
            logger.info(f"Results exported to {csv_path}")
            
            return csv_path
            
        except Exception as e:
            logger.error(f"Error in scraping process: {str(e)}")
            raise
        
        finally:
            # Clean up
            if 'google_crawler' in locals():
                google_crawler.crawler.close()
            if 'scraper' in locals():
                scraper.close()

def main():
    """Entry point for the scraper"""
    try:
        scraper = HajiUmrohScraper()
        csv_path = scraper.run()
        logger.info("Scraping completed successfully!")
        logger.info(f"Results saved to: {csv_path}")
        
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
