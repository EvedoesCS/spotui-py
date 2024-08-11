# -------------------------------- #
# Utility functions for spotui-py
# -------------------------------- #

class Queue():
    def __init__(self):
        self.items = []

    def isempty(self):
        return not self.items

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def peek(self):
        return self.items[0]


class Message():
    def __init__(self, header, body):
        self.header = header
        self.body = body


class Track():
    def __init__(self, album, artists, disc_number, duration_ms, id, name, track_number):
        self.album = album
        self.artists = artists
        self.disc_number = disc_number
        self.duration_ms = duration_ms
        self.id = id
        self.name = name
        self.track_number = track_number
        self.type = 'track'

    def __str__(self):
        return f'{self.name} by {self.artists}'


class Artist():
    def __init__(self, id, name, popularity, followers, genres):
        self.id = id
        self.name = name
        self.popularity = popularity
        self.followers = followers
        self.genres = genres
        self.type = 'artist'

    def __str__(self):
        return self.name


class Album():
    def __init__(self, album_type, artists, id, name, release_date, total_tracks):
        self.album_type = album_type
        self.artists = artists
        self.id = id
        self.name = name
        self.release_date = release_date
        self.total_tracks = total_tracks
        self.type = 'album'

    def __str__(self):
        return f'{self.name} by {self.artists} {self.release_date}'


class Playlist():
    def __init__(self, id, name, owner_name, total_tracks):
        self.id = id
        self.name = name
        self.owner_name = owner_name
        self.total_tracks = total_tracks
        self.type = 'playlist'

    def __str__(self):
        return f'{self.name} by {self.owner_name}'


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


def format_as_search_result(raw_data: dict) -> list:
    data = []

    for track in raw_data['tracks']['items']:
        data.append(Track(track['album']['name'],
                          track['artists'][0]['name'],
                          track['disc_number'],
                          track['duration_ms'],
                          track['id'],
                          track['name'],
                          track['track_number']))

    for artist in raw_data['artists']['items']:
        data.append(Artist(artist['id'],
                           artist['name'],
                           artist['popularity'],
                           artist['followers']['total'],
                           artist['genres']))

    for album in raw_data['albums']['items']:
        data.append(Album(album['album_type'],
                          album['artists'][0]['name'],
                          album['id'],
                          album['name'],
                          album['release_date'],
                          album['total_tracks']))

    for playlist in raw_data['playlists']['items']:
        data.append(Playlist(playlist['id'],
                             playlist['name'],
                             playlist['owner']['display_name'],
                             playlist['tracks']['total']))

    return data


def format_artist(artist: dict, tracks: list, albums: dict) -> list:
    data = []

    data.append({'name': artist['name'], 'followers': artist['followers']['total']})

    for track in tracks['tracks']:
        data.append(Track(track['album']['name'],
                          track['artists'][0]['name'],
                          track['disc_number'],
                          track['duration_ms'],
                          track['id'],
                          track['name'],
                          track['track_number']))

    for album in albums['items']:
        data.append(Album(album['album_type'],
                          album['artists'][0]['name'],
                          album['id'],
                          album['name'],
                          album['release_date'],
                          album['total_tracks']))

    return data


def format_album(album: dict, tracks: list) -> list:
    data = []

    data.append({'name': album['name'], 'release_date': album['release_date'], 'id': album['id']})

    for track in tracks['items']:
        data.append(Track(album['name'],
                          track['artists'][0]['name'],
                          track['disc_number'],
                          track['duration_ms'],
                          track['id'],
                          track['name'],
                          track['track_number']))

    return data


def format_playlist(playlist: dict, tracks: list) -> list:
    data = []

    data.append({'name': playlist['name'], 'total_tracks': playlist['tracks']['total'], 'id': playlist['id']})

    for track in tracks['items']:
        data.append(Track(track['track']['album']['name'],
                          track['track']['artists'][0]['name'],
                          track['track']['disc_number'],
                          track['track']['duration_ms'],
                          track['track']['id'],
                          track['track']['name'],
                          track['track']['track_number']))

    return data


def format_users_library(user: dict, playlists: dict, albums: dict, artists: dict, tracks: dict) -> list:
    data = []

    if type(tracks) is not int:
        for track in tracks['items']:
            data.append(Track(track['track']['album']['name'],
                              track['track']['artists'][0]['name'],
                              track['track']['disc_number'],
                              track['track']['duration_ms'],
                              track['track']['id'],
                              track['track']['name'],
                              track['track']['track_number']))

    if type(playlists) is not int:
        for playlist in playlists['items']:
            data.append(Playlist(playlist['id'],
                                 playlist['name'],
                                 playlist['owner']['display_name'],
                                 playlist['tracks']['total']))

    if type(artists) is not int:
        for artist in artists['artists']['items']:
            data.append(Artist(artist['id'],
                               artist['name'],
                               artist['popularity'],
                               artist['followers']['total'],
                               artist['genres']))

    if type(albums) is not int:
        for album in albums['items']:
            data.append(Album(album['album']['album_type'],
                              album['album']['artists'][0]['name'],
                              album['album']['id'],
                              album['album']['name'],
                              album['album']['release_date'],
                              album['album']['total_tracks']))

    return data


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
