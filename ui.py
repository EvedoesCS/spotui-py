# ----------------------------------------------- #
# UI will contain functions for rendering
# elements of the Spotui-py User interface
# ----------------------------------------------- #

import curses
from curses import wrapper
import routes
from util import format_to_QI
import auth

token = auth.authenticate()


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
                self.render()
                submitted = self.query
                self.query = ""
                return submitted
            elif key == 127:
                self.query = self.query[:-1]
                self.render(f'Search: {self.query}')
            elif key == 27:
                self.query = ""
                self.render()
                return 'exit'
            else:
                self.query += chr(key)
                self.render(f'Search: {self.query}')


class ContentWin():
    def __init__(self):
        self.win = curses.newwin((curses.LINES - 6), (curses.COLS - (curses.COLS // 4)), 3, (curses.COLS // 4))
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
                return ('play', self.data[highlight].id)
            elif key == 27:
                self.render_data()
                return ('exit', None)
            elif key == curses.KEY_UP or chr(key) == 'k':
                if highlight != 0:
                    highlight -= 1
            elif key == curses.KEY_DOWN or chr(key) == 'j':
                if highlight != len(self.data):
                    highlight += 1


class LinksWin():
    def __init__(self):
        self.data = []

    def render(self):
        self.win = curses.newwin((curses.LINES - 3), (curses.COLS // 4), 0, 0)
        self.win.border()
        self.win.addstr(1, 1, 'User Playlists Window')
        self.win.refresh()


class TimelineWin():
    def __init__(self):
        self.is_playing = False
        self.now_playing = ""

    def render(self):
        self.win = curses.newwin(3, curses.COLS, (curses.LINES - 3), 0)
        self.win.border()
        self.win.addstr(1, 1, 'Track Timeline')
        self.win.refresh()


def render_model(win):
    search_bar = SearchBarWin(win)
    content_window = ContentWin(win)
    links_window = LinksWin(win)
    timeline_bar = TimelineWin(win)

    search_bar.render()
    content_window.render()
    links_window.render()
    timeline_bar.render()

    win.refresh()

    while True:
        win.refresh()
        key = win.getch()
        if chr(key) == 'q':
            break
        elif chr(key) == 's':
            query = search_bar.get_query()
            if query != '':
                query_data = routes.search(token, query)
                fquery_data = format_to_QI(query_data)
                content_window.data = fquery_data
                content_window.render_data()
                timeline_bar.now_playing = content_window.traverse_content()
        elif chr(key) == 'c':
            timeline_bar.now_playing = content_window.traverse_content()
        elif key == 32 or chr(key) == 'p':
            if timeline_bar.playing == True:
                routes.pause(token)
                timeline_bar.is_playing = False
            else:
                routes.play(token, timeline_bar.now_playing)
                timeline_bar.is_playing = True


if __name__ == "__main__":
    win = curses.initscr()
    wrapper(render_model)
