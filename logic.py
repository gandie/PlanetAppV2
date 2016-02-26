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

    gamezone = ObjectProperty(None)

    # MODES like sandbox, solar system n shit?!

    # GUI DATA
    add_planet_mode = BooleanProperty(None)
    add_sun_mode = BooleanProperty(None)
    zoom_mode = BooleanProperty(None)
    del_mode = BooleanProperty(None)

    modes = ReferenceListProperty(add_planet_mode, add_sun_mode, 
                                  zoom_mode, del_mode)

    currindex = NumericProperty(1)

    def __init__(self):
        self.planets = {}

        self.distances = {}
        self.forces = {}

        self.planet_textures = self.load_textures('./media/textures/planets/')
        self.sun_textures = self.load_textures('./media/textures/suns/')

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
            'body' : body
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
        for index in D:
            self.gamezone.remove_widget(D[index]['widget'])

        D.clear()

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
        D = self.planets
        diameter = 2 * sqrt(D[index]['density'] * D[index]['mass'] / 3.14)
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

    def check_proximity(self, dt):
        P = self.planets
        D = self.distances
        #S = self.suns
        for index in P:
            if P[index]['body'] == 'sun':
                continue
            distances = []
            for index2 in P:
                if P[index2]['body'] != 'sun':
                    continue
                if index in D[index2] and index in D:
                    dist = D[index2][index]
                    distances.append(dist)
                else:
                    print 'nein'
                
            if distances:
                dist = min(distances)
                # do smart stuff HERE!
                offset = 1 * 0.5 ** (dist / 150)
                #print offset
                P[index]['widget'].set_color(offset)

    def check_collision(self, index1, index2):
        P = self.planets
        D = self.distances

        # get coords of second planet
        p2_x = P[index2]['position_x']
        p2_y = P[index2]['position_y']

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
        self.gamezone.remove_widget(D[index]['widget'])
        D.pop(index)

    def delete_planet_widget(self, widget):
        D = self.planets
        for index in D:
            if D[index]['widget'] == widget:
                self.delete_planet(index)
                break
