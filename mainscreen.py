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

class MainScreen(Screen):
    '''
    see kv file for background path
    '''

    # GUI
    menupanel = ObjectProperty(None)
    gamezone = ObjectProperty(None)

    # add widgets to interface for touch-handling
    interface = ReferenceListProperty(menupanel, gamezone)

    # LOGIC
    logic = ObjectProperty(None)

    def __init__(self, **kwargs):
       super(MainScreen, self).__init__(**kwargs)
       self.build_interface()
       self.logic = App.get_running_app().logic
       #Clock.schedule_once(self.allign_gamezone, -1)
       #Clock.schedule_once(self.allign_gamezone, 0)

    def on_enter(self):
        self.allign_gamezone()
        if not self.menupanel.paused:
            self.logic.start_game()

    def on_leave(self):
        self.logic.stop_game()

    def allign_gamezone(self):
        self.gamezone.center_x = self.center_x
        self.gamezone.center_y = self.center_y

    # hand down touch events, hand to gamezone if nothing else matches
    def on_touch_down(self, touch):
        for thingy in self.interface:
            if thingy == self.gamezone:
                continue
            if thingy.collide_point(touch.x,touch.y):
                thingy.on_touch_down(touch)
                return
        self.gamezone.on_touch_down(touch)

    def on_touch_move(self, touch):
        for thingy in self.interface:
            if thingy == self.gamezone:
                continue
            if thingy.collide_point(touch.x,touch.y):
                thingy.on_touch_move(touch)
                return
        self.gamezone.on_touch_move(touch)

    def on_touch_up(self, touch):
        for thingy in self.interface:
            if thingy == self.gamezone:
                continue
            if thingy.collide_point(touch.x,touch.y):
                thingy.on_touch_up(touch)
                return
        self.gamezone.on_touch_up(touch)

    def build_interface(self):
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

        self.calc_iconsize()

        self.menupanel = MenuPanel(
            #size_hint = (1,0.1)
            self.iconsize,
            self.iconratio,
            size_hint = (None, None),
            size = (self.iconsize, Window.height),
            pos_hint = {'x' : 0, 'y' : 0}
        )

        self.add_widget(self.menupanel)

    def calc_iconsize(self):
        icon_count = 7
        window_height = Window.height
        iconsize = window_height / icon_count
        self.iconratio = float(iconsize) / window_height
        self.iconsize = iconsize
        #print iconsize
        #print self.iconratio
        #print Window.height
        #self.settingsbutton.text = '{0} , {1}'.format(Window.width, Window.height)


