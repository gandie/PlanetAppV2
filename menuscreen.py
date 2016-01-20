from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import FadeTransition

class MenuScreen(Screen):

    def on_touch_down(self, touch):
        self.manager.transition = FadeTransition()
        self.manager.current = 'main'
