# KIVY
from kivy.uix.image import Image
from kivy.properties import *
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader

from kivy.graphics import Line, Color


# CUSTOM
from planet import Planet

# ENGINES
from cplanet import CPlanetKeeper
from engine_rk4 import Engine
from crk4engine import CRk4Engine

# BUILTIN
from random import choice, randint
from os import listdir
import math

from game_modi import AddBodyMode, AddBodyMode_Multi, ZoomMode, DelMode


class Logic(Screen):

    '''
    main logic object, directly accessible from app

    this object talks to the main engine of the planetapp and
    hands over informations to widgets and stuff.
    '''

    # gui elements to talk to
    gamezone = ObjectProperty(None)
    mainscreen = ObjectProperty(None)

    # MODI-FLAGS
    tutorial_mode = BooleanProperty(None)
    fixview_mode = BooleanProperty(None)
    show_orbit_mode = BooleanProperty(None)
    cur_guimode = ObjectProperty(None)

    # SELECTED PLANET
    selplanet = ObjectProperty(None, allownone=True)
    selplanet_index = NumericProperty(None, allownone=True)
    selplanet_index_temp = NumericProperty(None, allownone=True)

    # this is called when app is built!
    def __init__(self, settings):

        # set up dicts to be filled
        self.planets = {}
        self.settings = settings

        self.engine_map = {
            'cplanet': CPlanetKeeper,
            'crk4engine': CRk4Engine,
            'pythonrk4': Engine,
        }

        self.init_engines(self.settings['engine'])

        self.sound_map = {
            'piano': SoundLoader.load('media/sound/piano.wav'),
            'music': SoundLoader.load('media/sound/planets.wav')
        }

        # time per time ratio
        self.tick_ratio = 1.0

        self.texture_mapping = {
            'moon': self.load_textures('./media/textures/moons/'),
            'planet': self.load_textures('./media/textures/planets/'),
            'gasgiant': self.load_textures('./media/textures/gasgiants/'),
            'sun': self.load_textures('./media/textures/suns/'),
            'bigsun': self.load_textures('./media/textures/bigsuns/'),
            'giantsun': self.load_textures('./media/textures/giantsuns/'),
            'blackhole': self.load_textures('./media/textures/blackholes/'),
        }

        # observe selplanet
        self.bind(selplanet=self.on_selplanet)

    def init_engines(self, engine):
        '''
        if self.settings['use_rk4_engine'] is True:
            self.engine = 'rk4'
        else:
            self.engine = 'CPlanet'
        '''

        assert engine in self.engine_map, 'Unknown engine!'
        self.engine = engine
        # initialize planetkeeper
        # self.keeper = CPlanetKeeper()
        # self.keeper = Engine()
        self.keeper = self.engine_map[self.engine]()

        # temporary keeper for trajectory calculation
        # self.temp_keeper = CPlanetKeeper()
        # self.temp_keeper = Engine()
        self.temp_keeper = self.engine_map[self.engine]()

    def apply_settings(self):

        self.sound_map['music'].loop = True
        self.sound_map['music'].volume = self.settings['music_volume']

        if self.engine != self.settings['engine']:
            self.init_engines(self.settings['engine'])
        self.planet_transitions = {
            'moon': {'nextbody': 'planet',
                     'mass': self.settings['min_planet_mass'],
                     'density': self.settings['planet_density'],
                     'textures': self.texture_mapping['planet']},
            'planet': {'nextbody': 'gasgiant',
                       'mass': self.settings['min_gasgiant_mass'],
                       'density': self.settings['gasgiant_density'],
                       'textures': self.texture_mapping['gasgiant']},
            'gasgiant': {'nextbody': 'sun',
                         'mass': self.settings['min_sun_mass'],
                         'density': self.settings['sun_density'],
                         'textures': self.texture_mapping['sun']},
            'sun': {'nextbody': 'bigsun',
                    'mass': self.settings['min_bigsun_mass'],
                    'density': self.settings['bigsun_density'],
                    'textures': self.texture_mapping['bigsun']},
            'bigsun': {'nextbody': 'giantsun',
                       'mass': self.settings['min_giantsun_mass'],
                       'density': self.settings['giantsun_density'],
                       'textures': self.texture_mapping['giantsun']},
            'giantsun': {'nextbody': 'blackhole',
                         'mass': self.settings['min_blackhole_mass'],
                         'density': self.settings['blackhole_density'],
                         'textures': self.texture_mapping['blackhole']}
        }

        self.mode_setting = {
            'add_planet': {
                'min': self.settings['min_planet_mass'],
                'max': self.settings['min_gasgiant_mass'] * 0.9,
                'step': (self.settings['min_gasgiant_mass'] * 0.9 - self.settings['min_planet_mass']) / 10
            },
            'add_sun': {
                'min': self.settings['min_sun_mass'],
                'max': self.settings['min_bigsun_mass'] * 0.9,
                'step': (self.settings['min_bigsun_mass'] * 0.9 - self.settings['min_sun_mass']) / 10
            },
            'multi': {
                'min': int(self.settings['multi_shot_min']),
                'max': int(self.settings['multi_shot_max']),
                'step': int(0.1 * self.settings['multi_shot_max'])
            },
            'zoom': {
                'min': 0.0,
                'max': 2,
                'step': 0.01,
            }
        }

        self.mode_map = {
            'zoom': ZoomMode(
                self.gamezone,
                sizeable=True,
                settings=self.mode_setting['zoom'],
                slider_label='Time Ratio'
            ),
            'add_planet': AddBodyMode(
                self.gamezone,
                body='planet',
                draw_trajectory=True,
                sizeable=True,
                settings=self.mode_setting['add_planet'],
                slider_label='Body Mass'
            ),
            'add_sun': AddBodyMode(
                self.gamezone,
                body='sun',
                draw_trajectory=False,
                sizeable=True,
                settings=self.mode_setting['add_sun'],
                slider_label='Sun Mass'
            ),
            'multi': AddBodyMode_Multi(
                self.gamezone,
                body='moon',
                draw_trajectory=False,
                sizeable=True,
                settings=self.mode_setting['multi'],
                slider_label='Body Count'
            ),
            'del': DelMode(self.gamezone)
        }

        if self.cur_guimode is None:
            self.cur_guimode = self.mode_map['add_planet']
            self.mainscreen.add_value_slider(self.cur_guimode)
        self.bind(cur_guimode=self.on_cur_guimode)

    def on_cur_guimode(self, instance, value):
        # ask mode wether slider values have to be set
        # apply data from mode to slider...
        self.mainscreen.remove_value_slider()
        if value.sizeable:
            # value is a mode here!
            self.mainscreen.add_value_slider(value)

    def start_game(self):

        self.sound_map['music'].play()

        Clock.schedule_interval(self.update_game, 1.0 / 25.0)
        Clock.schedule_interval(self.tick_engine, 1.0 / 25.0)
        Clock.schedule_interval(self.clone_engine, 1.0 / 25.0)
        Clock.schedule_interval(self.collect_garbage, 1.0)  # / 10.0)

        '''
        self.lines = []
        Clock.schedule_interval(self.zirkus, 1.0 / 25.0)  # / 10.0)
        '''

    def stop_game(self):

        # self.gamezone.canvas.clear()
        self.gamezone.canvas.remove_group('nein')
        Clock.unschedule(self.update_game)
        Clock.unschedule(self.tick_engine)
        Clock.unschedule(self.clone_engine)
        Clock.unschedule(self.collect_garbage)
        self.sound_map['music'].stop()

    def zirkus(self, dt):
        for index, planet_d in self.planets.items():
            with self.gamezone.canvas:
                self.lines.append(
                    (Color(1, 1, 1),
                    Line(
                        circle=(planet_d['position_x'], planet_d['position_y'], 1),
                        group='nein'
                        ))
                )
            for color, line in self.lines:
                if color.a > 0:
                    color.a -= 0.01
                else:
                    self.gamezone.canvas.remove(line)
                    self.gamezone.canvas.remove(color)
                    self.lines.remove((color, line))
                    print 'removing...'

    def register_gamezone(self, gamezone):
        self.gamezone = gamezone

    def register_mainscreen(self, mainscreen):
        self.mainscreen = mainscreen

    def add_body(self, body='planet', pos=(0, 0), texture_index=None,
                 vel=(0, 0), density=1, mass=100, fixed=False,
                 light=0, temperature=0, **kwargs):

        # create new widget
        newplanet = Planet()

        # texture of new body, defaults to planet
        texture_list = self.texture_mapping[body]
        texture_index = texture_index or randint(0, len(texture_list) - 1)
        newplanet_texture = texture_list[texture_index]
        newplanet.set_base_image(newplanet_texture)

        # inform the keeper
        newindex = self.keeper.create_planet(
            pos_x=pos[0],
            pos_y=pos[1],
            vel_x=vel[0],
            vel_y=vel[1],
            mass=mass,
            density=density
        )

        # if keeper says no, do nothing
        if newindex == -1:
            return

        radius = self.keeper.get_planet_radius(newindex)
        planet_d = {
            'position_x': pos[0],
            'position_y': pos[1],
            'velocity_x': vel[0],
            'velocity_y': vel[1],
            'density': density,
            'mass': mass,
            'radius': radius,
            'fixed': fixed,
            'widget': newplanet,
            'texture_index': texture_index,
            'body': body
        }

        # fix body in keeper if neccessary
        if fixed:
            self.keeper.fix_planet(newindex)

        # write dict into planets-dict
        self.planets[newindex] = planet_d

        # modify planet widget
        newplanet.size = (radius * 2, radius * 2)
        newplanet.center = pos

        self.gamezone.add_widget(newplanet)

    def reset_planets(self, instance):
        for index in self.planets.keys():
            self.delete_planet(index)

    # USE THIS TO DELETE PLANETS!
    def delete_planet(self, index):
        if index not in self.planets:
            return
        widget = self.planets[index]['widget']
        self.gamezone.remove_widget(widget)
        if widget == self.selplanet:
            self.selplanet = None
        self.keeper.delete_planet(index)
        self.planets.pop(index)

    def delete_planet_widget(self, widget):
        index = self.get_planet_index(widget)
        self.delete_planet(index)

    # let the keeper do its work
    def tick_engine(self, dt):
        self.keeper.tick(self.tick_ratio)

    # collect orphaned widgets
    # TODO: collect bodies far away
    def collect_garbage(self, dt):
        for widget in self.gamezone.children:
            if self.get_planet_index(widget) is None:
                self.gamezone.remove_widget(widget)

    def update_game(self, dt):
        del_indexes = []
        for index in self.planets:
            if self.keeper.planet_exists(index):
                # fetch data from keeper
                pos_x = self.keeper.get_planet_pos_x(index)
                pos_y = self.keeper.get_planet_pos_y(index)
                mass = self.keeper.get_planet_mass(index)
                radius = self.keeper.get_planet_radius(index)
                vel_x = self.keeper.get_planet_vel_x(index)
                vel_y = self.keeper.get_planet_vel_y(index)

                # cleanup garbage
                if pos_x > self.gamezone.size[0] or pos_x < 0:
                    del_indexes.append(index)
                    continue
                if pos_y > self.gamezone.size[1] or pos_y < 0:
                    del_indexes.append(index)
                    continue

                # update physics data
                self.planets[index]['position_x'] = pos_x
                self.planets[index]['position_y'] = pos_y
                self.planets[index]['velocity_x'] = vel_x
                self.planets[index]['velocity_y'] = vel_y
                self.planets[index]['mass'] = mass
                self.planets[index]['radius'] = radius

                # update planet widget
                self.planets[index]['widget'].center_x = pos_x
                self.planets[index]['widget'].center_y = pos_y
                self.planets[index]['widget'].size = (radius * 2, radius * 2)

                transition = self.planet_transitions.get(self.planets[index]['body'])
                if transition:
                    if self.planets[index]['mass'] > transition['mass']:
                        self.planets[index]['body'] = transition['nextbody']
                        self.planets[index]['density'] = transition['density']

                        self.keeper.set_planet_density(index, transition['density'])

                        texture_index = randint(0, len(transition['textures']) - 1)
                        newplanet_texture = transition['textures'][texture_index]
                        self.planets[index]['widget'].set_base_image(newplanet_texture)
            else:
                # collect planets to be deleted
                del_indexes.append(index)

        for index in del_indexes:
            self.delete_planet(index)

        '''
        if self.selplanet_index is not None:
            self.calc_energy()
        '''

        if self.selplanet_index is not None and self.fixview_mode:
            self.center_planet(self.selplanet_index)

        if self.selplanet_index is not None and self.show_orbit_mode:
            self.calc_trajectory_selplanet()

    def load_textures(self, path):
        texture_list = []
        for filename in listdir(path):
            if not filename.endswith('.png'):
                continue
            texture_list.append(path + filename)
        return texture_list

    def get_planet_index(self, widget):
        P = self.planets
        for index in P:
            if P[index]['widget'] == widget:
                return index

    def select_planet(self, widget):
        if widget == self.selplanet:
            self.selplanet.unselect()
            self.selplanet = None
        else:
            if self.selplanet:
                self.selplanet.unselect()
            self.selplanet = widget
            self.selplanet.select()

    def on_selplanet(self, instance, value):
        if value is None:
            self.mainscreen.remove_infobox()
            self.mainscreen.remove_seltoggles()
            self.selplanet_index = None
            Clock.unschedule(self.update_infobox)
            Clock.unschedule(self.update_seltoggles)
            self.fixview_mode = False
            self.show_orbit_mode = False
            self.gamezone.canvas.remove_group('trajectory_selplanet')
        else:
            self.selplanet_index = self.get_planet_index(value)
            self.mainscreen.add_infobox()
            self.mainscreen.add_seltoggles()
            Clock.schedule_interval(self.update_infobox, 1.0)
            Clock.schedule_interval(self.update_seltoggles, 1.0 / 10.0)

    def calc_energy(self):
        # prototype to calculate if body orbits another
        planet_dict = self.planets[self.selplanet_index]
        for comp_index in self.planets:
            if comp_index == self.selplanet_index:
                continue
            comp_planet_dict = self.planets[comp_index]
            if comp_planet_dict['mass'] < planet_dict['mass'] * 10:
                continue
            dist_x = comp_planet_dict['position_x'] - planet_dict['position_x']
            dist_y = comp_planet_dict['position_y'] - planet_dict['position_y']
            dist = math.sqrt(dist_x ** 2 + dist_y ** 2)
            r_vel_x = planet_dict['velocity_x']
            r_vel_y = planet_dict['velocity_y']
            r_vel_sqrd = r_vel_x ** 2 + r_vel_y ** 2
            gravity = (planet_dict['mass'] * comp_planet_dict['mass']) / dist
            energy = 0.5 * planet_dict['mass'] * (r_vel_sqrd)
            print 'dist, grav > energy', dist, gravity > energy

    def update_infobox(self, dt):
        if self.selplanet_index is not None:
            planet_dict = self.planets[self.selplanet_index]
            self.mainscreen.infobox.update(**planet_dict)

    def update_seltoggles(self, dt):
        if self.selplanet_index is not None:
            planet_dict = self.planets[self.selplanet_index]
            # add fixview attribute to dict to update fixedview (eye-icon)
            planet_dict['fixview'] = self.fixview_mode
            planet_dict['show_orbit'] = self.show_orbit_mode
            self.mainscreen.seltoggles.update(**planet_dict)

    def delete_selected(self, instance):
        index = self.selplanet_index
        if index:
            self.delete_planet(index)

    def fix_selected(self, instance):
        index = self.selplanet_index
        if index is not None:
            if self.planets[index]['fixed']:
                self.keeper.unfix_planet(index)
                self.planets[index]['fixed'] = False
            else:
                self.keeper.fix_planet(index)
                self.planets[index]['fixed'] = True

    def addmass_selected(self, instance):
        index = self.selplanet_index
        if index is not None:
            newmass = self.planets[index]['mass'] * 1.1
            self.keeper.set_planet_mass(index, newmass)

    def submass_selected(self, instance):
        index = self.selplanet_index
        if index is not None:
            newmass = self.planets[index]['mass'] * 0.9
            self.keeper.set_planet_mass(index, newmass)

    def center_planet(self, index):
        pos_x = self.planets[index]['position_x']
        pos_y = self.planets[index]['position_y']
        newpos = self.gamezone.to_parent(pos_x, pos_y)
        offset_x = newpos[0] - Window.width / 2
        offset_y = newpos[1] - Window.height / 2
        new_center = (self.gamezone.center[0] - offset_x,
                      self.gamezone.center[1] - offset_y)

        self.gamezone.center = new_center

    def fixview_selected(self, value):
        self.fixview_mode = value

    def show_orbit_selected(self, value):
        self.show_orbit_mode = value
        if not value:
            self.gamezone.canvas.remove_group('trajectory_selplanet')

    def clone_engine(self, dt):

        # reset temporary keeper
        if self.engine in ['cplanet', 'crk4engine']:
            for index in xrange(1000):
                self.temp_keeper.delete_planet(index)
        else:
            self.temp_keeper.planets = {}

        # populate temp engine
        for index in self.planets:
            planet_d = self.planets[index]
            temp_id = self.temp_keeper.create_planet(
                pos_x=planet_d['position_x'],
                pos_y=planet_d['position_y'],
                vel_x=planet_d['velocity_x'],
                vel_y=planet_d['velocity_y'],
                mass=planet_d['mass'],
                density=planet_d['density']
            )
            if index == self.selplanet_index:
                self.selplanet_index_temp = temp_id
            # do not forget to also fix bodies for trajectory calc.
            if planet_d['fixed']:
                self.temp_keeper.fix_planet(temp_id)

    # calc trajectory of not-yet-existing body
    def calc_trajectory(self, planet_d):

        ticks = int(self.settings['ticks_ahead'])

        # list of points for trajectory in keeper coord.-system
        temp_list = []
        # return temp_list
        # create temporary body in temp keeper
        temp_index = self.temp_keeper.create_planet(
            pos_x=planet_d['position_x'],
            pos_y=planet_d['position_y'],
            vel_x=planet_d['velocity_x'],
            vel_y=planet_d['velocity_y'],
            mass=planet_d['mass'],
            density=planet_d['density']
        )

        # look into the future using the temp keeper
        for _ in xrange(ticks):
            self.temp_keeper.tick(self.tick_ratio)
            if self.temp_keeper.planet_exists(temp_index):
                # fetch data from keeper, track position
                pos_x = self.temp_keeper.get_planet_pos_x(temp_index)
                pos_y = self.temp_keeper.get_planet_pos_y(temp_index)
                pos = (pos_x, pos_y)
                temp_list.append(pos)

        return temp_list

    def calc_trajectory_selplanet(self):
        self.gamezone.canvas.remove_group('trajectory_selplanet')

        planet = self.planets.get(self.selplanet_index)
        if planet is None:
            return

        # selpannet index might differ from index in temp_keeper
        # see clone engine
        index = self.selplanet_index_temp
        ticks = int(self.settings['ticks_ahead'])

        trajectory_points = tuple()
        # look into the future using the temp keeper
        for _ in xrange(ticks):
            self.temp_keeper.tick(self.tick_ratio)
            if self.temp_keeper.planet_exists(index):
                # fetch data from keeper, track position
                pos_x = self.temp_keeper.get_planet_pos_x(index)
                pos_y = self.temp_keeper.get_planet_pos_y(index)
                pos = (pos_x, pos_y)
                trajectory_points += pos

        with self.gamezone.canvas:
            trajectory_line = [
                Line(points=trajectory_points,
                     width=1, dash_offset=1, group='trajectory_selplanet')]
