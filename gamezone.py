from kivy.uix.scatter import Scatter
from kivy.graphics import Line, Color
from kivy.properties import *
from kivy.app import App

from kivy.vector import Vector

class Gamezone(Scatter):

    logic = ObjectProperty(None)

    '''
    children of this dude will be planets!?
    '''

    def __init__(self, **kwargs):
       super(Gamezone, self).__init__(**kwargs)
       self.logic = App.get_running_app().logic
       self.logic.register(self)

    def on_touch_down(self, touch):
        if touch.is_double_tap:
            touch.push()
            touch.apply_transform_2d(self.to_local)
            #self.logic.add_sun(touch.pos)
            # fixed = True
            self.logic.add_body(pos = touch.pos, body = 'sun', mass = 10000, fixed = True)
            touch.pop()
            return

        if self.logic.zoom_mode:
            super(Gamezone, self).on_touch_down(touch)
        else:
            touch.push()
            touch.apply_transform_2d(self.to_local)
            ud = touch.ud
            ud['id'] = 'gametouch'
            ud['firstpos'] = touch.pos
            ud['group'] = g = str(touch.uid)
            with self.canvas:
                ud['lines'] = [
                    Line(points = (touch.x, touch.y, touch.x+1, touch.y+1),
                         width = 1, group = g)]
            touch.grab(self)
            touch.pop()

    def on_touch_move(self, touch):
        if self.logic.zoom_mode:
            super(Gamezone, self).on_touch_move(touch)
        else:
            if touch.grab_current is not self:
                return
            touch.push()
            touch.apply_transform_2d(self.to_local)
            ud = touch.ud
            ud['lines'][0].points = (ud['firstpos'][0],ud['firstpos'][1],
                                     touch.x,touch.y)
            touch.pop()

    def on_touch_up(self, touch):
        if self.logic.zoom_mode:
            super(Gamezone, self).on_touch_up(touch)
        else:
            if touch.grab_current is not self:
                return
            touch.push()
            touch.apply_transform_2d(self.to_local)
            ud = touch.ud
            touchdownv = Vector(ud['firstpos'])
            touchupv = Vector(touch.pos)
            velocity = (touchupv - touchdownv) / 50
            #self.logic.add_planet(ud['firstpos'], (velocity.x, velocity.y))
            self.logic.add_body(pos = ud['firstpos'], vel = (velocity.x, velocity.y))
            self.canvas.remove_group(ud['group'])
            touch.ungrab(self)
            touch.pop()
