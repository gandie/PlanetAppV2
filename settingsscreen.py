from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.properties import *
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

# does it need logic?!
# everyone needs logic xD

class SettingsScreen(Screen):

    logic = ObjectProperty(None)

    def __init__(self, **kwargs):
       super(SettingsScreen, self).__init__(**kwargs)
       self.logic = App.get_running_app().logic
       self.build_interface()

    def build_interface(self):
        pass

    def on_touch_down(self, touch):
        self.manager.transition = FadeTransition()
        self.manager.current = 'menu'
