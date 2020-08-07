'''
python rk4 gravity simulation.

This modules Engine class provides a fully functional gravity simulation engine
for the PocketCosmos App. Because its written in Python it is quite slow, but
makes testing changes in the algorith much easier than testing the compiled
C version (crk4engine).

Kudos to Thanassis Tsiodras, who made this module (and the C-version) possible
with this blog post:
https://www.thanassis.space/gravity.html
'''

import itertools


cdef class State:

    cdef public double pos_x, pos_y, vel_x, vel_y

    def __cinit__(self, double pos_x, double pos_y, double vel_x, double vel_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = vel_x
        self.vel_y = vel_y


cdef class Derivative:

    cdef public double dx, dy, dvx, dvy

    def __cinit__(self, double dx, double dy, double dvx, double dvy):
        self.dx = dx
        self.dy = dy
        self.dvx = dvx
        self.dvy = dvy


cdef class Planet:

    cdef public object engine
    cdef public double pos_x, pos_y, density, mass, vel_x, vel_y
    cdef public bint fixed
    cdef public object state
    cdef public double radius

    def __init__(self, engine, pos_x, pos_y, density, mass, vel_x=0, vel_y=0, fixed=False):

        self.engine = engine

        self.state = State(
            pos_x=pos_x,
            pos_y=pos_y,
            vel_x=vel_x,
            vel_y=vel_y
        )

        self.density = density
        self.mass = mass
        self.fixed = fixed
        self.calc_radius()

    cdef void _calc_radius(self):
        self.radius = ((3 * self.mass) / (4 * 3.1427 * self.density)) ** 0.5

    def calc_radius(self):
        self._calc_radius()

    cdef (double, double) calc_acceleration(self, object state, double unused_curtime):

        cdef double ax = 0.0
        cdef double ay = 0.0
        cdef double dist, delta_x, delta_y, force
        cdef object other_planet

        for other_planet in self.engine.planets.values():
            if not other_planet or other_planet == self:
                continue
            dist, delta_x, delta_y = self._calc_distance(state, other_planet)
            if dist == 0:
                dist = 0.00001
            force = 0.1 * self.calc_force(other_planet, dist)
            ax += (force * delta_x / dist) / self.mass
            ay += (force * delta_y / dist) / self.mass
        return ax, ay

    def calc_distance(self, object state, object planet2):
        return self._calc_distance(state, planet2)

    cdef (double, double, double) _calc_distance(self, object state, object planet2):

        cdef double delta_x, delta_y, dist

        delta_x = planet2.state.pos_x - state.pos_x
        delta_y = planet2.state.pos_y - state.pos_y
        dist = (delta_x ** 2 + delta_y ** 2) ** 0.5
        return dist, delta_x, delta_y

    cdef double calc_force(self, object planet2, double dist):

        cdef double force

        if dist == 0:
            dist = 0.001
        force = (self.mass * planet2.mass) / (dist ** 2)
        return force

    cdef object initialDerivative(self, object state, double curtime):

        cdef double ax, ay

        ax, ay = self.calc_acceleration(state, curtime)
        return Derivative(
            dx=state.vel_x,
            dy=state.vel_y,
            dvx=ax,
            dvy=ay
        )

    cdef object nextDerivative(self, object initialState, object derivative, double curtime, double dt):

        cdef double ax, ay

        nextState = State(
            pos_x=initialState.pos_x + derivative.dx * dt,
            pos_y=initialState.pos_y + derivative.dy * dt,
            vel_x=initialState.vel_x + derivative.dvx * dt,
            vel_y=initialState.vel_y + derivative.dvy * dt
        )
        ax, ay = self.calc_acceleration(nextState, curtime+dt)
        return Derivative(
            dx=nextState.vel_x,
            dy=nextState.vel_y,
            dvx=ax,
            dvy=ay
        )

    def update(self, double curtime, double delta_time):
        self._update(curtime, delta_time)

    cdef void _update(self, double curtime, double delta_time):

        cdef double delta_x_dt, delta_y_dt, delta_vx_dt, delta_vy_dt
        cdef double error_x, error_y, error_norm, MAGIC_ERROR
        cdef object initial_D, second_D, third_D, fourth_D

        if self.fixed:
            return

        # calculate first derivative
        initial_D = self.initialDerivative(self.state, curtime)

        # initialize deltas
        delta_x_dt = 0
        delta_y_dt = 0
        delta_vx_dt = 0
        delta_vy_dt = 0

        # check initial derivative
        if initial_D.dx != 0 and initial_D.dy != 0:

            # calculate second derivative
            second_D = self.nextDerivative(self.state, initial_D, curtime, delta_time * 0.5)

            # calculate difference between first two steps and normalize
            error_x = (second_D.dx - initial_D.dx)
            error_y = (second_D.dy - initial_D.dy)
            error_norm = (error_x ** 2 + error_y ** 2) ** 0.5

            MAGIC_ERROR = 0.1
            if error_norm < MAGIC_ERROR:
                # rk 2
                delta_x_dt = second_D.dx
                delta_y_dt = second_D.dy
                delta_vx_dt = second_D.dvx
                delta_vy_dt = second_D.dvy
            else:
                # rk 4
                third_D = self.nextDerivative(self.state, second_D, curtime, delta_time * 0.5)
                fourth_D = self.nextDerivative(self.state, third_D, curtime, delta_time)
                delta_x_dt = 1.0 / 6.0 * (initial_D.dx + 2 * (second_D.dx + third_D.dx) + fourth_D.dx)
                delta_y_dt = 1.0 / 6.0 * (initial_D.dy + 2 * (second_D.dy + third_D.dy) + fourth_D.dy)
                delta_vx_dt = 1.0 / 6.0 * (initial_D.dvx + 2 * (second_D.dvx + third_D.dvx) + fourth_D.dvx)
                delta_vy_dt = 1.0 / 6.0 * (initial_D.dvy + 2 * (second_D.dvy + third_D.dvy) + fourth_D.dvy)

        self.state.pos_x += delta_x_dt * delta_time
        self.state.pos_y += delta_y_dt * delta_time
        self.state.vel_x += delta_vx_dt * delta_time
        self.state.vel_y += delta_vy_dt * delta_time


cdef class Engine:

    cdef public int cur_index, curtime, timerate
    cdef public dict planets

    def __init__(self):
        self.cur_index = 0
        self.curtime = 0
        self.timerate = 1
        self.planets = {}

    def planet_exists(self, index):
        planet = self.planets.get(index)
        if planet is not None:
            return True
        else:
            return False

    def create_planet(self, *args, **kwargs):
        '''
        see Planet constructor for argument details
        '''
        if len(self.planets) > 1000:
            return -1
        self.cur_index += 1
        new_planet = Planet(self, *args, **kwargs)
        self.planets[self.cur_index] = new_planet
        return self.cur_index

    def delete_planet(self, index):
        del_planet = self.planets.get(index)
        if del_planet is not None:
            del self.planets[index]

    # GETTER / SETTER START
    def get_planet_radius(self, index):
        planet = self.planets.get(index)
        if planet is not None:
            return planet.radius

    def fix_planet(self, index):
        planet = self.planets.get(index)
        if planet is not None:
            planet.fixed = True

    def unfix_planet(self, index):
        planet = self.planets.get(index)
        if planet is not None:
            planet.fixed = False

    def get_planet_pos_x(self, index):
        planet = self.planets.get(index)
        if planet is not None:
            return planet.state.pos_x

    def get_planet_pos_y(self, index):
        planet = self.planets.get(index)
        if planet is not None:
            return planet.state.pos_y

    def get_planet_vel_x(self, index):
        planet = self.planets.get(index)
        if planet is not None:
            return planet.state.vel_x

    def get_planet_vel_y(self, index):
        planet = self.planets.get(index)
        if planet is not None:
            return planet.state.vel_y

    def get_planet_mass(self, index):
        planet = self.planets.get(index)
        if planet is not None:
            return planet.mass

    def get_planet_radius(self, index):
        planet = self.planets.get(index)
        if planet is not None:
            return planet.radius

    def set_planet_mass(self, index, newmass):
        planet = self.planets.get(index)
        if planet is not None:
            planet.mass = newmass
            planet.calc_radius()

    def set_planet_density(self, index, newdensity):
        planet = self.planets.get(index)
        if planet is not None:
            planet.density = newdensity
            planet.calc_radius()
    # GETTER / SETTER END

    cdef object check_collision(self, object planet1, object planet2):

        cdef double dist, delta_x, delta_y, impulse_x, impulse_y

        dist, delta_x, delta_y = planet1.calc_distance(planet1.state, planet2)
        if not (dist < (planet1.radius + planet2.radius)):
            return None
        impulse_x = planet1.state.vel_x * planet1.mass + planet2.state.vel_x * planet2.mass
        impulse_y = planet1.state.vel_y * planet1.mass + planet2.state.vel_y * planet2.mass
        if planet1.mass <= planet2.mass:
            update_planet, del_planet = planet2, planet1
        else:
            update_planet, del_planet = planet1, planet2

        update_planet.mass += del_planet.mass
        update_planet.state.vel_x = impulse_x / update_planet.mass
        update_planet.state.vel_y = impulse_y / update_planet.mass
        update_planet.calc_radius()
        return del_planet

    def tick(self, int timerate):

        cdef int index1, index2, index
        cdef list del_indexes = []

        #del_indexes = []
        self.curtime += timerate

        for planet in self.planets.values():
            planet.update(self.curtime, timerate)

        for index1, index2 in itertools.combinations(self.planets, 2):
            planet1 = self.planets[index1]
            planet2 = self.planets[index2]
            del_planet = self.check_collision(planet1, planet2)
            if del_planet == planet1:
                del_indexes.append(index1)
            elif del_planet == planet2:
                del_indexes.append(index2)

        for index in del_indexes:
            self.delete_planet(index)