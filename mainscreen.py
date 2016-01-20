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
from logic import Logic
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
import time
from kivy.uix.behaviors import ToggleButtonBehavior
from menupanel import MenuPanel
from gamezone import Gamezone

class MainScreen(Screen):
    '''
    see kv file for background path
    '''

    # GUI
    menupanel = ObjectProperty(None)
    gamezone = ObjectProperty(None)

    # add widgets to interface for touch-handling
    interface = ReferenceListProperty(menupanel, gamezone)

    # GUI DATA
    option1 = BooleanProperty(None)
    option2 = BooleanProperty(None)

    # LOGIC
    logic = ObjectProperty(None)

    def __init__(self, **kwargs):
       super(MainScreen, self).__init__(**kwargs)
       self.logic = Logic(self)
       self.build_interface()

    # hand down touch events, hand to gamezone if nothing else matches
    def on_touch_down(self, touch):
        for thingy in self.interface:
            if thingy == self.gamezone:
                continue
            if thingy.collide_point(touch.x,touch.y):
                thingy.on_touch_down(touch)
                return
        self.gamezone.on_touch_down(touch)

    def on_touch_up(self, touch):
        for thingy in self.interface:
            if thingy == self.gamezone:
                continue
            if thingy.collide_point(touch.x,touch.y):
                thingy.on_touch_up(touch)

    def build_interface(self):

        self.gamezone = Gamezone(
            do_rotation=False,
            do_translation_y=False,
            do_translation_x=False
        )
        self.add_widget(self.gamezone)

        self.menupanel = MenuPanel(
            size_hint = (1,0.2)
        )

        self.add_widget(self.menupanel)

