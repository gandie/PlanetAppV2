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
        D = self.planets
        merged_planets = []
        for index1 in D:
            for index2 in D:
                if index1 == index2:
                    continue

                # collision, maybe write own collision-thingy?
                #if not D[index1]['widget'].collide_widget(D[index2]['widget']):
                #    continue
                
                if not self.check_collision(index1, index2):
                    continue
                
                # bigger body eats smaller one
                if D[index1]['mass'] < D[index2]['mass']:
                    continue

                # ask the mighty planetcore for help doing calculations
                planetcore = CPlanetcore(D[index1]['position_x'],
                                         D[index1]['position_y'],
                                         D[index1]['velocity_x'],
                                         D[index1]['velocity_y'],
                                         D[index1]['mass'])

                # planetcore knows how to calculate collision stuff
                newmass = planetcore.calc_impulse(D[index2]['velocity_x'],
                                                  D[index2]['velocity_y'],
                                                  D[index2]['mass'])

                # ask mighty planetcore for new velocity
                new_vx = planetcore.get_vel_x()
                new_vy = planetcore.get_vel_y()

                #print type(new_vx)

                D[index1]['velocity_x'] = planetcore.get_vel_x()
                D[index1]['velocity_y'] = planetcore.get_vel_y()

                D[index1]['mass'] = newmass

                # kill planetcore due to memory-sanity
                del planetcore

                # calculate new size
                self.calc_planetsize(index1)

                if not index2 in merged_planets:
                    merged_planets.append(index2)

        # remove merged planets afterwards
        for planetindex in merged_planets:
            self.delete_planet(planetindex)
            #self.gamezone.remove_widget(D[planetindex]['widget'])
            #D.pop(planetindex)

    def calc_gravity(self, dt):
        D = self.planets
        # loop over planets
        for index1 in D:
            # initialize the mighty planetcore!
            planetcore = CPlanetcore(D[index1]['position_x'],
                                     D[index1]['position_y'],
                                     D[index1]['velocity_x'],
                                     D[index1]['velocity_y'],
                                     D[index1]['mass'])
            # loop over planets...again
            for index2 in D:
                # do not create singularites ;-)
                if index1 == index2:
                    continue
                # let the mighty planetcore do its work
                force = planetcore.calc_body(D[index2]['position_x'],
                                             D[index2]['position_y'],
                                             D[index2]['mass'])

            # ask mighty planetcore for results
            D[index1]['velocity_x'] = planetcore.get_vel_x()
            D[index1]['velocity_y'] = planetcore.get_vel_y()

            # clear planetcore for hygienic purposes
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
        #S = self.suns
        for index in P:
            if P[index]['body'] == 'sun':
                continue
            distances = []
            for index2 in P:
                if P[index2]['body'] != 'sun':
                    continue
                # ask the mighty planetcore for help doing calculations
                planetcore = CPlanetcore(P[index]['position_x'],
                                         P[index]['position_y'],
                                         P[index]['velocity_x'],
                                         P[index]['velocity_y'],
                                         P[index]['mass'])
                dist = planetcore.calc_dist(P[index2]['position_x'],
                                            P[index2]['position_y'])
                # kill planetcore - it's no longer needed...
                del planetcore
                distances.append(dist)
            if distances:
                dist = min(distances)
                # do smart stuff HERE!
                offset = 1 * 0.5 ** (dist / 150)
                #print offset
                P[index]['widget'].set_color(offset)

    def check_collision(self, index1, index2):
        D = self.planets

        # get coords of second planet
        p2_x = D[index2]['position_x']
        p2_y = D[index2]['position_y']

        # get size of each planet / body
        size1 = D[index1]['widget'].size[0]
        size2 = D[index2]['widget'].size[0]

        # cook planetcore for dist-calculation
        planetcore = CPlanetcore(D[index1]['position_x'],
                                 D[index1]['position_y'],
                                 D[index1]['velocity_x'],
                                 D[index1]['velocity_y'],
                                 D[index1]['mass'])

        dist = planetcore.calc_dist(p2_x, p2_y)

        del planetcore

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
