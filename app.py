# --------------------------------- #
# Application class which runs the
# main event loop
# --------------------------------- #


import threading
import curses
from curses import wrapper
from time import sleep

import auth
import routes
import ui
import util
from util import Queue, Message


class App():
    def __init__(self, win):
        self.win = win
        self.token = auth.authenticate()
        self.message_queue = Queue()
        self.history = [{
                'search_bar': ui.SearchBarWin(),
                'content_window': ui.ContentWin(),
                'links_window': ui.LinksWin(),
                'timeline_bar': ui.TimelineWin()
                }]
        self.history_index = 0

        # Application State Variables
        self.runtime = 0
        self.focused = False
        self.playback_state = routes.get_playback_state(self.token)

    # T1 Methods

    def event_handler(self):
        self.win.nodelay(True)
        new_message = Message(None, None)
        # Iterates over event sites and checks for unhandled events
        while new_message.header != 'exit':
            sleep(0.33)
            self.runtime += 0.33
            if self.runtime >= 1800:
                self.token = auth.authenticate()
            self.playback_state = routes.get_playback_state(self.token)
            self.message_queue.enqueue(Message('update_timeline', None))

            if not self.focused:
                key = self.win.getch()
                if key != -1:
                    new_message = self.handle_key(key)
                    if new_message.header != 'err':
                        self.message_queue.enqueue(new_message)

        routes.pause(self.token)

    def handle_key(self, key):
        # Handler assembles and returns message objects based on key events
        if chr(key) == 'q':
            return Message('exit', None)
        elif chr(key) == 's':
            return Message('search', None)
        elif chr(key) == 'c':
            return Message('traverse', self.find_traversable())
        elif chr(key) == 'p':
            if self.playback_state['is_playing'] == True:
                return Message('pause', None)
            else:
                return Message('resume', None)

        return Message('err', None)

    # T2 Methods

    # Handler Methods

    def search(self):
        self.focused = True
        query = self.history[self.history_index]['search_bar'].get_query()
        self.focused = False
        if query != 'esc':
            r = routes.search(self.token, query)
            return [query, r]
        else:
            return ['esc', None]

    def find_traversable(self):
        for component in self.history[self.history_index]:
            if component in ['search_window', 'artist_window', 'album_window']:
                window_obj = self.history[self.history_index][component]

        return window_obj

    def traverse(self, message: Message):
        self.focused = True
        r = message.body.traverse()
        self.focused = False
        if r.header == 'track':
            self.message_queue.enqueue(Message('play_track', r.body))
            return Message('ok', None)
        elif r.header == 'artist':
            self.message_queue.enqueue(Message('load_artist', r.body))
            return Message('ok', None)
        elif r.header == 'album':
            self.message_queue.enqueue(Message('load_album', r.body))
            return Message('ok', None)
        elif r.header == 'play_album':
            self.message_queue.enqueue(Message('play_album', r.body))
            return Message('ok', None)
        elif r.header == 'next_page':
            self.message_queue.enqueue(Message('load_next_history', None))
            return Message('ok', None)
        elif r.header == 'prev_page':
            self.message_queue.enqueue(Message('load_prev_history', None))
            return Message('ok', None)

        return Message('esc', None)

    def play(self, id):
        r = routes.play(self.token, id)
        if r == 200:
            return Message('ok', r)
        else:
            return Message('err', r)

    def play_album(self, data):
        r = routes.play_album(self.token, data['id'], data['offset'])
        if r == 200:
            return Message('ok', r)
        else:
            return Message('err', r)

    def pause(self):
        r = routes.pause(self.token)
        if r == 200:
            return Message('ok', r)
        else:
            return Message('err', r)

    def resume(self):
        r = routes.resume(self.token, self.playback_state['progress_ms'])
        if r == 200:
            return Message('ok', r)
        else:
            return Message('err', r)

    def update_timeline(self):
        self.history[self.history_index]['timeline_bar'].update_vars(self.playback_state['item'],
                                                    self.playback_state['is_playing'],
                                                    self.playback_state['device']['volume_percent'],
                                                    self.playback_state['progress_ms'] // 1000)

    def load_artist(self, id):
        tracks = routes.get_artists_top_tracks(self.token, id)
        albums = routes.get_artists_albums(self.token, id)
        artist = routes.get_artist(self.token, id)
        data = util.format_artist(artist, tracks, albums)

        return Message('artist_window', data)

    def load_album(self, id):
        tracks = routes.get_album_tracks(self.token, id)
        album = routes.get_album(self.token, id)
        data = util.format_album(album, tracks)

        return Message('album_window', data)

    # Main Methods

    def handle_msg(self, message: Message):
        # Keybind Related Messages
        if message.header == 'search':
            r = self.search()
            if r[0] == 'esc':
                return Message('esc', None)
            elif r[0] == 'err':
                return Message('err', None)
            else:
                return Message('search_window', r)

        # Traverse Related Messages
        elif message.header == 'traverse':
            r = self.traverse(message)
            if r.header == 'artist':
                self.message_queue.enqueue(Message('load_artist', r.body))
            elif r.header == 'album':
                self.message_queue.enqueue(Message('load_album', r.body))

            return Message('ok', None)

        # History Related Messages
        elif message.header == 'load_next_history':
            if self.history_index != len(self.history):
                self.history_index += 1
            self.message_queue.enqueue(Message('traverse', self.find_traversable()))
            return Message('history_updated', None)

        elif message.header == 'load_prev_history':
            if self.history_index != 0:
                self.history_index -= 1
            self.message_queue.enqueue(Message('traverse', self.find_traversable()))
            return Message('history_updated', None)

        # Route Related Messages
        elif message.header == 'play_track':
            r = self.play(message.body)
            return r
        elif message.header == 'pause':
            r = self.pause()
            return r
        elif message.header == 'resume':
            r = self.resume()
            return r
        elif message.header == 'play_album':
            r = self.play_album(message.body)
            return r

        # UI Related Messages
        elif message.header == 'update_timeline':
            self.update_timeline()
            return Message('updated_timeline', self.history[self.history_index]['timeline_bar'])

        elif message.header == 'load_artist':
            r = self.load_artist(message.body)
            return r

        elif message.header == 'load_album':
            r = self.load_album(message.body)
            return r

    def add_to_history(self, components):
        slice = self.history[:self.history_index + 1]
        self.history = slice

        self.history.append(components)
        self.history_index += 1

    def build_model(self, data):
        if data.header == 'search_window':
            components = {
                    'search_bar': ui.SearchBarWin(),
                    'search_window': ui.SearchWindow(),
                    'links_window': ui.LinksWin(),
                    'timeline_bar': ui.TimelineWin()
                    }
            self.add_to_history(components)
            self.history[self.history_index]['search_window'].data = util.format_as_search_result(data.body[1])
            self.history[self.history_index]['search_window'].query_phrase = data.body[0]
            self.message_queue.enqueue(Message('traverse', self.find_traversable()))

            return Message('search_updated', None)

        elif data.header == 'updated_timeline':
            return Message('update', data.body)

        elif data.header == 'artist_window':
            components = {
                    'search_bar': ui.SearchBarWin(),
                    'artist_window': ui.ArtistWin(),
                    'links_window': ui.LinksWin(),
                    'timeline_bar': ui.TimelineWin()
                    }
            self.add_to_history(components)
            self.history[self.history_index]['artist_window'].data = data.body
            self.message_queue.enqueue(Message('traverse', self.find_traversable()))

            return Message('artist_updated', None)

        elif data.header == 'album_window':
            components = {
                    'search_bar': ui.SearchBarWin(),
                    'album_window': ui.AlbumWin(),
                    'links_window': ui.LinksWin(),
                    'timeline_bar': ui.TimelineWin()
                    }
            self.add_to_history(components)
            self.history[self.history_index]['album_window'].data = data.body
            self.message_queue.enqueue(Message('traverse', self.find_traversable()))

            return Message('album_updated', None)

        else:
            return Message('full_refresh', None)

    def render_model(self, model, item='full_refresh'):
        if item == 'full_refresh':
            for component in model:
                model[component].render()
        else:
            item.render()

        self.win.refresh()

    def message_dispatcher(self):
        message = Message(None, None)
        while message.header != 'exit':
            if not self.message_queue.isempty():
                message = self.message_queue.dequeue()
                data = self.handle_msg(message)
                if data.header != 'err' and data.header != 'esc':
                    r = self.build_model(data)
                if r.header == 'update':
                    self.render_model(self.history[self.history_index], item=r.body)
                else:
                    self.render_model(self.history[self.history_index])

    def run(self):
        self.render_model(self.history[self.history_index])
        t1 = threading.Thread(target=self.event_handler)
        t2 = threading.Thread(target=self.message_dispatcher)

        t1.start()
        t2.start()

        t1.join()
        t2.join()


def main(win):
    app = App(win)
    app.run()


if __name__ == "__main__":
    win = curses.initscr()
    wrapper(main)
