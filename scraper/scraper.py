from abc import ABC, abstractmethod


class Scraper(ABC):
    @abstractmethod
    def fetch_data(self, url: str):
        pass

    @abstractmethod
    def parse_response(self, html):
        pass
