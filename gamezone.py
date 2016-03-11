from kivy.uix.scatter import Scatter
from kivy.graphics import Line, Color
from kivy.properties import *
from kivy.app import App

from kivy.vector import Vector

import time

from random import randint

class Gamezone(Scatter):

    logic = ObjectProperty(None)

    '''
    children of this dude will be planets!?
    '''

    # BUILT DECORATORS FOR TOUCH TRANSFORMATION N SHIT!!!
    # PUT SPECIAL CODE INTO FUNCTIONS

    def __init__(self, **kwargs):
        super(Gamezone, self).__init__(**kwargs)
        self.logic = App.get_running_app().logic
        self.logic.register(self)

    def on_touch_down(self, touch):
        if self.logic.zoom_mode:
            # do pickmode stuff if collision is found
            touch.push()
            touch.apply_transform_2d(self.to_local)
            for thingy in self.children:
                if thingy.collide_point(touch.x,touch.y):
                    self.logic.select_planet(thingy)
                    return
            touch.pop()
            super(Gamezone, self).on_touch_down(touch)
        elif self.logic.del_mode:
            touch.push()
            touch.apply_transform_2d(self.to_local)
            for thingy in self.children:
                if thingy.collide_point(touch.x,touch.y):
                    self.logic.delete_planet_widget(thingy)
                    break
            touch.pop()
        elif self.logic.pick_mode:
            touch.push()
            touch.apply_transform_2d(self.to_local)
            for thingy in self.children:
                if thingy.collide_point(touch.x,touch.y):
                    self.logic.select_planet(thingy)
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
            ud['group'] = g = str(touch.uid)
            with self.canvas:
                ud['lines'] = [
                    Line(points = (touch.x, touch.y, touch.x+1, touch.y+1),
                         width = 1, group = g)]
            touch.grab(self)
            touch.pop()
        elif self.logic.multi_mode:
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
        elif self.logic.add_sun_mode:
            if touch.grab_current is not self:
                return
            touch.push()
            touch.apply_transform_2d(self.to_local)
            ud = touch.ud
            ud['lines'][0].points = (ud['firstpos'][0],ud['firstpos'][1],
                                     touch.x,touch.y)
            touch.pop()
        elif self.logic.multi_mode:
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
            velocity = (touchupv - touchdownv) / 10
            newmass = (((time.time() - ud['touchtime']) / 0.2) ** 2)
            if newmass < self.logic.settings['min_planet_mass']:
                newmass = self.logic.settings['min_planet_mass']
            print newmass
            self.logic.add_body(
                pos = ud['firstpos'], 
                vel = (velocity.x, velocity.y),
                mass = newmass,
                density = self.logic.settings['planet_density']
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
            touchdownv = Vector(ud['firstpos'])
            touchupv = Vector(touch.pos)
            velocity = (touchupv - touchdownv) / 10
            newmass = (((time.time() - ud['touchtime']) / 0.01) ** 2) * 5
            # put smallest sun mass here!
            if newmass < self.logic.settings['min_sun_mass']:
                newmass = self.logic.settings['min_sun_mass']
            self.logic.add_body(
                pos = ud['firstpos'],
                body = 'sun',
                mass = newmass,
                vel = (velocity.x, velocity.y),
                #fixed = True,
                density = self.logic.settings['sun_density']
            )
            self.canvas.remove_group(ud['group'])
            touch.ungrab(self)
            touch.pop()
        elif self.logic.multi_mode:
            if touch.grab_current is not self:
                return
            touch.push()
            touch.apply_transform_2d(self.to_local)
            ud = touch.ud
            touchdownv = Vector(ud['firstpos'])
            touchupv = Vector(touch.pos)
            velocity = (touchupv - touchdownv) / 10
            newmass = 5

            random_pos = 20
            random_vel = 2
            body_count = 10
            for i in range(body_count):

                randpos = (ud['firstpos'][0] + randint(-random_pos, random_pos),
                           ud['firstpos'][1] + randint(-random_pos, random_pos))
                randvel = (velocity.x + randint(-random_vel, random_vel),
                           velocity.y + randint(-random_vel, random_vel))
                self.logic.add_body(
                    pos = randpos,
                    vel = randvel,
                    mass = newmass,
                    body = 'moon',
                    density = self.logic.settings['planet_density']
                )

            self.canvas.remove_group(ud['group'])
            touch.ungrab(self)
            touch.pop()
