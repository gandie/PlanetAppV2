from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import *
from kivy.uix.behaviors import ToggleButtonBehavior

from kivy.clock import Clock

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
            self.function(self)
            self.pressed = False
        else:
            self.source = self.realtexture_pressed
            self.reload()
            self.function(self)
            self.pressed = True

    def on_release(self):
        pass

class RealMenuToggleButton(ToggleButtonBehavior, Image):

    def __init__(self, realtexture, realtexture_pressed, keyword,**kwargs):
        super(RealMenuToggleButton, self).__init__(**kwargs)
        self.realtexture = realtexture
        self.realtexture_pressed = realtexture_pressed
        self.keyword = keyword

    def on_state(self, widget, value):
        # i hate this code, togglebuttons are strange
        if self.parent != None:
            if value == 'down':

                '''
                # switch option
                for button in self.parent.option_map:
                    if button == widget:
                        self.parent.option_map[button] = True
                    else:
                        self.parent.option_map[button] = False
                '''
                self.parent.cur_mode = self.keyword

                # update textures
                for dude in self.parent.optionbuttons:
                    if widget == dude:
                        dude.source = dude.realtexture_pressed
                        dude.reload()
                    else:
                        dude.source = dude.realtexture
                        dude.reload()
