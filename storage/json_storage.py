import json
import os
from storage.storage import Storage
import logging

logging.basicConfig(level=logging.INFO)


class JSONStorage(Storage):
    def get_file_path(self, parser_name: str) -> str:
        """Generate a file path based on the parser name."""
        return os.path.join(self.directory, f"{parser_name}_data.json")

    def save(self, data: dict, parser_name: str):
        """Save the data into a specific file based on the parser."""
        file_path = self.get_file_path(parser_name)

        try:
            # Load existing data if the file exists, otherwise start with an empty list
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    all_data = json.load(file)
            else:
                all_data = []

            # Append new data
            all_data.append(data)

            # Save updated data back to the file
            with open(file_path, 'w') as file:
                json.dump(all_data, file, indent=4)

        except (IOError, json.JSONDecodeError) as e:
            logging.critical(f"Error saving data to {file_path}: {e}")

    def search(self, keyword: str, parser_name: str):
        """Search for a keyword only in the values of the specific parser's JSON file."""
        file_path = self.get_file_path(parser_name)

        try:
            if not os.path.exists(file_path):
                return []

            with open(file_path, 'r') as file:
                all_data = json.load(file)

            flattened_data = [item for sublist in all_data for item in sublist]

            # Search only in values of each data entry
            results = [
                data for data in flattened_data
                if any(keyword.lower() in str(value).lower() for value in data.values())
            ]
            return results

        except (IOError, json.JSONDecodeError) as e:
            logging.critical(f"Error reading from {file_path}: {e}")
            return []
