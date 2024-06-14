from datetime import datetime
from typing import List

import pytz
from pydantic import field_validator
from selenium.webdriver.common.by import By

from lib.models import Launch
from lib.sources import Scraper


class WAILaunch(Launch):

    @field_validator('t_zero', mode='before')
    def _format_datetime(cls, v):
        return pytz.utc.localize(datetime.strptime(v[:-4], '%B %d, %Y - %H:%M'))


class WAIScraper(Scraper):

    def __init__(self):
        super().__init__(
            'What About It',
            'https://www.whataboutit.space/launches',
            'https://www.whataboutit.space/favicon.png'
        )

    def _get_launches(self) -> List[Launch]:
        driver = self._get()
        schedule_text = driver.find_element(By.CLASS_NAME, 'grid-cols-1').text
        schedule_text = schedule_text.split('\n')
        launches = []
        for _, _, name, _, date_string in zip(*[iter(schedule_text)] * 5):
            if not any([s in date_string.lower() for s in ['tbd', 'tdb']]):
                launches.append(WAILaunch(name=name, t_zero=date_string, sources=[self.as_model()]))
        return launches
