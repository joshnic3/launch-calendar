# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG PYTHON_VERSION=3.12.4
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install poetry
WORKDIR /launch_calendar
COPY . .
COPY ./launch_calendar/static ./static
RUN poetry install
EXPOSE 5000
CMD ls
# CMD ls launch_calendar
CMD poetry run uvicorn 'launch_calendar.main:app' --host=0.0.0.0 --port=5000
