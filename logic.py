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
        self.suns = {}

        self.planet_textures_hot = []
        self.planet_textures_cold = []
        self.planet_textures_livable = []

        self.load_planet_textures()
        self.load_sun_textures()

        self.texture_mapping = {
            'cold' : self.planet_textures_cold,
            'hot' : self.planet_textures_hot,
            'livable' : self.planet_textures_livable
        }

    def start_game(self):
        Clock.schedule_interval(self.move_planets, 1.0 / 30.0)
        Clock.schedule_interval(self.calc_gravity, 1.0 / 30.0)
        Clock.schedule_interval(self.merge_planets, 1.0 / 60.0)
        Clock.schedule_interval(self.check_proximity, 1.0 / 30)

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
        proximity = args.get('proximity', 'cold')

        if body == 'planet':
            if 'texture_indexes' in args.keys():
                texture_indexes = args.get('texture_indexes')
            else:
                # get new set of random textures
                texture_indexes = {
                    'cold' : randint(0, len(self.texture_mapping['cold']) - 1),
                    'hot' : randint(0, len(self.texture_mapping['hot']) - 1),
                    'livable' : randint(0, len(self.texture_mapping['livable']) - 1)
                }

            texture_index = texture_indexes[proximity]
            newplanet_texture = self.texture_mapping[proximity][texture_index]
        elif body == 'sun':
            if 'texture_indexes' in args.keys():
                texture_indexes = args.get('texture_indexes')
            else:
                texture_indexes = {
                    'sun' : randint(0, len(self.sun_textures) - 1)
                }
            texture_index = texture_indexes['sun']
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
            'texture_indexes' : texture_indexes,
            'body' : body,
            'proximity' : proximity
        }

        # write dict into planets-dict
        self.planets[index] = planet_d

        # also write suns to separate place to examine proximity between
        # planets and stars
        if body == 'sun':
            self.suns[index] = planet_d

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
        '''
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
        '''
        self.planet_textures_hot = self.load_textures('./media/textures/hot/')
        self.planet_textures_cold = self.load_textures('./media/textures/cold/')
        self.planet_textures_livable = self.load_textures(
            './media/textures/livable/'
        )

    def load_sun_textures(self):
        '''
        self.sun_textures = []
        L = []
        path = ('./media/textures/suns/')
        for filename in listdir(path):
            if not filename.endswith('.png'):
                continue
            L.append(path + filename)
        for string in L:
            newimage = Image(source=string)
            newtexture = newimage.texture
            self.sun_textures.append(newtexture)
        '''
        self.sun_textures = self.load_textures('./media/textures/suns/')

    def load_textures(self, path):
        L = []
        texture_list = []
        for filename in listdir(path):
            if not filename.endswith('.png'):
                continue
            L.append(path + filename)
        for string in L:
            newimage = Image(source=string)
            newtexture = newimage.texture
            texture_list.append(newtexture)
        return texture_list

    def set_texture(self, pindex, proximity):
        P = self.planets
        texture_list = self.texture_mapping[proximity]
        new_texureindex = P[pindex]['texture_indexes'][proximity]
        new_texture = texture_list[new_texureindex]
        #P[pindex]['texture_index'] = new_texureindex
        P[pindex]['proximity'] = proximity
        P[pindex]['widget'].set_texture(new_texture)

    def check_proximity(self, dt):
        P = self.planets
        S = self.suns
        for index in P:
            if P[index]['body'] == 'sun':
                continue
            distances = []
            for index2 in S:
                # code-code fpr distance calculation!
                dist_x = S[index2]['position_x'] - P[index]['position_x']
                dist_y = S[index2]['position_y'] - P[index]['position_y']
                dist = sqrt(dist_x ** 2 + dist_y ** 2)
                distances.append(dist)
            if distances:
                dist = min(distances)
                if dist > 0 and dist < 300:
                    proximity = 'hot'
                elif dist > 300 and dist < 1500:
                    proximity = 'livable'
                else:
                    proximity = 'cold'
                if proximity != P[index]['proximity']:
                    self.set_texture(index, proximity)
