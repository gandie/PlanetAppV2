# KIVY
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import *
from kivy.core.window import Window

# CUSTOM
from mainscreen import MainScreen
from menuscreen import MenuScreen
from settingsscreen import SettingsScreen
from savegamescreen import SavegameScreen
from creditsscreen import CreditsScreen
from logic import Logic
from pc_config import ConfigController

# BUILTIN
import json
import copy
import os.path
import time

'''
main module of application. entry point when application is run. build-method
is run first, on_start and on_stop fire when app is actually started or closed.

also contains load/save mechanism for settings and savegames.
'''


class PlanetApp(App):

    # SCREENS AND SCREENMANAGER
    screenmanager = ObjectProperty(None)
    mainscreen = ObjectProperty(None)
    menuscreen = ObjectProperty(None)
    settingsscreen = ObjectProperty(None)
    savegamescreen = ObjectProperty(None)
    creditsscreen = ObjectProperty(None)

    logic = ObjectProperty(None)

    def build(self):
        self.calc_iconsize()
        self.settings = ConfigController('settings.json')
        self.logic = Logic(settings=self.settings)

        self.screenmanager = ScreenManager()

        self.mainscreen = MainScreen(
            logic=self.logic,
            iconsize=self.iconsize,
            iconratio_x=self.iconratio_x,
            iconratio_y=self.iconratio_y,
            name='main'
        )

        # MenuScreen does not need logic
        self.menuscreen = MenuScreen(name='menu')

        self.settingsscreen = SettingsScreen(
            logic=self.logic,
            iconsize=self.iconsize,
            iconratio_x=self.iconratio_x,
            iconratio_y=self.iconratio_y,
            name='settings'
        )

        self.savegamescreen = SavegameScreen(
            logic=self.logic,
            iconsize=self.iconsize,
            iconratio_x=self.iconratio_x,
            iconratio_y=self.iconratio_y,
            name='savegames'
        )

        self.creditsscreen = CreditsScreen(
            iconsize=self.iconsize,
            name='credits'
        )

        # XXX: order adding here reflects which screen is shown first!
        self.screenmanager.add_widget(self.menuscreen)
        self.screenmanager.add_widget(self.mainscreen)
        self.screenmanager.add_widget(self.settingsscreen)
        self.screenmanager.add_widget(self.savegamescreen)
        self.screenmanager.add_widget(self.creditsscreen)

        self.logic.apply_settings()

        return self.screenmanager

    def on_start(self):
        # self.load_settings()
        # self.logic.load_transitions()
        self.load_game()

    def on_stop(self):
        self.save_settings()
        self.save_game()

    def save_settings(self):
        self.settings.save()

    def load_game(self, slot='current'):
        save_name = 'save_{slot}.json'.format(slot=slot)
        save_exists = os.path.exists(save_name)
        if save_exists:
            self.logic.reset_planets(self)
            with open(save_name, 'r') as save_file:
                json_d = save_file.readline()
                planets_d = json.loads(json_d)
            for planet_d in planets_d.values():
                # make tuples from pos and vel
                pos = (planet_d['position_x'], planet_d['position_y'])
                vel = (planet_d['velocity_x'], planet_d['velocity_y'])
                self.logic.add_body(pos=pos, vel=vel, **planet_d)

    def save_game(self, slot='current'):
        # make deepcopy to avoid deleting widget ref from actual logic.planets
        planets_d = copy.deepcopy(self.logic.planets)
        # delete widget reference, it's not needed in savegames
        for index in planets_d:
            planets_d[index].pop('widget')

        json_d = json.dumps(planets_d)
        with open('save_{}.json'.format(slot), 'w') as save_file:
            save_file.write(json_d)

    def scan_savegames(self):
        save_mtimes = {}
        for i in range(1, 6):
            save_name = 'save_{}.json'.format(i)
            save_exists = os.path.exists(save_name)
            if save_exists:
                time_raw = os.path.getmtime('save_{}.json'.format(i))
                time_save = time.ctime(time_raw)
                save_mtimes[i] = str(time_save)
            else:
                save_mtimes[i] = '<Empty>'

        return save_mtimes

    def calc_iconsize(self):
        # TODO: is this neccessary?
        icon_count = 8
        window_height = Window.height
        window_width = Window.width
        iconsize = window_height / icon_count
        self.iconratio_y = float(iconsize) / window_height
        self.iconratio_x = float(iconsize) / window_width
        self.iconsize = iconsize


if __name__ == '__main__':
    PlanetApp().run()
