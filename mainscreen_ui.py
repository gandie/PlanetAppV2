'''
All widgets shown on mainscreen live here
'''

# KIVY
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.screenmanager import Screen
from kivy.uix.slider import Slider
from kivy.uix.label import Label

from kivy.properties import *
from kivy.animation import Animation
from kivy.app import App

from kivy.clock import Clock

# CUSTOM
from realbutton import RealButton
from realbutton import RealToggleButton
from realbutton import RealMenuToggleButton
from realbutton import RealTimedButton

'''
MenuPanel shown on the left side of the screen in mainscreen
contains buttons to control the game: menu, pause, reset

AddMenuPanel shown on the top left of the mainscreen contains buttons
to switch to different add-modes. if no mode is chosen, zoom is default

ModPanel appears when a body is selected and provides buttons to alter the body's
properties, e.g. fix its position or alter its mass.

SliderPanel contains sliders to contol ticks_ahead and tick_ratio -- KILL THIS

SoundPanel controlls sooundmanager
'''


class MenuPanel(FloatLayout):

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

        self.visible = False

    def on_cur_mode(self, instance, value):
        self.logic.cur_guimode = self.logic.mode_map[value]

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
            pos_hint={'x': 0, 'y': 1.0/5},
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            source='./media/icons/pause.png',
            always_release=True
        )

        self.resetbutton = RealButton(
            './media/icons/reset.png',
            './media/icons/reset_pressed.png',
            self.logic.reset_planets,
            pos_hint={'x': 0, 'y': 2.0/5},
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            source='./media/icons/reset.png',
            always_release=True
        )

        self.draw_traces_btn = RealToggleButton(
            './media/icons/showorbit.png',
            './media/icons/showorbit_pressed.png',
            self.toggle_traces,
            pos_hint={'x': 0, 'y': 3.0/5},
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            source='./media/icons/showorbit.png',
            always_release=True
        )

        self.show_hide_button = RealButton(
            './media/icons/timer_panel.png',
            './media/icons/timer_panel.png',
            self.show_hide,
            pos_hint={'x': 0, 'y': 4.0/5},
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            source='./media/icons/timer_panel.png',
            always_release=True
        )

        self.ticks_ahead_label = Label(
            text='Ticks ahead',
            size_hint=(2, 0.2),
            pos_hint={'x': -5, 'y': 1},
            halign='left'
        )

        self.ticks_ahead_slider = Slider(
            min=100,
            max=1000,
            value=self.logic.settings['ticks_ahead'],
            step=1,
            orientation='horizontal',
            pos_hint={'x': -3, 'y': 1},
            size_hint=(3, 0.2)
        )

        self.timeratio_label = Label(
            text='Timeratio',
            size_hint=(2, 0.2),
            pos_hint={'x': -5, 'y': 6.0/5},
            halign='left'
        )

        self.timeratio_slider = Slider(
            min=0,
            max=2,
            value=self.logic.tick_ratio,
            step=.1,
            orientation='horizontal',
            pos_hint={'x': -3, 'y': 6.0/5},
            size_hint=(3, 0.2)
        )

        self.add_widget(self.menubutton)
        self.add_widget(self.pausebutton)
        self.add_widget(self.resetbutton)

        self.add_widget(self.draw_traces_btn)
        self.add_widget(self.show_hide_button)
        self.add_widget(self.ticks_ahead_label)
        self.add_widget(self.ticks_ahead_slider)

        self.add_widget(self.timeratio_label)
        self.add_widget(self.timeratio_slider)

        self.ticks_ahead_slider.bind(value=self.ticks_ahead_change)
        self.timeratio_slider.bind(value=self.timeratio_change)

        self.hide_labels = [
             self.ticks_ahead_slider,
             self.timeratio_slider,
        ]

        self.hide_sliders = [
            self.timeratio_label,
            self.ticks_ahead_label,
        ]

    def goto_menu(self, instance):
        self.parent.manager.current = 'menu'

    def pause_game(self, value):
        if value:
            self.logic.stop_game()
        else:
            self.logic.start_game()
        self.paused = value

    def ticks_ahead_change(self, instance, value):
        self.logic.settings['ticks_ahead'] = int(value)

    def timeratio_change(self, instance, value):
        self.logic.tick_ratio = value

    def toggle_traces(self, value):
        self.logic.lines = set()
        if not value:
            Clock.unschedule(self.logic.draw_traces)
            self.logic.gamezone.canvas.remove_group('nein')
        else:
            Clock.schedule_interval(self.logic.draw_traces, 0.5)

        self.logic.settings['traces'] = value

    def show_hide(self, value):
        if self.visible:
            scroll_label = Animation(
                pos_hint={
                    'x': -5
                },
                duration=0.5,
                t='in_out_back'
            )
            scroll_slider = Animation(
                pos_hint={
                    'x': -3
                },
                duration=0.5,
                t='in_out_back'
            )

            for item in self.hide_labels:
                scroll_label.start(item)
            for item in self.hide_sliders:
                scroll_slider.start(item)
            self.visible = False
        else:
            scroll_label = Animation(
                pos_hint={
                    'x': 2
                },
                duration=0.5,
                t='in_out_back'
            )
            scroll_slider = Animation(
                pos_hint={
                    'x': 0
                },
                duration=0.5,
                t='in_out_back'
            )

            for item in self.hide_labels:
                scroll_label.start(item)
            for item in self.hide_sliders:
                scroll_slider.start(item)
            self.visible = True


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

        self.build_interface()

    def on_cur_mode(self, instance, value):
        self.logic.cur_guimode = self.logic.mode_map[value]

    def build_interface(self):

        self.multi_button = RealMenuToggleButton(
            './media/icons/multipass.png',
            './media/icons/multipass_pressed.png',
            'multi',
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            pos_hint={'x': 0, 'y': 0},
            group='menu',
            source='./media/icons/multipass.png',
            allow_no_selection=True
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
            './media/icons/addplanet_pressed.png',
            'add_planet',
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            pos_hint={'x': 0.5, 'y': 0},
            group='menu',
            source='./media/icons/add_planet.png',
            allow_no_selection=True
        )

        self.show_hide_button = RealToggleButton(
            './media/icons/down.png',
            './media/icons/up.png',
            self.show_hide,
            pos_hint={'x': 0.75, 'y': 0},
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            source='./media/icons/down.png',
            always_release=True
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
            pos_hint={'x': -1, 'y': 0},
            size_hint=(1, 1)
        )

        self.value_label = Label(
            text='Some value: 9999',
            size_hint=(1, 1),
            pos_hint={'x': -2, 'y': 0},
            halign='left'
        )

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
                    'y': -1.05
                },
                duration=0.5,
                t='in_out_back'
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
                t='in_out_back'
            )
            for item in self.hide_items:
                scrolldown.start(item)
            # scrolldown.start(self.seltoggles)
            self.visible = True


class ModPanel(FloatLayout):

    '''
    buttons shown on the right bottom when a planet is selected. needs to be
    updated depending on planet data (fixed) and logic fixview mode
    '''
    logic = ObjectProperty(None)

    planet_fix_button = ObjectProperty(None)
    planet_del_button = ObjectProperty(None)

    planet_addmass_button = ObjectProperty(None)
    planet_submass_button = ObjectProperty(None)

    planet_fixview_button = ObjectProperty(None)

    visible = BooleanProperty(True)

    def __init__(self, iconsize, iconratio, **kwargs):
        super(ModPanel, self).__init__(**kwargs)
        self.logic = App.get_running_app().logic
        self.iconsize = iconsize
        self.iconratio = iconratio
        self.build_interface()

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

        self.planet_del_button = RealButton(
            './media/icons/delete.png',
            './media/icons/delete_pressed.png',
            self.logic.delete_selected,
            pos_hint={'x': 1.0 / 7, 'y': 0},
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            source='./media/icons/delete.png',
            always_release=True
        )

        self.planet_addmass_button = RealTimedButton(
            './media/icons/weightplus.png',
            './media/icons/weightplus_pressed.png',
            self.logic.addmass_selected,
            pos_hint={'x': 2.0 / 7, 'y': 0},
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            source='./media/icons/weightplus.png',
            always_release=True
        )

        self.planet_submass_button = RealTimedButton(
            './media/icons/weightminus.png',
            './media/icons/weightminus_pressed.png',
            self.logic.submass_selected,
            pos_hint={'x': 3.0 / 7, 'y': 0},
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            source='./media/icons/weightminus.png',
            always_release=True
        )

        self.planet_fixview_button = RealToggleButton(
            './media/icons/view.png',
            './media/icons/view_pressed.png',
            self.logic.fixview_selected,
            pos_hint={'x': 4.0 / 7, 'y': 0},
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            source='./media/icons/view.png',
            always_release=True
        )

        self.show_orbit_button = RealToggleButton(
            './media/icons/showorbit.png',
            './media/icons/showorbit_pressed.png',
            self.logic.show_orbit_selected,
            pos_hint={'x': 5.0 / 7, 'y': 0},
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            source='./media/icons/showorbit.png',
            always_release=True
        )

        self.planet_fix_button = RealToggleButton(
            './media/icons/fix.png',
            './media/icons/fix_pressed.png',
            self.logic.fix_selected,
            pos_hint={'x': 6.0 / 7, 'y': 0},
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            source='./media/icons/fix.png',
            always_release=True
        )

        self.add_widget(self.show_hide_button)

        self.add_widget(self.planet_fix_button)
        self.add_widget(self.planet_del_button)
        self.add_widget(self.planet_addmass_button)
        self.add_widget(self.planet_submass_button)
        self.add_widget(self.planet_fixview_button)
        self.add_widget(self.show_orbit_button)

        self.hide_items = [
            self.planet_fix_button, self.planet_del_button,
            self.planet_addmass_button, self.planet_submass_button,
            self.planet_fixview_button, self.show_orbit_button
        ]

    def update(self, **kwargs):
        # update buttons depending in planet selected. kwargs contain
        # complete planet dictionary and fixview flag from logic
        buttons_d = {
            self.planet_fix_button:     kwargs.get('fixed', False),
            self.planet_fixview_button: kwargs.get('fixview', False),
            self.show_orbit_button:     kwargs.get('show_orbit', False)
        }
        for button, value in buttons_d.items():
            button.pressed = value
            if value:
                button.source = button.realtexture_pressed
            else:
                button.source = button.realtexture
            button.reload()

    def show_hide(self, instance):
        if self.visible:
            for item in self.hide_items:
                scrolldown = Animation(
                    pos_hint={
                        'y': 1
                    },
                    duration=0.5,
                    t='in_out_back'
                )
                scrolldown.start(item)
            self.visible = False
        else:
            for item in self.hide_items:
                scrolldown = Animation(
                    pos_hint={
                        'y': 0
                    },
                    duration=0.5,
                    t='in_out_back'
                )
                scrolldown.start(item)
            self.visible = True


class SoundPanel(FloatLayout):
    '''Simple widget to show current track and start next one
    '''

    def __init__(self, iconsize, iconratio, soundmanager, **kwargs):
        super(SoundPanel, self).__init__(**kwargs)

        self.iconsize = iconsize
        self.iconratio = iconratio
        self.soundmanager = soundmanager

        self.build_interface()

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

        self.next_button = RealButton(
            './media/icons/arrow.png',
            './media/icons/arrow_pressed.png',
            self.next,
            pos_hint={'x': 0, 'y': 0},
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            source='./media/icons/reset.png',
            always_release=True
        )

        self.play_pause_button = RealToggleButton(
            './media/icons/up.png',
            './media/icons/down.png',
            self.play_pause,
            pos_hint={'x': 0, 'y': 0},
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            source='./media/icons/up.png',
            always_release=True
        )

        self.track_label = Label(
            text='very good music',
            size_hint=(1, 1),
            pos_hint={'x': 2, 'y': 0},
            halign='left'
        )

        self.hide_items = []
        self.visible = True

    def show_hide(self, instance):
        if self.visible:
            scrolldown = Animation(
                pos_hint={
                    'y': 1.05
                },
                duration=0.5,
                t='in_out_back'
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
                t='in_out_back'
            )
            for item in self.hide_items:
                scrolldown.start(item)
            # scrolldown.start(self.seltoggles)
            self.visible = True

    def next(self, instance):
        self.soundmanager.stop()
        self.soundmanager.next()
        if self.soundmanager.autoplay:
            self.soundmanager.start()

    def play_pause(self, instance):
        if self.soundmanager.autoplay:
            self.soundmanager.autoplay = False
            self.soundmanager.stop()
        else:
            self.soundmanager.autoplay = True
            self.soundmanager.start()

    def show_trackname(self):
        pass


class Gamezone(Scatter):
    '''
    This is the widget where the actuall simluation is displayed.
    Scatter widget can be zoomed, translated and rotated which is basically the
    zooming functionality. Hands down touch events to current mode.
    '''

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


class Infobox(ScrollView):

    '''UNUSED!
    Infoxbox displayed on the top right when a body is seleceted. Recieves
    Planet dictionary in update method to display planet information in
    corresponding labels
    '''

    layout = ObjectProperty(None)

    logic = ObjectProperty(None)

    planet_index = NumericProperty(0)

    planet_mass_label = ObjectProperty(None)
    planet_body_label = ObjectProperty(None)
    planet_vel_label = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Infobox, self).__init__(**kwargs)
        self.logic = App.get_running_app().logic
        self.build_interface()

    def build_interface(self):
        self.layout = GridLayout(
            cols=1,
            size_hint_y=None,
            spacing=10
        )
        self.layout.bind(minimum_height=self.layout.setter('height'))

        self.planet_mass_label = Label(
            text='mass',
            size_hint=(1, None)
        )

        self.planet_body_label = Label(
            text='body',
            size_hint=(1, None)
        )

        self.planet_vel_label = Label(
            text='vel',
            size_hint=(1, None)
        )

        self.layout.add_widget(self.planet_mass_label)
        self.layout.add_widget(self.planet_body_label)
        self.layout.add_widget(self.planet_vel_label)
        self.add_widget(self.layout)

    def update(self, **kwargs):
        # write smarter stuff here!!
        mass = kwargs.get('mass', 0)
        body = kwargs.get('body', '<None>')
        fixed = kwargs.get('fixed', False)
        temp = kwargs.get('temperature', 0.0)
        light = kwargs.get('light', 0.0)
        vel_x = round(kwargs.get('velocity_x', 0.0), 1)
        vel_y = round(kwargs.get('velocity_y', 0.0), 1)
        vel = (vel_x, vel_y)

        if fixed:
            self.planet_vel_label.text = 'Vel. : {}'.format((0, 0))
        else:
            self.planet_vel_label.text = 'Vel. : {}'.format(vel)
        self.planet_mass_label.text = 'Mass : {}'.format(round(mass, 2))
        self.planet_body_label.text = 'Body : {}'.format(body)
