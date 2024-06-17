# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12.4
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install poetry
WORKDIR /launch_calendar
COPY . .
COPY ./launch_calendar/static ./static
COPY ./launch_calendar/templates ./templates
RUN poetry install
EXPOSE 8080
CMD poetry run uvicorn 'launch_calendar.main:app' --host=0.0.0.0 --port=8080
