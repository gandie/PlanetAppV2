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
from realbutton import RealTimedButton

class Seltoggles(FloatLayout):

    logic = ObjectProperty(None)

    planet_fix_button = ObjectProperty(None)
    planet_del_button = ObjectProperty(None)

    planet_addmass_button = ObjectProperty(None)
    planet_submass_button = ObjectProperty(None)

    planet_fixview_button = ObjectProperty(None)

    def __init__(self, iconsize, iconratio, **kwargs):
       super(Seltoggles, self).__init__(**kwargs)
       self.logic = App.get_running_app().logic

       self.iconsize = iconsize
       self.iconratio = iconratio

       self.build_interface()

    def build_interface(self):

        self.planet_fix_button = RealToggleButton(
            './media/icons/fix.png',
            './media/icons/fix_pressed.png',
            self.logic.fix_selected,
            pos_hint = {'x' : 0, 'y' : 0},
            size_hint = (None, None),
            size = (self.iconsize, self.iconsize),
            source = './media/icons/fix.png',
            always_release = True
        )

        self.planet_del_button = RealButton(
            './media/icons/delete.png',
            './media/icons/delete_pressed.png',
            self.logic.delete_selected,
            pos_hint = {'x' : 0.2, 'y' : 0},
            size_hint = (None, None),
            size = (self.iconsize, self.iconsize),
            source = './media/icons/delete.png',
            always_release = True
        )

        self.planet_addmass_button = RealTimedButton(
            './media/icons/addsize.png',
            './media/icons/addsize_pressed.png',
            self.logic.addmass_selected,
            pos_hint = {'x' : 0.4, 'y' : 0},
            size_hint = (None, None),
            size = (self.iconsize, self.iconsize),
            source = './media/icons/addsize.png',
            always_release = True
        )

        self.planet_submass_button = RealTimedButton(
            './media/icons/subsize.png',
            './media/icons/subsize_pressed.png',
            self.logic.submass_selected,
            pos_hint = {'x' : 0.6, 'y' : 0},
            size_hint = (None, None),
            size = (self.iconsize, self.iconsize),
            source = './media/icons/subsize.png',
            always_release = True
        )

        self.planet_fixview_button = RealToggleButton(
            './media/icons/view.png',
            './media/icons/view_pressed.png',
            self.logic.fixview_selected,
            pos_hint = {'x' : 0.8, 'y' : 0},
            size_hint = (None, None),
            size = (self.iconsize, self.iconsize),
            source = './media/icons/settings.png',
            always_release = True
        )

        self.add_widget(self.planet_fix_button)
        self.add_widget(self.planet_del_button)
        self.add_widget(self.planet_addmass_button)
        self.add_widget(self.planet_submass_button)
        self.add_widget(self.planet_fixview_button)

    def update(self, **kwargs):
        fixed = kwargs.get('fixed', False)
        fixview = kwargs.get('fixview', False)
        temp = kwargs.get('temperature', '<None>')
        fixbutton = self.planet_fix_button
        fixview_button = self.planet_fixview_button
        if fixbutton:
            if fixed:
                fixbutton.pressed = True
                fixbutton.source = fixbutton.realtexture_pressed
                fixbutton.reload()
            else:
                fixbutton.pressed = False
                fixbutton.source = fixbutton.realtexture
                fixbutton.reload()
        if fixview_button:
            if fixview:
                fixview_button.pressed = True
                fixview_button.source = fixview_button.realtexture_pressed
                fixview_button.reload()
            else:
                fixview_button.pressed = False
                fixview_button.source = fixview_button.realtexture
                fixview_button.reload()
