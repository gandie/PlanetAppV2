from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from layout import MainScreen

sm = ScreenManager()
main = MainScreen(name='main')
sm.add_widget(main)

class PlanetApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    PlanetApp().run()
