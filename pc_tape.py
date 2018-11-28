'''
module to handle communication between app and engine

goal is create an api for the app to fetch current, past and future planet
position data. this is done by using several instances of the current used
engine.
'''

# BUILTIN
import time
from collections import deque

# ENGINES
from cplanet import CPlanetKeeper
from engine_rk4 import Engine
from crk4engine import CRk4Engine

MAX_PLANETS = 1000
TICKS_PER_TICK = 10


class Tape(object):
    '''app talks to instance of this using logic module. this controlls
    engine instances'''

    def __init__(self, logic, engine_name):
        self.logic = logic
        self.engine_name = engine_name

        self.engine_map = {
            'cplanet': CPlanetKeeper,
            'crk4engine': CRk4Engine,
            'pythonrk4': Engine,
        }

        self.init_engine(engine_name)
        self.history_data = deque(iterable=[], maxlen=1000)
        self.future_data = deque(iterable=[], maxlen=1000)

    def init_engine(self, engine_name):
        '''this is called once when app is built and on engine settings change
        via apply_settings in logic'''

        # sleep better
        assert engine_name in self.engine_map, 'Unknown engine!'

        self.engine_name = engine_name
        # initialize planetkeeper
        self.engine = self.engine_map[self.engine_name]()

    # XXX: this must be called when future changes, e.g. planet is added
    def clone_engine(self):
        ''' create new temporary engine instance for trajectory calculations'''

        # throw away old instance if we have one
        if hasattr(self, 'temp_engine'):
            del self.temp_engine

        self.temp_engine = self.engine_map[self.engine_name]()

        # populate temp engine from status quo saved in planets dict of logic
        for index, planet_d in self.logic.planets.items():
            temp_id = self.temp_engine.create_planet(
                pos_x=planet_d['position_x'],
                pos_y=planet_d['position_y'],
                vel_x=planet_d['velocity_x'],
                vel_y=planet_d['velocity_y'],
                mass=planet_d['mass'],
                density=planet_d['density']
            )

            # do not forget to also fix bodies for trajectory calc.
            if planet_d['fixed']:
                self.temp_engine.fix_planet(temp_id)

    def fetch_data(self, engine):
        '''fetch data from an engine, filter non existing planets
        '''

        existing_indexes = [
            index for index in range(MAX_PLANETS)
            if engine.planet_exists(index)
        ]

        res = {}
        for index in existing_indexes:
            res[index] = {
                'pos_x':  engine.get_planet_pos_x(index),
                'pos_y':  engine.get_planet_pos_y(index),
                'mass':   engine.get_planet_mass(index),
                'radius': engine.get_planet_radius(index),
                'vel_x':  engine.get_planet_vel_x(index),
                'vel_y':  engine.get_planet_vel_y(index),
            }
        return res

    def tick_engine(self, dt):
        '''tick main engine representing the present time'''
        self.engine.tick(self.logic.tick_ratio)

        data = self.fetch_data(self.engine)
        self.cur_data = data
        self.history_data.append(data)

    def tick_clone(self, dt):
        '''tick engine clone and put data to future stack'''
        # abort if future has changed. wait for update and fresh engine clone
        if self.logic.future_changed:
            return

        # XXX: add smart(er) timing code here!
        cur_len = len(self.future_data)
        diff = self.logic.settings['ticks_ahead'] - cur_len
        if diff > TICKS_PER_TICK:
            ticks = TICKS_PER_TICK
        else:
            ticks = diff

        for _ in range(ticks):
            self.temp_engine.tick(self.logic.tick_ratio)
            self.future_data.append(self.fetch_data(self.temp_engine))

    def update_game(self, dt):
        '''
        apply self.cur_data to logic.planets (l_planets) dict
        check if new engine has to be cloned and future stack has to be reset
        '''

        l_planets = self.logic.planets

        del_indexes = [
           index for index in l_planets if index not in self.cur_data
        ]

        for index, planet_d in self.cur_data.items():
            pos_x = planet_d['pos_x']
            pos_y = planet_d['pos_y']
            mass = planet_d['mass']
            radius = planet_d['radius']
            vel_x = planet_d['vel_x']
            vel_y = planet_d['vel_y']

            # cleanup garbage
            if pos_x > self.logic.gamezone.size[0] or pos_x < 0:
                del_indexes.append(index)
                continue
            if pos_y > self.logic.gamezone.size[1] or pos_y < 0:
                del_indexes.append(index)
                continue

            # update physics data
            l_planets[index]['position_x'] = pos_x
            l_planets[index]['position_y'] = pos_y
            l_planets[index]['velocity_x'] = vel_x
            l_planets[index]['velocity_y'] = vel_y
            l_planets[index]['mass'] = mass
            l_planets[index]['radius'] = radius

            # update planet widget
            l_planets[index]['widget'].center_x = pos_x
            l_planets[index]['widget'].center_y = pos_y
            l_planets[index]['widget'].size = (radius * 2, radius * 2)

            # TRANSITION CHECK
            transition = self.logic.planet_transitions.get(
                l_planets[index]['body']
            )

            if transition and l_planets[index]['mass'] > transition['mass']:
                l_planets[index]['body'] = transition['nextbody']
                l_planets[index]['density'] = transition['density']
                self.engine.set_planet_density(index, transition['density'])
                texture_index = randint(0, len(transition['textures']) - 1)
                newplanet_texture = transition['textures'][texture_index]
                l_planets[index]['widget'].set_base_image(newplanet_texture)
                l_planets[index]['texture_index'] = texture_index

        for index in del_indexes:
            self.logic.delete_planet(index)

        # invalidate future data and clone new engine if future changed
        if self.logic.future_changed:
            self.future_data.clear()
            self.clone_engine()
            self.logic.future_changed = False

        # pop oldest value from future
        if len(self.future_data):
            self.future_data.popleft()

    def simple_trajectory(self, major_body, minor_body):
        '''Build and fill engine to calculate approximate trajectory of a minor
        body dominated by major_body
        '''
        temp_engine = self.engine_map[self.engine_name]()

        major_index = temp_engine.create_planet(
            pos_x=major_body['position_x'],
            pos_y=major_body['position_y'],
            vel_x=major_body['velocity_x'],
            vel_y=major_body['velocity_y'],
            mass=major_body['mass'],
            density=major_body['density']
        )

        minor_index = temp_engine.create_planet(
            pos_x=minor_body['position_x'],
            pos_y=minor_body['position_y'],
            vel_x=minor_body['velocity_x'],
            vel_y=minor_body['velocity_y'],
            mass=minor_body['mass'],
            density=minor_body['density']
        )

        ticks = int(self.logic.settings['ticks_ahead'])
        temp_list = []

        for _ in xrange(ticks):
            temp_engine.tick(self.logic.tick_ratio)
            if temp_engine.planet_exists(minor_index):
                # fetch data from keeper, track position
                pos_x = temp_engine.get_planet_pos_x(minor_index)
                pos_y = temp_engine.get_planet_pos_y(minor_index)
                pos = (pos_x, pos_y)
                temp_list.append(pos)

        return temp_list