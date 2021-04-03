import json
from kivy.uix.screenmanager import Screen
import kivy.properties as props
from kivy.app import App
from loguru import logger
from minigame.imgbutton import ImageButton
import numpy as np
import minigame.locgenerator as locgenerator

class ScreenFactory(Screen):
    orders = props.ListProperty([''])
    cur_img = props.NumericProperty()
    last_img = props.NumericProperty()
    """Parses the image files to generate the game screen."""

    def __init__(self, game_name, **kwargs):
        super(ScreenFactory, self).__init__(**kwargs)
        self.GAME_PREFIX = game_name
        self.imgs = {}
        self.orders = ['']

    def generate_cell(self):
        """Adds the cell parts to the screen."""
        img_locs = locgenerator.generate_picture_layout(self.imgs, self.load_order)
        order = list(range(len(self.imgs)))
        np.random.shuffle(order)
        label_order = [""] * len(self.imgs)
        for i in range(len(img_locs)):
            count = order[i]
            img_info = img_locs[i]
            self.add_widget(ImageButton(count, img_info["label"], img_info["source"], img_info["loc"], img_info["size"]))
            label_order[order[i]] = img_info["label"]
        logger.debug(label_order)
        self.orders = label_order
        self.cur_img = 0
        self.last_img = len(self.orders)-1

    def parse(self):
        """Parses the JSON file to initialize the properties for the game."""
        with open(f"minigame/data/{self.GAME_PREFIX}.json", "r") as f:
            pic_dict = json.load(f)
            self.imgs = pic_dict["images"]
        logger.debug(len(self.imgs))
        self.load_order = pic_dict["load_order"]

    def on_enter(self):
        """Starts the timer when moved to the game screen."""
        self.time.reset_time()
        self.time.start_time()

    def reset(self):
        """Resets the timer and game with the same layout."""
        self.time.reset_time()
        self.cur_img = 0
