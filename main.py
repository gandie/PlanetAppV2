from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import *

from mainscreen import MainScreen
from menuscreen import MenuScreen


class PlanetApp(App):

    screenmanager = ObjectProperty(None)
    mainscreen = ObjectProperty(None)
    menuscreen = ObjectProperty(None)

    def build(self):

        self.screenmanager = ScreenManager()
        self.mainscreen = MainScreen(name='main')
        self.menuscreen = MenuScreen(name='menu')
        self.screenmanager.add_widget(self.menuscreen)
        self.screenmanager.add_widget(self.mainscreen)

        return self.screenmanager

if __name__ == '__main__':
    PlanetApp().run()
