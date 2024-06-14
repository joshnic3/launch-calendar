import logging
import time
from typing import List

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome

from launch_calendar.lib.models import Source, Launch

logger = logging.getLogger('source')


def suppress_loggers(loggers: List):
    for log in loggers:
        logging.getLogger(log).setLevel(logging.WARNING)


suppress_loggers([
    'selenium.webdriver.remote.remote_connection',
    'urllib3.connectionpool',
    'selenium.webdriver.common.service',
    'selenium.webdriver.common.selenium_manager',
])


class Scraper:

    @classmethod
    def web_driver(cls) -> Chrome:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.page_load_strategy = "none"
        driver = Chrome(options=options)
        driver.implicitly_wait(5)
        time.sleep(10)
        return driver

    def __init__(self, name: str, url: str, icon: str, count: int =0):
        self.name = name
        self.url = url
        self.icon = icon
        self.count = count

    def _get(self) -> Chrome:
        driver = self.web_driver()
        driver.get(self.url)
        return driver

    def _get_launches(self) -> List[Launch]:
        raise NotImplemented

    def as_model(self) -> Source:
        return Source(name=self.name, url=self.url, icon=self.icon, count=self.count)

    def get_launches(self) -> List[Launch]:
        logger.debug(f'Scraping {self.url}...')
        try:
            launches = self._get_launches()
            self.count = len(launches)
        except NoSuchElementException:
            logger.warn(f'Failed to parse {self.url}')
            return []
        if launches:
            logger.debug(f'Found {len(launches)} launches on {self.url}')
        else:
            logger.warn(f'Didn\'t find any launches on {self.url}, try re-running')
        return launches
