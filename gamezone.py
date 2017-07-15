# KIVY
from kivy.uix.scatter import Scatter
from kivy.graphics import Line, Color
from kivy.properties import *
from kivy.app import App
from kivy.vector import Vector

# BUILTIN
import time
from random import randint

'''
This is the widget where the actuall simluation is displayed.
Scatter widget can be zoomed, translated and rotated which is basically the
zooming functionality. Hands down touch events to current mode.
'''


class Gamezone(Scatter):

    logic = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Gamezone, self).__init__(**kwargs)
        self.logic = App.get_running_app().logic
        self.logic.register_gamezone(self)

    def on_touch_down(self, touch):
        self.logic.cur_guimode.touch_down(touch)

    def on_touch_move(self, touch):
        self.logic.cur_guimode.touch_move(touch)

    def on_touch_up(self, touch):
        self.logic.cur_guimode.touch_up(touch)
