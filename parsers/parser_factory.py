from parsers.whiskey_parser import WhiskeyParser
from parsers.news_parser import NewsParser
from parsers.parser import Parser


class ParserFactory:
    @staticmethod
    def create_parser(parser_name: str) -> Parser:
        if parser_name.lower() == 'news':
            return NewsParser()
        elif parser_name.lower() == 'whiskey':
            return WhiskeyParser()
        else:
            raise ValueError(f"Parser '{parser_name}' is not available.")
