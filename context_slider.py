from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.properties import *
from kivy.uix.slider import Slider
from kivy.app import App


class Context_Slider(FloatLayout):

    '''
    labeled slider with changing context depending on current game-mode
    '''

    logic = ObjectProperty(None)

    slider = ObjectProperty(None)
    label = ObjectProperty(None)

    value = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Context_Slider, self).__init__(**kwargs)
        self.logic = App.get_running_app().logic
        self.build_interface()

    def build_interface(self):

        self.slider = Slider(
            min=1,
            max=10,
            value=5,
            step=1,
            orientation='horizontal',
            pos_hint={'x': 0, 'y': 0},
            size_hint=(0.5, 1)
        )
        self.add_widget(self.slider)

        self.label = Label(
            text='bla'
            pos_hint={'x': 0, 'y': 0},
            size_hint=(0.5, 1)
        )
        self.add_widget(self.label)
