from kivy.uix.floatlayout import FloatLayout
#from kivy.uix.textinput import TextInput
from kivy.properties import *
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.screenmanager import FadeTransition

class Slot(FloatLayout):

    logic = ObjectProperty(None)

    number = NumericProperty(0)

    loadbutton = ObjectProperty(None)
    savebutton = ObjectProperty(None)

    label = ObjectProperty(None)

    def __init__(self, number, switchto_main,**kwargs):
       super(Slot, self).__init__(**kwargs)
       self.logic = App.get_running_app().logic
       self.number = number
       self.build_interface()
       self.switchto_main = switchto_main

    def update_label(self, newtext):
        self.label.text = newtext

    def save(self, instance):
        App.get_running_app().save_game(slot = self.number)
        self.parent.parent.parent.update_saves()

    def load(self, instance):
        App.get_running_app().load_game(slot = self.number)
        self.switchto_main(self)

    def build_interface(self):
        self.label = Label(
            text = 'Slot: {}'.format(self.number),
            size_hint = (0.5, 1),
            pos_hint = {'x' : 0, 'y' : 0}            
        )
        self.loadbutton = Button(
            text = 'Load',
            size_hint = (0.25, 1),
            pos_hint = {'x' : 0.5, 'y' : 0},
            on_press = self.load
        )
        self.savebutton = Button(
            text = 'Save',
            size_hint = (0.25, 1),
            pos_hint = {'x' : 0.75, 'y' : 0},
            on_press = self.save
        )

        self.add_widget(self.label)
        self.add_widget(self.loadbutton)
        self.add_widget(self.savebutton)
