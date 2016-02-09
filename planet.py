from kivy.uix.widget import Widget

class Planet(Widget):

    def set_texture(self, texture):
        self.canvas.children[1].texture = texture
