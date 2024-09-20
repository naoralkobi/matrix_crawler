import json
from pathlib import Path
import logging
from storage.storage import Storage

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

logger = logging.getLogger()


class JSONStorage(Storage):
    def get_file_path(self, parser_name: str) -> Path:
        return Path(self.directory) / f"{parser_name}_data.json"

    def save(self, new_data: list, parser_name: str):
        """
            Save the data into a specific file based on the parser, avoiding duplicate entries by 'url' key.
        """
        file_path = self.get_file_path(parser_name)

        try:
            if file_path.exists():
                all_data = json.loads(file_path.read_text(encoding='utf-8'))
                logging.info(f"Loaded existing data from {file_path} with {len(all_data)} entries.")
            else:
                all_data = []
                logging.info(f"No existing file found. Starting a new data file: {file_path}")

            existing_urls = {entry['url'] for entry in all_data if 'url' in entry}
            logging.info(f"Checking for duplicates among {len(existing_urls)} existing entries.")

            new_entries = [entry for entry in new_data if entry.get('url') not in existing_urls]

            if new_entries:
                logging.info(f"Adding {len(new_entries)} new entries to {file_path}.")
                all_data.extend(new_entries)
                file_path.write_text(json.dumps(all_data, indent=4, ensure_ascii=False), encoding='utf-8')
                logging.info(f"Successfully updated {file_path} with new entries.")
            else:
                logging.info(f"No new entries to add. All provided data already exists in {file_path}.")

        except (IOError, json.JSONDecodeError) as e:
            logging.error(f"Error saving data to {file_path}: {e}", exc_info=True)

    def search(self, keyword: str, parser_name: str):
        """
            Search for a keyword only in the values of the specific parser's JSON file.
        """
        file_path = self.get_file_path(parser_name)

        try:
            if not file_path.exists():
                logging.warning(f"File {file_path} not found for parser: {parser_name}. No search results.")
                return []

            all_data = json.loads(file_path.read_text())
            logging.info(f"Loaded {len(all_data)} entries from {file_path} for searching.")

            # Search only in values of each data entry
            results = [
                data.get('url') for data in all_data
                if any(keyword.lower() in str(value).lower() for value in data.values())
            ]

            logging.info(f"Search for '{keyword}' in {file_path} returned {len(results)} results.")
            return results

        except (IOError, json.JSONDecodeError) as e:
            logging.error(f"Error reading from {file_path}: {e}", exc_info=True)
            return []
