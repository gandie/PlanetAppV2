from kivy.uix.floatlayout import FloatLayout
#from kivy.uix.textinput import TextInput
from kivy.properties import *
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.app import App

from cplanetcore import CPlanetcore
from logic import Logic

class MenuToggleButton(ToggleButtonBehavior, Button):
    def __init__(self, **kwargs):
        super(MenuToggleButton, self).__init__(**kwargs)

    def on_state(self, widget, value):
        # i hate this code, togglebuttons are strange
        if self.parent != None:
            if value == 'down':
                if widget.text == 'add_planet_mode':
                    self.parent.option1 = True
                    self.parent.option2 = False
                elif widget.text == 'zoom_mode':
                    self.parent.option1 = False
                    self.parent.option2 = True

class MenuPanel(FloatLayout):
    fadebutton = ObjectProperty(None)
    opened = BooleanProperty(True)

    testbutton1 = ObjectProperty(None)
    testbutton1 = ObjectProperty(None)

    menubutton = ObjectProperty(None)

    option1 = BooleanProperty(True)
    option2 = BooleanProperty(False)

    options = ReferenceListProperty(option1, option2)

    logic = ObjectProperty(None)

    def __init__(self,**kwargs):
       super(MenuPanel, self).__init__(**kwargs)
       self.logic = App.get_running_app().logic
       self.build_interface()
       # set default mode in logic...please somebody rewrite this menu...
       self.logic.add_planet_mode = True
       self.logic.zoom_mode = False

    def on_options(self, instance, value):
        self.logic.add_planet_mode = self.option1
        self.logic.zoom_mode = self.option2

    def build_interface(self):

        self.fadebutton = Button(text = 'Down',
                                 pos_hint = {'x':0,'y':0.5},
                                 size_hint = (0.25,0.5),
                                 on_press = self.btn_fade)
        self.add_widget(self.fadebutton)


        self.testbutton1 = MenuToggleButton(
            text = 'add_planet_mode', 
            pos_hint = {'x':0.2,'y':0},
            size_hint = (0.4,0.5),
            group='menu',
            state='down',
            allow_no_selection=False
        )
        self.testbutton2 = MenuToggleButton(
            text = 'zoom_mode', 
            pos_hint = {'x':0.6,'y':0},
            size_hint = (0.4,0.5),
            group='menu',
            allow_no_selection=False
        )

        self.menubutton = Button(
            text = 'Menu', 
            pos_hint = {'x':0,'y':0},
            size_hint = (0.2,0.5),
            on_press = self.goto_menu
        )

        self.add_widget(self.testbutton1)
        self.add_widget(self.testbutton2)
        self.add_widget(self.menubutton)

    def goto_menu(self, instance):
        self.parent.manager.current = 'menu'

    def btn_fade(self, instance):
        offset = self.size[1] / 2
        if self.opened:
            self.fadebutton.text = 'Up'
            anim1 = Animation(y = -offset, t='out_bounce')
            anim1.start(self)
            self.opened = False
        else:
            self.fadebutton.text = 'Down'
            # why 1? wtf!?
            anim1 = Animation(y = 1, t='out_bounce')
            anim1.start(self)
            self.opened = True
