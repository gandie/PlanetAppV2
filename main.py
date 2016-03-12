from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import *

from mainscreen import MainScreen

from menuscreen import MenuScreen
from settingsscreen import SettingsScreen
from savegamescreen import SavegameScreen

from logic import Logic

import json

import copy
import os.path
import time

from kivy.core.window import Window

class PlanetApp(App):

    screenmanager = ObjectProperty(None)
    mainscreen = ObjectProperty(None)
    menuscreen = ObjectProperty(None)
    settingsscreen = ObjectProperty(None)
    savegamescreen = ObjectProperty(None)

    logic = ObjectProperty(None)

    def build(self):
        self.calc_iconsize()
        self.logic = Logic()
        self.screenmanager = ScreenManager()
        self.mainscreen = MainScreen(
            name = 'main', 
            iconsize = self.iconsize,
            iconratio_x = self.iconratio_x,
            iconratio_y = self.iconratio_y
        )
        self.menuscreen = MenuScreen(name = 'menu')
        self.settingsscreen = SettingsScreen(
            name = 'settings',
            iconsize = self.iconsize,
            iconratio_x = self.iconratio_x,
            iconratio_y = self.iconratio_y
        )
        self.savegamescreen = SavegameScreen(
            name = 'savegames',
            iconsize = self.iconsize,
            iconratio_x = self.iconratio_x,
            iconratio_y = self.iconratio_y
        )
        self.screenmanager.add_widget(self.menuscreen)
        self.screenmanager.add_widget(self.mainscreen)
        self.screenmanager.add_widget(self.settingsscreen)
        self.screenmanager.add_widget(self.savegamescreen)

        return self.screenmanager

    def on_start(self):
        self.load_settings()
        self.logic.load_transitions()
        self.load_game()

    def on_stop(self):
        self.save_settings()
        self.save_game()

    def load_settings(self):
        try:
            f = open('settings.json', 'r')
            json_d = f.readline()
            D = json.loads(json_d)
            f.close
        except:
            # default settings
            D = {
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

                'norm_temp' : 200
            }
        self.logic.settings = D

    def save_settings(self):
        f = open('settings.json', 'w')
        D = copy.deepcopy(self.logic.settings)
        json_d = json.dumps(D)
        f.write(json_d)
        f.close()

    def load_game(self, slot = 'current'):
        self.logic.reset_planets(self)
        try:
            f = open('save_{}.json'.format(slot), 'r')
            json_d = f.readline()
            D = json.loads(json_d)
            for index in D:
                pos = (D[index]['position_x'], D[index]['position_y'])
                vel = (D[index]['velocity_x'], D[index]['velocity_y'])
                self.logic.add_body(pos = pos, vel = vel, **D[index])
            f.close()
        except:
            print 'nein'

    def save_game(self, slot = 'current'):
        f = open('save_{}.json'.format(slot), 'w')
        # make deepcopy to avoid deleting widget ref from logic.planets
        D = copy.deepcopy(self.logic.planets)
        # delete widget reference, it's not needed in savegames
        for index in D:
            D[index].pop('widget')
        json_d = json.dumps(D)
        f.write(json_d)
        f.close()

    def scan_savegames(self):
        save_mtimes = {}
        for i in range(1, 6):
            try:
                time_raw = os.path.getmtime('save_{}.json'.format(i))
                time_save = time.ctime(time_raw)
                save_mtimes[i] = str(time_save)
            except Exception as e:
                save_mtimes[i] = '<Empty>'

        return save_mtimes

    def calc_iconsize(self):
        icon_count = 8
        window_height = Window.height
        window_width = Window.width
        iconsize = window_height / icon_count
        self.iconratio_y = float(iconsize) / window_height
        self.iconratio_x = float(iconsize) / window_width
        self.iconsize = iconsize

if __name__ == '__main__':
    PlanetApp().run()
