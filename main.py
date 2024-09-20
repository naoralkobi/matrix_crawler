import argparse
from scraper.scraper_manager import ScraperManager
from storage.json_storage import JSONStorage
from storage.search_service import SearchService
import logging
import validators

logging.basicConfig(level=logging.INFO)


def start_crawl(**kwargs):
    """
    should get url and parser name
    :param kwargs:
    :return:
    """
    # Input validation
    if not validators.url(kwargs.get('url')):
        logging.error(f"Invalid URL: {kwargs.get('url')}")
        raise ValueError(f"Invalid URL: {kwargs.get('url')}")

    if kwargs.get('parser_name') not in {'news', 'whiskey'}:
        logging.error(f"Invalid parser: {kwargs.get('parser_name')}")
        raise ValueError(f"Invalid parser: {kwargs.get('parser_name')}")

    storage = JSONStorage()
    scraper_manager = ScraperManager(storage)
    scraper_manager.scrape_and_store(**kwargs)


def search_keyword(keyword: str, parser_name: str):
    """Search for a keyword in the stored data."""
    storage = JSONStorage()
    search_service = SearchService(storage)
    return search_service.search(keyword, parser_name)


def get_args():
    parser = argparse.ArgumentParser(description='Crawl a URL with a specific parser.')
    parser.add_argument('--url', required=True, help='The URL to crawl')
    parser.add_argument('--parser', required=True, help='The parser to use (e.g., news, whiskey)')
    parser.add_argument('--search', help='The keyword to search for in the stored data.')
    return parser.parse_args()


if __name__ == "__main__":
    """
    --url "https://www.gov.il/en/collectors/news" --parser "news"
    --url "https://www.paneco.co.il/whiskey" --parser "whiskey"
    --------------------------
    --search "" --url "https://www.gov.il/en/collectors/news" --parser "news"
    --search "מילק" --url "https://www.paneco.co.il/whiskey" --parser "whiskey"
    """
    arguments = get_args()
    try:
        if arguments.search:
            logging.info("start searching")
            results = search_keyword(keyword=arguments.search, parser_name=arguments.parser)
            logging.info(results)
        elif arguments.url:
            logging.info("start crawling")
            start_crawl(url=arguments.url, parser_name=arguments.parser)
        else:
            print("You must provide either a --url to crawl or a --search keyword to search.")
    except Exception as e:
        logging.error(f"Failed to start crawling: {e}")
