from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.properties import *
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

# does it need logic?!
# everyone needs logic xD

from realbutton import RealButton

class SettingsScreen(Screen):

    logic = ObjectProperty(None)

    mainlayout = ObjectProperty(None)
    menubutton = ObjectProperty(None)


    def __init__(self, **kwargs):
       super(SettingsScreen, self).__init__(**kwargs)
       self.logic = App.get_running_app().logic
       self.iconsize = kwargs.get('iconsize')
       self.iconratio_x = kwargs.get('iconratio_x')
       self.iconratio_y = kwargs.get('iconratio_y')

       self.build_interface()

    def build_interface(self):
        self.mainlayout = FloatLayout()
        self.menubutton = RealButton(
            './media/icons/menu.png',
            './media/icons/menu_pressed.png',
            self.switchto_menu,
            size_hint = (None, None),
            size = (self.iconsize, self.iconsize),
            pos_hint = {'x' : 0, 'y' : 0},
            source = './media/icons/menu.png',
            always_release = True
        )

        self.mainlayout.add_widget(self.menubutton)

        self.add_widget(self.mainlayout)

        
    def switchto_menu(self, instance):
        self.manager.transition = FadeTransition()
        self.manager.current = 'menu'

    '''
    def on_touch_down(self, touch):
        self.manager.transition = FadeTransition()
        self.manager.current = 'menu'
    '''
