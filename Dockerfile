FROM python:3.6-alpine

RUN pip install poetry

ADD pyproject.* /app/
WORKDIR /app

RUN poetry config settings.virtualenvs.create false \
 && poetry install
ADD gh_browser.py /app/

CMD gunicorn --bind 0.0.0.0:$PORT gh_browser:app
