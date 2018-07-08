# KIVY
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.properties import *
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

# CUSTOM
# TODO: rename this to reflect what kind of slot
from slot import Slot
from realbutton import RealButton

'''
This screen will provide gui to save and load savegames
from json-files
savegame-files are:
save_current.json -> allways keep current game
save_1.json -> First savegame-slot
[...]
save_5.json -> last savegame-slot
'''


class SavegameScreen(Screen):

    buttonlayout = ObjectProperty(None)
    mainlayout = ObjectProperty(None)
    menubutton = ObjectProperty(None)
    logic = ObjectProperty(None)

    def __init__(self, logic, iconsize, iconratio_x, iconratio_y, **kwargs):

        super(SavegameScreen, self).__init__(**kwargs)

        self.logic = logic

        self.iconsize = iconsize
        self.iconratio_x = iconratio_x
        self.iconratio_y = iconratio_y

        self.build_interface()

    def on_enter(self):
        self.update_saves()

    def update_saves(self):
        save_times = App.get_running_app().scan_savegames()
        slots = self.buttonlayout.children
        for index in save_times:
            for slot in slots:
                if not slot.number == index:
                    continue
                slot.update_label(save_times[index])

    def build_interface(self):

        self.mainlayout = FloatLayout()
        self.buttonlayout = GridLayout(
            cols=1,
            size_hint=(0.75, 0.5),
            pos_hint={"x": 0.125,
                      "y": 0.25}
        )

        for i in range(1, 6):
            self.buttonlayout.add_widget(Slot(i, self.switchto_main))

        self.mainlayout.add_widget(self.buttonlayout)

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
        self.add_widget(self.mainlayout)

    def switchto_menu(self, instance):
        self.manager.transition = FadeTransition()
        self.manager.current = 'menu'

    def switchto_main(self, instance):
        self.manager.transition = FadeTransition()
        self.manager.current = 'main'
