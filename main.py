from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import *

from mainscreen import MainScreen
from menuscreen import MenuScreen
from settingsscreen import SettingsScreen

from logic import Logic

import json

class PlanetApp(App):

    screenmanager = ObjectProperty(None)
    mainscreen = ObjectProperty(None)
    menuscreen = ObjectProperty(None)
    settingsscreen = ObjectProperty(None)

    logic = ObjectProperty(None)

    def build(self):

        self.logic = Logic()
        self.screenmanager = ScreenManager()
        self.mainscreen = MainScreen(name = 'main')
        self.menuscreen = MenuScreen(name = 'menu')
        self.settingsscreen = SettingsScreen(name = 'settings')
        self.screenmanager.add_widget(self.menuscreen)
        self.screenmanager.add_widget(self.mainscreen)
        self.screenmanager.add_widget(self.settingsscreen)

        return self.screenmanager

    def on_start(self):
        try:
            f = open('save.json', 'r')
            json_d = f.readline()
            D = json.loads(json_d)
            for index in D:
                pos = (D[index]['position_x'], D[index]['position_y'])
                vel = (D[index]['velocity_x'], D[index]['velocity_y'])
                self.logic.add_body(pos = pos, vel = vel, **D[index])
            f.close()
        except:
            print 'nein'

    def save_game(self):
        f = open('save.json', 'w')
        D = self.logic.planets
        # delete widget reference
        for index in D:
            D[index].pop('widget')
        json_d = json.dumps(D)
        f.write(json_d)
        f.close()

    def on_stop(self):
        self.save_game()

if __name__ == '__main__':
    PlanetApp().run()
