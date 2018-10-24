# KIVY
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.properties import *
from kivy.vector import Vector
from kivy.graphics import Line, Color

# BUILTIN
from random import randint
import math

# CUSTOM
from mainscreen_ui import Gamezone

'''
Module for game add-mode controls.
Starts with abstract class GameMode nearly all specific modes inherit from.

Each class inheriting from GameMode represents a mode selected from AddMenuPanel
in MainScreen and implements a specific behaviour for touch-events we get from
gamezone widget.

Main purpose of this mpdule is to avoid code duplication for game modes adding
bodies to the simulation.
'''

# TODO: this may be an object, property is not needed!
class GameMode(Screen):  # not actually a screen, using this a dummy class

    logic = ObjectProperty(None)

    def __init__(self, gamezone, body='', draw_trajectory=False, sizeable=False,
                 slider_label='', **kwargs):
        super(GameMode, self).__init__(**kwargs)
        self.gamezone = gamezone
        self.body = body
        self.logic = App.get_running_app().logic
        self.slider_label = slider_label
        self.draw_trajectory = draw_trajectory
        self.radial_coordinates = list(self.circle_coords(6, 0, 0))
        self.distance = 0

        self.sizeable = sizeable
        if self.sizeable:
            self.settings = kwargs.get('settings')
            #self.slider_value = (self.settings['max'] + self.settings['min']) / 2
            self.slider_value = self.settings['min'] + self.settings['step']*5

        if self.body != '':
            # stuff for trajectory calculation
            min_mass_key = 'min_{}_mass'.format(self.body)
            '''
            if self.body == 'moon':
                self.min_mass = 9
            else:
            '''
            self.min_mass = self.logic.settings[min_mass_key]

            density_key = '{}_density'.format(self.body)
            self.density = self.logic.settings[density_key]

    def calc_velocity(self, touch):
        ud = touch.ud
        touchdownv = Vector(ud['firstpos_local'])
        curpos_local = self.gamezone.to_local(touch.pos[0], touch.pos[1])
        touchupv = Vector(curpos_local)
        # velocity = (touchupv - touchdownv) / 25
        velocity = (touchupv - touchdownv).normalize() * (touchupv - touchdownv).length() ** 0.3

        return velocity

    def prepare_touch(self, touch):
        ud = touch.ud
        ud['firstpos'] = touch.pos
        ud['group'] = str(touch.uid)
        ud['firstpos_local'] = self.gamezone.to_local(touch.pos[0], touch.pos[1])

    def trajectory_start(self, touch):
        ud = touch.ud
        with self.gamezone.parent.canvas:
            ud['lines'] = [
                Line(points=(touch.x, touch.y, touch.x + 1, touch.y + 1),
                     width=1, dash_offset=1, group=ud['group'])]

    def trajectory_complex(self, touch):

        ud = touch.ud

        velocity = self.calc_velocity(touch)
        mass = self.slider_value
        temp_planet_d = {
            'position_x': ud['firstpos_local'][0],
            'position_y': ud['firstpos_local'][1],
            'velocity_x': velocity.x,
            'velocity_y': velocity.y,
            'density': self.density,
            # 'mass': self.min_mass,
            'mass': mass
        }

        trajectory = self.logic.calc_trajectory(temp_planet_d)
        trajectory_tuple = tuple()
        for point in trajectory:
            point = self.gamezone.to_parent(point[0], point[1])
            trajectory_tuple += point

        points = (ud['firstpos'][0], ud['firstpos'][1])
        points += trajectory_tuple

        ud['lines'][0].points = points

    def trajectory_line(self, touch):
        ud = touch.ud
        ud['lines'][0].points = (ud['firstpos'][0], ud['firstpos'][1],
                                 touch.x, touch.y)

    def touch_down(self, touch):
        pass

    def touch_move(self, touch):
        pass

    def touch_up(self, touch):
        pass

    def circle_coords(self, R, cx, cy):
        '''
        get coordinates radial from center for circle with radius R
        '''
        radius = int(R)
        yielded = []
        for radius_step in xrange(1, radius + 1):
            for angle_index in xrange(2**(radius_step + 1)):
                angle = angle_index * math.pi / (2 ** radius_step)
                x = int(math.cos(angle) * radius_step)
                y = int(math.sin(angle) * radius_step)
                if (x, y) not in yielded:
                    yielded.append((x, y))
                    yield x+cx, y+cy


class AddBodyMode(GameMode):

    def touch_down(self, touch):

        touch.push()

        self.prepare_touch(touch)

        self.trajectory_start(touch)

        touch.grab(self.gamezone)
        touch.pop()

    def touch_move(self, touch):

        if touch.grab_current is not self.gamezone:
            return
        touch.push()

        ud = touch.ud

        if self.draw_trajectory:
            self.trajectory_complex(touch)
        else:
            self.trajectory_line(touch)

        touch.pop()

    def touch_up(self, touch):

        if touch.grab_current is not self.gamezone:
            return
        touch.push()

        ud = touch.ud
        velocity = self.calc_velocity(touch)

        # mass = self.logic.slider_value  # self.min_mass
        mass = self.slider_value

        self.logic.add_body(
            body=self.body,
            pos=ud['firstpos_local'],
            vel=(velocity.x, velocity.y),
            mass=mass,
            density=self.density
        )

        self.gamezone.parent.canvas.remove_group(ud['group'])
        self.logic.temp_planet_d = None
        touch.ungrab(self.gamezone)
        touch.pop()


class AddBodyMode_Multi(AddBodyMode):

    def touch_up(self, touch):
        if touch.grab_current is not self.gamezone:
            return
        touch.push()

        ud = touch.ud
        velocity = self.calc_velocity(touch)

        newmass = 5
        # body_count = int(self.logic.slider_value)
        body_count = int(self.slider_value)
        random_pos = body_count * 2
        random_vel = 1

        for x, y in self.radial_coordinates[:body_count]:
            randpos = (
                ud['firstpos_local'][0] + x*35,
                ud['firstpos_local'][1] + y*35
            )

            randvel = (velocity.x + randint(-random_vel, random_vel),
                       velocity.y + randint(-random_vel, random_vel))
            self.logic.add_body(
                pos=randpos,
                vel=randvel,
                mass=self.min_mass,
                body=self.body,
                density=self.density
            )

        self.gamezone.parent.canvas.remove_group(ud['group'])
        self.logic.temp_planet_d = None
        touch.ungrab(self.gamezone)
        touch.pop()


class ZoomMode(GameMode):
    '''
    Select body if a body is hit or call scatter object zooming functionality
    '''

    def touch_down(self, touch):
        touch.push()
        touch.apply_transform_2d(self.gamezone.to_local)
        for body in self.gamezone.children:
            if body.collide_point(touch.x, touch.y):
                self.logic.select_planet(body)
        touch.pop()
        super(Gamezone, self.gamezone).on_touch_down(touch)

    def touch_move(self, touch):
        super(Gamezone, self.gamezone).on_touch_move(touch)

    def touch_up(self, touch):
        super(Gamezone, self.gamezone).on_touch_up(touch)
        # mode may have switched so delete trajectory if group is found
        ud = touch.ud
        group = ud.get('group')
        if group is not None:
            self.gamezone.parent.canvas.remove_group(ud['group'])


class DelMode(GameMode):

    def touch_down(self, touch):
        touch.push()
        touch.apply_transform_2d(self.gamezone.to_local)
        for body in self.gamezone.children:
            if body.collide_point(touch.x, touch.y):
                self.logic.delete_planet_widget(body)
                break
        touch.pop()
