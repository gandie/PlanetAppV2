# KIVY
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import *
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.slider import Slider
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.app import App
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.clock import Clock
from kivy.core.window import Window

# CUSTOM
from menupanel import MenuPanel
from gamezone import Gamezone
from tutorial_label import Tutorial_Label
from infobox import Infobox
from seltoggles import Seltoggles

'''
Screen shown when the game is played. Contains gamezone and control widgets.
Divides touch events for control widgets and gamezone and hands them down.
'''


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

    # context slider for gui modes
    value_slider = ObjectProperty(None)

    # add touchable widgets to interface for touch-handling
    interface = ReferenceListProperty(
        menupanel, gamezone, tutorial_label, infobox,
        seltoggles, value_slider
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
            self.background.size = (0, 0)

        if not self.menupanel.paused:
            self.logic.start_game()

        # check tutorial setting
        if self.logic.settings['show_tutorial'] is True:
            if self.tutorial_label not in self.children:
                self.add_widget(self.tutorial_label)
        else:
            if self.tutorial_label in self.children:
                self.remove_widget(self.tutorial_label)

    def add_seltoggles(self):
        if self.seltoggles not in self.children:
            self.add_widget(self.seltoggles)

    def remove_seltoggles(self):
        if self.seltoggles in self.children:
            self.remove_widget(self.seltoggles)

    def add_infobox(self):
        if self.infobox not in self.children:
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
        # center gamezone widget so simulation starts in the middle
        self.gamezone.center_x = self.center_x
        self.gamezone.center_y = self.center_y

    def on_touch_down(self, touch):
        # hand down touch events, hand to gamezone if nothing else matches
        for widget in self.interface:
            # dont check invisible widgets
            if widget not in self.children:
                continue
            # gamezone is last
            if widget == self.gamezone:
                continue
            # check for collision
            if widget.collide_point(touch.x, touch.y):
                widget.on_touch_down(touch)
                return
        self.gamezone.on_touch_down(touch)

    def on_touch_move(self, touch):
        for widget in self.interface:
            if widget not in self.children:
                continue
            if widget == self.gamezone:
                continue
            if widget.collide_point(touch.x, touch.y):
                widget.on_touch_move(touch)
                return
        self.gamezone.on_touch_move(touch)

    def on_touch_up(self, touch):
        for widget in self.interface:
            if widget not in self.children:
                continue
            if widget == self.gamezone:
                continue
            if widget.collide_point(touch.x, touch.y):
                widget.on_touch_up(touch)
                return
        self.gamezone.on_touch_up(touch)

    def build_interface(self):

        self.tutorial_label = Tutorial_Label(
            self.iconsize,
            self.iconratio_x,
            size_hint=(None, None),
            size=(8 * self.iconsize, self.iconsize),
            pos_hint={'x': 1 - 8 * self.iconratio_x - 0.2, 'y': 0.875}
        )

        self.infobox = Infobox(
            size_hint=(0.2, 0.5),
            pos_hint={'x': 0.8, 'y': 0.5}
        )

        self.seltoggles = Seltoggles(
            self.iconsize,
            self.iconratio_x,
            size_hint=(None, None),
            size=(5 * self.iconsize, self.iconsize),
            pos_hint={'x': 1 - 5 * self.iconratio_x, 'y': 0}
        )

        self.gamezone = Gamezone(
            # zooming stuff
            # do_rotation=False,
            # do_translation_y=False,
            # do_translation_x=False,
            auto_bring_to_front=False,
            scale_min=0.15,
            scale_max=10,
            size_hint=(25, 25)
        )
        self.add_widget(self.gamezone)

        self.menupanel = MenuPanel(
            self.iconsize,
            self.iconratio_y,
            size_hint=(None, None),
            size=(self.iconsize, Window.height),
            pos_hint={'x': 0, 'y': 0}
        )

        self.value_slider = Slider(
            min=5,
            max=50,
            value=10,
            step=1,
            orientation='horizontal',
            pos_hint={'x': self.iconratio_x, 'y': 0},
            size_hint=(0.3, 0.1)
        )

        self.label = Label(
            text='Some value: 9999',
            size_hint=(0.2, 0.1),
            pos_hint={'x': self.iconratio_x + 0.3, 'y': 0},
            halign='left'
        )

        self.value_slider.bind(value=self.value_slider_change)
        self.tutorial_label.register_menupanel(self.menupanel)
        self.add_widget(self.menupanel)

    def value_slider_change(self, instance, value):
        # check current mode and update value in logic module
        if self.logic.cur_guimode == self.logic.mode_map['zoom']:
            self.logic.tick_ratio = value
        else:
            self.logic.slider_value = value
        self.logic.cur_guimode.slider_value = value
        # update label
        self.label.text = ':'.join(
            [self.logic.cur_guimode.slider_label, str(value)]
        )

    def add_value_slider(self, mode):
        if self.value_slider not in self.children:
            self.value_slider.min = mode.settings['min']
            self.value_slider.max = mode.settings['max']
            self.value_slider.step = mode.settings['step']
            self.value_slider.value = mode.settings['min']
            self.label.text = mode.slider_label + ':' + str(self.value_slider.value)
            self.add_widget(self.value_slider)
            self.add_widget(self.label)

    def remove_value_slider(self):
        if self.value_slider in self.children:
            self.remove_widget(self.value_slider)
            self.remove_widget(self.label)
