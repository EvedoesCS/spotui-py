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


def parse_dict_r(r: dict):
    for item in r['tracks']['items']:
        print(f"Track name: {item['name']} by {item['artists'][0]['name']}")
        print(f"Track ID: {item['id']}")
        print()


def play(token: str, id: str, context='track') -> int:
    headers = {
            'device_id': get_devices(token)[0]['id'],
            'Authorization': f"Bearer {token}",
            'Content-Type': 'application/json'
            }
    data = {
            'uris': [f"spotify:track:{id}"],
            'position_ms': 0
            }

    url = 'https://api.spotify.com/v1/me/player/play'

    r = requests.put(url, headers=headers, data=json.dumps(data))
    return r.status_code


def pause(token: str) -> int:
    headers = {
            'Authorization': f"Bearer {token}",
            'device_id': get_devices(token)[0]['id']
            }

    url = 'https://api.spotify.com/v1/me/player/pause'

    r = requests.put(url, headers=headers)
    return r.status_code


def get_devices(token: str) -> list:
    headers = {
            'Authorization': f"Bearer {token}"
            }
    endpoint = 'https://api.spotify.com/v1/me/player/devices'

    r = requests.get(endpoint, headers=headers)
    return json.loads(r.content)['devices']
