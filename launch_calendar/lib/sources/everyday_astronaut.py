import time
from datetime import datetime
from typing import List

import pytz
from pydantic import field_validator, ValidationError
from selenium.webdriver.common.by import By

from lib.models import Launch
from lib.sources import Scraper


class EALaunch(Launch):

    @field_validator('t_zero', mode='before')
    def _format_datetime(cls, v):
        return datetime.strptime(v, '%a %b %d %Y %H:%M:%S UTC%z').astimezone(pytz.utc)


class EAScraper(Scraper):

    def __init__(self):
        super().__init__(
            'Everyday Astronaut',
            'https://everydayastronaut.com/upcoming-launches/',
            'https://everydayastronaut.com/favicon.ico'
        )

    def _get_launches(self) -> List[Launch]:
        driver = self._get()
        time.sleep(5)
        launches = []
        schedule = driver.find_elements(By.CLASS_NAME, 'upcoming-launches-block')
        for element in schedule:
            data = element.text.split('\n')
            try:
                name = data[0].split(' | ')[1] if '|' in data[0] else data[0]
                launches.append(EALaunch(name=name, t_zero=data[-4], sources=[self.as_model()]))
            except ValidationError:
                pass
        return launches
