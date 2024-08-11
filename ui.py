# ----------------------------------------------- #
# UI will contain functions for rendering
# elements of the Spotui-py User interface
# ----------------------------------------------- #

import curses
import util
from util import Message
from math import ceil


class SearchBarWin():
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.win = curses.newwin(3, (self.x - (self.x // 4)), 0, (self.x // 4))
        self.query = ""

    def update_size(self, y, x):
        self.win.erase()
        self.y = y
        self.x = x
        self.win = curses.newwin(3, (self.x - (self.x // 4)), 0, (self.x // 4))

    def render(self, txt='Search: '):
        self.win.erase()
        self.win.border()
        self.win.addstr(1, 1, txt)
        self.win.refresh()

    def get_query(self):
        while True:
            self.win.move(1, len(f"Search: {self.query}") + 1)
            key = self.win.getch()
            if key == 10:
                # Handle 'return'
                self.render()
                response = self.query
                self.query = ""
                self.focused = False
                return response
            elif key == 127:
                # Handle 'backspace'
                self.query = self.query[:-1]
                self.render(f'Search: {self.query}')
            elif key == 27:
                # Handle 'ESC'
                self.query = ""
                self.focused = False
                self.render()
                return 'esc'
            else:
                # Handle valid keypress [a-Z | 0-9 | !@#$%...]
                if chr(key).isprintable():
                    self.query += chr(key)
                    self.render(f'Search: {self.query}')


class ContentWin():
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.win = curses.newwin((self.y - 7), (self.x - (self.x // 4)), 3, (self.x // 4))
        self.components = {
                'splash_window': SplashWin(y, x),
                'Controls_window': ControlsWin(y, x),
                'Info_window': InfoWin(y, x)
                }

    def update_size(self, y, x):
        self.win.erase()
        self.y = y
        self.x = x
        self.win = curses.newwin((self.y - 7), (self.x - (self.x // 4)), 3, (self.x // 4))
        for component in self.components:
            self.components[component].update_size(y, x)

    def render(self):
        self.win.erase()
        self.win.border()
        self.win.refresh()
        for component in self.components:
            self.components[component].render()


class SplashWin():
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.win = curses.newwin(10, 102, 5, (self.x // 4) * 2)

    def update_size(self, y, x):
        self.win.erase()
        self.y = y
        self.x = x
        self.win = curses.newwin(10, 102, 5, (self.x // 4) * 2)

    def render(self):
        self.win.erase()
        # Splash Text
        self.win.addstr(1, 0, " _    _      _                            _          _____             _         _       ______      ")
        self.win.addstr(2, 0, "| |  | |    | |                          | |        /  ___|           | |       (_)      | ___ \\     ")
        self.win.addstr(3, 0, "| |  | | ___| | ___ ___  _ __ ___   ___  | |_ ___   \\ `--. _ __   ___ | |_ _   _ _ ______| |_/ /   _ ")
        self.win.addstr(4, 0, "| |/\\| |/ _ \\ |/ __/ _ \\| '_ ` _ \\ / _ \\ | __/ _ \\   `--. \\ '_ \\ / _ \\| __| | | | |______|  __/ | | |")
        self.win.addstr(5, 0, "\\  /\\  /  __/ | (_| (_) | | | | | |  __/ | || (_) | /\\__/ / |_) | (_) | |_| |_| | |      | |  | |_| |")
        self.win.addstr(6, 0, " \\/  \\/ \\___|_|\\___\\___/|_| |_| |_|\\___|  \\__\\___/  \\____/| .__/ \\___/ \\__|\\__,_|_|      \\_|   \\__, |")
        self.win.addstr(7, 0, "                                                          | |                                   __/ |")
        self.win.addstr(8, 0, "                                                          |_|                                  |___/ ")
        self.win.refresh()


class ControlsWin():
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.win = curses.newwin(16,
                                 ((self.x) - self.x // 4) // 6,
                                 15,
                                 (self.x // 4) + 2)

    def update_size(self, y, x):
        self.win.erase()
        self.y = y
        self.x = x
        self.win = curses.newwin(16,
                                 ((self.x) - self.x // 4) // 6,
                                 15,
                                 (self.x // 4) + 2)

    def render(self):
        self.win.erase()
        # Controls
        self.win.addstr(1, 3, "-- Controls --")
        self.win.addstr(2, 1, "[q]: Quit")
        self.win.addstr(3, 1, "[s]: Search")
        self.win.addstr(4, 1, "[u]: User")
        self.win.addstr(5, 1, "[c]: Content")
        self.win.addstr(6, 1, "[p]: Play/Pause")
        self.win.addstr(7, 1, "Traversal:")
        self.win.addstr(8, 1, "[j]: Down")
        self.win.addstr(9, 1, "[k]: Up")
        self.win.addstr(10, 1, "[h]: Previous Page")
        self.win.addstr(11, 1, "[l]: Next Page")
        self.win.addstr(12, 1, "[b]: Previous")
        self.win.addstr(13, 1, "[w]: Forward")
        self.win.border()
        self.win.refresh()


class InfoWin():
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.win = curses.newwin(16,
                                 ((self.x) - self.x // 4) - ((self.x) - self.x // 4) // 6,
                                 15,
                                 ((self.x // 4) + 2) + ((self.x) - self.x // 4) // 6 - 4)

    def update_size(self, y, x):
        self.win.erase()
        self.y = y
        self.x = x
        self.win = curses.newwin(16,
                                 ((self.x) - self.x // 4) - ((self.x) - self.x // 4) // 6,
                                 15,
                                 ((self.x // 4) + 2) + ((self.x) - self.x // 4) // 6 - 4)

    def render(self):
        self.win.erase()
        self.win.border()
        self.win.refresh()


class SearchWindow():
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.win = curses.newwin((self.y - 7), (self.x - (self.x // 4)), 3, (self.x // 4))
        self.data = []
        self.max = self.y - 14
        self.current_page = 0
        self.query_phrase = ""

    def update_size(self, y, x):
        self.win.erase()
        self.y = y
        self.x = x
        self.win = curses.newwin((self.y - 7), (self.x - (self.x // 4)), 3, (self.x // 4))

    def render(self):
        self.win.erase()
        y = 4
        start = self.max * self.current_page
        stop = start + self.max
        if len(self.data) - start < self.max:
            stop = start + (len(self.data) - start)
        self.win.addstr(1, 1, f'Showing search results for "{self.query_phrase}" Page:{self.current_page + 1}/{ceil(len(self.data) / self.max)}')
        self.win.addstr(2, 1, f'{'-' * (self.x - (self.x // 4))}')
        self.win.addstr(3, 1, f'{'title'}')
        for i in range(start, stop):
            self.win.addstr(y, 1, str(self.data[i]))
            y += 1
        self.win.border()
        self.win.refresh()

    def traverse(self):
        highlight = 0

        while True:
            self.win.erase()
            self.win.addstr(1, 1, f'Showing search results for "{self.query_phrase}" Page:{self.current_page + 1}/{ceil(len(self.data) / self.max)}')
            self.win.addstr(3, 1, f'{'title'}')
            self.win.addstr(2, 1, f'{'-' * (self.x - (self.x // 4))}')
            self.win.border()
            self.win.refresh()
            y = 4
            start = self.max * self.current_page
            stop = start + self.max
            if len(self.data) - start < self.max:
                stop = start + (len(self.data) - start)
            for i in range(start, stop):
                if (i - start) == highlight:
                    self.win.addstr(y, 1, str(self.data[i]), curses.A_REVERSE)
                    y += 1
                else:
                    self.win.addstr(y, 1, str(self.data[i]))
                    y += 1

            key = self.win.getch()
            if key == 10:
                # Handle 'Return'
                self.render()
                type = self.data[highlight + start].type
                if type == 'track':
                    return Message('track', self.data[highlight + start].id)
                elif type == 'artist':
                    return Message('artist', self.data[highlight + start].id)
                elif type == 'album':
                    return Message('album', self.data[highlight + start].id)
                elif type == 'playlist':
                    return Message('playlist', self.data[highlight + start].id)
            elif key == 27:
                # Handle 'ESC'
                self.render()
                return Message('esc', None)
            elif key == curses.KEY_UP or chr(key) == 'k':
                if highlight != 0:
                    highlight -= 1
            elif key == curses.KEY_DOWN or chr(key) == 'j':
                if highlight != len(self.data):
                    highlight += 1
            elif key == curses.KEY_LEFT or chr(key) == 'h':
                if self.current_page > 0:
                    self.current_page -= 1
            elif key == curses.KEY_RIGHT or chr(key) == 'l':
                if self.current_page + 1 < ceil(len(self.data) / self.max):
                    self.current_page += 1
            elif chr(key) == 'w':
                self.render()
                return Message('next_page', None)
            elif chr(key) == 'b':
                self.render()
                return Message('prev_page', None)


class ArtistWin():
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.win = curses.newwin((self.y - 7), (self.x - (self.x // 4)), 3, (self.x // 4))
        self.data = []

    def update_size(self, y, x):
        self.win.erase()
        self.y = y
        self.x = x
        self.win = curses.newwin((self.y - 7), (self.x - (self.x // 4)), 3, (self.x // 4))

    def render(self):
        self.win.erase()
        y = 4
        self.win.addstr(1, 1, f'{self.data[0]['name']}')
        self.win.addstr(2, 1, f'{self.data[0]['followers']:,}')
        self.win.addstr(3, 1, f'{'-' * (self.x - (self.x // 4))}')
        for i in range(1, len(self.data)):
            if i <= 10:
                self.win.addstr(y, 1, f'{i}. {str(self.data[i])}')
            else:
                self.win.addstr(y, 1, f'{str(self.data[i])}')
            y += 1
        self.win.border()
        self.win.refresh()

    def traverse(self):
        highlight = 1
        max = len(self.data)
        if max > 40:
            max = 40

        while True:
            self.win.erase()
            self.win.addstr(1, 1, f'{self.data[0]['name']}')
            self.win.addstr(2, 1, f'{self.data[0]['followers']:,}')
            self.win.addstr(3, 1, f'{'-' * (self.x - (self.x // 4))}')
            self.win.border()
            self.win.refresh()
            for i in range(1, max):
                if i <= 10:
                    if i == highlight:
                        self.win.addstr((i + 3), 1, f'{i}. {str(self.data[i])}', curses.A_REVERSE)
                    else:
                        self.win.addstr((i + 3), 1, f'{i}. {str(self.data[i])}')
                else:
                    if i == highlight:
                        self.win.addstr((i + 3), 1, f'{str(self.data[i])}', curses.A_REVERSE)
                    else:
                        self.win.addstr((i + 3), 1, f'{str(self.data[i])}')

            key = self.win.getch()
            if key == 10:
                # Handle 'Return'
                self.render()
                type = self.data[highlight].type
                if type == 'track':
                    return Message('track', self.data[highlight].id)
                elif type == 'album':
                    return Message('album', self.data[highlight].id)
            elif key == 27:
                # Handle 'ESC'
                self.render()
                return Message('esc', None)
            elif key == curses.KEY_UP or chr(key) == 'k':
                if highlight != 0:
                    highlight -= 1
            elif key == curses.KEY_DOWN or chr(key) == 'j':
                if highlight != len(self.data):
                    highlight += 1
            elif chr(key) == 'w':
                self.render()
                return Message('next_page', None)
            elif chr(key) == 'b':
                self.render()
                return Message('prev_page', None)


class AlbumWin():
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.win = curses.newwin((self.y - 7), (self.x - (self.x // 4)), 3, (self.x // 4))
        self.data = []

    def update_size(self, y, x):
        self.win.erase()
        self.y = y
        self.x = x
        self.win = curses.newwin((self.y - 7), (self.x - (self.x // 4)), 3, (self.x // 4))

    def render(self):
        self.win.erase()
        y = 4
        self.win.addstr(1, 1, f'{self.data[0]['name']}')
        self.win.addstr(2, 1, f'{self.data[0]['release_date']}')
        self.win.addstr(3, 1, f'{'-' * (self.x - (self.x // 4))}')
        for i in range(1, len(self.data)):
            self.win.addstr(y, 1, str(self.data[i]))
            y += 1
        self.win.border()
        self.win.refresh()

    def traverse(self):
        highlight = 1
        max = len(self.data)
        if max > 40:
            max = 40

        while True:
            self.win.erase()
            self.win.addstr(1, 1, f'{self.data[0]['name']}')
            self.win.addstr(2, 1, f'{self.data[0]['release_date']}')
            self.win.addstr(3, 1, f'{'-' * (self.x - (self.x // 4))}')
            self.win.border()
            self.win.refresh()
            for i in range(1, max):
                if i == highlight:
                    self.win.addstr((i + 3), 1, str(self.data[i]), curses.A_REVERSE)
                else:
                    self.win.addstr((i + 3), 1, str(self.data[i]))

            key = self.win.getch()
            if key == 10:
                # Handle 'Return'
                self.render()
                return Message('play_album', {'id': self.data[0]['id'], 'offset': highlight - 1})
            elif key == 27:
                # Handle 'ESC'
                self.render()
                return Message('esc', None)
            elif key == curses.KEY_UP or chr(key) == 'k':
                if highlight != 0:
                    highlight -= 1
            elif key == curses.KEY_DOWN or chr(key) == 'j':
                if highlight != len(self.data):
                    highlight += 1
            elif chr(key) == 'w':
                self.render()
                return Message('next_page', None)
            elif chr(key) == 'b':
                self.render()
                return Message('prev_page', None)


class PlaylistWin():
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.win = curses.newwin((self.y - 7), (self.x - (self.x // 4)), 3, (self.x // 4))
        self.data = []
        self.max = self.y - 14
        self.current_page = 0

    def update_size(self, y, x):
        self.win.erase()
        self.y = y
        self.x = x
        self.win = curses.newwin((self.y - 7), (self.x - (self.x // 4)), 3, (self.x // 4))

    def render(self):
        self.win.erase()
        y = 4
        start = self.max * self.current_page
        stop = start + self.max
        if len(self.data) - start < self.max:
            stop = start + (len(self.data) - start)
        self.win.addstr(1, 1, f'{self.data[0]['name']}')
        self.win.addstr(2, 1, f'{self.data[0]['total_tracks']} Page:{self.current_page + 1}/{ceil(len(self.data) / self.max)}')
        self.win.addstr(3, 1, f'{'-' * (self.x - (self.x // 4))}')
        for i in range(start + 1, stop):
            self.win.addstr(y, 1, str(self.data[i]))
            y += 1
        self.win.border()
        self.win.refresh()

    def traverse(self):
        highlight = 1

        while True:
            self.win.erase()
            self.win.addstr(1, 1, f'{self.data[0]['name']}')
            self.win.addstr(2, 1, f'{self.data[0]['total_tracks']} Page:{self.current_page + 1}/{ceil(len(self.data) / self.max)}')
            self.win.addstr(3, 1, f'{'-' * (self.x - (self.x // 4))}')
            self.win.border()
            self.win.refresh()
            y = 4
            start = self.max * self.current_page
            stop = start + self.max
            if len(self.data) - start < self.max:
                stop = start + (len(self.data) - start)
            for i in range(start + 1, stop):
                if i == highlight:
                    self.win.addstr(y, 1, str(self.data[i]), curses.A_REVERSE)
                    y += 1
                else:
                    self.win.addstr(y, 1, str(self.data[i]))
                    y += 1

            key = self.win.getch()
            if key == 10:
                # Handle 'Return'
                self.render()
                return Message('play_playlist', {'id': self.data[0]['id'], 'offset': highlight - 1})
            elif key == 27:
                # Handle 'ESC'
                self.render()
                return Message('esc', None)
            elif key == curses.KEY_UP or chr(key) == 'k':
                if highlight != 0:
                    highlight -= 1
            elif key == curses.KEY_DOWN or chr(key) == 'j':
                if highlight != len(self.data):
                    highlight += 1
            elif key == curses.KEY_LEFT or chr(key) == 'h':
                if self.current_page > 0:
                    self.current_page -= 1
            elif key == curses.KEY_RIGHT or chr(key) == 'l':
                if self.current_page + 1 < ceil(len(self.data) / self.max):
                    self.current_page += 1
            elif chr(key) == 'w':
                self.render()
                return Message('next_page', None)
            elif chr(key) == 'b':
                self.render()
                return Message('prev_page', None)


class LibraryWin():
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.win = curses.newwin((self.y - 4), (self.x // 4), 0, 0)
        self.data = []
        self.max = self.y - 10
        self.current_page = 0
        self.filters = ['track', 'album', 'artist', 'playlist']

    def update_size(self, y, x):
        self.win.erase()
        self.y = y
        self.x = x
        self.win = curses.newwin((self.y - 4), (self.x // 4), 0, 0)

    def render(self):
        self.win.erase()
        self.win.addstr(1, 1, '\U0001F56E  Your Library')
        self.win.addstr(2, 1, f'{'-' * (self.x // 4)}')
        y = 3
        start = self.max * self.current_page
        stop = start + self.max
        if len(self.data) - start < self.max:
            stop = start + (len(self.data) - start)
        for i in range(start, stop):
            self.win.addstr(y, 1, str(self.data[i]))
            y += 1
        self.win.border()
        self.win.refresh()

    def traverse(self):
        highlight = 0

        while True:
            self.win.erase()
            self.win.addstr(1, 1, '\U0001F56E  Your Library')
            self.win.addstr(2, 1, f'{'-' * (self.x // 4)}')
            self.win.border()
            self.win.refresh()
            y = 3
            start = self.max * self.current_page
            stop = start + self.max
            if len(self.data) - start < self.max:
                stop = start + (len(self.data) - start)
            for i in range(start, stop):
                if (i - start) == highlight:
                    self.win.addstr(y, 1, str(self.data[i]), curses.A_REVERSE)
                    y += 1
                else:
                    self.win.addstr(y, 1, str(self.data[i]))
                    y += 1

            key = self.win.getch()
            if key == 10:
                # Handle 'Return'
                self.render()
                type = self.data[highlight + start].type
                if type == 'track':
                    return Message('track', self.data[highlight + start].id)
                elif type == 'artist':
                    return Message('artist', self.data[highlight + start].id)
                elif type == 'album':
                    return Message('album', self.data[highlight + start].id)
                elif type == 'playlist':
                    return Message('playlist', self.data[highlight + start].id)
            elif key == 27:
                # Handle 'ESC'
                self.render()
                return Message('esc', None)
            elif key == curses.KEY_UP or chr(key) == 'k':
                if highlight != 0:
                    highlight -= 1
            elif key == curses.KEY_DOWN or chr(key) == 'j':
                if highlight != len(self.data):
                    highlight += 1
            elif key == curses.KEY_LEFT or chr(key) == 'h':
                if self.current_page > 0:
                    self.current_page -= 1
            elif key == curses.KEY_RIGHT or chr(key) == 'l':
                if self.current_page + 1 < ceil(len(self.data) / self.max):
                    self.current_page += 1
            elif chr(key) == 'w':
                self.render()
                return Message('next_page', None)
            elif chr(key) == 'b':
                self.render()
                return Message('prev_page', None)


class TimelineWin():
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.win = curses.newwin(4, self.x, (self.y - 4), 0)
        self.now_playing = {'name': '', 'artists': [{'name': ''}]}
        self.is_playing = False
        self.components = {
                'progress_bar': ProgressBar(y, x),
                'volume_bar': VolumeBar(y, x),
                'track_info': TrackInfo(y, x, self.now_playing),
                'media_controls': MediaControls(y, x)
                }

    def update_size(self, y, x):
        self.win.erase()
        self.y = y
        self.x = x
        self.win = curses.newwin(4, self.x, (self.y - 4), 0)
        for component in self.components:
            self.components[component].update_size(y, x)

    def render(self):
        self.win.erase()
        self.win.border()
        self.win.refresh()
        for component in self.components:
            self.components[component].render()

    def update_vars(self, now_playing, is_playing, volume, progress):
        self.now_playing = now_playing
        self.is_playing = is_playing

        self.components['progress_bar'].update_progress(progress, (now_playing['duration_ms'] // 1000))
        self.components['volume_bar'].update_volume(volume)
        self.components['track_info'].update_info(self.now_playing)
        self.components['media_controls'].update_is_playing(is_playing)
        self.render()


class ProgressBar():
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.win = curses.newwin(1, 66, (self.y - 2), ((self.x - 66) // 2))
        self.progress = 0
        self.track_duration = 1
        self._percent_remaining = int((self.progress / self.track_duration) * 100) // 2
        self._progress_bar = f'{util.format_to_min_sec(self.progress)} [{'=' * self._percent_remaining}{'.' * (50 - self._percent_remaining)}] {util.format_to_min_sec(self.track_duration)}'

    def update_size(self, y, x):
        self.win.erase()
        self.y = y
        self.x = x
        self.win = curses.newwin(1, 66, (self.y - 2), ((self.x - 66) // 2))

    def render(self):
        self.win.erase()
        self.win.addstr(0, 0, self._progress_bar)
        self.win.refresh()

    def update_progress(self, progress, track_duration):
        self.progress = progress
        self.track_duration = track_duration
        self._percent_remaining = int((self.progress / self.track_duration) * 100) // 2
        self._progress_bar = f'{util.format_to_min_sec(self.progress)} [{'=' * self._percent_remaining}{'.' * (50 - self._percent_remaining)}] {util.format_to_min_sec(self.track_duration)}'


class VolumeBar():
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.win = curses.newwin(1, 18, (self.y - 3), (self.x - 20))
        self.volume = 0
        self._volume_bar = f'[{'=' * (self.volume // 10)}{' ' * (10 - (self.volume // 10))}]'

    def update_size(self, y, x):
        self.win.erase()
        self.y = y
        self.x = x
        self.win = curses.newwin(1, 18, (self.y - 3), (self.x - 20))

    def render(self):
        self.win.erase()
        self.win.addstr(0, 0, self._volume_bar)
        self.win.refresh()

    def update_volume(self, volume):
        self.volume = volume
        self._volume_bar = f'[{'=' * (self.volume // 10)}{' ' * (10 - (self.volume // 10))}]{self.volume}%'


class TrackInfo():
    def __init__(self, y, x, now_playing):
        self.y = y
        self.x = x
        self.win = curses.newwin(2, (self.x // 4), (self.y - 3), 1)
        self._track_name = now_playing['name']
        self._artists_names = now_playing['artists']

    def update_size(self, y, x):
        self.win.erase()
        self.y = y
        self.x = x
        self.win = curses.newwin(2, (self.x // 4), (self.y - 3), 1)

    def render(self):
        self.win.erase()
        if len(self._track_name) >= (self.x // 4):
            self.win.addstr(0, 0, f'{self._track_name[:(self.x // 4) -4]}...', curses.A_BOLD)
        else:
            self.win.addstr(0, 0, self._track_name, curses.A_BOLD)

        if len(self._artists_names[0]['name']) >= (self.x // 4):
            self.win.addstr(1, 0, f'{self._artists_names[0]['name'][:(self.x // 4) - 4]}...', curses.A_ITALIC)
        else:
            self.win.addstr(1, 0, self._artists_names[0]['name'], curses.A_ITALIC)
        self.win.refresh()

    def update_info(self, now_playing):
        self._track_name = now_playing['name']
        self._artists_names = now_playing['artists']


class MediaControls():
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.win = curses.newwin(1, 66, (self.y - 3), ((self.x - 66) // 2))
        self.is_playing = False

    def update_size(self, y, x):
        self.win.erase()
        self.y = y
        self.x = x
        self.win = curses.newwin(1, 66, (self.y - 3), ((self.x - 66) // 2))

    def render(self):
        self.win.erase()
        if self.is_playing == True:
            self.win.addstr(0, 22, '\u27F215  \u23EE  \u23F8  \u23ED  15\u27F3', curses.A_BOLD)
        else:
            self.win.addstr(0, 22, '\u27F215  \u23EE  \u23F5  \u23ED  15\u27F3', curses.A_BOLD)
        self.win.refresh()

    def update_is_playing(self, is_playing):
        self.is_playing = is_playing
