# KIVY
from kivy.uix.image import Image
from kivy.properties import *
from kivy.uix.floatlayout import FloatLayout

'''
this widget is used to show planets in the gamezone
'''


class Planet(FloatLayout):

    base_image = ObjectProperty(None)
    select_overlay = ObjectProperty(None)

    # TODO: complete this!?
    shadow_overlay = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Planet, self).__init__(**kwargs)
        self.size = (100, 100)
        self.base_image = Image(
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0},
            source='./media/textures/planets/sandyone.png',
            allow_stretch=True
        )

        self.select_overlay = Image(
            size_hint=(None, None),
            pos_hint={'x': -0.25, 'y': -0.25},
            source='./media/textures/picked/picked.png',
            allow_stretch=True
        )

        self.add_widget(self.base_image)

    def on_size(self, instance, value):
        if self.base_image:
            self.base_image.size = value
            if self.select_overlay:
                newsize = (self.base_image.size[0] * 1.5, self.base_image.size[1] * 1.46)
                self.select_overlay.size = newsize
                self.select_overlay.center = self.center

    def select(self):
        newsize = (self.base_image.size[0] * 1.5, self.base_image.size[1] * 1.46)
        self.select_overlay.size = newsize
        self.select_overlay.center = self.center
        self.add_widget(self.select_overlay)

    def unselect(self):
        self.remove_widget(self.select_overlay)

    def set_base_image(self, source):
        self.base_image.source = source
        self.base_image.reload()
