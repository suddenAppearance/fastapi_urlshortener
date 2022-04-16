import pytest


def test_user_create(client, user):
    # test create user
    response = client.post("api/v1/users/", json=user.dict())
    assert response.status_code == 200
    response = response.json()
    assert response.get('message') == 'ok'

    # test same login fails
    response = client.post("api/v1/users/", json=user.dict())
    assert response.status_code == 409


def test_user_login(client, user):
    # test login user
    response = client.post("api/v1/oauth2/token/", data=user.dict())
    assert response.status_code == 200
    response = response.json()
    assert response.get('access_token')

    # test wrong credentials
    response = client.post("api/v1/oauth2/token/", data={'username': user.username, 'password': 'wrong'})
    assert response.status_code == 401


def test_get_current_user(client, authorized_client, user):
    # test 401 on unauthorized
    response = client.get("api/v1/users/me/")
    assert response.status_code == 401

    # test get current user
    response = authorized_client.get("api/v1/users/me/")
    assert response.status_code == 200
    response = response.json()
    assert response.get("username") == user.username


def test_create_url(authorized_client, url):
    # test create url
    response = authorized_client.post("api/v1/", json=url.dict())
    assert response.status_code == 200
    response = response.json()

    # save url response for next tests
    pytest._url = response

    # test create 2 urls with different hashes
    response = authorized_client.post("api/v1/", json=url.dict())
    assert response.status_code == 200
    response = response.json()
    assert pytest._url.get('hash') != response.get('hash')


def test_get_my_urls(authorized_client):
    # test get my urls
    response = authorized_client.get("api/v1/")
    assert response.status_code == 200

    # test my urls contain created url
    contains_url = False
    response = response.json()
    for url in response:
        if url.get('hash') == pytest._url.get('hash'):
            pytest._url = url  # update with id
            contains_url = True

    assert contains_url


def test_get_real_url(authorized_client):
    # test get real url is redirecting
    response = authorized_client.get(f"api/v1/{pytest._url.get('hash')}", follow_redirects=True)
    assert len(response.history) > 0
    assert response.url == pytest._url.get('url')


def test_get_real_url_incr_visits(authorized_client):
    # test redirect increments visits of url
    response = authorized_client.get("/api/v1/").json()
    visits = None
    for url in response:
        if url.get('hash') == pytest._url.get('hash'):
            visits = url.get('visits')

    assert visits == 1


def test_delete_url_by_id(authorized_client):
    # test delete url by id
    response = authorized_client.delete(f"/api/v1/{pytest._url.get('id')}/")
    assert response.status_code == 200

    # test url is deleted
    response = authorized_client.get("api/v1/")
    contains_url = False
    response = response.json()
    assert isinstance(response, list)
    for url in response:
        if url.get('id') == pytest._url.get('id'):
            pytest._url = url  # update with id
            contains_url = True

    assert not contains_url
