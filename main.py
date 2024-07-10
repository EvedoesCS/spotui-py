# ----------------------------------------- #
# Main: Responsible for running the runtime
# loop for the application
# ----------------------------------------- #

import curses
from curses import wrapper
import threading
import time

import auth
import routes
import ui
import util


class App:
    def __init__(self, win):
        self.win = win
        self.token = auth.authenticate()
        search_bar = ui.SearchBarWin()
        content_window = ui.ContentWin()
        links_window = ui.LinksWin()
        timeline_bar = ui.TimelineWin()
        self.exiting = False
        self.components = {
                'search_bar': search_bar,
                'content_window': content_window,
                'links_window': links_window,
                'timeline_bar': timeline_bar
                }
        self.p_state = routes.get_playback_state(self.token)

    def refresh_p_state(self):
        while True:
            time.sleep(0.5)
            if self.exiting is True:
                break
            self.p_state = routes.get_playback_state(self.token)
            if self.p_state == 204:
                routes.transfer_playback(self.token)
                self.p_state = routes.get_playback_state(self.token)
            if type(self.p_state) is not int:
                self.components['timeline_bar'].update_vars(
                                            self.p_state['item'],
                                            self.p_state['is_playing'],
                                            self.p_state['device']['volume_percent'],
                                            self.p_state['progress_ms'] // 1000)
            curses.curs_set(0)

    def search(self):
        r = self.components['search_bar'].get_query()
        code, query = r.split('=')
        if code == 'query':
            raw_data = routes.search(self.token, query)
            data = util.format_to_QI(raw_data)
            self.components['content_window'].data = data
            self.components['content_window'].render_data()
            return code
        elif code == 'exit':
            return code

    def play(self):
        track_id = self.components['timeline_bar'].now_playing.id
        routes.play(self.token, track_id)

    def pause(self):
        routes.pause(self.token)

    def resume(self):
        track_id = self.p_state['item']['id']
        position = self.p_state['progress_ms']
        routes.play(self.token, track_id, position_ms=position)

    def skip_to_previous(self):
        routes.back(self.token)

    def skip_to_next(self):
        routes.next(self.token)

    def handle_keys(self):
        while True:
            key = self.win.getch()
            # Defines keybinds
            if chr(key) == 'q':
                self.exiting = True
                break

            elif chr(key) == 's':
                c = self.search()
                if c == 'query':
                    r = self.components['content_window'].traverse()
                    if r is not None:
                        self.components['timeline_bar'].now_playing = r
                        self.play()

            elif chr(key) == 'c':
                r = self.components['content_window'].traverse()
                if r is not None:
                    self.components['timeline_bar'].now_playing = r
                    self.play()

            elif chr(key) == 'p':
                try:
                    is_playing = self.p_state['is_playing']
                except TypeError:
                    routes.transfer_playback(self.token)
                    is_playing = self.p_state['is_playing']

                if is_playing is False:
                    self.resume()
                elif is_playing is True:
                    self.pause()

            elif chr(key) == 'b':
                self.skip_to_previous()

            elif chr(key) == 'n':
                self.skip_to_next()

    def render_model(self):
        for component in self.components:
            self.components[component].render()

        self.win.refresh()

        t1 = threading.Thread(target=self.handle_keys)
        t2 = threading.Thread(target=self.refresh_p_state)

        t1.start()
        t2.start()

        t1.join()
        t2.join()


def main(win):
    app = App(win)
    app.render_model()


if __name__ == "__main__":
    win = curses.initscr()
    wrapper(main)
