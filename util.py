# -------------------------------- #
# Utility functions for spotui-py
# -------------------------------- #


class QueryItem:
    def __init__(self, id, name, artists, album, duration_ms):
        self.id = id
        self.name = name
        self.artists = artists
        self.album = album
        self.duration_ms = int(duration_ms) / 60000

    def __repr__(self):
        print("id, name, artists, album, duration_ms")

    def __str__(self):
        return f"{self.name:<} by {self.artists['name']}"


def format_to_QI(raw_data: dict) -> list:
    # Converts a dict of json data into a list of QueryItem objects
    data = []

    for item in raw_data['tracks']['items']:
        data.append(QueryItem(item['id'], item['name'], item['artists'][0], item['album'], item['duration_ms']))

    return data


def read_config():
    """
    Reads client_id and client_secret from the config file
    """
    try:
        file = open("config", 'r')
    except:
        print("Error config file is missing")

    lines = file.readlines()
    config = {}
    for line in lines:
        line = line.strip().split('=')
        config[line[0]] = line[1]

    return config


def format_to_min_sec(num: int) -> str:
    # Converts a number of seconds into a string of min:sec
    min = str(num // 60)
    sec = str(num % 60)
    if len(sec) < 2:
        sec = '0' + sec
    return f'{min}:{sec}'


def round_up(num: int) -> int:
    if num - int(num) != 0:
        return int(num) + 1
    else:
        return num
