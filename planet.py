from kivy.uix.image import Image
#from kivy.uix.widget import Widget
from kivy.properties import *
from kivy.uix.floatlayout import FloatLayout

class Planet(FloatLayout):

    base_image = ObjectProperty(None)
    #base_image_source = StringProperty(None)

    shadow_overlay = ObjectProperty(None)

    def __init__(self,**kwargs):
        super(Planet, self).__init__(**kwargs)
        self.size = (100, 100)
        self.base_image = Image(
            #size = (100,100),
            size_hint = (1, 1),
            pos_hint = {'x' : 0, 'y' : 0},
            #allow_stretch = True,
            source = './media/textures/planets/planet.png'
        )
        self.add_widget(self.base_image)
        #print self.children

    def on_size(self, instance, value):
        #print value
        if self.base_image:
            self.base_image.size = value
            #self.base_image.color[0] -= 0.1

    def set_base_image(self, source):
        #pass
        self.base_image.source = source
        self.base_image.reload()
        #print self.base_image.size, self.size

    def set_color(self, offset):
        self.base_image.color[1] = (1 - offset)
        self.base_image.color[2] = (1 - offset)
        #pass
