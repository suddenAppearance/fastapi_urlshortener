FROM python:3.8

WORKDIR /app

# Poetry settings
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
COPY ./pyproject.toml  /app/
ENV PATH=/root/.poetry/bin:${PATH}
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . .

#run celery worker