from storage.storage import Storage


class SearchService:
    def __init__(self, storage: Storage):
        self.storage = storage

    def search(self, keyword: str, parser_name: str):
        if not keyword:
            raise ValueError("Keyword cannot be empty.")

        # Perform search using the storage's search method
        return self.storage.search(keyword, parser_name)
