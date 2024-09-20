from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from parsers.parser import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class NewsParser(Parser):
    def __init__(self):
        """
        Initialize the Scraper with Selenium WebDriver.
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(service=Service('/opt/homebrew/bin/chromedriver'), options=chrome_options)

    @staticmethod
    def _get_articles_urls(html):
        urls = set()
        for match in re.finditer(r'''text-secondary[^>]+href="([^"]+)''', html, re.DOTALL | re.IGNORECASE):
            if match:
                urls.add(f"https://www.gov.il{match.group(1)}")
        return urls

    def _get_page_source(self, url, class_name):
        logging.info(f"Get html from {url}")
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, class_name))
            )
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
            page_source = self._get_page_source(url, "Results")
            urls = self._get_articles_urls(page_source)
            logger.info(f"found {len(urls)} to crawl")
            for url in urls:
                page_source = self._get_page_source(url, "contentPageHeadTitle")
                article = self.parse_response(url, page_source)
                json_data.append(article)
        except Exception as e:
            logger.critical(f"Error fetching data from {url}: {e}")

        finally:
            # Close the browser
            self.driver.quit()
            return json_data

    def _fetch_and_parse(self, url):
        page_source = self._get_page_source(url)
        return self.parse_response(url, page_source)

    @staticmethod
    def _clean_html(content):
        content = re.sub(r'''<[^>]+>''', '', content)
        return content

    def parse_response(self, url, html):
        title = self.extract_data(html, r'''contentPageHeadTitle[^>]+>([^<]+)''')
        content = self.extract_data(html, r'''mt-2 html-section[^>]+>(.*?)<[^>]+col-12\s+p-0\s+col-lg-3''')
        content = self._clean_html(content)
        publish_date = self.extract_data(html, r'''metaData_publishDate_0[^>]+>([^<]+)''')
        _type = self.extract_data(html, r'''metaData_promotedData_0_0[^>]+>([^<]+)''')
        government = self.extract_data(html, r'''metaData_head_1_0[^>]+>([^<]+)''')

        return {"url": url,
                "title": title,
                "content": content,
                "publish_date": publish_date,
                "type": _type,
                "government": government
                }
