# KIVY
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.properties import *
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.app import App


class Infobox(ScrollView):

    '''
    infobox show when planet is selected
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
