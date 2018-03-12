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
from kivy.uix.label import Label

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
            pos_hint={'x': 0, 'y': 1.0/3},
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            source='./media/icons/pause.png',
            always_release=True
        )

        self.resetbutton = RealButton(
            './media/icons/reset.png',
            './media/icons/reset_pressed.png',
            self.logic.reset_planets,
            pos_hint={'x': 0, 'y': 2.0/3},
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            source='./media/icons/reset.png',
            always_release=True
        )

        '''
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
        '''

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


class AddMenuPanel(FloatLayout):

    # toggle buttons
    add_planet_button = ObjectProperty(None)
    add_sun_button = ObjectProperty(None)
    multi_button = ObjectProperty(None)

    optionbuttons = ReferenceListProperty(
        add_planet_button,
        add_sun_button,
        multi_button
    )

    logic = ObjectProperty(None)
    cur_mode = StringProperty('zoom')

    visible = BooleanProperty(True)

    def __init__(self, iconsize, iconratio, **kwargs):
        super(AddMenuPanel, self).__init__(**kwargs)
        self.logic = App.get_running_app().logic

        self.iconsize = iconsize
        self.iconratio = iconratio

        # keywords to press buttons from other modules
        self.keyword_map = {
            'add_planet': self.add_planet_button,
            'add_sun': self.add_sun_button,
            'multi': self.multi_button
        }

        self.build_interface()

    def on_cur_mode(self, instance, value):
        self.logic.cur_guimode = self.logic.mode_map[value]

    def build_interface(self):

        self.show_hide_button = RealToggleButton(
            './media/icons/up.png',
            './media/icons/down.png',
            self.show_hide,
            pos_hint={'x': 0, 'y': 0},
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            source='./media/icons/up.png',
            always_release=True
        )

        self.add_sun_button = RealMenuToggleButton(
            './media/icons/sunmode.png',
            './media/icons/sunmode_pressed.png',
            'add_sun',
            pos_hint={'x': 0.25, 'y': 0},
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            source='./media/icons/sunmode.png',
            group='menu',
            allow_no_selection=True
        )

        self.add_planet_button = RealMenuToggleButton(
            './media/icons/add_planet.png',
            './media/icons/add_planet_pressed.png',
            'add_planet',
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            pos_hint={'x': 0.5, 'y': 0},
            group='menu',
            source='./media/icons/add_planet.png',
            allow_no_selection=True

            # allow_no_selection=False,
        )

        self.multi_button = RealMenuToggleButton(
            './media/icons/multipass.png',
            './media/icons/multipass_pressed.png',
            'multi',
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            pos_hint={'x': 0.75, 'y': 0},
            group='menu',
            source='./media/icons/multipass.png',
            allow_no_selection=True
            # allow_no_selection=False,
        )

        self.add_widget(self.add_planet_button)
        self.add_widget(self.add_sun_button)
        self.add_widget(self.multi_button)
        self.add_widget(self.show_hide_button)

        self.value_slider = Slider(
            min=5,
            max=50,
            value=10,
            step=1,
            orientation='horizontal',
            pos_hint={'x':  1, 'y': 0},
            size_hint=(1, 1)
        )

        self.value_label = Label(
            text='Some value: 9999',
            size_hint=(1, 1),
            pos_hint={'x': 2, 'y': 0},
            halign='left'
        )

        # self.add_widget(self.value_slider)
        # self.add_widget(self.value_label)
        self.value_slider.bind(value=self.value_slider_change)

        self.hide_items = [
            self.value_slider, self.value_label, self.add_planet_button,
            self.add_sun_button, self.multi_button
        ]

    def value_slider_change(self, instance, value):
        if self.no_callbacks:
            return
        # check current mode and update value in logic module
        if self.logic.cur_guimode == self.logic.mode_map['zoom']:
            self.logic.tick_ratio = value
        self.logic.cur_guimode.slider_value = value
        # update label
        self.value_label.text = ':'.join(
            [self.logic.cur_guimode.slider_label, str(value)]
        )

    def add_value_slider(self, mode):
        self.no_callbacks = True
        if self.value_slider not in self.children:
            self.value_slider.min = mode.settings['min']
            self.value_slider.max = mode.settings['max']
            self.value_slider.step = mode.settings['step']
            self.value_slider.value = mode.slider_value  # mode.settings['min']
            self.value_label.text = mode.slider_label + ':' + str(self.value_slider.value)
            self.add_widget(self.value_slider)
            self.add_widget(self.value_label)
        self.no_callbacks = False

    def remove_value_slider(self):
        if self.value_slider in self.children:
            self.remove_widget(self.value_slider)
            self.remove_widget(self.value_label)

    def show_hide(self, instance):
        if self.visible:
            scrolldown = Animation(
                pos_hint={
                    'y': 1.05
                },
                duration=0.5,
                t='out_bounce'
            )
            for item in self.hide_items:
                scrolldown.start(item)
            # scrolldown.start(self.seltoggles)
            self.visible = False
        else:
            scrolldown = Animation(
                pos_hint={
                    'y': 0
                },
                duration=0.5,
                t='out_bounce'
            )
            for item in self.hide_items:
                scrolldown.start(item)
            # scrolldown.start(self.seltoggles)
            self.visible = True
