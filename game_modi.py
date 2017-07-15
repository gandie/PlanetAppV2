# KIVY
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.properties import *
from kivy.vector import Vector
from kivy.graphics import Line, Color

# BUILTIN
from random import randint

# CUSTOM
from gamezone import Gamezone

'''
Module for game mode controls.
Starts with abstract class GameMode nearly all specific modes inherit from.
Main purpose of this mpdule is to avoid code duplication for game modes adding
bodies to the simulation.
'''


class GameMode(Screen):

    logic = ObjectProperty(None)

    def __init__(self, gamezone, logic_settings, body='', draw_trajectory=False,
                 sizeable=False, slider_label='', **kwargs):
        super(GameMode, self).__init__(**kwargs)
        self.gamezone = gamezone
        self.body = body
        self.logic = App.get_running_app().logic
        self.slider_label = slider_label
        self.draw_trajectory = draw_trajectory

        self.distance = 0

        self.sizeable = sizeable
        if self.sizeable:
            self.settings = kwargs.get('settings')

        if self.body != '':
            # stuff for trajectory calculation
            min_mass_key = 'min_{}_mass'.format(self.body)
            self.min_mass = self.logic.settings[min_mass_key]
            # stupid patch foor moon mass, fix this!
            if self.body == 'moon':
                self.min_mass = 29

            density_key = '{}_density'.format(self.body)
            self.density = self.logic.settings[density_key]

    def calc_velocity(self, touch):
        ud = touch.ud
        touchdownv = Vector(ud['firstpos_local'])
        curpos_local = self.gamezone.to_local(touch.pos[0], touch.pos[1])
        touchupv = Vector(curpos_local)
        velocity = (touchupv - touchdownv) / 10

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
                     width=1, group=ud['group'])]

    def trajectory_complex(self, touch):

        ud = touch.ud

        velocity = self.calc_velocity(touch)
        temp_planet_d = {
            'position_x': ud['firstpos_local'][0],
            'position_y': ud['firstpos_local'][1],
            'velocity_x': velocity.x,
            'velocity_y': velocity.y,
            'density': self.density,
            'mass': self.min_mass,
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

        mass = self.logic.slider_value  # self.min_mass

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
        body_count = int(self.logic.slider_value)
        random_pos = body_count * 2

        for i in xrange(body_count):

            randpos = (ud['firstpos_local'][0] + randint(-random_pos, random_pos),
                       ud['firstpos_local'][1] + randint(-random_pos, random_pos))
            randvel = (velocity.x,  # + randint(-random_vel, random_vel),
                       velocity.y)  # + randint(-random_vel, random_vel))
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
                return
        touch.pop()
        super(Gamezone, self.gamezone).on_touch_down(touch)

    def touch_move(self, touch):
        super(Gamezone, self.gamezone).on_touch_move(touch)

    def touch_up(self, touch):
        super(Gamezone, self.gamezone).on_touch_up(touch)


class DelMode(GameMode):

    def touch_down(self, touch):
        touch.push()
        touch.apply_transform_2d(self.gamezone.to_local)
        for body in self.gamezone.children:
            if body.collide_point(touch.x, touch.y):
                self.logic.delete_planet_widget(body)
                break
        touch.pop()
