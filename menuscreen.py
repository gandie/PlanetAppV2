from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import FadeTransition

# does it need logic?!

class MenuScreen(Screen):

    '''
    add fancy main menu here!
    '''

    def on_touch_down(self, touch):
        self.manager.transition = FadeTransition()
        self.manager.current = 'main'
