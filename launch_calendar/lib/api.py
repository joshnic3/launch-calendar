import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from launch_calendar.lib.models import Launch, LaunchCalendar
from launch_calendar.lib.sources.everyday_astronaut import EAScraper
from launch_calendar.lib.sources.nasa_space_flight import NSFScraper
from launch_calendar.lib.sources.what_about_it import WAIScraper

SAVE_DIR = Path('/Users/joshnicholls/Documents/Projects/starship')
# SOURCES = [NSFScraper(), EAScraper(), WAIScraper()]
SOURCES = [NSFScraper()]


logger = logging.getLogger('launches')


def _normalise_name(launch: Launch) -> Launch:
    if 'starlink' in launch.name.lower():
        launch.name = launch.name.replace('Group ', '')
    return launch


def _sameness_ratio(launch, other) -> float:
    days_diff = abs((launch.t_zero.date() - other.t_zero.date()).days)
    if launch.name > other.name:
        big = launch
        small = other
    else:
        big = other
        small = launch
    big_name = big.name.lower()
    small_name = small.name.lower()
    uncommon_letters = set(big_name).symmetric_difference(small_name)
    ratio = (1 - (len(uncommon_letters) / len(big_name))) - (days_diff * 0.1)
    return ratio


def _in_launches(launches: List[Launch], other: Launch) -> Optional[Launch]:
    matches = []
    for launch in launches:
        ratio = _sameness_ratio(launch, other)
        if ratio > 0.5:
            matches.append((launch, ratio))
    if matches:
        match = sorted(matches, key=lambda x: x[1])[0]
        return match[0]
    else:
        return None


# TODO Should get atleast 10 launches as that is the most we get back from a single source
def _get_launch_calendar() -> LaunchCalendar:
    # all_launches = {s.name: [] for s in SOURCES}
    launches = []
    for source in SOURCES:
        for launch in source.get_launches():
            # all_launches[source.name].append(launch)
            launch = _normalise_name(launch)
            match = _in_launches(launches, launch)
            if match is not None:
                if launch.sources[0] not in match.sources:
                    match.sources.append(launch.sources[0])
            else:
                launches.append(launch)
    return LaunchCalendar(
        calendar=launches,
        sources=[s.as_model() for s in SOURCES]
    )


def _save_launches_to_json(launch_calendar: LaunchCalendar, file_path: Path):
    with open(file_path, 'w') as file:
        json.dump(launch_calendar.model_dump(), file, indent=4)
    logger.info(f'Saved {len(launch_calendar.calendar)} launches to {file_path}')


def _load_launches_from_json(file_path: Path) -> LaunchCalendar:
    with open(file_path) as file:
        data = json.load(file)
    launch_calendar = LaunchCalendar(**data)
    launch_calendar.last_updated = datetime.fromtimestamp(os.path.getmtime(file_path))
    logger.info(f'Loaded {len(launch_calendar.calendar)} launches from {file_path}')
    return launch_calendar


def load_launch_calendar(file_name: str) -> LaunchCalendar:
    try:
        return _load_launches_from_json(SAVE_DIR / file_name)
    except FileNotFoundError:
        logger.error(f'File {file_name} does not exist!')
        return LaunchCalendar()
    except Exception as e:
        logger.error(str(e))
        return LaunchCalendar()


def scrape_launches(file_name: str) -> LaunchCalendar:
    launch_calendar = _get_launch_calendar()
    _save_launches_to_json(launch_calendar, SAVE_DIR / file_name)
    return launch_calendar
