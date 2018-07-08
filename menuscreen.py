# KIVY
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.properties import *
from kivy.uix.floatlayout import FloatLayout

# CUSTOM
from realbutton import RealButton

'''
Menuscreen shown when app has started. Access savegames, settings, credits and
the actual game from here.
'''


class MenuScreen(Screen):

    startbutton = ObjectProperty(None)
    creditsbutton = ObjectProperty(None)
    settingsbutton = ObjectProperty(None)
    savegamebutton = ObjectProperty(None)
    mainlayout = ObjectProperty(None)
    logic = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.build_interface()

    def switchto_main(self, instance):
        self.manager.transition = FadeTransition()
        self.manager.current = 'main'

    def switchto_settings(self, instance):
        self.manager.transition = FadeTransition()
        self.manager.current = 'settings'

    def switchto_savegames(self, instance):
        self.manager.transition = FadeTransition()
        self.manager.current = 'savegames'

    def switchto_credits(self, instance):
        self.manager.transition = FadeTransition()
        self.manager.current = 'credits'

    def build_interface(self):
        self.mainlayout = FloatLayout()

        self.startbutton = RealButton(
            './media/buttons/play.png',
            './media/buttons/play_pressed.png',
            self.switchto_main,
            size_hint=(0.3, 0.2),
            pos_hint={'x': 0, 'y': 0.7},
            source='./media/buttons/play.png',
            always_release=True
        )

        self.settingsbutton = RealButton(
            './media/buttons/settings.png',
            './media/buttons/settings_pressed.png',
            self.switchto_settings,
            size_hint=(0.3, 0.2),
            pos_hint={'x': 0.7, 'y': 0.7},
            source='./media/buttons/settings.png',
            always_release=True
        )

        self.savegamebutton = RealButton(
            './media/buttons/saves.png',
            './media/buttons/saves_pressed.png',
            self.switchto_savegames,
            size_hint=(0.3, 0.2),
            pos_hint={'x': 0, 'y': 0.1},
            source='./media/buttons/saves.png',
            always_release=True
        )

        self.creditsbutton = RealButton(
            './media/buttons/credits.png',
            './media/buttons/credits_pressed.png',
            self.switchto_credits,
            size_hint=(0.3, 0.2),
            pos_hint={'x': 0.7, 'y': 0.1},
            source='./media/buttons/credits.png',
            always_release=True
        )

        self.mainlayout.add_widget(self.startbutton)
        self.mainlayout.add_widget(self.creditsbutton)
        self.mainlayout.add_widget(self.settingsbutton)
        self.mainlayout.add_widget(self.savegamebutton)
        self.add_widget(self.mainlayout)
