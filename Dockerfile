# https://hub.docker.com/_/python
FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install fastapi openai requests

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]