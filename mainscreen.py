from kivy.uix.floatlayout import FloatLayout
#from kivy.uix.textinput import TextInput
#from kivy.uix.boxlayout import BoxLayout
from kivy.properties import *
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
#from kivy.uix.gridlayout import GridLayout
#from kivy.clock import Clock
#from kivy.uix.label import Label
#from kivy.network.urlrequest import UrlRequest
#import json
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
#from logic import Logic
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.app import App
import time
from kivy.uix.behaviors import ToggleButtonBehavior
from menupanel import MenuPanel
from gamezone import Gamezone

from kivy.clock import Clock

from kivy.core.window import Window

from tutorial_label import Tutorial_Label

from infobox import Infobox

from seltoggles import Seltoggles

class MainScreen(Screen):
    '''
    see kv file for background path
    '''

    # GUI
    menupanel = ObjectProperty(None)
    gamezone = ObjectProperty(None)

    # label for tutorial texts
    tutorial_label = ObjectProperty(None)

    # showing infos about selected planets
    infobox = ObjectProperty(None)

    seltoggles = ObjectProperty(None)

    # add widgets to interface for touch-handling
    interface = ReferenceListProperty(menupanel, gamezone, tutorial_label, infobox, seltoggles)

    # LOGIC
    logic = ObjectProperty(None)

    def __init__(self, **kwargs):
       super(MainScreen, self).__init__(**kwargs)
       self.build_interface()
       self.logic = App.get_running_app().logic
       self.logic.register_mainscreen(self)
       #Clock.schedule_once(self.allign_gamezone, -1)
       #Clock.schedule_once(self.allign_gamezone, 0)

    def on_enter(self):
        self.allign_gamezone()
        if not self.menupanel.paused:
            self.logic.start_game()
        if self.logic.tutorial_mode:
            self.add_widget(self.tutorial_label)

    def add_seltoggles(self):
        if not self.seltoggles in self.children:
            self.add_widget(self.seltoggles)

    def remove_seltoggles(self):
        if self.seltoggles in self.children:
            self.remove_widget(self.seltoggles)

    def add_infobox(self):
        if not self.infobox in self.children:
            self.add_widget(self.infobox)

    def remove_infobox(self):
        if self.infobox in self.children:
            self.remove_widget(self.infobox)

    def on_leave(self):
        self.logic.stop_game()
        if self.logic.tutorial_mode:
            self.remove_widget(self.tutorial_label)
            self.logic.tutorial_mode = False

    def allign_gamezone(self):
        self.gamezone.center_x = self.center_x
        self.gamezone.center_y = self.center_y

    # hand down touch events, hand to gamezone if nothing else matches
    def on_touch_down(self, touch):
        for thingy in self.interface:
            if not thingy in self.children:
                continue
            if thingy == self.gamezone:
                continue
            if thingy.collide_point(touch.x,touch.y):
                thingy.on_touch_down(touch)
                return
        self.gamezone.on_touch_down(touch)

    def on_touch_move(self, touch):
        for thingy in self.interface:
            if not thingy in self.children:
                continue
            if thingy == self.gamezone:
                continue
            if thingy.collide_point(touch.x,touch.y):
                thingy.on_touch_move(touch)
                return
        self.gamezone.on_touch_move(touch)

    def on_touch_up(self, touch):
        for thingy in self.interface:
            if not thingy in self.children:
                continue
            if thingy == self.gamezone:
                continue
            if thingy.collide_point(touch.x,touch.y):
                thingy.on_touch_up(touch)
                return
        self.gamezone.on_touch_up(touch)

    def build_interface(self):
        self.calc_iconsize()

        self.tutorial_label = Tutorial_Label(
            size_hint = (0.8, 0.1),
            pos_hint = {'x' : 0.2, 'y' : 0.9}
        )

        self.infobox = Infobox(
            size_hint = (0.2, 0.5),
            pos_hint = {'x' : 0.8, 'y' :0.5}
        )

        self.seltoggles = Seltoggles(
            self.iconsize,
            self.iconratio_x,
            size_hint = (None, None),
            size = (4 * self.iconsize, self.iconsize),
            pos_hint = {'x' : 1 - 4 * self.iconratio_x, 'y' : 0}
        )

        self.gamezone = Gamezone(
            #do_rotation=False,
            #do_translation_y=False,
            #do_translation_x=False,
            auto_bring_to_front = False,
            scale_min = 0.1,
            scale_max = 1,
            size_hint = (10000,10000)
            #pos_hint = {'x':-0.5,'y':-0.5}
        )
        self.add_widget(self.gamezone)

        self.menupanel = MenuPanel(
            #size_hint = (1,0.1)
            self.iconsize,
            self.iconratio_y,
            size_hint = (None, None),
            size = (self.iconsize, Window.height),
            pos_hint = {'x' : 0, 'y' : 0}
        )

        self.add_widget(self.menupanel)

    def calc_iconsize(self):
        icon_count = 8
        window_height = Window.height
        window_width = Window.width
        iconsize = window_height / icon_count
        self.iconratio_y = float(iconsize) / window_height
        self.iconratio_x = float(iconsize) / window_width
        self.iconsize = iconsize
