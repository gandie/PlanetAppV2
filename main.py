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

class PlanetApp(App):

    screenmanager = ObjectProperty(None)
    mainscreen = ObjectProperty(None)
    menuscreen = ObjectProperty(None)
    settingsscreen = ObjectProperty(None)
    savegamescreen = ObjectProperty(None)

    logic = ObjectProperty(None)

    def build(self):

        self.logic = Logic()
        self.screenmanager = ScreenManager()
        self.mainscreen = MainScreen(name = 'main')
        self.menuscreen = MenuScreen(name = 'menu')
        self.settingsscreen = SettingsScreen(name = 'settings')
        self.savegamescreen = SavegameScreen(name = 'savegames')
        self.screenmanager.add_widget(self.menuscreen)
        self.screenmanager.add_widget(self.mainscreen)
        self.screenmanager.add_widget(self.settingsscreen)
        self.screenmanager.add_widget(self.savegamescreen)

        return self.screenmanager

    def on_start(self):
        self.load_settings()
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
            print 'nein, keine settings'
            D = {
                'min_planet_mass' : 20,
                'min_sun_mass' : 50000,
                'planet_density' : 0.01,
                'sun_density' : 0.005,
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
            #self.logic.calc_gravity(1)
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

if __name__ == '__main__':
    PlanetApp().run()
