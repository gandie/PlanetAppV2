#from kivy.core.image import Image
from kivy.uix.image import Image
from kivy.properties import *
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from planet import Planet
from cplanetcore import CPlanetcore

from random import choice, randint
# put that into c code!
from math import sqrt
from os import listdir

from kivy.core.window import Window

# logic needs to be a kivy object to make properties work? 
class Logic(Screen):

    # gui elements to talk to
    gamezone = ObjectProperty(None)
    mainscreen = ObjectProperty(None)

    tutorial_mode = BooleanProperty(None)

    # GUI DATA
    add_planet_mode = BooleanProperty(None)
    add_sun_mode = BooleanProperty(None)
    zoom_mode = BooleanProperty(None)
    del_mode = BooleanProperty(None)
    #pick_mode = BooleanProperty(None)
    multi_mode = BooleanProperty(None)

    fixview_mode = BooleanProperty(None)

    currindex = NumericProperty(1)

    selplanet = ObjectProperty(None, allownone = True)

    selplanet_index = NumericProperty(None, allownone = True)

    #settings = DictProperty(None)

    def __init__(self):

        # set up dicts to be filled
        self.planets = {}
        self.settings = {}
        self.distances = {}
        self.forces = {}

        # load textures for body-categories
        self.moon_textures = self.load_textures('./media/textures/moons/')
        self.planet_textures = self.load_textures('./media/textures/planets/')
        self.gasgiant_textures = self.load_textures('./media/textures/gasgiants/')
        self.sun_textures = self.load_textures('./media/textures/suns/')
        self.bigsun_textures = self.load_textures('./media/textures/bigsuns/')
        self.giantsun_textures = self.load_textures('./media/textures/giantsuns/')
        self.blackhole_textures = self.load_textures('./media/textures/blackholes/')

        # observe selplanet
        self.bind(selplanet = self.selplanet_change)

    def load_transitions(self):
        self.planet_transitions = {
            'moon' : {'nextbody' : 'planet',
                      'mass' : self.settings['min_planet_mass'],
                      'density' : self.settings['planet_density'],
                      'textures' : self.planet_textures},
            'planet' : {'nextbody' : 'gasgiant',
                        'mass' : self.settings['min_gasgiant_mass'],
                        'density' : self.settings['gasgiant_density'],
                        'textures' : self.gasgiant_textures},
            'gasgiant' : {'nextbody' : 'sun',
                          'mass' : self.settings['min_sun_mass'],
                          'density' : self.settings['sun_density'],
                          'textures' : self.sun_textures},
            'sun' : {'nextbody' : 'bigsun',
                     'mass' : self.settings['min_bigsun_mass'],
                     'density' : self.settings['bigsun_density'],
                     'textures' : self.bigsun_textures},
            'bigsun' : {'nextbody' : 'giantsun',
                        'mass' : self.settings['min_giantsun_mass'],
                        'density' : self.settings['giantsun_density'],
                        'textures' : self.giantsun_textures},
            'giantsun' : {'nextbody' : 'blackhole',
                          'mass' : self.settings['min_blackhole_mass'],
                          'density' : self.settings['blackhole_density'],
                          'textures' : self.blackhole_textures}
        }

        self.texture_mapping = {
            'moon' : self.moon_textures,
            'planet' : self.planet_textures,
            'gasgiant' : self.gasgiant_textures,
            'sun' : self.sun_textures,
            'bigsun' : self.bigsun_textures,
            'giantsun' : self.giantsun_textures,
            'blackhole' : self.blackhole_textures
        }

    def start_game(self):
        Clock.schedule_interval(self.move_planets, 1.0 / 30.0)
        Clock.schedule_interval(self.calc_gravity, 1.0 / 30.0)
        Clock.schedule_interval(self.merge_planets, 1.0 / 30.0)
        #Clock.schedule_interval(self.check_proximity, 1.0 / 20.0)

    def stop_game(self):
        Clock.unschedule(self.move_planets)
        Clock.unschedule(self.calc_gravity)
        Clock.unschedule(self.merge_planets)
        #Clock.unschedule(self.check_proximity)

    def register_gamezone(self, gamezone):
        self.gamezone = gamezone

    def register_mainscreen(self, mainscreen):
        self.mainscreen = mainscreen

    # my own tiny planet-factory
    def add_body(self, **args):
        index = self.currindex
        newplanet = Planet()
        body = args.get('body', 'planet')
        pos = args.get('pos', (0, 0))

        texture_list = self.texture_mapping.get(body, self.planet_textures)
        texture_index = args.get('texture_index',
                                 randint(0, len(texture_list) - 1))
        newplanet_texture = texture_list[texture_index]

        newplanet.set_base_image(newplanet_texture)

        # build planet dictionary
        planet_d = {
            'position_x' : pos[0],
            'position_y' : pos[1],
            'velocity_x' : args.get('vel', (0, 0))[0],
            'velocity_y' : args.get('vel', (0, 0))[1],
            'density' : args.get('density', 1),
            'mass' : args.get('mass', 100),
            'fixed' : args.get('fixed', False),
            'hillbodies' : [],
            'widget' : newplanet,
            'texture_index' : texture_index,
            'body' : body,
            'light' : args.get('light', 0),
            'temperature' : args.get('temperature', 0)
        }

        # write dict into planets-dict
        self.planets[index] = planet_d

        self.calc_planetsize(index)
        newplanet.center = pos
        self.gamezone.add_widget(newplanet)
        self.currindex += 1

    def reset_planets(self, instance):
        D = self.planets
        L = []
        for index in D.keys():
            self.delete_planet(index)
            
    def move_planets(self, dt):
        D = self.planets
        for index in D:
            if D[index]['fixed']:
                continue
            D[index]['position_x'] += D[index]['velocity_x']
            D[index]['position_y'] += D[index]['velocity_y']
            D[index]['widget'].center_x = D[index]['position_x']
            D[index]['widget'].center_y = D[index]['position_y']

        # fixing view on a body must be done here to avoid ugly glitches
        if self.selplanet_index and self.fixview_mode:
            #print 'ball'
            self.center_planet(self.selplanet_index)

    def merge_planets(self, dt):
        P = self.planets
        merged_planets = []
        for index1 in P:
            for index2 in P:
                if index1 == index2:
                    continue
                if not self.check_collision(index1, index2):
                    continue
                
                # bigger body eats smaller one
                if P[index1]['mass'] < P[index2]['mass']:
                    continue

                planetcore = CPlanetcore(P[index1]['position_x'],
                                         P[index1]['position_y'],
                                         P[index2]['position_x'],
                                         P[index2]['position_y'],
                                         P[index1]['velocity_x'],
                                         P[index1]['velocity_y'],
                                         P[index2]['velocity_x'],
                                         P[index2]['velocity_y'],
                                         P[index1]['mass'],
                                         P[index2]['mass'])

                P[index1]['mass'] = planetcore.calc_impulse()
                P[index1]['velocity_x'] = planetcore.get_vel_p1_x()
                P[index1]['velocity_y'] = planetcore.get_vel_p1_y()

                del planetcore

                # calculate new size
                self.calc_planetsize(index1)

                if P[index2]['fixed']:
                    P[index1]['fixed'] = True

                if not index2 in merged_planets:
                    merged_planets.append(index2)

        # remove merged planets afterwards
        for planetindex in merged_planets:
            self.delete_planet(planetindex)

    def calc_gravity(self, dt):
        P = self.planets
        newlist = P.keys()
        remove = newlist.remove

        # prepare distances and forces to be filled
        D = self.distances        
        F = self.forces
        for index in P:
            D[index] = {}
            F[index] = {}

        for index1 in P:
            remove(index1)
            for index2 in newlist:
                # initialize the new mighty planetcore
                planetcore = CPlanetcore(P[index1]['position_x'],
                                         P[index1]['position_y'],
                                         P[index2]['position_x'],
                                         P[index2]['position_y'],
                                         P[index1]['velocity_x'],
                                         P[index1]['velocity_y'],
                                         P[index2]['velocity_x'],
                                         P[index2]['velocity_y'],
                                         P[index1]['mass'],
                                         P[index2]['mass'])
                dist = planetcore.calc_dist()
                D[index1][index2] = dist
                D[index2][index1] = dist
                force = planetcore.calc_gravity()
                F[index1][index2] = force
                F[index2][index1] = force
                P[index1]['velocity_x'] = planetcore.get_vel_p1_x()
                P[index1]['velocity_y'] = planetcore.get_vel_p1_y()
                P[index2]['velocity_x'] = planetcore.get_vel_p2_x()
                P[index2]['velocity_y'] = planetcore.get_vel_p2_y()
                
                del planetcore

    def calc_trajectory(self):
        pass

    def calc_hillbodies(self):
        pass

    # now calculating in 3-dimensional space n shit (planets are spheres)
    def calc_planetsize(self, index):
        D = self.planets

        # disabled - reactivate when light-calculation is reworked
        '''
        # calculate light emission
        if D[index]['body'] in ['sun', 'bigsun', 'giantsun']:
            light = D[index]['mass'] / self.settings['min_sun_mass']
            D[index]['light'] = light
        '''

        # new transitions system
        transition = self.planet_transitions.get(D[index]['body'], None)
        if transition:
            if D[index]['mass'] > transition['mass']:
                D[index]['temperature'] = 0
                D[index]['widget'].set_color(0, 0, 0)
                D[index]['body'] = transition['nextbody']
                D[index]['density'] = transition['density']
                texture_index = randint(0, len(transition['textures']) - 1)
                newplanet_texture = transition['textures'][texture_index]
                D[index]['widget'].set_base_image(newplanet_texture)

        diameter = ((3 * D[index]['mass']) / (4 * 3.14 * D[index]['density'])) ** (1/3.0)
        D[index]['widget'].size = (diameter, diameter)

    # build separate module for canvas-shizzle?
    def draw_trajectory(self):
        pass

    def draw_hillbodies(self):
        pass

    def load_textures(self, path):
        texture_list = []
        for filename in listdir(path):
            if not filename.endswith('.png'):
                continue
            texture_list.append(path + filename)
        return texture_list

    # REWORK THIS!
    def check_proximity(self, dt):
        P = self.planets
        D = self.distances
        #S = self.suns
        for index in P:
            if P[index]['body'] == 'sun':
                continue

            distances = []
            offset = 0.8

            emitters = ['sun', 'bigsun', 'giantsun']

            for index2 in P:
                #if P[index2]['body'] != 'sun':
                #    continue
                if P[index2]['body'] not in emitters:
                    continue
                dist = D.get(index2, {}).get(index, None)
                if dist:
                    distances.append((dist, index2))
            if distances:
                for dist_tuple in distances:
                    y = dist_tuple[0] / 250
                    index_sun = dist_tuple[1]
                    light_change = P[index_sun]['light'] * 0.5 ** (y)
                    offset -= light_change

            P[index]['widget'].set_color(offset, offset, offset)

    def check_collision(self, index1, index2):
        P = self.planets
        D = self.distances

        # get size of each planet / body
        size1 = P[index1]['widget'].size[0]
        size2 = P[index2]['widget'].size[0]

        dist = D[index1][index2]

        if dist < ((size1 + size2)/2):
            return True
        else:
            return False

    # USE THIS TO DELETE PLANETS!
    def delete_planet(self, index):
        D = self.planets
        if not index in D:
            return
        widget = D[index]['widget']
        self.gamezone.remove_widget(widget)
        if widget == self.selplanet:
            self.selplanet = None
        D.pop(index)

    def delete_planet_widget(self, widget):
        index = self.get_planet_index(widget)
        self.delete_planet(index)

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

    def selplanet_change(self, instance, value):
        if value == None:
            self.mainscreen.remove_infobox()
            self.mainscreen.remove_seltoggles()
            self.selplanet_index = None
            Clock.unschedule(self.update_infobox)
            Clock.unschedule(self.update_seltoggles)
            self.fixview_mode = False
            #Clock.schedule(self.fix_view)
        else:
            self.selplanet_index = self.get_planet_index(value)
            self.mainscreen.add_infobox()
            self.mainscreen.add_seltoggles()
            Clock.schedule_interval(self.update_infobox, 1.0 / 10.0)
            Clock.schedule_interval(self.update_seltoggles, 1.0 / 10.0)
            #Clock.schedule_interval(self.fix_view, 1.0 / 60.0)

    def update_infobox(self, dt):
        if self.selplanet_index:
            P = self.planets
            D = P[self.selplanet_index]
            self.mainscreen.infobox.update(**D)

    def update_seltoggles(self, dt):
        if self.selplanet_index:
            P = self.planets
            D = P[self.selplanet_index]
            D['fixview'] = self.fixview_mode
            self.mainscreen.seltoggles.update(**D)

    def delete_selected(self, instance):
        index = self.selplanet_index
        if index:
            self.delete_planet(index)

    def fix_selected(self, instance):
        index = self.selplanet_index
        if index:
            P = self.planets
            if P[index]['fixed']:
                P[index]['velocity_x'] = 0
                P[index]['velocity_y'] = 0
                P[index]['fixed'] = False
            else:
                P[index]['fixed'] = True

    def addmass_selected(self, instance):
        index = self.selplanet_index
        if index:
            P = self.planets
            P[index]['mass'] *= 1.1
            self.calc_planetsize(index)

    def submass_selected(self, instance):
        index = self.selplanet_index
        if index:
            P = self.planets
            P[index]['mass'] *= 0.9
            self.calc_planetsize(index)

    # delete planets far away from anything else
    def collect_garbage(self):
        P = self.planets

    def center_planet(self, index):
        P = self.planets
        pos_x = P[index]['position_x']
        pos_y = P[index]['position_y']
        newpos = self.gamezone.to_parent(pos_x, pos_y)
        offset_x = newpos[0] - Window.width/2
        offset_y = newpos[1] - Window.height/2
        new_center = (self.gamezone.center[0] - offset_x,
                      self.gamezone.center[1] - offset_y)
        self.gamezone.center = new_center
        
    def fixview_selected(self, instance):
        if self.fixview_mode:
            self.fixview_mode = False
        else:
            self.fixview_mode = True
