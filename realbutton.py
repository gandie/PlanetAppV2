from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import *
from kivy.uix.behaviors import ToggleButtonBehavior


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

    def __init__(self, realtexture, realtexture_pressed, **kwargs):
        super(RealMenuToggleButton, self).__init__(**kwargs)
        self.realtexture = realtexture
        self.realtexture_pressed = realtexture_pressed

    def on_state(self, widget, value):
        # i hate this code, togglebuttons are strange
        if self.parent != None:
            if value == 'down':
                #print '###'

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

                for dude in self.parent.optionbuttons:
                    if widget == dude:
                        #print 'ja'
                        #self.parent.optionmap[dude] = True
                        dude.source = dude.realtexture_pressed
                        dude.reload()
                    else:
                        #print 'nein'
                        #self.parent.optionmap[dude] = False
                        dude.source = dude.realtexture
                        dude.reload()
