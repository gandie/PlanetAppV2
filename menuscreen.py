from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.properties import *
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

# does it need logic?!
# everyone needs logic xD

class MenuScreen(Screen):

    '''
    add fancy main menu here!
    '''

    startbutton = ObjectProperty(None)
    quitbutton = ObjectProperty(None)
    settingsbutton = ObjectProperty(None)

    buttonlayout = ObjectProperty(None)
    mainlayout = ObjectProperty(None)

    logic = ObjectProperty(None)

    def __init__(self, **kwargs):
       super(MenuScreen, self).__init__(**kwargs)
       self.logic = App.get_running_app().logic
       self.build_interface()

    def switchto_main(self, instance):
        self.manager.transition = FadeTransition()
        self.manager.current = 'main'

    def switchto_settings(self, instance):
        self.manager.transition = FadeTransition()
        self.manager.current = 'settings'

    def build_interface(self):
        self.mainlayout = FloatLayout()
        self.buttonlayout = GridLayout(cols=1,
                                       size_hint=(0.4,0.5),
                                       pos_hint={"x":0.6,"y":0})
        self.startbutton = Button(text = "Start Game",
                                  on_press = self.switchto_main)
        self.settingsbutton = Button(text = "Settings",
                                  on_press = self.switchto_settings)

        self.buttonlayout.add_widget(self.startbutton)
        self.buttonlayout.add_widget(self.settingsbutton)
        self.mainlayout.add_widget(self.buttonlayout)
        self.add_widget(self.mainlayout)
