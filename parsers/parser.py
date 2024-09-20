from abc import ABC, abstractmethod
import logging
import re

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

logger = logging.getLogger()


class Parser(ABC):
    @abstractmethod
    def get_json_data(self, url: str):
        pass

    @staticmethod
    def extract_data(html, pattern):
        match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
        return match.group(1) if match else ""
