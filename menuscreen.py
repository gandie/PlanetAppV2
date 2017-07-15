# KIVY
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.properties import *
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.core.window import Window

# CUSTOM
from realbutton import RealButton

'''
Menuscreen shown when app has started. Access savegames, settings, credits and
tutorial from here.
'''


class MenuScreen(Screen):

    startbutton = ObjectProperty(None)
    tutorialbutton = ObjectProperty(None)
    settingsbutton = ObjectProperty(None)
    savegamebutton = ObjectProperty(None)
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

    def switchto_savegames(self, instance):
        self.manager.transition = FadeTransition()
        self.manager.current = 'savegames'

    def switchto_tutorial(self, instance):
        self.logic.tutorial_mode = True
        self.logic.reset_planets(self)
        self.manager.transition = FadeTransition()
        self.manager.current = 'main'

    def build_interface(self):
        self.mainlayout = FloatLayout()

        self.startbutton = RealButton(
            './media/buttons/play.png',
            './media/buttons/play_pressed.png',
            self.switchto_main,
            size_hint=(0.4, 0.4),
            pos_hint={'x': 0.6, 'y': 0.3},
            source='./media/buttons/play.png',
            always_release=True
        )

        self.settingsbutton = RealButton(
            './media/buttons/settings.png',
            './media/buttons/settings_pressed.png',
            self.switchto_settings,
            size_hint=(0.2, 0.2),
            pos_hint={'x': 0.32, 'y': 0.7},
            source='./media/buttons/settings.png',
            always_release=True
        )

        self.savegamebutton = RealButton(
            './media/buttons/saves.png',
            './media/buttons/saves_pressed.png',
            self.switchto_savegames,
            size_hint=(0.2, 0.2),
            pos_hint={'x': 0.07, 'y': 0.4},
            source='./media/buttons/saves.png',
            always_release=True
        )

        self.tutorialbutton = RealButton(
            './media/buttons/tutorial.png',
            './media/buttons/tutorial_pressed.png',
            self.switchto_tutorial,
            size_hint=(0.2, 0.2),
            pos_hint={'x': 0.57, 'y': 0.06},
            source='./media/buttons/tutorial.png',
            always_release=True
        )

        self.mainlayout.add_widget(self.startbutton)
        self.mainlayout.add_widget(self.tutorialbutton)
        self.mainlayout.add_widget(self.settingsbutton)
        self.mainlayout.add_widget(self.savegamebutton)
        self.add_widget(self.mainlayout)
