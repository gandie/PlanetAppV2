# KIVY
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import *
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.togglebutton import ToggleButton
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.slider import Slider

# CUSTOM
from logic import Logic
from realbutton import RealButton
from realbutton import RealToggleButton
from realbutton import RealMenuToggleButton

'''
menupanel shown on the left side of the screen in mainscreen
contains main buttons to control the game
'''


class MenuPanel(FloatLayout):

    # toggle buttons
    add_planet_button = ObjectProperty(None)
    zoom_button = ObjectProperty(None)
    add_sun_button = ObjectProperty(None)
    del_button = ObjectProperty(None)
    multi_button = ObjectProperty(None)

    optionbuttons = ReferenceListProperty(
        add_planet_button,
        zoom_button,
        add_sun_button,
        del_button,
        multi_button
    )

    # normal button
    menubutton = ObjectProperty(None)
    resetbutton = ObjectProperty(None)
    pausebutton = ObjectProperty(None)

    paused = BooleanProperty(False)

    logic = ObjectProperty(None)

    cur_mode = StringProperty('add_planet')

    def __init__(self, iconsize, iconratio, **kwargs):
        super(MenuPanel, self).__init__(**kwargs)
        self.logic = App.get_running_app().logic
        self.iconsize = iconsize
        self.iconratio = iconratio
        self.build_interface()

        # keywords to press buttons from other modules
        self.keyword_map = {
            'add_planet': self.add_planet_button,
            'add_sun': self.add_sun_button,
            'del': self.del_button,
            'zoom': self.zoom_button,
            'multi': self.multi_button
        }

    def on_cur_mode(self, instance, value):
        self.logic.cur_guimode = self.logic.mode_map[value]

    def press_button(self, keyword):
        button = self.keyword_map[keyword]
        for otherbutton in self.optionbuttons:
            if otherbutton == button:
                continue
            otherbutton.state = 'normal'
        button.state = 'down'

    def build_interface(self):

        self.menubutton = RealButton(
            './media/icons/menu.png',
            './media/icons/menu_pressed.png',
            self.goto_menu,
            pos_hint={'x': 0, 'y': 0},
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            source='./media/icons/menu.png',
            always_release=True
        )

        self.pausebutton = RealToggleButton(
            './media/icons/pause.png',
            './media/icons/pause_pressed.png',
            self.pause_game,
            pos_hint={'x': 0, 'y': self.iconratio},
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            source='./media/icons/pause.png',
            always_release=True
        )

        self.resetbutton = RealButton(
            './media/icons/reset.png',
            './media/icons/reset_pressed.png',
            self.logic.reset_planets,
            pos_hint={'x': 0, 'y': self.iconratio * 2},
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            source='./media/icons/reset.png',
            always_release=True
        )

        self.del_button = RealMenuToggleButton(
            './media/icons/delete.png',
            './media/icons/delete_pressed.png',
            'del',
            pos_hint={'x': 0, 'y': self.iconratio * 3},
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            source='./media/icons/delete.png',
            group='menu',
            allow_no_selection=False
        )

        self.add_sun_button = RealMenuToggleButton(
            './media/icons/sunmode.png',
            './media/icons/sunmode_pressed.png',
            'add_sun',
            pos_hint={'x': 0, 'y': self.iconratio * 4},
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            source='./media/icons/sunmode.png',
            group='menu',
            allow_no_selection=False
        )

        self.add_planet_button = RealMenuToggleButton(
            './media/icons/add_planet.png',
            './media/icons/add_planet_pressed.png',
            'add_planet',
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            pos_hint={'x': 0, 'y': self.iconratio * 5},
            group='menu',
            state='down',
            allow_no_selection=False,
            source='./media/icons/add_planet_pressed.png'
        )

        self.zoom_button = RealMenuToggleButton(
            './media/icons/zoom.png',
            './media/icons/zoom_mode.png',
            'zoom',
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            pos_hint={'x': 0, 'y': self.iconratio * 6},
            group='menu',
            allow_no_selection=False,
            source='./media/icons/zoom.png'
        )

        self.multi_button = RealMenuToggleButton(
            './media/icons/multipass.png',
            './media/icons/multipass_pressed.png',
            'multi',
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            pos_hint={'x': 0, 'y': self.iconratio * 7},
            group='menu',
            allow_no_selection=False,
            source='./media/icons/multipass.png'
        )

        self.add_widget(self.add_planet_button)
        self.add_widget(self.zoom_button)
        self.add_widget(self.add_sun_button)
        self.add_widget(self.del_button)
        self.add_widget(self.multi_button)
        self.add_widget(self.menubutton)
        self.add_widget(self.pausebutton)
        self.add_widget(self.resetbutton)

    def goto_menu(self, instance):
        self.parent.manager.current = 'menu'

    def pause_game(self, value):
        if value:
            self.logic.stop_game()
        else:
            self.logic.start_game()
        self.paused = value
