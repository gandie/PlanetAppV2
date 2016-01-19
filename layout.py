from kivy.uix.floatlayout import FloatLayout
#from kivy.uix.textinput import TextInput
#from kivy.uix.boxlayout import BoxLayout
from kivy.properties import *
from kivy.uix.button import Button
#from kivy.uix.gridlayout import GridLayout
#from kivy.clock import Clock
#from kivy.uix.label import Label
#from kivy.network.urlrequest import UrlRequest
#import json
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from logic import Logic

class MenuPanel(FloatLayout):
    pass
    #
    #def animate(self, instance):
        


class MainScreen(Screen):

    # GUI
    mainlayout = ObjectProperty(None)
    menupanel = ObjectProperty(None)
    fadebutton = ObjectProperty(None)

    # SESSION DATA

    logic = ObjectProperty(None)

    def __init__(self, **kwargs):
       super(MainScreen, self).__init__(**kwargs)

       self.logic = Logic(self)
       
       self.build_interface()

    def btn_test(self, instance):
        print instance.id

    def btn_fade(self, instance):
        offset = self.menupanel.size[1]
        if self.fadebutton.pos[1] == 0:
            instance.text = 'Down'
            anim1 = Animation(pos=(0, offset), t='out_bounce')
            anim1.start(instance)
            anim2 = Animation(pos=(0, 0), t='out_bounce')
            anim2.start(self.menupanel)
        else:
            instance.text = 'Up'
            anim1 = Animation(pos=(0, 0), t='out_bounce')
            anim1.start(instance)
            anim2 = Animation(pos=(0, -offset), t='out_bounce')
            anim2.start(self.menupanel)


    def build_interface(self):
        self.mainlayout = FloatLayout()
        self.menupanel = MenuPanel(size_hint = (1,0.1),
                                   pos = (0, -self.size[1])
        )



        self.menupanel.add_widget(Button(text = 'ball', 
                                    pos_hint = {'x':0,'y':0},
                                    size_hint = (1,1),
                                    on_press = self.btn_test))

        self.mainlayout.add_widget(self.menupanel)

        self.fadebutton = Button(text = 'up',
                                 #pos_hint = {'x':0,'y':0},
                                 size_hint = (0.1,0.1),
                                 on_press = self.btn_fade)

        self.add_widget(self.mainlayout)
        self.add_widget(self.fadebutton)
