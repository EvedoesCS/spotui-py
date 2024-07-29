# ----------------------------------------------- #
# Routes for retrieving data from the Spotify-api
# ----------------------------------------------- #

from auth import read_config
import requests
import urllib.parse
import json

config = read_config()
client_id, client_secret = config['client_id'], config['client_secret']


def get_users_profile(token: str) -> int:
    headers = {
            'Authorization': f"Bearer {token}",
            }

    url = 'https://api.spotify.com/v1/me'

    r = requests.get(url, headers=headers)
    return r.status_code


def search(token: str, query: str) -> dict:
    headers = {
            'Authorization': f'Bearer {token}'
        }

    data = {
            'q': query,
            'type': 'album,artist,track'
            }

    endpoint = 'https://api.spotify.com/v1/search'

    url = endpoint + '?' + urllib.parse.urlencode(data)

    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return json.loads(r.content)
    else:
        return r.status_code


def play(token: str, id, context='track', position_ms=0) -> int:
    headers = {
            'device_id': get_devices(token)['devices'][0]['id'],
            'Authorization': f"Bearer {token}",
            'Content-Type': 'application/json'
            }

    data = {
            'uris': [f'spotify:track:{id}'],
            'position_ms': position_ms
            }

    url = 'https://api.spotify.com/v1/me/player/play'

    r = requests.put(url, headers=headers, data=json.dumps(data))
    return r.status_code


def resume(token: str, position_ms: int) -> int:
    queue = get_users_queue(token)
    uris = []

    headers = {
            'device_id': get_devices(token)['devices'][0]['id'],
            'Authorization': f"Bearer {token}",
            'Content-Type': 'application/json'
            }

    uris.append(f'spotify:track:{queue['currently_playing']['id']}')
    for track in queue['queue']:
        uris.append(f'spotify:track:{track['id']}')

    data = {
            'uris': uris,
            'position_ms': position_ms
            }

    url = 'https://api.spotify.com/v1/me/player/play'

    r = requests.put(url, headers=headers, data=json.dumps(data))

    return r.status_code


def play_album(token: str, id, offset: int) -> int:
    headers = {
            'device_id': get_devices(token)['devices'][0]['id'],
            'Authorization': f"Bearer {token}",
            'Content-Type': 'application/json'
            }

    data = {
            'context_uri': f'spotify:album:{id}',
            'offset': {
                'position': offset
                },
            'position_ms': 0
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


def get_users_queue(token) -> int:
    headers = {
            'Authorization': f"Bearer {token}"
            }

    url = 'https://api.spotify.com/v1/me/player/queue'

    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return json.loads(r.content)
    else:
        return r.status_code


def add_item_to_playback_queue(token: str, track: str) -> int:
    headers = {
            'Authorization': f"Bearer {token}"
            }

    data = {
            'uri': track
            }

    endpoint = 'https://api.spotify.com/v1/me/player/queue'

    url = endpoint + '?' + urllib.parse.urlencode(data)

    r = requests.post(url, headers=headers)

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


def get_artist(token: str, id: str) -> dict:
    headers = {
            'Authorization': f"Bearer {token}"
            }

    url = f'https://api.spotify.com/v1/artists/{id}'

    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return json.loads(r.content)
    else:
        return r.status_code


def get_artists_top_tracks(token: str, id: str) -> dict:
    headers = {
            'Authorization': f"Bearer {token}"
            }

    url = f'https://api.spotify.com/v1/artists/{id}/top-tracks'

    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return json.loads(r.content)
    else:
        return r.status_code


def get_artists_albums(token: str, id: str) -> dict:
    headers = {
            'Authorization': f"Bearer {token}"
            }
    data = {
            'include_groups': 'album,single,compilation'
            }

    endpoint = f'https://api.spotify.com/v1/artists/{id}/albums'
    url = endpoint + '?' + urllib.parse.urlencode(data)

    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return json.loads(r.content)
    else:
        return r.status_code


def get_album(token: str, id: str) -> dict:
    headers = {
            'Authorization': f"Bearer {token}"
            }

    url = f'https://api.spotify.com/v1/albums/{id}'

    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return json.loads(r.content)
    else:
        return r.status_code


def get_album_tracks(token: str, id: str) -> dict:
    headers = {
            'Authorization': f"Bearer {token}"
            }

    url = f'https://api.spotify.com/v1/albums/{id}/tracks'

    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return json.loads(r.content)
    else:
        return r.status_code
