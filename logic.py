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
    zoom_mode = BooleanProperty(None)

    currindex = NumericProperty(1)

    def __init__(self):
        self.planets = {}
        self.load_planet_textures()
        self.load_sun_textures()

    def start_game(self):
        Clock.schedule_interval(self.move_planets, 1.0 / 30.0)
        Clock.schedule_interval(self.calc_gravity, 1.0 / 30.0)
        Clock.schedule_interval(self.merge_planets, 1.0 / 60.0)

    def stop_game(self):
        Clock.unschedule(self.move_planets)
        Clock.unschedule(self.calc_gravity)
        Clock.unschedule(self.merge_planets)

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

        newplanet.set_texture(newplanet_texture)

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
        self.currindex += 1

    def reset_planets(self, instance):
        print 'planets have been removed'
        D = self.planets
        L = []
        for index in D:
            self.gamezone.remove_widget(D[index]['widget'])

        D.clear()

    def move_planets(self, dt):
        D = self.planets
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
                if not D[index1]['widget'].collide_widget(D[index2]['widget']):
                    continue
                # bigger body eats smaller one
                if D[index1]['mass'] < D[index2]['mass']:
                    continue

                # build c extension for collision calculation!!
                # calculate impulse
                impulse_x = (D[index1]['velocity_x'] * D[index1]['mass'] +
                             D[index2]['velocity_x'] * D[index2]['mass'])
                impulse_y = (D[index1]['velocity_y'] * D[index1]['mass'] +
                             D[index2]['velocity_y'] * D[index2]['mass'])

                # add mass to first planet
                D[index1]['mass'] += D[index2]['mass']

                # update first body's velocity
                D[index1]['velocity_x'] = impulse_x / D[index1]['mass']
                D[index1]['velocity_y'] = impulse_y / D[index1]['mass']

                # calculate new size
                self.calc_planetsize(index1)

                if not index2 in merged_planets:
                    merged_planets.append(index2)

        # remove merged planets afterwards
        for planetindex in merged_planets:
            self.gamezone.remove_widget(D[planetindex]['widget'])
            D.pop(planetindex)

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
        # C Code!
        diameter = 2 * sqrt(D[index]['density'] * D[index]['mass'] / 3.14)
        D[index]['widget'].size = (diameter, diameter)

    # build separate module for canvas-shizzle?
    def draw_trajectory(self):
        pass

    def draw_hillbodies(self):
        pass

    def load_planet_textures(self):
        self.planet_textures = []
        L = []
        path = ('./media/textures/')
        for filename in listdir(path):
            if not filename.endswith('.png'):
                continue
            if not 'planet' in filename:
                continue
            L.append(path + filename)
        for string in L:
            newimage = Image(source=string)
            newtexture = newimage.texture
            self.planet_textures.append(newtexture)

    def load_sun_textures(self):
        self.sun_textures = []
        L = []
        path = ('./media/textures/')
        for filename in listdir(path):
            if not filename.endswith('.png'):
                continue
            if not 'sun' in filename:
                continue
            L.append(path + filename)
        for string in L:
            newimage = Image(source=string)
            newtexture = newimage.texture
            self.sun_textures.append(newtexture)
