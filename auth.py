# ----------------------------------------------- #
# Program: To generate an oauth token with PKCE
# ----------------------------------------------- #

import base64
import pkce
import webbrowser
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
from datetime import datetime, timedelta
import requests
import json


path = []
class CallbackServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

        self.wfile.write(bytes("<html><body><h1>You may now close this page :)</h1></body></html>", "utf-8"))
        path.append(self.path.split('='))


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


HOST = '127.0.0.1'
PORT = 8080
config = read_config()
client_id = config['client_id']
client_secret = config['client_secret']
redirect_uri = 'http://localhost:8080'
scope = 'user-read-private user-read-email user-modify-playback-state user-read-playback-state'
url = 'https://accounts.spotify.com/authorize'
code_verifier, code_challenge = pkce.generate_pkce_pair(43)


def get_access_code():
    params = {
            'response_type': 'code',
            'client_id': client_id,
            'scope': scope,
            'code_challenge_method': 'S256',
            'code_challenge': code_challenge,
            'redirect_uri': redirect_uri

        }

    webbrowser.open(url + '?' + urllib.parse.urlencode(params))

    server = HTTPServer((HOST, PORT), CallbackServer)
    while True:
        server.handle_request()
        if path != []:
            os.system("clear")
            break
    return path[0][1]


def set_token(code):
    """ Sets the enviroment variable 'spotui_token' equal to token retrieved
        from the /api/token endpoint """

    headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
            }

    data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'code_verifier': code_verifier
            }

    r = requests.post('https://accounts.spotify.com/api/token', data=data, headers=headers)
    token = json.loads(r.content)['access_token']
    os.environ['spotui_token'] = token


def refresh_token(access_token):
    headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': base64.b64encode(f"{client_id}:{client_secret}".encode())
            }

    data = {
            'grant_type': 'refresh_token',
            'refresh_token': access_token,
            'client_id': client_id
            }

    r = requests.post('https://accounts.spotify.com/api/token', data=data, headers=headers)
    token = json.loads(r.content)['access_token']
    os.environ['spotui_token'] = token


def authenticate():
    try:
        token = os.environ['spotui_token']
    except KeyError:
        token = None
    while token == None:
        set_token(get_access_code())
        token = os.environ['spotui_token']


    return token