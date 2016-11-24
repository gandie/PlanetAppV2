from kivy.uix.floatlayout import FloatLayout
from kivy.properties import *
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.slider import Slider
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
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

    # buttons for selected planet
    seltoggles = ObjectProperty(None)

    # experimental slider for time ratio
    ratio_slider = ObjectProperty(None)

    value_slider = ObjectProperty(None)

    # add touchable widgets to interface for touch-handling
    interface = ReferenceListProperty(
        menupanel, gamezone, tutorial_label, infobox, 
        seltoggles, ratio_slider, value_slider
    )

    # LOGIC
    logic = ObjectProperty(None)

    def __init__(self, **kwargs):
       super(MainScreen, self).__init__(**kwargs)
       self.logic = App.get_running_app().logic
       self.logic.register_mainscreen(self)

       self.iconsize = kwargs.get('iconsize')
       self.iconratio_x = kwargs.get('iconratio_x')
       self.iconratio_y = kwargs.get('iconratio_y')

       self.build_interface()

       # get background rect from canvas
       self.background = self.canvas.get_group('background')[0]

    def on_enter(self):
        self.allign_gamezone()

        # check for background
        if self.logic.settings['background']:
            self.background.size = self.size
        else:
            self.background.size = (0,0)

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
        for widget in self.interface:
            if not widget in self.children:
                continue
            if widget == self.gamezone:
                continue
            if widget.collide_point(touch.x,touch.y):
                widget.on_touch_down(touch)
                return
        self.gamezone.on_touch_down(touch)

    def on_touch_move(self, touch):
        for widget in self.interface:
            if not widget in self.children:
                continue
            if widget == self.gamezone:
                continue
            if widget.collide_point(touch.x,touch.y):
                widget.on_touch_move(touch)
                return
        self.gamezone.on_touch_move(touch)

    def on_touch_up(self, touch):
        for widget in self.interface:
            if not widget in self.children:
                continue
            if widget == self.gamezone:
                continue
            if widget.collide_point(touch.x,touch.y):
                widget.on_touch_up(touch)
                return
        self.gamezone.on_touch_up(touch)

    def build_interface(self):

        self.tutorial_label = Tutorial_Label(
            self.iconsize,
            self.iconratio_x,
            size_hint = (None, None),
            size = (8 * self.iconsize, self.iconsize),
            pos_hint = {'x' : 1 - 8 * self.iconratio_x - 0.2, 'y' : 0.875}
        )

        self.infobox = Infobox(
            size_hint = (0.2, 0.5),
            pos_hint = {'x' : 0.8, 'y' :0.5}
        )

        self.seltoggles = Seltoggles(
            self.iconsize,
            self.iconratio_x,
            size_hint = (None, None),
            size = (5 * self.iconsize, self.iconsize),
            pos_hint = {'x' : 1 - 5 * self.iconratio_x, 'y' : 0}
        )

        self.gamezone = Gamezone(
            #do_rotation=False,
            #do_translation_y=False,
            #do_translation_x=False,
            auto_bring_to_front = False,
            scale_min = 0.01,
            scale_max = 50,
            size_hint = (10000,10000)
        )
        self.add_widget(self.gamezone)

        self.menupanel = MenuPanel(
            self.iconsize,
            self.iconratio_y,
            size_hint = (None, None),
            size = (self.iconsize, Window.height),
            pos_hint = {'x' : 0, 'y' : 0}
        )

        self.ratio_slider = Slider(
            min = 0.1,
            max = 2.0,
            value = 1.0,
            orientation = 'vertical',
            pos_hint = {'x' : 0.9, 'y' : 0},
            size_hint = (0.1, 1)
        )

        self.value_slider = Slider(
            min = 5,
            max = 50,
            value = 10,
            step = 1,
            orientation = 'horizontal',
            pos_hint = {'x' : self.iconratio_x, 'y' : 0},
            size_hint = (0.3, 0.1)
        )

        self.ratio_slider.bind(value = self.slider_change)
        self.value_slider.bind(value = self.value_slider_change)

        self.add_widget(self.ratio_slider)

        self.tutorial_label.register_menupanel(self.menupanel)

        self.add_widget(self.menupanel)

    def slider_change(self, instance, value):
        self.logic.tick_ratio = value
        #print value

    def value_slider_change(self, instance, value):
        self.logic.slider_value = value
        #print value

    def add_value_slider(self):
        if not self.value_slider in self.children:
            self.add_widget(self.value_slider)

    def remove_value_slider(self):
        self.remove_widget(self.value_slider)
