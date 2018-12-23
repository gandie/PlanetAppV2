# KIVY
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.properties import *
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

# CUSTOM
from realbutton import RealButton

'''
simple screen to show some credits using a scrollview
'''


class CreditsScreen(Screen):


    logic = ObjectProperty(None)
    mainlayout = ObjectProperty(None)

    def __init__(self, iconsize, **kwargs):
        super(CreditsScreen, self).__init__(**kwargs)

        self.iconsize = iconsize

        self.build_interface()

    def build_interface(self):
        self.mainlayout = FloatLayout()

        self.creditsview = ScrollView(
            size_hint=(0.7, 0.7),
            pos_hint={'x': 0.15, 'y': 0.15}
        )

        self.creditslayout = GridLayout(
            cols=1,
            size_hint_y=None,
            spacing=10
        )
        self.creditslayout.bind(
            minimum_height=self.creditslayout.setter('height')
        )
        self.creditsview.add_widget(self.creditslayout)

        for line in self.creditlines():
            creditline = Label(
                text=line,
                size_hint=(1, None)
            )
            self.creditslayout.add_widget(creditline)

        self.menubutton = RealButton(
            './media/icons/arrowleft.png',
            './media/icons/arrowleft_pressed.png',
            self.switchto_menu,
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            pos_hint={'x': 0, 'y': 0},
            source='./media/icons/arrowleft.png',
            always_release=True
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
            'gandie -- main developer -- lars@bergmann82.de',
            'https://github.com/gandie'
            '',
            '## Artists ##',
            'dude -- layout, graphics, music',
            'https://www.instagram.com/ikone.official/',
            '',
            'rafikibeats -- music',
            'https://soundcloud.com/rafikibeats',
            '',
            '## Tester ##',
            'McStorm',
            'mattis',
            'nichtpeter',
            'jean_borrow',
            'Peter Oswald',
            'Uedii',
            'many many more people from FLAFLA',
            '',
            '## Thanks to ##',
            'My roommates for enduring my endless hours of talk about this project',
            'Everyone else i forgtot to mention'
        ]
