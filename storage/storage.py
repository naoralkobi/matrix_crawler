from abc import ABC, abstractmethod
import os


class Storage(ABC):
    def __init__(self, directory: str = None):
        """
        Initialize storage base class with a directory for storing data.
        :param directory: Optional custom directory path for storage.
        """
        self.directory = directory or f"{os.getcwd()}/data"
        self._ensure_directory_exists()

    def _ensure_directory_exists(self):
        """Ensure the storage directory exists, create it if not."""
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    @abstractmethod
    def save(self, data: dict, parser_name: str):
        pass

    @abstractmethod
    def search(self, keyword: str, parser_name: str):
        pass
