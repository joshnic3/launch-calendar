from datetime import datetime
from typing import List

import pytz
from pydantic import field_validator, ValidationError
from selenium.webdriver.common.by import By

from launch_calendar.lib.models import Launch
from launch_calendar.lib.sources import Scraper


class NSFLaunch(Launch):

    @field_validator('t_zero', mode='before')
    def _format_datetime(cls, v):
        c = v[-1]
        v = v[:-1] + f'0{c}00'
        return datetime.strptime(v, '%a, %b %d, %Y, %H:%M %p GMT%z').astimezone(pytz.utc)


class NSFScraper(Scraper):

    def __init__(self):
        super().__init__(
            'NASA Space Flight',
            'https://www.nasaspaceflight.com/schedule/',
            'https://www.nasaspaceflight.com/favicon.ico'
        )

    def _get_launches(self) -> List[Launch]:
        driver = self._get()
        schedule = driver.find_elements(By.CLASS_NAME, "launch-schedule__card")
        launches = []
        for launch in schedule:
            name = launch.find_element(By.CLASS_NAME, "launch-schedule__name").text
            schedule = launch.find_element(By.CLASS_NAME, "launch-schedule__net").text
            try:
                launches.append(NSFLaunch(name=name, t_zero=schedule, sources=[self.as_model()]))
            except ValidationError:
                pass
            except IndexError:
                pass
        return launches

