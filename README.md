# URL SHORTENER

## About

This is API for url shortening (like TinyUrl).

Technologies:

* Database - _Postgres_
* HTTP Server - _Uvicorn_
* Web Framework - _FastAPI_
* Database Framework - _SQLAlchemy's async ORM_
* Migrations Mechanism - _Alembic_

## Local run

1. Add `.env` file to project root and define next env variables:
    * `DATABASE_URL_SYNC` - Database url with sync driver. Alembic uses that for migrations
        * _default_: `postgresql://postgres:postgres@db/urlshortener`
    * `DATABASE_URL_ASYNC` - Database url with async driver. SQLAlchemy uses that for db connections
        * _deault_: `postgresql+asyncpg://postgres:postgres@db/urlshortener`
    * `SECRET_KEY` - Secret key of app. PyJWT uses that to safely encode and decode jwt tokens
        * _default_: random string, e.g. script for generating `binascii.hexlify(os.urandom(20)).decode()`
2. Run `docker-compose up --build` to run server and database
   * consider running `docker-compose down --volumes` to delete all existing volumes
   * or delete only postgres volumes with `docker-compose volume rm`
3. Optional. Debug run in PyCharm
    * You have to change `@db` to `@localhost` in `.env` variables
    * Then add this `.env` to EnvFile setting of `main.py`
    * Run `docker-compose up --build db` to only run database (`docker-compose down --volumes` if needed)
    * Run `docker-compose run web alembic upgrade head` to migrate
    * Start `main.py` in debug mode

# Tests execution
1. Add `test.env` file to project root and define next env variables
   * all env variables from local run.
2. Run `docker-compose down --volumes && docker-compose -f docker-compose.pytest.yml up --build --abort-on-container-exit` to run server, database and pytest 
3. Optional. Debug pytest in PyCharm
   * You have to locally run web server and database. Then debug tests via PyCharm run & debug tools

## Alembic

### Run alembic revision (makemigrations)

`docker-compose run web alembic revision --autogenerate -m "Commit message"`

### Run alembic upgrade (migrate)

`docker-compose run web alembic upgrade head`