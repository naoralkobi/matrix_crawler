from parsers.parser import *


class WhiskeyParser(Parser):
    def fetch_data(self, url: str):
        response = requests.get(url)
        return response

    def parse_response(self, **kwargs):
        # Implement logic to parse news articles
        return {"url": kwargs.get("url"), "name": "Whiskey Name", "price": "100$", "size": "750ml"}
