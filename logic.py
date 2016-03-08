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
    pick_mode = BooleanProperty(None)

    multi_mode = BooleanProperty(None)

    currindex = NumericProperty(1)

    selplanet = ObjectProperty(None, allownone = True)

    selplanet_index = NumericProperty(None, allownone = True)

    #settings = DictProperty(None)

    def __init__(self):
        self.planets = {}
        self.settings = {}
        self.distances = {}
        self.forces = {}

        self.planet_textures = self.load_textures('./media/textures/planets/')
        self.sun_textures = self.load_textures('./media/textures/suns/')
        self.bind(selplanet = self.selplanet_change)

    def start_game(self):
        Clock.schedule_interval(self.move_planets, 1.0 / 30.0)
        Clock.schedule_interval(self.calc_gravity, 1.0 / 30.0)
        Clock.schedule_interval(self.merge_planets, 1.0 / 30.0)
        Clock.schedule_interval(self.check_proximity, 1.0 / 20.0)

    def stop_game(self):
        Clock.unschedule(self.move_planets)
        Clock.unschedule(self.calc_gravity)
        Clock.unschedule(self.merge_planets)
        Clock.unschedule(self.check_proximity)

    def register(self, gamezone):
        self.gamezone = gamezone

    def register_mainscreen(self, mainscreen):
        self.mainscreen = mainscreen

    # my own tiny planet-factory
    def add_body(self, **args):
        index = self.currindex
        newplanet = Planet()
        body = args.get('body', 'planet')
        pos = args.get('pos', (0, 0))

        if body == 'planet':
            texture_index = args.get('texture_index',
                                     randint(0, len(self.planet_textures) - 1))
            newplanet_texture = self.planet_textures[texture_index]
        elif body == 'sun':
            texture_index = args.get('texture_index',
                                     randint(0, len(self.sun_textures) - 1))
            newplanet_texture = self.sun_textures[texture_index]

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
        #print self.gamezone.children
        self.currindex += 1

    def reset_planets(self, instance):
        D = self.planets
        L = []
        for index in D.keys():
            self.delete_planet(index)
            
    def move_planets(self, dt):
        D = self.planets
        #print D
        for index in D:
            if D[index]['fixed']:
                continue
            D[index]['position_x'] += D[index]['velocity_x']
            D[index]['position_y'] += D[index]['velocity_y']
            D[index]['widget'].center_x = D[index]['position_x']
            D[index]['widget'].center_y = D[index]['position_y']

    def merge_planets(self, dt):
        P = self.planets
        merged_planets = []
        for index1 in P:
            for index2 in P:
                if index1 == index2:
                    continue

                # collision, maybe write own collision-thingy?
                #if not P[index1]['widget'].collide_widget(P[index2]['widget']):
                #    continue
                
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
            #self.gamezone.remove_widget(P[planetindex]['widget'])
            #P.pop(planetindex)

    def calc_gravity(self, dt):
        P = self.planets
        newlist = P.keys()
        remove = newlist.remove

        # prepare distances
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

    def calc_planetsize(self, index):
        # now calculating in 3-dimensional space n shit (planets are spheres)
        D = self.planets
        #diameter = 2 * sqrt(D[index]['density'] * D[index]['mass'] / 3.14)
        diameter = ((3 * D[index]['mass']) / (4 * 3.14 * D[index]['density'])) ** (1/3.0)
        D[index]['widget'].size = (diameter, diameter)

        # calculate light emission
        if D[index]['body'] == 'sun':
            light = D[index]['mass'] / self.settings['min_sun_mass']
            D[index]['light'] = light

        # transition from planet to sun
        if (D[index]['body'] == 'planet'): 
            if D[index]['mass'] > self.settings['min_sun_mass']:
                D[index]['temperature'] = 0
                D[index]['widget'].set_color(0, 0, 0)
                D[index]['body'] = 'sun'
                D[index]['density'] = self.settings['sun_density']
                texture_index = randint(0, len(self.sun_textures) - 1)
                newplanet_texture = self.sun_textures[texture_index]
                D[index]['widget'].set_base_image(newplanet_texture)

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

    def check_proximity(self, dt):
        P = self.planets
        D = self.distances
        #S = self.suns
        for index in P:
            if P[index]['body'] == 'sun':
                continue

            distances = []

            offset_red = 0.7
            offset_green = 0.7
            offset_blue = 0.7

            for index2 in P:
                if P[index2]['body'] != 'sun':
                    continue
                dist = D.get(index2, {}).get(index, None)
                if dist:
                    distances.append((dist, index2))
            if distances:
                for dist_tuple in distances:
                    x = dist_tuple[0] / 500
                    y = dist_tuple[0] / 50
                    index_sun = dist_tuple[1]
                    temp_change = P[index_sun]['light'] / (x**2)
                    light_change = P[index_sun]['light'] / (y**2)
                    offset_red -= light_change
                    offset_green -= light_change
                    offset_blue -= light_change
                    P[index]['temperature'] += temp_change
                    #print P[index]['temperature']
            P[index]['temperature'] *= 0.99

            #if P[index]['temperature'] > self.settings['norm_temp']:
            norm_temp = self.settings['norm_temp']
            diff = P[index]['temperature'] - norm_temp
            if diff > 0:
                offset_red -= 0.6 * (diff / norm_temp)
            else:
                offset_blue += 0.8 * (diff / norm_temp)
            offset_green *= 0.1 * abs(diff / norm_temp)

            P[index]['widget'].set_color(offset_red, offset_green, offset_blue)

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

    def delete_planet(self, index):
        D = self.planets
        if not index in D:
            return
        widget = D[index]['widget']
        #self.gamezone.remove_widget(D[index]['widget'])
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
            #print 'ball None!'
        else:
            self.selplanet_index = self.get_planet_index(value)
            #print self.selplanet_index
            self.mainscreen.add_infobox()
            self.mainscreen.add_seltoggles()
            Clock.schedule_interval(self.update_infobox, 1.0 / 10.0)
            Clock.schedule_interval(self.update_seltoggles, 1.0 / 10.0)
            #print 'foo'

    def update_infobox(self, dt):
        if self.selplanet_index:
            P = self.planets
            D = P[self.selplanet_index]
            self.mainscreen.infobox.update(**D)

    def update_seltoggles(self, dt):
        if self.selplanet_index:
            P = self.planets
            D = P[self.selplanet_index]
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
