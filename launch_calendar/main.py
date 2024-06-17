import logging
import sys

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from launch_calendar.lib.api import scrape_launches, load_launch_calendar
from launch_calendar.lib.models import LaunchCalendarResponse, HTMLData

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger('main')

file_name = 'launch_calendar_data.json'
calendar = load_launch_calendar(file_name)
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/api/scrape', response_model=LaunchCalendarResponse)
async def _scrape_api():
    global calendar
    calendar = scrape_launches(file_name)
    return calendar


@app.get('/api/calendar', response_model=LaunchCalendarResponse)
async def _starship_launch_api():
    return calendar


@app.get('/{page}', response_class=HTMLResponse)
async def _starship_launch(request: Request, page: str):
    context = HTMLData(sources=True) if page.lower() == 'sources' else HTMLData(calendar=True)
    return templates.TemplateResponse(request=request, name="index.html", context=context.model_dump())


if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
