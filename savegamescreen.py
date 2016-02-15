from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.properties import *
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

# does it need logic?!
# everyone needs logic xD

from slot import Slot

class SavegameScreen(Screen):
    '''
    This screen will provide gui to save and load savegames
    from json-files
    savegame-files are:
    save_current.json -> allways keep current game
    save_1.json -> First savegame-slot
    [...]
    save_5.json -> last savegame-slot
    '''

    buttonlayout = ObjectProperty(None)
    mainlayout = ObjectProperty(None)

    menubutton = ObjectProperty(None)

    logic = ObjectProperty(None)

    def __init__(self, **kwargs):
       super(SavegameScreen, self).__init__(**kwargs)
       self.logic = App.get_running_app().logic
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
            size_hint=(0.75,0.5),
            pos_hint={"x" : 0.125,
                      "y" : 0.25}
        )

        for i in range(1, 6):
            self.buttonlayout.add_widget(Slot(i, self.switchto_main))

        self.mainlayout.add_widget(self.buttonlayout)

        self.menubutton = Button(
            text = 'Menu',
            size_hint = (0.1, 0.1),
            pos_hint = {'x' : 0, 'y' : 0},
            on_press = self.switchto_menu
        )

        self.mainlayout.add_widget(self.menubutton)

        self.add_widget(self.mainlayout)

        
    def switchto_menu(self, instance):
        self.manager.transition = FadeTransition()
        self.manager.current = 'menu'

    def switchto_main(self, instance):
        self.manager.transition = FadeTransition()
        self.manager.current = 'main'
    
