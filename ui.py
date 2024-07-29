# ----------------------------------------------- #
# UI will contain functions for rendering
# elements of the Spotui-py User interface
# ----------------------------------------------- #

import curses
import util
from util import Message


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
    def __init__(self):
        self.win = curses.newwin((curses.LINES - 7), (curses.COLS - (curses.COLS // 4)), 3, (curses.COLS // 4))
        self.data = []
        self.win_type = 'init'

    def render(self):
        self.win.erase()
        self.win.border()
        self.win.refresh()


class SearchWindow():
    def __init__(self):
        self.win = curses.newwin((curses.LINES - 7), (curses.COLS - (curses.COLS // 4)), 3, (curses.COLS // 4))
        self.data = []
        self.query_phrase = ""

    def render(self):
        self.win.erase()
        y = 4
        max = len(self.data)
        if max > 40:
            max = 40
        self.win.addstr(1, 1, f'Showing search results for "{self.query_phrase}"')
        self.win.addstr(2, 1, f'{'-' * (curses.COLS - (curses.COLS // 4))}')
        self.win.addstr(3, 1, f'{'title'}')
        for i in range(max):
            self.win.addstr(y, 1, str(self.data[i]))
            y += 1
        self.win.border()
        self.win.refresh()

    def traverse(self):
        highlight = 0
        max = len(self.data)
        if max > 40:
            max = 40

        while True:
            self.win.erase()
            self.win.addstr(1, 1, f'Showing search results for "{self.query_phrase}"')
            self.win.addstr(3, 1, f'{'title'}')
            self.win.addstr(2, 1, f'{'-' * (curses.COLS - (curses.COLS // 4))}')
            self.win.border()
            self.win.refresh()
            for i in range(max):
                if i == highlight:
                    self.win.addstr((i + 4), 1, str(self.data[i]), curses.A_REVERSE)
                else:
                    self.win.addstr((i + 4), 1, str(self.data[i]))

            key = self.win.getch()
            if key == 10:
                # Handle 'Return'
                self.win.erase()
                self.win.addstr(1, 1, f'Showing search results for "{self.query_phrase}"')
                self.win.addstr(3, 1, f'{'title'}')
                self.win.addstr(2, 1, f'{'-' * (curses.COLS - (curses.COLS // 4))}')
                self.win.border()
                self.win.refresh()
                type = self.data[highlight].type
                if type == 'track':
                    return Message('track', self.data[highlight].id)
                elif type == 'artist':
                    return Message('artist', self.data[highlight].id)
                elif type == 'album':
                    return Message('album', self.data[highlight].id)
            elif key == 27:
                # Handle 'ESC'
                self.win.erase()
                self.win.addstr(1, 1, f'Showing search results for "{self.query_phrase}"')
                self.win.addstr(3, 1, f'{'title'}')
                self.win.addstr(2, 1, f'{'-' * (curses.COLS - (curses.COLS // 4))}')
                self.win.border()
                self.win.refresh()
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


class ArtistWin():
    def __init__(self):
        self.win = curses.newwin((curses.LINES - 7), (curses.COLS - (curses.COLS // 4)), 3, (curses.COLS // 4))
        self.data = []

    def render(self):
        self.win.erase()
        y = 4
        self.win.addstr(1, 1, f'{self.data[0]['name']}')
        self.win.addstr(2, 1, f'{self.data[0]['followers']}')
        self.win.addstr(3, 1, f'{'-' * (curses.COLS - (curses.COLS // 4))}')
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
            self.win.addstr(2, 1, f'{self.data[0]['followers']}')
            self.win.addstr(3, 1, f'{'-' * (curses.COLS - (curses.COLS // 4))}')
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
    def __init__(self):
        self.win = curses.newwin((curses.LINES - 7), (curses.COLS - (curses.COLS // 4)), 3, (curses.COLS // 4))
        self.data = []

    def render(self):
        self.win.erase()
        y = 4
        self.win.addstr(1, 1, f'{self.data[0]['name']}')
        self.win.addstr(2, 1, f'{self.data[0]['release_date']}')
        self.win.addstr(3, 1, f'{'-' * (curses.COLS - (curses.COLS // 4))}')
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
            self.win.addstr(3, 1, f'{'-' * (curses.COLS - (curses.COLS // 4))}')
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
        self._progress_bar = f'{util.format_to_min_sec(self.progress)} [{'=' * self._percent_remaining}{'.' * (50 - self._percent_remaining)}] {util.format_to_min_sec(self.track_duration)}'

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
    def __init__(self):
        self.win = curses.newwin(1, 18, (curses.LINES - 3), (curses.COLS - 20))
        self.volume = 0
        self._volume_bar = f'[{'=' * (self.volume // 10)}{' ' * (10 - (self.volume // 10))}]'

    def render(self):
        self.win.erase()
        self.win.addstr(0, 0, self._volume_bar)
        self.win.refresh()

    def update_volume(self, volume):
        self.volume = volume
        self._volume_bar = f'[{'=' * (self.volume // 10)}{' ' * (10 - (self.volume // 10))}]{self.volume}%'


class TrackInfo():
    def __init__(self, now_playing):
        self.win = curses.newwin(2, (curses.COLS // 4), (curses.LINES - 3), 1)
        self._track_name = now_playing['name']
        self._artists_names = now_playing['artists']

    def render(self):
        self.win.erase()
        if len(self._track_name) >= (curses.COLS // 4):
            self.win.addstr(0, 0, f'{self._track_name[:(curses.COLS // 4) -4]}...', curses.A_BOLD)
        else:
            self.win.addstr(0, 0, self._track_name, curses.A_BOLD)

        if len(self._artists_names[0]['name']) >= (curses.COLS // 4):
            self.win.addstr(1, 0, f'{self._artists_names[0]['name'][:(curses.COLS // 4) - 4]}...', curses.A_ITALIC)
        else:
            self.win.addstr(1, 0, self._artists_names[0]['name'], curses.A_ITALIC)
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
            self.win.addstr(0, 22, '\u27F215  \u23EE  \u23F8  \u23ED  15\u27F3', curses.A_BOLD)
        else:
            self.win.addstr(0, 22, '\u27F215  \u23EE  \u23F5  \u23ED  15\u27F3', curses.A_BOLD)
        self.win.refresh()

    def update_is_playing(self, is_playing):
        self.is_playing = is_playing
