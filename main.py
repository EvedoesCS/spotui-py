# ----------------------------------------- #
# Main: Responsible for running the runtime
# loop for the application
# ----------------------------------------- #

import curses
from curses import wrapper
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
        self.components = {
                'search_bar': search_bar,
                'content_window': content_window,
                'links_window': links_window,
                'timeline_bar': timeline_bar
                }

    def handle_msg(self, msg):
        if msg[0] == 'search':
            query = self.components['search_bar'].get_query()
            if query != 'exit' or query != '':
                self.handle_msg(('query', query))
            else:
                return ''

        elif msg[0] == 'query':
            query_data = routes.search(self.token, msg[1])
            fquery_data = util.format_to_QI(query_data)
            self.components['content_window'].data = fquery_data
            self.handle_msg(('update_content', None))

        elif msg[0] == 'update_content':
            self.components['content_window'].render_data()
            self.handle_msg(('traverse_content', None))

        elif msg[0] == 'traverse_content':
            selected = self.components['content_window'].traverse()
            if selected[0] == 'play':
                self.handle_msg(('play', selected[1]))
            else:
                return ''

        elif msg[0] == 'play':
            self.components['timeline_bar'].is_playing = True
            self.components['timeline_bar'].now_playing = msg[1]
            routes.play(self.token, msg[1])

        elif msg[0] == 'pause':
            self.components['timeline_bar'].is_playing = False
            routes.pause(self.token)

        elif msg[0] == 'resume':
            pass

    def render_model(self):
        for component in self.components:
            self.components[component].render()

        self.win.refresh()

        while True:
            self.win.refresh()
            key = self.win.getch()

            # Defines keybinds
            if chr(key) == 'q':
                break

            elif chr(key) == 's':
                self.handle_msg(('search', None))

            elif chr(key) == 'c':
                self.handle_msg(('traverse_content', None))

            elif chr(key) == 'p':
                if self.components['timeline_bar'].is_playing == False:
                    self.handle_msg(('play', self.components['timeline_bar'].now_playing))
                elif self.components['timeline_bar'].is_playing == True:
                    self.handle_msg(('pause'))
                


def main(win):
    app = App(win)
    app.render_model()


if __name__ == "__main__":
    win = curses.initscr()
    wrapper(main)
