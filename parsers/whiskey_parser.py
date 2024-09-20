from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from parsers.parser import *
import time


class WhiskeyParser(Parser):
    def __init__(self):
        """
        Initialize the Scraper with Selenium WebDriver.
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--blink-settings=imagesEnabled=false")
        self.driver = webdriver.Chrome(service=Service('/opt/homebrew/bin/chromedriver'), options=chrome_options)

    def _get_page_source(self, url):
        logging.info(f"Getting HTML from {url}")
        self.driver.get(url)
        scroll_pause_time = 5  # Time to wait for the page to load after each scroll
        max_scrolls = 15
        # Get the initial page height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        try:
            for i in range(max_scrolls):
                logger.info(f"scrolling number: {i}")
                # Scroll down to the bottom of the page
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load the new content
                time.sleep(scroll_pause_time)

                # Calculate new scroll height and compare with the last height
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break

                last_height = new_height
        except Exception as e:
            logging.error(f"Error waiting for page to load: {e}")

        return self.driver.page_source

    def get_json_data(self, url: str) -> list:
        """
        Fetch the raw HTML content from the given URL using Selenium.
        :param url: The URL to fetch content from.
        :return: The HTML content as a string.
        """
        json_data = []
        try:
            page_source = self._get_page_source(url)
            json_data = self.parse_response(url, page_source)
        except Exception as e:
            print(f"Error fetching data from {url}: {e}")

        finally:
            # Close the browser
            self.driver.quit()
            return json_data

    @staticmethod
    def _clean_content(content):
        if content:
            return content.strip()
        return content

    def parse_response(self, url, html):
        json_data = []
        for match in re.finditer(r'''item product[^>]+>(.*?)<[^>]+action tocart primary''', html,
                                 re.DOTALL | re.IGNORECASE):
            # Fix the regex pattern for extracting URLs
            url = self.extract_data(match.group(1), r'''product-grid[^<]+<a\s+href="([^"]+)"''')
            title = self.extract_data(match.group(1), r'''product-item-link[^>]+>([^<]+)''')
            original_price = self.extract_data(match.group(1), r'''data-price-amount\D+(\d+)" data-price-type="finalPrice"''')
            size = self.extract_data(match.group(1), r'''"unit">([^<]+)''')
            discount_price = self.extract_data(match.group(1), r'''data-price-amount\D+(\d+)" data-price-type="registerPrice"''')

            json_data.append({
                "url": self._clean_content(url),
                "title": self._clean_content(title),
                "original_price": original_price,
                "discount_price": discount_price,
                "size": self._clean_content(size)
            })

        return json_data
