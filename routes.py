# ----------------------------------------------- #
# Routes for retrieving data from the Spotify-api
# ----------------------------------------------- #

from auth import read_config
import requests
import urllib.parse
import json

config = read_config()
client_id, client_secret = config['client_id'], config['client_secret']


def search(token: str, query: str) -> dict:
    headers = {
            'Authorization': f'Bearer {token}'
        }

    data = {
            'q': query,
            'type': 'track'
            }

    endpoint = 'https://api.spotify.com/v1/search'

    url = endpoint + '?' + urllib.parse.urlencode(data)

    r = requests.get(url, headers=headers)
    r_dict = json.loads(r.content)
    return (r_dict)


def play(token: str, id: str, context='track', position_ms=0) -> int:
    r = get_devices(token)
    if type(r) is int:
        print(r)
    else:
        device_id = r['devices'][0]['id']
        headers = {
                'device_id': device_id,
                'Authorization': f"Bearer {token}",
                'Content-Type': 'application/json'
                }
        data = {
                'uris': [f"spotify:track:{id}"],
                'position_ms': position_ms
                }

        url = 'https://api.spotify.com/v1/me/player/play'

        r = requests.put(url, headers=headers, data=json.dumps(data))
        return r.status_code


def pause(token: str) -> int:
    headers = {
            'Authorization': f"Bearer {token}",
            'device_id': get_devices(token)['devices'][0]['id']
            }

    url = 'https://api.spotify.com/v1/me/player/pause'

    r = requests.put(url, headers=headers)
    return r.status_code


def next(token: str) -> int:
    headers = {
            'Authorization': f"Bearer {token}",
            'device_id': get_devices(token)['devices'][0]['id']
            }

    url = 'https://api.spotify.com/v1/me/player/next'

    r = requests.put(url, headers=headers)
    return r.status_code


def back(token: str) -> int:
    headers = {
            'Authorization': f"Bearer {token}",
            'device_id': get_devices(token)['devices'][0]['id']
            }

    url = 'https://api.spotify.com/v1/me/player/previous'

    r = requests.put(url, headers=headers)
    return r.status_code


def get_devices(token: str) -> list:
    headers = {
            'Authorization': f"Bearer {token}"
            }
    endpoint = 'https://api.spotify.com/v1/me/player/devices'

    r = requests.get(endpoint, headers=headers)
    if r.status_code == 200:
        return json.loads(r.content)
    else:
        return r.status_code


def get_playback_state(token: str) -> dict:
    headers = {
            'Authorization': f"Bearer {token}"
            }

    endpoint = 'https://api.spotify.com/v1/me/player'

    r = requests.get(endpoint, headers=headers)
    if r.status_code == 200:
        return json.loads(r.content)
    else:
        return r.status_code


def transfer_playback(token: str) -> int:
    headers = {
            'Authorization': f"Bearer {token}"
            }

    data = {
            'device_ids': [get_devices(token)['devices'][0]['id']]
            }

    url = 'https://api.spotify.com/v1/me/player'

    r = requests.put(url, headers=headers, data=json.dumps(data))
    return r.status_code
