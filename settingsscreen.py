# KIVY
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.properties import *
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

# CUSTOM
from realbutton import RealButton
from slot import SettingsSlot

'''
screen to alter settings. basically a scrollview containing settings slots.
also access kivy settings from here.
'''


# TODO: should be view part of mvc pattern (to be implemented)
class SettingsScreen(Screen):

    logic = ObjectProperty(None)
    mainlayout = ObjectProperty(None)
    menubutton = ObjectProperty(None)
    settingsbutton = ObjectProperty(None)
    settingsview = ObjectProperty(None)

    def __init__(self, logic, iconsize, iconratio_x, iconratio_y, **kwargs):

        super(SettingsScreen, self).__init__(**kwargs)

        self.logic = logic

        self.iconsize = iconsize
        self.iconratio_x = iconratio_x
        self.iconratio_y = iconratio_y

        self.setting_items = {}

        self.build_interface()

    def on_enter(self):
        '''
        get settings from logic
        '''
        logic_settings = self.logic.settings
        for key in logic_settings.keys():
            if key in self.setting_items:
                self.setting_items[key].value = logic_settings[key]

    def on_leave(self):
        '''
        write setting to logic and save to file
        '''
        logic_settings = self.logic.settings
        for key in logic_settings.keys():
            if key in self.setting_items:
                logic_settings[key] = self.setting_items[key].value
        self.logic.apply_settings()
        App.get_running_app().save_settings()

    def build_interface(self):
        # TODO: check min / max of settings against defaults!
        self.mainlayout = FloatLayout()

        self.settingsview = ScrollView(
            size_hint=(0.7, 0.7),
            pos_hint={'x': 0.15, 'y': 0.15}
        )

        # use gridlayout to put items into scrollview
        self.settingslayout = GridLayout(
            cols=1,
            size_hint_y=None,
            spacing=10
        )

        # magic binding
        self.settingslayout.bind(
            minimum_height=self.settingslayout.setter('height')
        )

        self.engine_select = SettingsSlot(
            size_hint=(1, None),
            setting_type='select',
            label_text='Engine',
            items=['cplanet', 'crk4engine', 'pythonrk4']
            # items=['cplanet', 'pythonrk4']
        )
        self.setting_items['engine'] = self.engine_select
        self.settingslayout.add_widget(self.engine_select)

        self.background_toggle = SettingsSlot(
            size_hint=(1, None),
            setting_min=0.8,
            setting_max=1.2,
            setting_value=1,
            setting_type='bool',
            label_text='Background'
        )
        self.setting_items['background'] = self.background_toggle
        self.settingslayout.add_widget(self.background_toggle)

        ''' DEACTIVATED, needs rework!
        self.tutorial_toggle = SettingsSlot(
            size_hint=(1, None),
            setting_min=0.8,
            setting_max=1.2,
            setting_value=1,
            setting_type='bool',
            label_text='Tutorial (broken!)'
        )
        self.setting_items['show_tutorial'] = self.tutorial_toggle
        self.settingslayout.add_widget(self.tutorial_toggle)
        '''

        self.ticks_ahead = SettingsSlot(
            size_hint=(1, None),
            setting_min=100,
            setting_max=1000,
            setting_value=100,
            setting_type='number',
            label_text='Ticks ahead'
        )
        self.setting_items['ticks_ahead'] = self.ticks_ahead
        self.settingslayout.add_widget(self.ticks_ahead)

        self.music_volume = SettingsSlot(
            size_hint=(1, None),
            setting_min=0,
            setting_max=1,
            setting_value=0.0,
            setting_type='number',
            label_text='Music volume'
        )
        self.setting_items['music_volume'] = self.music_volume
        self.settingslayout.add_widget(self.music_volume)

        # create items and add to settingslayout
        self.multi_shot_min = SettingsSlot(
            size_hint=(1, None),
            setting_min=5,
            setting_max=50,
            setting_value=10,
            setting_type='number',
            label_text='Min Multi Shots'
        )
        self.setting_items['multi_shot_min'] = self.multi_shot_min
        self.settingslayout.add_widget(self.multi_shot_min)

        self.multi_shot_max = SettingsSlot(
            size_hint=(1, None),
            setting_min=50,
            setting_max=100,
            setting_value=75,
            setting_type='number',
            label_text='Max Multi Shots'
        )
        self.setting_items['multi_shot_max'] = self.multi_shot_max
        self.settingslayout.add_widget(self.multi_shot_max)

        self.planet_mass = SettingsSlot(
            size_hint=(1, None),
            setting_min=10,
            setting_max=50,
            setting_value=30,
            setting_type='number',
            label_text='Min. Planet Mass'
        )
        self.setting_items['min_planet_mass'] = self.planet_mass
        self.settingslayout.add_widget(self.planet_mass)

        self.gasgiant_mass = SettingsSlot(
            size_hint=(1, None),
            setting_min=500,
            setting_max=3500,
            setting_value=2000,
            setting_type='number',
            label_text='Min. Gasgiant Mass'
        )
        self.setting_items['min_gasgiant_mass'] = self.gasgiant_mass
        self.settingslayout.add_widget(self.gasgiant_mass)

        self.sun_mass = SettingsSlot(
            size_hint=(1, None),
            setting_min=5000,
            setting_max=95000,
            setting_value=50000,
            setting_type='number',
            label_text='Min. Sun Mass'
        )
        self.setting_items['min_sun_mass'] = self.sun_mass
        self.settingslayout.add_widget(self.sun_mass)

        self.bigsun_mass = SettingsSlot(
            size_hint=(1, None),
            setting_min=100000,
            setting_max=900000,
            setting_value=500000,
            setting_type='number',
            label_text='Min. Bigsun Mass'
        )
        self.setting_items['min_bigsun_mass'] = self.bigsun_mass
        self.settingslayout.add_widget(self.bigsun_mass)

        self.giantsun_mass = SettingsSlot(
            size_hint=(1, None),
            setting_min=500000,
            setting_max=1500000,
            setting_value=1000000,
            setting_type='number',
            label_text='Min. Giantsun Mass'
        )
        self.setting_items['min_giantsun_mass'] = self.giantsun_mass
        self.settingslayout.add_widget(self.giantsun_mass)

        self.blackhole_mass = SettingsSlot(
            size_hint=(1, None),
            setting_min=1000000,
            setting_max=3000000,
            setting_value=2000000,
            setting_type='number',
            label_text='Min. Blackhole Mass'
        )
        self.setting_items['min_blackhole_mass'] = self.blackhole_mass
        self.settingslayout.add_widget(self.blackhole_mass)

        self.moon_density = SettingsSlot(
            size_hint=(1, None),
            setting_min=1,
            setting_max=3,
            setting_value=2,
            setting_type='number',
            label_text='Moon density'
        )
        self.setting_items['moon_density'] = self.moon_density
        self.settingslayout.add_widget(self.moon_density)

        self.planet_density = SettingsSlot(
            size_hint=(1, None),
            setting_min=1,
            setting_max=5,
            setting_value=3,
            setting_type='number',
            label_text='Planet density'
        )
        self.setting_items['planet_density'] = self.planet_density
        self.settingslayout.add_widget(self.planet_density)

        self.gasgiant_density = SettingsSlot(
            size_hint=(1, None),
            setting_min=1,
            setting_max=5,
            setting_value=3,
            setting_type='number',
            label_text='Gasgiant density'
        )
        self.setting_items['gasgiant_density'] = self.gasgiant_density
        self.settingslayout.add_widget(self.gasgiant_density)

        self.sun_density = SettingsSlot(
            size_hint=(1, None),
            setting_min=2,
            setting_max=6,
            setting_value=4,
            setting_type='number',
            label_text='Sun density'
        )
        self.setting_items['sun_density'] = self.sun_density
        self.settingslayout.add_widget(self.sun_density)

        self.bigsun_density = SettingsSlot(
            size_hint=(1, None),
            setting_min=2,
            setting_max=6,
            setting_value=4,
            setting_type='number',
            label_text='Bigsun density'
        )
        self.setting_items['bigsun_density'] = self.bigsun_density
        self.settingslayout.add_widget(self.bigsun_density)

        self.giantsun_density = SettingsSlot(
            size_hint=(1, None),
            setting_min=2,
            setting_max=6,
            setting_value=4,
            setting_type='number',
            label_text='Giantsun density'
        )
        self.setting_items['giantsun_density'] = self.giantsun_density
        self.settingslayout.add_widget(self.giantsun_density)

        self.blackhole_density = SettingsSlot(
            size_hint=(1, None),
            setting_min=10,
            setting_max=30,
            setting_value=20,
            setting_type='number',
            label_text='Blackhole density'
        )
        self.setting_items['blackhole_density'] = self.blackhole_density
        self.settingslayout.add_widget(self.blackhole_density)

        self.menubutton = RealButton(
            './media/icons/arrowleft.png',
            './media/icons/arrowleft.png',
            self.switchto_menu,
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            pos_hint={'x': 0, 'y': 0},
            source='./media/icons/arrowleft.png',
            always_release=True
        )

        self.settingsbutton = Button(
            text='KivySettings',
            size_hint=(1, None),
            on_press=self.switchto_kivysettings
        )
        self.settingslayout.add_widget(self.settingsbutton)

        # add settingslayout to scrollview
        self.settingsview.add_widget(self.settingslayout)
        self.mainlayout.add_widget(self.menubutton)
        self.mainlayout.add_widget(self.settingsview)
        self.add_widget(self.mainlayout)

    def switchto_menu(self, instance):
        self.manager.transition = FadeTransition()
        self.manager.current = 'menu'

    def switchto_credits(self, instance):
        self.manager.transition = FadeTransition()
        self.manager.current = 'credits'

    def switchto_kivysettings(self, instance):
        App.get_running_app().open_settings()
