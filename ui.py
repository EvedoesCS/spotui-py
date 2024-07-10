# ----------------------------------------------- #
# UI will contain functions for rendering
# elements of the Spotui-py User interface
# ----------------------------------------------- #

import curses
from curses import wrapper
import routes
from util import format_to_QI, format_to_min_sec
import auth


class SearchBarWin():
    def __init__(self):
        self.win = curses.newwin(3, (curses.COLS - (curses.COLS // 4)), 0, (curses.COLS // 4))
        self.query = ""

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
                response = f'query={self.query}'
                self.query = ""
                return response
            elif key == 127:
                # Handle 'backspace'
                self.query = self.query[:-1]
                self.render(f'Search: {self.query}')
            elif key == 27:
                # Handle 'ESC'
                self.query = ""
                self.render()
                return f'exit={None}'
            else:
                # Handle valid keypress [a-Z | 0-9 | !@#$%...]
                if chr(key).isprintable():
                    self.query += chr(key)
                    self.render(f'Search: {self.query}')


class ContentWin():
    def __init__(self):
        self.win = curses.newwin((curses.LINES - 7), (curses.COLS - (curses.COLS // 4)), 3, (curses.COLS // 4))
        self.data = []

    def render(self):
        self.win.erase()
        self.win.addstr(1, 1, 'Title')
        self.win.addstr(2, 1, ('-' * (curses.COLS - (curses.COLS // 4))))
        self.win.border()
        self.win.refresh()

    def render_data(self):
        self.render()
        y = 3
        for i in range(len(self.data)):
            self.win.addstr(y, 1, str(self.data[i]))
            y += 1
        self.win.border()
        self.win.refresh()

    def traverse(self):
        highlight = 0

        while True:
            self.render()
            for i in range(len(self.data)):
                if i == highlight:
                    self.win.addstr((i + 3), 1, str(self.data[i]), curses.A_REVERSE)
                else:
                    self.win.addstr((i + 3), 1, str(self.data[i]))

            key = self.win.getch()
            if key == 10:
                # Handle 'Return'
                self.render_data()
                return self.data[highlight]
            elif key == 27:
                # Handle 'ESC'
                self.render_data()
                return None
            elif key == curses.KEY_UP or chr(key) == 'k':
                if highlight != 0:
                    highlight -= 1
            elif key == curses.KEY_DOWN or chr(key) == 'j':
                if highlight != len(self.data):
                    highlight += 1


class LinksWin():
    def __init__(self):
        self.win = curses.newwin((curses.LINES - 4), (curses.COLS // 4), 0, 0)
        self.data = []

    def render(self):
        self.win.border()
        self.win.addstr(1, 1, 'User Playlists Window')
        self.win.refresh()


class TimelineWin():
    def __init__(self):
        self.win = curses.newwin(4, curses.COLS, (curses.LINES - 4), 0)
        self.now_playing = {'name': '', 'artists': [{'name': ''}]}
        self.is_playing = False
        progress_bar = ProgressBar()
        volume_bar = VolumeBar()
        track_info = TrackInfo(self.now_playing)
        media_controls = MediaControls()
        self.components = {
                'progress_bar': progress_bar,
                'volume_bar': volume_bar,
                'track_info': track_info,
                'media_controls': media_controls
                }

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
    def __init__(self):
        self.win = curses.newwin(1, 66, (curses.LINES - 2), ((curses.COLS - 66) // 2))
        self.progress = 0
        self.track_duration = 1
        self._percent_remaining = int((self.progress / self.track_duration) * 100) // 2
        self._progress_bar = f'{format_to_min_sec(self.progress)} [{'=' * self._percent_remaining}{'.' * (50 - self._percent_remaining)}] {format_to_min_sec(self.track_duration)}'

    def render(self):
        self.win.erase()
        self.win.addstr(0, 0, self._progress_bar)
        self.win.refresh()

    def update_progress(self, progress, track_duration):
        self.progress = progress
        self.track_duration = track_duration
        self._percent_remaining = int((self.progress / self.track_duration) * 100) // 2
        self._progress_bar = f'{format_to_min_sec(self.progress)} [{'=' * self._percent_remaining}{'.' * (50 - self._percent_remaining)}] {format_to_min_sec(self.track_duration)}'


class VolumeBar():
    def __init__(self):
        self.win = curses.newwin(1, 18, (curses.LINES - 3), (curses.COLS - 19))
        self.volume = 0
        self._volume_bar = f'[{'-' * (self.volume // 10)}{' ' * (10 - (self.volume // 10))}]'

    def render(self):
        self.win.erase()
        self.win.addstr(0, 0, self._volume_bar)
        self.win.refresh()

    def update_volume(self, volume):
        self.volume = volume
        self._volume_bar = f'[{'-' * (self.volume // 10)}{' ' * (10 - (self.volume // 10))}]{self.volume}%'


class TrackInfo():
    def __init__(self, now_playing):
        self.win = curses.newwin(2, (curses.COLS // 4), (curses.LINES - 3), 1)
        self._track_name = now_playing['name']
        self._artists_names = now_playing['artists']

    def render(self):
        self.win.erase()
        if len(self._track_name) >= (curses.COLS // 4):
            self.win.addstr(0, 0, f'{self._track_name[:(curses.COLS // 4) -4]}...')
        else:
            self.win.addstr(0, 0, self._track_name)

        if len(self._artists_names[0]['name']) >= (curses.COLS // 4):
            self.win.addstr(1, 0, f'{self._artists_names[0]['name'][:(curses.COLS // 4) - 4]}...')
        else:
            self.win.addstr(1, 0, self._artists_names[0]['name'])
        self.win.refresh()

    def update_info(self, now_playing):
        self._track_name = now_playing['name']
        self._artists_names = now_playing['artists']


class MediaControls():
    def __init__(self):
        self.win = curses.newwin(1, 66, (curses.LINES - 3), ((curses.COLS - 66) // 2))
        self.is_playing = False

    def render(self):
        self.win.erase()
        if self.is_playing == True:
            self.win.addstr(0, 22, '\u27F215  \u23EE  \u23F8  \u23ED  15\u27F3')
        else:
            self.win.addstr(0, 22, '\u27F215  \u23EE  \u23F5  \u23ED  15\u27F3')
        self.win.refresh()

    def update_is_playing(self, is_playing):
        self.is_playing = is_playing
