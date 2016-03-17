from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.properties import *
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

from kivy.uix.scrollview import ScrollView

# does it need logic?!
# everyone needs logic xD

from realbutton import RealButton
from kivy.uix.slider import Slider

from slot import SettingsSlot

class SettingsScreen(Screen):

    logic = ObjectProperty(None)

    mainlayout = ObjectProperty(None)
    menubutton = ObjectProperty(None)

    settingsview = ObjectProperty(None)

    def __init__(self, **kwargs):
       super(SettingsScreen, self).__init__(**kwargs)
       self.logic = App.get_running_app().logic
       self.iconsize = kwargs.get('iconsize')
       self.iconratio_x = kwargs.get('iconratio_x')
       self.iconratio_y = kwargs.get('iconratio_y')

       self.build_interface()

    def build_interface(self):
        self.mainlayout = FloatLayout()

        self.settingsview = ScrollView(
            size_hint = (0.7, 0.7),
            pos_hint = {'x' : 0.15, 'y' : 0.15}
        )

        self.settingslayout = GridLayout(
            cols = 1,
            size_hint_y = None,
            spacing = 10
        )
        self.settingslayout.bind(minimum_height = self.settingslayout.setter('height'))

        for i in range(5):
            slider = SettingsSlot(
                size_hint = (1, None),
                setting_min = 0,
                setting_max = 100,
                setting_value = 50,
                setting_type = 'number',
                label_text = 'Ball?'
            )
            self.settingslayout.add_widget(slider)

        for i in range(5):
            toggle = SettingsSlot(
                size_hint = (1, None),
                setting_min = 0,
                setting_max = 100,
                setting_value = 50,
                setting_type = 'bool',
                label_text = 'Nein?'
            )
            self.settingslayout.add_widget(toggle)


        self.menubutton = RealButton(
            './media/icons/menu.png',
            './media/icons/menu_pressed.png',
            self.switchto_menu,
            size_hint = (None, None),
            size = (self.iconsize, self.iconsize),
            pos_hint = {'x' : 0, 'y' : 0},
            source = './media/icons/menu.png',
            always_release = True
        )

        self.settingsview.add_widget(self.settingslayout)
        self.mainlayout.add_widget(self.menubutton)
        self.mainlayout.add_widget(self.settingsview)
        self.add_widget(self.mainlayout)

        
    def switchto_menu(self, instance):
        self.manager.transition = FadeTransition()
        self.manager.current = 'menu'


    '''
    'min_moon_mass' : 0,
    'min_planet_mass' : 30,
    'min_gasgiant_mass' : 2000,
    'min_sun_mass' : 50000,
    'min_bigsun_mass' : 500000,
    'min_giantsun_mass' : 1000000,
    'min_blackhole_mass' : 2000000,

    'moon_density' : 0.01,
    'planet_density' : 0.01,
    'gasgiant_density' : 0.008,
    'sun_density' : 0.005,
    'bigsun_density' : 0.006,
    'giantsun_density' : 0.01,
    'blackhole_density' : 1,
    '''



    '''
    def on_touch_down(self, touch):
        self.manager.transition = FadeTransition()
        self.manager.current = 'menu'
    '''
