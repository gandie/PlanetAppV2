# KIVY
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import *
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.clock import Clock

'''
custom button mechanics due to problems with texture scaling in kivy buttons
'''


class RealButton(ButtonBehavior, Image):

    def __init__(self, realtexture, realtexture_pressed, function, **kwargs):
        super(RealButton, self).__init__(**kwargs)
        self.realtexture = realtexture
        self.realtexture_pressed = realtexture_pressed
        self.function = function

    def on_press(self):
        self.source = self.realtexture_pressed
        self.reload()
        self.function(self)

    def on_release(self):
        self.source = self.realtexture
        self.reload()


class RealTimedButton(ButtonBehavior, Image):

    def __init__(self, realtexture, realtexture_pressed, function, **kwargs):
        super(RealTimedButton, self).__init__(**kwargs)
        self.realtexture = realtexture
        self.realtexture_pressed = realtexture_pressed
        self.function = function

    def on_press(self):
        self.source = self.realtexture_pressed
        self.reload()
        Clock.schedule_interval(self.function, 1.0 / 10.0)

    def on_release(self):
        Clock.unschedule(self.function)
        self.source = self.realtexture
        self.reload()


class RealToggleButton(ButtonBehavior, Image):

    pressed = BooleanProperty(False)

    def __init__(self, realtexture, realtexture_pressed, function, **kwargs):
        super(RealToggleButton, self).__init__(**kwargs)
        self.realtexture = realtexture
        self.realtexture_pressed = realtexture_pressed
        self.function = function

    def on_press(self):
        if self.pressed:
            self.source = self.realtexture
            self.reload()
            self.pressed = False
        else:
            self.source = self.realtexture_pressed
            self.reload()
            self.pressed = True
        self.function(self.pressed)

    def on_release(self):
        pass


class RealMenuToggleButton(ToggleButtonBehavior, Image):

    def __init__(self, realtexture, realtexture_pressed, keyword,
                 default_mode='zoom', **kwargs):
        super(RealMenuToggleButton, self).__init__(**kwargs)
        self.realtexture = realtexture
        self.realtexture_pressed = realtexture_pressed
        self.keyword = keyword
        self.default_mode = default_mode

    def on_state(self, widget, value):
        if self.parent is not None:
            if value == 'down':
                self.parent.cur_mode = self.keyword
                self.source = self.realtexture_pressed
            elif value == 'normal':
                self.parent.cur_mode = self.default_mode
                self.source = self.realtexture
            self.reload()
