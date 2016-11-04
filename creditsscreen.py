# KIVY
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.properties import *
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

# CUSTOM
from realbutton import RealButton

class CreditsScreen(Screen):

    logic = ObjectProperty(None)
    mainlayout = ObjectProperty(None)

    def __init__(self, **kwargs):
       super(CreditsScreen, self).__init__(**kwargs)
       self.logic = App.get_running_app().logic
       self.iconsize = kwargs.get('iconsize')
       self.iconratio_x = kwargs.get('iconratio_x')
       self.iconratio_y = kwargs.get('iconratio_y')

       self.build_interface()


    def build_interface(self):
        self.mainlayout = FloatLayout()

        self.creditsview = ScrollView(
            size_hint = (0.7, 0.7),
            pos_hint = {'x' : 0.15, 'y' : 0.15}
        )

        self.creditslayout = GridLayout(
            cols = 1,
            size_hint_y = None,
            spacing = 10
        )
        self.creditslayout.bind(minimum_height = self.creditslayout.setter('height'))
        self.creditsview.add_widget(self.creditslayout)

        for line in self.creditlines():
            creditline = Label(
                text = line,
                size_hint = (1, None)
            )
            self.creditslayout.add_widget(creditline)

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
        self.mainlayout.add_widget(self.creditsview)
        self.add_widget(self.mainlayout)

    def switchto_menu(self, instance):
        self.manager.transition = FadeTransition()
        self.manager.current = 'menu'

    def creditlines(self):
        return [
            '#### Credits ####',
            '',
            '## Devs ##',
            'gandie -- main developer -- lb@perfact.de',
            'mattis -- developer, tester',
            'nichtpeter -- developer, tester',
            'jean_borrow -- developer, tester',
            '',
            '## Artists ##',
            'dude -- layout, graphics',
            '',
            '## Tester ##',
            'McStorm',
            'Peter Oswald',
            'Uedii',
            'many many more people from FLAFLA',
            '',
            '## Thanks to ##',
            'Everyone else i forgtot to mention'
            ]
