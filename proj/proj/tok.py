"""Spotify token helper utilities."""

from __future__ import annotations

import os
from typing import Optional

import requests

CLIENT_ID_ENV = 'CLIENT_ID'
CLIENT_SECRET_ENV = 'CLIENT_SECRET'


def _get_env_value(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Environment variable {name} is required.")
    return value


def _fetch_access_token(client_id: str, client_secret: str) -> str:
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    }
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, data=data, timeout=25)
    auth_response.raise_for_status()
    access_token_value: Optional[str] = auth_response.json().get('access_token')
    if not access_token_value:
        raise RuntimeError('Unable to retrieve Spotify access token.')
    return access_token_value


client_id = _get_env_value(CLIENT_ID_ENV)
client_secret = _get_env_value(CLIENT_SECRET_ENV)
access_token = _fetch_access_token(client_id, client_secret)
