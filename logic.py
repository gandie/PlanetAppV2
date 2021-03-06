# KIVY
from kivy.uix.image import Image
from kivy.properties import *
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Line, Color


# CUSTOM
from planet import Planet
from game_modi import AddBodyMode, AddBodyMode_Multi, ZoomMode, DelMode
from pc_tape import Tape

# ENGINES
from cplanet import CPlanetKeeper
from engine_rk4 import Engine
from crk4engine import CRk4Engine

# BUILTIN
from random import choice, randint
from os import listdir
import math


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
    # tutorial_mode = BooleanProperty(None)
    fixview_mode = BooleanProperty(False)
    show_orbit_mode = BooleanProperty(False)
    cur_guimode = ObjectProperty(None)

    # SELECTED PLANET
    selplanet = ObjectProperty(None, allownone=True)
    selplanet_index = NumericProperty(None, allownone=True)
    selplanet_index_temp = NumericProperty(None, allownone=True)

    # this is called when app is built!
    def __init__(self, settings, sound_manager):

        # set up dicts to be filled
        self.planets = {}

        self.intervals = {
            'tick':       1 / 25.0,
            'garbage':    1,
            'next_track': 5,
        }

        self.settings = settings
        self.sound_manager = sound_manager
        self.sound_manager.logic = self

        self.tape = Tape(self, self.settings['engine'])

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

        self.lines = dict()
        self.future_changed = False

    def show_track(self, trackname):
        '''pass trackname to sound widget'''
        # print('Sound next callback: %s' % trackname)
        self.mainscreen.sound_panel.track_label.text = trackname.split('.')[0]
        Clock.schedule_once(self.mainscreen.sound_panel.show_track, 0)
        Clock.schedule_once(self.mainscreen.sound_panel.hide_track, 5)

    def apply_settings(self):

        if self.tape.engine_name != self.settings['engine']:
            self.tape.init_engine(self.settings['engine'])

        # changing setting also changes the future ^^
        self.future_changed = True
        self.tape.init_tapes()

        self.planet_transitions = {
            'moon': {
                'nextbody': 'planet',
                'mass': self.settings['min_planet_mass'],
                'density': self.settings['planet_density'],
                'textures': self.texture_mapping['planet']
            },
            'planet': {
                'nextbody': 'gasgiant',
                'mass': self.settings['min_gasgiant_mass'],
                'density': self.settings['gasgiant_density'],
                'textures': self.texture_mapping['gasgiant']#
            },
            'gasgiant': {
                'nextbody': 'sun',
                'mass': self.settings['min_sun_mass'],
                'density': self.settings['sun_density'],
                'textures': self.texture_mapping['sun']
            },
            'sun': {
                'nextbody': 'bigsun',
                'mass': self.settings['min_bigsun_mass'],
                'density': self.settings['bigsun_density'],
                'textures': self.texture_mapping['bigsun']
            },
            'bigsun': {
                'nextbody': 'giantsun',
                'mass': self.settings['min_giantsun_mass'],
                'density': self.settings['giantsun_density'],
                'textures': self.texture_mapping['giantsun']
            },
            'giantsun': {
                'nextbody': 'blackhole',
                'mass': self.settings['min_blackhole_mass'],
                'density': self.settings['blackhole_density'],
                'textures': self.texture_mapping['blackhole']
            }
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
                settings=self.mode_setting['zoom']
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
            self.cur_guimode = self.mode_map['zoom']
            # self.mainscreen.add_value_slider(self.cur_guimode)
        self.bind(cur_guimode=self.on_cur_guimode)

    def on_cur_guimode(self, instance, value):
        # ask mode wether slider values have to be set
        # apply data from mode to slider...
        self.mainscreen.add_menupanel.remove_value_slider()
        if value.sizeable:
            # value is a mode here!
            self.mainscreen.add_menupanel.add_value_slider(value)

    def start_game(self):

        Clock.schedule_interval(self.tape.update_game, self.intervals['tick'])
        Clock.schedule_interval(self.tape.tick_clone, self.intervals['tick'])

        Clock.schedule_interval(self.collect_garbage, self.intervals['garbage'])
        Clock.schedule_interval(self.sound_manager.autoplay, self.intervals['next_track'])

    def stop_game(self, keep_traces=True, keep_sound=True):

        Clock.unschedule(self.tape.update_game)
        Clock.unschedule(self.tape.tick_clone)

        Clock.unschedule(self.collect_garbage)
        Clock.unschedule(self.sound_manager.autoplay)

        if self.settings['traces'] and not keep_traces:
            Clock.unschedule(self.draw_traces)
            self.clear_traces()
            # self.gamezone.canvas.remove_group('nein')
            self.lines = dict()
            self.settings['traces'] = False

        if not keep_sound:
            self.sound_manager.stop()

    def clear_traces(self):
        '''called from stop_game and reset_planets'''
        indexes = self.planets.keys()
        for index in indexes:
            self.gamezone.canvas.remove_group('planet_%s' % index)
            if index in self.lines:
                self.lines.pop(index)

    def draw_traces(self, dt):
        '''fetch and filter history_data from tape and draw line for each
        body. only create new line object if planet index is not found
        in self.lines dict storing one line per planet. deleted planets
        lines will be removed during delete_planet call using the index-unique
        canvas group.'''
        for index, planet_d in self.planets.items():
            history = [entry for entry in self.tape.history_data if index in entry]
            body_hist = [entry[index] for entry in history]
            points = [(entry['pos_x'], entry['pos_y']) for entry in body_hist]
            points_t = tuple()
            for p in points:
                points_t += p
            if index in self.lines:
                self.lines[index].points = points_t
            else:
                with self.gamezone.canvas:
                    c = Color(1, 1, 1)
                    self.lines[index] = Line(
                        points=points_t,
                        group='planet_%s' % index,  # mark line for planet
                        cap='none',
                        joint='none'
                    )

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

        # inform the engine
        newindex = self.tape.engine.create_planet(
            pos_x=pos[0],
            pos_y=pos[1],
            vel_x=vel[0],
            vel_y=vel[1],
            mass=mass,
            density=density
        )

        # if engine says no, do nothing
        if newindex == -1:
            return

        radius = self.tape.engine.get_planet_radius(newindex)
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
            self.tape.engine.fix_planet(newindex)

        # write dict into planets-dict
        self.planets[newindex] = planet_d

        # modify planet widget
        newplanet.size = (radius * 2, radius * 2)
        newplanet.center = pos

        self.gamezone.add_widget(newplanet)

        self.future_changed = True

    def reset_planets(self, instance):
        '''
        called from reset button in MainScreen
        delete all planets and reset traces
        '''

        del_keys = list(self.planets.keys())
        for index in del_keys:
            self.delete_planet(index)

        # self.gamezone.canvas.remove_group('nein')
        self.clear_traces()
        self.lines = dict()

    # USE THIS TO DELETE PLANETS!
    def delete_planet(self, index):
        if index not in self.planets:
            return
        widget = self.planets[index]['widget']
        self.gamezone.remove_widget(widget)
        if widget == self.selplanet:
            self.selplanet = None
        self.tape.engine.delete_planet(index)
        self.planets.pop(index)
        if index in self.lines:
            self.lines.pop(index)
            self.gamezone.canvas.remove_group('planet_%s' % index)
        for entry in self.tape.history_data:
            if index in entry:
                entry.pop(index)

    def delete_planet_widget(self, widget):
        index = self.get_planet_index(widget)
        self.delete_planet(index)

    def collect_garbage(self, dt):
        '''collect orphaned widgets'''
        for widget in self.gamezone.children:
            if self.get_planet_index(widget) is None:
                self.gamezone.remove_widget(widget)

    def check_modes(self):
        '''called from tape update'''
        if self.selplanet_index is not None and self.fixview_mode:
            self.center_planet(self.selplanet_index)

        if self.selplanet_index is not None and self.show_orbit_mode:
            self.draw_trajectory_selplanet()

    def load_textures(self, path):
        # XXX: build textures+transitions module?
        texture_list = []
        for filename in listdir(path):
            if not filename.endswith('.png'):
                continue
            texture_list.append(path + filename)
        return texture_list

    def get_planet_index(self, widget):
        for index in self.planets:
            if self.planets[index]['widget'] == widget:
                return index

    def select_planet(self, widget):
        '''called from zoom mode'''
        if widget == self.selplanet:
            self.selplanet.unselect()
            self.selplanet = None
        else:
            if self.selplanet:
                self.selplanet.unselect()
            self.selplanet = widget
            self.selplanet.select()

    def on_selplanet(self, instance, value):
        # XXX: check if selplanet is altered from different place then method
        # select_planet above
        if value is None:
            # self.mainscreen.remove_infobox()
            self.mainscreen.remove_modpanel()
            self.selplanet_index = None
            # Clock.unschedule(self.update_infobox)
            Clock.unschedule(self.update_modpanel)
            self.fixview_mode = False
            self.show_orbit_mode = False
            self.gamezone.canvas.remove_group('trajectory_selplanet')
        else:
            self.selplanet_index = self.get_planet_index(value)
            # self.mainscreen.add_infobox()
            self.mainscreen.add_modpanel()
            # Clock.schedule_interval(self.update_infobox, 1.0)
            Clock.schedule_interval(self.update_modpanel, 1.0 / 10.0)

    def calc_energy(self):
        '''UNUSED'''
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
            # print 'dist, grav > energy', dist, gravity > energy

    def update_infobox(self, dt):
        '''UNUSED'''
        if self.selplanet_index is not None:
            planet_dict = self.planets[self.selplanet_index]
            self.mainscreen.infobox.update(**planet_dict)

    def update_modpanel(self, dt):
        # XXX: really call this periodically?
        if self.selplanet_index is not None:
            planet_dict = self.planets[self.selplanet_index]
            # add fixview attribute to dict to update fixedview (eye-icon)
            planet_dict['fixview'] = self.fixview_mode
            planet_dict['show_orbit'] = self.show_orbit_mode
            self.mainscreen.modpanel.update(**planet_dict)

    def delete_selected(self, instance):
        index = self.selplanet_index
        if index is not None:
            self.delete_planet(index)

    def fix_selected(self, instance):
        index = self.selplanet_index
        if index is not None:
            if self.planets[index]['fixed']:
                self.tape.engine.unfix_planet(index)
                self.planets[index]['fixed'] = False
            else:
                self.tape.engine.fix_planet(index)
                self.planets[index]['fixed'] = True
            self.future_changed = True

    def addmass_selected(self, instance):
        index = self.selplanet_index
        if index is not None:
            newmass = self.planets[index]['mass'] * 1.1
            self.tape.engine.set_planet_mass(index, newmass)
            self.future_changed = True

    def submass_selected(self, instance):
        index = self.selplanet_index
        if index is not None:
            newmass = self.planets[index]['mass'] * 0.9
            self.tape.engine.set_planet_mass(index, newmass)
            self.future_changed = True

    def center_planet(self, index):
        '''put center of view (gamezone) to planet coords'''

        pos_x = self.planets[index]['position_x']
        pos_y = self.planets[index]['position_y']
        newpos = self.gamezone.to_parent(pos_x, pos_y)

        # calc center
        offset_x = newpos[0] - Window.width / 2
        offset_y = newpos[1] - Window.height / 2
        new_center = (self.gamezone.center[0] - offset_x,
                      self.gamezone.center[1] - offset_y)

        self.gamezone.center = new_center

    def fixview_selected(self, value):
        self.fixview_mode = value

    def show_orbit_selected(self, value):
        # invalidate future stack when orbit is shown
        if value:
            self.future_changed = True
        self.show_orbit_mode = value
        self.gamezone.canvas.remove_group('trajectory_selplanet')

    def draw_trajectory_selplanet(self):
        '''fetch and filter data from future tape and draw a line from it'''

        if self.future_changed:
            return

        self.gamezone.canvas.remove_group('trajectory_selplanet')
        temp_index = self.tape.index_map[self.selplanet_index]

        future = [
            entry for entry in self.tape.future_data if temp_index in entry
        ]

        body_fut = [entry[temp_index] for entry in future]
        points = [(entry['pos_x'], entry['pos_y']) for entry in body_fut]
        points_t = tuple()
        for p in points:
            points_t += p

        with self.gamezone.canvas:
            trajectory_line = [
                Line(points=points_t,
                     width=1,
                     group='trajectory_selplanet')
            ]

    def calc_distance(self, pos1, pos2):
        '''helper function to calculate distance. may vanish in favour of more
        performant solution like kivy vector library or even usage of c-powered
        engine
        '''
        a = (pos1[0] - pos2[0]) ** 2
        b = (pos1[1] - pos2[1]) ** 2
        return (a + b) ** 0.5

    def find_major_body(self, pos):
        '''find body excercising most force relative to a given position
        assuming body has mass 1

        return index of body for further processing
        may vanish in favour of more performant solution written in c
        '''
        major_force = {
            index: planet_d['mass'] / (self.calc_distance(pos, (planet_d['position_x'], planet_d['position_y'])) ** 2)
            for index, planet_d in self.planets.items()
        }
        if major_force:
            major_index = max(major_force, key=major_force.get)
            return self.planets[major_index]

        return None
