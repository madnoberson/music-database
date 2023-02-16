import pytest

from httpx import AsyncClient
from .config import client, anyio_backend, user_data_in, other_user_data_in


@pytest.mark.anyio
async def test_create_track(client: AsyncClient):
    # Тест с авторизованным пользователем

    sign_in_response = await client.post(
        url='/sign_in/',
        json=user_data_in
    )
    access_token = sign_in_response.json()['access_token']

    track_in = {
        "name": "heroes"
    }

    track_out = {
        "track": {
            "id": 1,
            "name": "heroes",
            "rate": None,
            "rates_number": 0,
            "user_rate": None 
        }
    }

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = await client.post(
        url='/tracks/',
        json=track_in,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json() == track_out


@pytest.mark.anyio
async def test_get_basic_track(client: AsyncClient):
    track_out = {
        "id": 1,
        "name": "heroes",
        "rate": None,
        "rates_number": 0,
        "user_rate": None
    }

    response = await client.get(
        url='/tracks/1/basic/',
    )

    assert response.status_code == 200
    assert response.json() == track_out


@pytest.mark.anyio
async def test_get_track(client: AsyncClient):
    track_out = {
        "track": {
            "id": 1,
            "name": "heroes",
            "rate": None,
            "rates_number": 0,
            "user_rate": None
        }
    }

    response = await client.get(
        url='/tracks/1/',
    )

    assert response.status_code == 200
    assert response.json() == track_out


@pytest.mark.anyio
async def test_create_track_user_rate(client: AsyncClient):
    # /////////////////////////////////////////////
    # /// Тест с неавторизованным пользователем ///
    # /////////////////////////////////////////////
    
    track_user_rate_in = {
        "track_id": 1,
        "rate": 7,
    }
    track_user_rate_out = {
        "rate": 7,
        "rates_number": 1,
        "user_rate": 7
    }

    response = await client.post(
        url='/tracks/1/rates/',
        json=track_user_rate_in
    )

    assert response.status_code == 401

    # ///////////////////////////////////////////
    # /// Тест с авторизованным пользователем ///
    # ///////////////////////////////////////////

    response = await client.post(
        url='/sign_in/',
        json=user_data_in
    )
    access_token = response.json()['access_token']

    response = await client.post(
        url='/tracks/1/rates/',
        json=track_user_rate_in,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200
    assert response.json() == track_user_rate_out

    # //////////////////////////////////////////////////
    # /// Тест с другим авторизованным пользователем ///
    # //////////////////////////////////////////////////

    track_user_rate_in = {
        "track_id": 1,
        "rate": 3.5,
    }
    track_user_rate_out = {
        "rate": 5.25,
        "rates_number": 2,
        "user_rate": 3.5
    }

    response = await client.post(
        url='/sign_up/',
        json=other_user_data_in
    )
    access_token = response.json()['access_token']

    headers={
        "Authorization": f"Bearer {access_token}"
    }

    response = await client.post(
        url='/tracks/1/rates/',
        json=track_user_rate_in,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json() == track_user_rate_out


@pytest.mark.anyio
async def test_get_user_rated_tracks(client: AsyncClient):
    #/////////////////////////////////////////////
    #/// Тест с неавторизованным пользователем ///
    #/////////////////////////////////////////////

    user_rated_tracks_out = {
        "id": 1,
        "name": "heroes",
        "rate": 5.25,
        "rates_number": 2,
        "owner_rate": 7,
        "user_rate": None
    }

    response = await client.get(
        url='/users/1/rates/'
    )

    assert response.status_code == 200
    assert response.json() == user_rated_tracks_out

    #/////////////////////////////////////////////
    #/// Тест с авторизованным пользователем /////
    #/////////////////////////////////////////////

    user_rated_tracks_out = {
        "id": 1,
        "name": "heroes",
        "rate": 5.25,
        "rates_number": 2,
        "user_rate": 7,
        "owner_rate": None
    }

    sign_in_response = await client.post(
        url='/sign_in/',
        json=user_data_in
    )
    access_token = sign_in_response.json()['access_token']
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = await client.get(
        url='/users/1/rates/',
        headers=headers
    )

    assert response.status_code == 200
    assert response.json() == user_rated_tracks_out

    #////////////////////////////////////////////////////
    #/// Тест с другим авторизованным пользователем /////
    #////////////////////////////////////////////////////

    user_rated_tracks_out = {
        "id": 1,
        "name": "heroes",
        "rate": 5.25,
        "rates_number": 2,
        "user_rate": 7,
        "owner_rate": 3.5
    }

    sign_in_response = await client.post(
        url='/sign_in/',
        json=other_user_data_in
    )
    access_token = sign_in_response.json()['access_token']
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = await client.get(
        url='/users/1/rates/',
        headers=headers
    )

    assert response.status_code == 200
    assert response.json() == user_rated_tracks_out

