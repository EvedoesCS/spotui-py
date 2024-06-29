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
