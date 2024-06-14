from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, field_serializer, field_validator

NICE_DATETIME_FORMAT = '%a %d %b %Y %H:%M'
DATETIME_FORMAT_TZ = '%Y-%m-%d %H:%M:%S UTC%z'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class Source(BaseModel):
    name: str
    url: str
    icon: str
    count: int = 0


class Launch(BaseModel):
    name: str
    t_zero: Optional[datetime] = None
    sources: Optional[List[Source]] = []

    @field_validator('t_zero', mode='before')
    def _validate_t_zero(cls, v):
        return datetime.strptime(v, DATETIME_FORMAT_TZ) if isinstance(v, str) else v

    @field_serializer('t_zero')
    def _serialise_t_zero(self, v):
        return v.strftime(DATETIME_FORMAT_TZ)


class LaunchCalendar(BaseModel):
    last_updated: datetime = datetime.now()
    calendar: List[Launch] = []
    sources: List[Source] = []

    @field_serializer('last_updated')
    def _serialise_response_timestamp(self, v):
        return v.strftime(DATETIME_FORMAT)


class LaunchResponse(Launch):

    @field_serializer('t_zero')
    def _serialise_t_zero(self, v):
        return v.strftime(NICE_DATETIME_FORMAT)


class LaunchCalendarResponse(LaunchCalendar):
    calendar: List[LaunchResponse] = []

    @field_serializer('last_updated')
    def _serialise_response_timestamp(self, v):
        return v.strftime(NICE_DATETIME_FORMAT)

    @field_validator('calendar')
    def _sort_calendar(cls, v):
        return sorted(v, key=lambda x: x.t_zero)


class HTMLData(BaseModel):
    calendar: bool = False
    sources: bool = False
