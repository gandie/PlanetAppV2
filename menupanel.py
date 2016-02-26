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
from kivy.uix.togglebutton import ToggleButton
from kivy.app import App

from cplanetcore import CPlanetcore
from logic import Logic

from kivy.core.window import Window

from realbutton import RealButton
from realbutton import RealToggleButton
from realbutton import RealMenuToggleButton
class MenuToggleButton(ToggleButtonBehavior, Button):

    def __init__(self, **kwargs):
        super(MenuToggleButton, self).__init__(**kwargs)

    def on_state(self, widget, value):
        # i hate this code, togglebuttons are strange
        if self.parent != None:
            if value == 'down':
                if widget == self.parent.testbutton1:
                    self.parent.option1 = True
                    self.parent.option2 = False
                    self.parent.option3 = False
                    self.parent.option4 = False
                elif widget == self.parent.testbutton2:
                    self.parent.option1 = False
                    self.parent.option2 = True
                    self.parent.option3 = False
                    self.parent.option4 = False
                elif widget == self.parent.testbutton3:
                    self.parent.option1 = False
                    self.parent.option2 = False
                    self.parent.option3 = True
                    self.parent.option4 = False
                elif widget == self.parent.testbutton4:
                    self.parent.option1 = False
                    self.parent.option2 = False
                    self.parent.option3 = False
                    self.parent.option4 = True


class MenuPanel(FloatLayout):

    # buttons
    testbutton1 = ObjectProperty(None)
    testbutton2 = ObjectProperty(None)
    testbutton3 = ObjectProperty(None)
    testbutton4 = ObjectProperty(None)
    menubutton = ObjectProperty(None)
    resetbutton = ObjectProperty(None)
    pausebutton = ObjectProperty(None)

    optionbuttons = ReferenceListProperty(
        testbutton1,
        testbutton2,
        testbutton3,
        testbutton4
        #menubutton,
        #resetbutton,
        #pausebutton
    )

    realbutton = ObjectProperty(None)

    paused = BooleanProperty(False)

    option1 = BooleanProperty(True)
    option2 = BooleanProperty(False)
    option3 = BooleanProperty(False)
    option4 = BooleanProperty(False)
    options = ReferenceListProperty(option1, option2, option3, option4)

    logic = ObjectProperty(None)

    def __init__(self, iconsize, iconratio, **kwargs):
       super(MenuPanel, self).__init__(**kwargs)
       self.logic = App.get_running_app().logic

       #self.calc_iconsize()
       self.iconsize = iconsize
       self.iconratio = iconratio

       self.build_interface()
       self.logic.add_planet_mode = True
       self.logic.zoom_mode = False

    def on_options(self, instance, value):
        self.logic.add_planet_mode = self.option1
        self.logic.zoom_mode = self.option2
        self.logic.add_sun_mode = self.option3
        self.logic.del_mode = self.option4

    def build_interface(self):

        self.menubutton = RealButton(
            #text = 'Menu',
            './media/icons/menu.png',
            './media/icons/menu_pressed.png',
            self.goto_menu,
            pos_hint = {'x' : 0, 'y' : 0},
            size_hint = (None, None),
            size = (self.iconsize, self.iconsize),
            #on_press = self.goto_menu,
            source = './media/icons/menu.png',
            always_release = True
        )

        self.pausebutton = RealToggleButton(
            './media/icons/pause.png',
            './media/icons/pause_pressed.png',
            #self.testfunction,
            self.pause_game,
            pos_hint = {'x' : 0, 'y' : self.iconratio},
            size_hint = (None, None),
            size = (self.iconsize, self.iconsize),
            #on_press = self.goto_menu,
            source = './media/icons/pause.png',
            always_release = True
        )

        self.resetbutton = RealButton(
            #text = 'Menu',
            './media/icons/reset.png',
            './media/icons/reset_pressed.png',
            self.logic.reset_planets,
            pos_hint = {'x' : 0, 'y' : self.iconratio * 2},
            size_hint = (None, None),
            size = (self.iconsize, self.iconsize),
            #on_press = self.goto_menu,
            source = './media/icons/reset.png',
            always_release = True
        )

        self.testbutton4 = RealMenuToggleButton(
            #text = 'del', 
            './media/icons/delete.png',
            './media/icons/delete_pressed.png',
            pos_hint = {'x' : 0, 'y' : self.iconratio * 3},
            size_hint = (None, None),
            size = (self.iconsize, self.iconsize),
            #background_normal = './media/icons/delete.png',
            #background_down = './media/icons/delete_pressed.png',
            source = './media/icons/delete.png',
            group = 'menu',
            allow_no_selection = False
        )

        self.testbutton3 = RealMenuToggleButton(
            #text = 'sun', 
            './media/icons/add_sun.png',
            './media/icons/add_sun_pressed.png',
            pos_hint = {'x' : 0, 'y' : self.iconratio * 4},
            size_hint = (None, None),
            size = (self.iconsize, self.iconsize),
            #background_normal = './media/icons/add_sun.png',
            #background_down = './media/icons/add_sun_pressed.png',
            source = './media/icons/add_sun.png',
            group = 'menu',
            allow_no_selection = False
        )

        self.testbutton1 = RealMenuToggleButton(
            #text = 'add_planet_mode',
            './media/icons/add_planet.png',
            './media/icons/add_planet_pressed.png',
            size_hint = (None, None), 
            size = (self.iconsize, self.iconsize),
            pos_hint = {'x' : 0, 'y' : self.iconratio * 5},
            #size_hint = (0.09,1),
            #size_hint = (0.07,1),

            group = 'menu',
            state = 'down',
            allow_no_selection = False,
            #background_normal = './media/icons/add_planet.png',
            #background_down = './media/icons/add_planet_pressed.png'
            source = './media/icons/add_planet.png'
        )

        self.testbutton2 = RealMenuToggleButton(
            #text = 'zoom',
            './media/icons/zoom_mode.png',
            './media/icons/zoom_mode_pressed.png',
            size_hint = (None, None), 
            size = (self.iconsize, self.iconsize),
            pos_hint = {'x' : 0, 'y' : self.iconratio * 6},
            #size_hint = (0.1,1),
            group = 'menu',
            allow_no_selection = False,
            #background_normal = './media/icons/zoom_mode.png',
            #background_down = './media/icons/zoom_mode_pressed.png'
            source = './media/icons/zoom_mode.png'
        )

        self.add_widget(self.testbutton1)
        self.add_widget(self.testbutton2)
        self.add_widget(self.testbutton3)
        self.add_widget(self.testbutton4)
        self.add_widget(self.menubutton)
        self.add_widget(self.pausebutton)
        self.add_widget(self.resetbutton)
        #self.add_widget(self.realbutton)

    def goto_menu(self, instance):
        self.parent.manager.current = 'menu'

    def pause_game(self, instance):
        if not self.paused:
            self.logic.stop_game()
            self.paused = True
        else:
            self.logic.start_game()
            self.paused = False

    def testfunction(self, instance):
        print 'Jau!'
