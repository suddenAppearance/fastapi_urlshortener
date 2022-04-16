import pytest
from httpx import Client

from schemas.urls import BaseUrlSchema
from schemas.users import LoginUserSchema


@pytest.fixture(scope='session')
def client():
    client = Client(base_url='http://127.0.0.1:8000/')
    yield client
    client.close()


@pytest.fixture(scope='session')
def user() -> LoginUserSchema:
    yield LoginUserSchema(username='test123456', password='test123')

@pytest.fixture(scope='session')
def url() -> BaseUrlSchema:
    yield BaseUrlSchema(url='https://docs.pytest.org/en/6.2.x/getting-started.html')


@pytest.fixture(scope='session')
def authorized_client(user):
    client = Client(base_url='http://127.0.0.1:8000/')
    response = client.post('api/v1/oauth2/token/', data=user.dict()).json()
    client.headers.update({'Authorization': f'Bearer {response.get("access_token")}'})
    yield client
    client.close()