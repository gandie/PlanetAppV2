# KIVY
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.properties import *
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.scrollview import ScrollView

# CUSTOM
from realbutton import RealButton
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

       self.setting_items = {}

       self.build_interface()

    def on_enter(self):
        logic_settings = self.logic.settings
        for key in logic_settings.keys():
            if self.setting_items.has_key(key):
                self.setting_items[key].value = logic_settings[key]

    def on_leave(self):
        logic_settings = self.logic.settings
        for key in logic_settings.keys():
            if self.setting_items.has_key(key):
                logic_settings[key] = self.setting_items[key].value

    def build_interface(self):
        self.mainlayout = FloatLayout()

        self.settingsview = ScrollView(
            size_hint = (0.7, 0.7),
            pos_hint = {'x' : 0.15, 'y' : 0.15}
        )

        # use gridlayout to put items into scrollview
        self.settingslayout = GridLayout(
            cols = 1,
            size_hint_y = None,
            spacing = 10
        )

        # magic binding
        self.settingslayout.bind(minimum_height = self.settingslayout.setter('height'))

        # create items and add to settingslayout
        self.planet_mass = SettingsSlot(
                size_hint = (1, None),
                #height = 100,
                setting_min = 10,
                setting_max = 50,
                setting_value = 30,
                setting_type = 'number',
                label_text = 'Min. Planet Mass'
            )
        self.setting_items['min_planet_mass'] = self.planet_mass
        self.settingslayout.add_widget(self.planet_mass)

        self.gasgiant_mass = SettingsSlot(
                size_hint = (1, None),
                #height = 100,
                setting_min = 500,
                setting_max = 3500,
                setting_value = 2000,
                setting_type = 'number',
                label_text = 'Min. Gasgiant Mass'
            )
        self.setting_items['min_gasgiant_mass'] = self.gasgiant_mass
        self.settingslayout.add_widget(self.gasgiant_mass)

        self.sun_mass = SettingsSlot(
                size_hint = (1, None),
                #height = 100,
                setting_min = 5000,
                setting_max = 95000,
                setting_value = 50000,
                setting_type = 'number',
                label_text = 'Min. Sun Mass'
            )
        self.setting_items['min_sun_mass'] = self.sun_mass
        self.settingslayout.add_widget(self.sun_mass)

        self.bigsun_mass = SettingsSlot(
                size_hint = (1, None),
                #height = 100,
                setting_min = 100000,
                setting_max = 900000,
                setting_value = 500000,
                setting_type = 'number',
                label_text = 'Min. Bigsun Mass'
            )
        self.setting_items['min_bigsun_mass'] = self.bigsun_mass
        self.settingslayout.add_widget(self.bigsun_mass)

        self.giantsun_mass = SettingsSlot(
                size_hint = (1, None),
                #height = 100,
                setting_min = 500000,
                setting_max = 1500000,
                setting_value = 1000000,
                setting_type = 'number',
                label_text = 'Min. Giantsun Mass'
            )
        self.setting_items['min_giantsun_mass'] = self.giantsun_mass
        self.settingslayout.add_widget(self.giantsun_mass)

        self.blackhole_mass = SettingsSlot(
                size_hint = (1, None),
                #height = 100,
                setting_min = 500000,
                setting_max = 1500000,
                setting_value = 1000000,
                setting_type = 'number',
                label_text = 'Min. Blackhole Mass'
            )
        self.setting_items['min_blackhole_mass'] = self.blackhole_mass
        self.settingslayout.add_widget(self.blackhole_mass)

        self.moon_density = SettingsSlot(
                size_hint = (1, None),
                #height = 100,
                setting_min = 0.005,
                setting_max = 0.015,
                setting_value = 0.01,
                setting_type = 'number',
                label_text = 'Moon sparsity'
            )
        self.setting_items['moon_density'] = self.moon_density
        self.settingslayout.add_widget(self.moon_density)

        self.planet_density = SettingsSlot(
                size_hint = (1, None),
                #height = 100,
                setting_min = 0.005,
                setting_max = 0.015,
                setting_value = 0.01,
                setting_type = 'number',
                label_text = 'Planet sparsity'
            )
        self.setting_items['planet_density'] = self.planet_density
        self.settingslayout.add_widget(self.planet_density)

        self.gasgiant_density = SettingsSlot(
                size_hint = (1, None),
                #height = 100,
                setting_min = 0.004,
                setting_max = 0.012,
                setting_value = 0.008,
                setting_type = 'number',
                label_text = 'Gasgiant sparsity'
            )
        self.setting_items['gasgiant_density'] = self.gasgiant_density
        self.settingslayout.add_widget(self.gasgiant_density)

        self.sun_density = SettingsSlot(
                size_hint = (1, None),
                #height = 100,
                setting_min = 0.001,
                setting_max = 0.009,
                setting_value = 0.005,
                setting_type = 'number',
                label_text = 'Sun sparsity'
            )
        self.setting_items['sun_density'] = self.sun_density
        self.settingslayout.add_widget(self.sun_density)

        self.bigsun_density = SettingsSlot(
                size_hint = (1, None),
                #height = 100,
                setting_min = 0.002,
                setting_max = 0.01,
                setting_value = 0.006,
                setting_type = 'number',
                label_text = 'Bigsun sparsity'
            )
        self.setting_items['bigsun_density'] = self.bigsun_density
        self.settingslayout.add_widget(self.bigsun_density)

        self.giantsun_density = SettingsSlot(
                size_hint = (1, None),
                #height = 100,
                setting_min = 0.005,
                setting_max = 0.015,
                setting_value = 0.01,
                setting_type = 'number',
                label_text = 'Giantsun sparsity'
            )
        self.setting_items['giantsun_density'] = self.giantsun_density
        self.settingslayout.add_widget(self.giantsun_density)

        self.blackhole_density = SettingsSlot(
                size_hint = (1, None),
                #height = 100,
                setting_min = 0.8,
                setting_max = 1.2,
                setting_value = 1,
                setting_type = 'number',
                label_text = 'Blackhole sparsity'
            )
        self.setting_items['blackhole_density'] = self.blackhole_density
        self.settingslayout.add_widget(self.blackhole_density)

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

        self.creditsbutton = Button (
            text = 'Credits',
            size_hint = (0.1, 0.1),
            pos_hint = {'x' : 0.9, 'y' : 0},
            on_press = self.switchto_credits
        )

        # add settingslayout to scrollview
        self.settingsview.add_widget(self.settingslayout)
        self.mainlayout.add_widget(self.menubutton)
        self.mainlayout.add_widget(self.creditsbutton)
        self.mainlayout.add_widget(self.settingsview)
        self.add_widget(self.mainlayout)

        
    def switchto_menu(self, instance):
        self.manager.transition = FadeTransition()
        self.manager.current = 'menu'

    def switchto_credits(self, instance):
        self.manager.transition = FadeTransition()
        self.manager.current = 'credits'
