from kivy.uix.scatter import Scatter
from kivy.graphics import Line, Color
from kivy.properties import *
from kivy.app import App

from kivy.vector import Vector

import time

class Gamezone(Scatter):

    logic = ObjectProperty(None)

    '''
    children of this dude will be planets!?
    '''

    # BUILD TOUCH-HANDLER CLASS, SUBCLASS FOR SPECIAL BEHAVIOUR

    def __init__(self, **kwargs):
        super(Gamezone, self).__init__(**kwargs)
        self.logic = App.get_running_app().logic
        self.logic.register(self)

    def on_touch_down(self, touch):
        if self.logic.zoom_mode:
            super(Gamezone, self).on_touch_down(touch)
        elif self.logic.del_mode:
            touch.push()
            touch.apply_transform_2d(self.to_local)
            for thingy in self.children:
                if thingy.collide_point(touch.x,touch.y):
                    self.logic.delete_planet_widget(thingy)
                    break
            touch.pop()
        elif self.logic.add_planet_mode:
            touch.push()
            touch.apply_transform_2d(self.to_local)
            ud = touch.ud
            ud['id'] = 'gametouch'
            ud['touchtime'] = time.time()
            ud['firstpos'] = touch.pos
            ud['group'] = g = str(touch.uid)
            with self.canvas:
                ud['lines'] = [
                    Line(points = (touch.x, touch.y, touch.x+1, touch.y+1),
                         width = 1, group = g)]
            touch.grab(self)
            touch.pop()
        elif self.logic.add_sun_mode:
            touch.push()
            touch.apply_transform_2d(self.to_local)
            ud = touch.ud
            ud['id'] = 'gametouch'
            ud['touchtime'] = time.time()
            ud['firstpos'] = touch.pos
            touch.grab(self)
            touch.pop()

    def on_touch_move(self, touch):
        if self.logic.zoom_mode:
            super(Gamezone, self).on_touch_move(touch)
        elif self.logic.add_planet_mode:
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
        elif self.logic.add_planet_mode:
            if touch.grab_current is not self:
                return
            touch.push()
            touch.apply_transform_2d(self.to_local)
            ud = touch.ud
            touchdownv = Vector(ud['firstpos'])
            touchupv = Vector(touch.pos)
            velocity = (touchupv - touchdownv) / 25
            # make this a squared function
            newmass = ((time.time() - ud['touchtime']) ** 2 / 0.3) * 40
            self.logic.add_body(
                pos = ud['firstpos'], 
                vel = (velocity.x, velocity.y),
                mass = newmass
            )
            self.canvas.remove_group(ud['group'])
            touch.ungrab(self)
            touch.pop()
        elif self.logic.add_sun_mode:
            if touch.grab_current is not self:
                return
            touch.push()
            touch.apply_transform_2d(self.to_local)
            ud = touch.ud
            newmass = ((time.time() - ud['touchtime']) ** 2 / 0.1) * 500
            self.logic.add_body(
                pos = ud['firstpos'],
                body = 'sun',
                mass = newmass,
                fixed = True,
                density = 0.5
            )
            touch.ungrab(self)
            touch.pop()
