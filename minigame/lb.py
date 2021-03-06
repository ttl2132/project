from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from heroku_app.app import HEROKU_URL
from kivy.graphics import Color, Rectangle
from loguru import logger
import requests
import pandas as pd
from kivy.app import App

class Leaderboard(GridLayout):
    """A widget that contains the initials and times for the leaderboard."""

    def __init__(self, size_hint=None, pos_hint=None, popup=False, **kwargs):
        super(Leaderboard, self).__init__(**kwargs)
        self.label_refs = []
        if size_hint:
            self.size_hint = size_hint
        if popup:
            self.add_popup_bg()
        self.pos_hint={'center_x':.5, 'center_y': .5}
        t_size = '25sp'
        self.add_widget(Label(text='Initials', font_size=t_size))
        self.add_widget(Label(text='Time', font_size=t_size))
        self.game = App.get_running_app().GAMEID
        self.update()
        self.bg = None
        self.cols = 2

    def add_popup_bg(self):
        """Used to add a background rectangle for the leaderboard popup."""
        with self.canvas.before:
            Color(0, 0, 0)
            self.bg = Rectangle(
                pos=(300, 100),
                height = self.parent.height,
                size=self.parent.size
                )
            self.bind(pos=self.update_bg, size=self.update_bg)

    def update_bg(self, *args):
        """Allows the leaderboard to be scalable when changing window size."""
        self.bg.pos = self.pos
        self.bg.size = self.size

    def generate_leaderboard(self, lb=None):
        """Used for created the widgets to display in the grid layout"""
        self.clear_widgets()
        t_size = '25sp'
        self.add_widget(Label(text='Initials', font_size=t_size))
        self.add_widget(Label(text='Time', font_size=t_size))
        updated_lb = lb
        if not lb:
            updated_lb = self.get_lb()
        logger.debug(updated_lb)
        updated_lb = pd.DataFrame.from_dict(updated_lb)
        num_ranks = updated_lb.shape[0]
        t_size = '20sp'
        for i in range(num_ranks):
            initials_label = Label(
                text=updated_lb["initials"][str(i)], font_size=t_size
                )
            rounded_time = "{:.2f}".format(updated_lb["time"][str(i)])
            score_label = Label(text=rounded_time, font_size=t_size)
            self.label_refs.append(initials_label)
            self.label_refs.append(score_label)
            self.add_widget(initials_label)
            self.add_widget(score_label)
        logger.debug("Leaderboard generated")

    def update(self, time=None):
        """Will update leaderboard based on new time"""
        db_lb = self.get_lb()
        num_ranks = len(db_lb)
        if time:
            for i in range(num_ranks):
                if (db_lb["initials"][str(i)] == "N/A"
                    or time < float(db_lb["time"][str(i)])):
                    name = App.get_running_app().INITIALS
                    logger.debug(f"Name: {name}")
                    requests.post(
                    f"{HEROKU_URL}/scores/{self.game}/{name}/{time}/{i}"
                    )
        self.generate_leaderboard()

    def get_lb(self):
        """Will make get REST call to heroku app."""
        db_info = requests.get(f"{HEROKU_URL}/scores/{self.game}")
        if db_info.status_code == 200:
            return pd.DataFrame.from_dict(db_info.json())
        else:
            logger.error(f"{db_info.status_code}: Error returned.")
