# KIVY
from kivy.uix.scatter import Scatter
from kivy.graphics import Line, Color
from kivy.properties import *
from kivy.app import App
from kivy.vector import Vector

# BUILTIN
import time
from random import randint

class Gamezone(Scatter):

    logic = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Gamezone, self).__init__(**kwargs)
        self.logic = App.get_running_app().logic
        self.logic.register_gamezone(self)

    def on_touch_down(self, touch):
        self.logic.cur_guimode.touch_down(touch)

        '''
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

        elif self.logic.add_planet_mode:
            self.add_body_down(touch)

        elif self.logic.add_sun_mode:
            self.add_body_down(touch)

        elif self.logic.multi_mode:
            self.add_body_down(touch)
        '''

    def on_touch_move(self, touch):
        self.logic.cur_guimode.touch_move(touch)
        '''
        if self.logic.zoom_mode:
            super(Gamezone, self).on_touch_move(touch)
        elif self.logic.add_planet_mode:
            self.add_body_move(touch)

        elif self.logic.add_sun_mode:
            self.add_body_move(touch, body = 'sun')

        elif self.logic.multi_mode:
            self.add_body_move(touch, body = 'moon')
        '''

    def on_touch_up(self, touch):
        self.logic.cur_guimode.touch_up(touch)
        '''
        if self.logic.zoom_mode:
            super(Gamezone, self).on_touch_up(touch)

        elif self.logic.add_planet_mode:
            self.add_body_up(touch)

        elif self.logic.add_sun_mode:
            self.add_body_up(touch, body = 'sun')

        elif self.logic.multi_mode:
            self.add_body_up(touch, body = 'moon', multi = True)
        '''

    def add_body_down(self, touch):
        touch.push()

        ud = touch.ud
        ud['touchtime'] = time.time()
        ud['firstpos'] = touch.pos

        ud['group'] = g = str(touch.uid)

        with self.parent.canvas:
            ud['lines'] = [
                Line(points = (touch.x, touch.y, touch.x+1, touch.y+1),
                     width = 1, group = g)]

        touch.grab(self)
        touch.pop()

    def add_body_move(self, touch, body = 'planet'):
        if touch.grab_current is not self:
            return
        touch.push()

        ud = touch.ud
        relpos = self.to_local(ud['firstpos'][0], ud['firstpos'][1])

        # stuff for trajectory calculation
        min_mass_key = 'min_{}_mass'.format(body)
        min_mass = self.logic.settings[min_mass_key]
        # stupid patch foor moon mass, fix this!
        if body == 'moon':
            min_mass = 5

        density_key = '{}_density'.format(body)
        density = self.logic.settings[density_key]

        touchdownv = Vector(relpos)
        touchupv = Vector(self.to_local(touch.pos[0], touch.pos[1]))

        velocity = (touchupv - touchdownv) / 10
        
        temp_planet_d = {
            'position_x' : relpos[0],
            'position_y' : relpos[1],
            'velocity_x' : velocity.x,
            'velocity_y' : velocity.y,
            'density' : density,
            'mass' : min_mass,
        }

        trajectory = self.logic.calc_trajectory(temp_planet_d)
        trajectory_tuple = tuple()
        for point in trajectory:
            point = self.to_parent(point[0], point[1])
            trajectory_tuple += point

        points = (ud['firstpos'][0],ud['firstpos'][1])
        points += trajectory_tuple

        ud['lines'][0].points = points

        touch.pop()

    def add_body_up(self, touch, body = 'planet', multi = False):
        if touch.grab_current is not self:
            return
        touch.push()

        ud = touch.ud

        relpos = self.to_local(ud['firstpos'][0], ud['firstpos'][1])

        #touchdownv = Vector(ud['firstpos'])
        touchdownv = Vector(relpos)
        touchupv = Vector(self.to_local(touch.pos[0], touch.pos[1]))
        velocity = (touchupv - touchdownv) / 10

        min_mass_key = 'min_{}_mass'.format(body)
        density_key = '{}_density'.format(body)

        min_mass = self.logic.settings[min_mass_key]
        newmass = min_mass

        if multi:

            newmass = 5
            random_pos = int(self.logic.slider_value) * 2#20
            random_vel = 2
            body_count = int(self.logic.slider_value)#10

            for i in range(body_count):

                randpos = (relpos[0] + randint(-random_pos, random_pos),
                           relpos[1] + randint(-random_pos, random_pos))
                randvel = (velocity.x + randint(-random_vel, random_vel),
                           velocity.y + randint(-random_vel, random_vel))
                self.logic.add_body(
                    pos = randpos,
                    vel = randvel,
                    mass = newmass,
                    body = body,
                    density = self.logic.settings[density_key]
                )

        else:

            self.logic.add_body(
                body = body,
                pos = relpos,
                vel = (velocity.x, velocity.y),
                mass = newmass,
                density = self.logic.settings[density_key]
            )


        self.parent.canvas.remove_group(ud['group'])
        self.logic.temp_planet_d = None
        touch.ungrab(self)
        touch.pop()
        
