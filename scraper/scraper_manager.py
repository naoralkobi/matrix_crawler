from parsers.parser_factory import ParserFactory
from scraper.scraper import Scraper
from storage.storage import Storage


class ScraperManager:
    def __init__(self, storage: Storage):
        self.storage = storage

    def scrape_and_store(self, **kwargs):
        parser = ParserFactory.create_parser(kwargs.get("parser_name"))
        parsed_data = parser.get_json_data(url=kwargs.get("url"))
        self.storage.save(parsed_data, kwargs.get("parser_name"))

    def search_data(self, keyword: str, parser_name: str):
        return self.storage.search(keyword, parser_name)
