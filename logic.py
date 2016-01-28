from kivy.properties import *
from kivy.uix.screenmanager import Screen
from planet import Planet
from kivy.clock import Clock

from cplanetcore import CPlanetcore
'''
planet_dictionary = {
    'position_x' : 0,
    'position_y' : 0,
    'velocity_x' : 0,
    'velocity_y' : 0,
    'density' : 1,
    'mass' : 1,
    'fixed' : False,
    'hillbodies' : [],
    'widget' : None
}

planets_dictionary = {
    1 : planet_dictionary
}

# testcode for c integration
bodies = [
(0 , -5, 0.1),
(0 ,-10, 0.2),
(10, 0, 0.1),
]
A = CPlanetcore(0, 0, 0, 0, 1)
for body in bodies:
A.calc_body(body[0], body[1], body[2])
testlabel = str(A.get_vel_x()) + ' , ' + str(A.get_vel_y())
#

'''

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
        Clock.schedule_interval(self.move_planets, 1.0 / 30.0)
        Clock.schedule_interval(self.calc_gravity, 1.0 / 30.0)
        Clock.schedule_interval(self.merge_planets, 1.0 / 60.0)

    def register(self, gamezone):
        self.gamezone = gamezone

    def add_planet(self, pos, vel):
        newplanet = Planet()
        newplanet.center = pos
        print pos,vel
        self.planets[self.currindex] = {
            'position_x' : pos[0],
            'position_y' : pos[1],
            'velocity_x' : vel[0],
            'velocity_y' : vel[1],
            'density' : 1,
            'mass' : 1,
            'fixed' : False,
            'hillbodies' : [],
            'widget' : newplanet
        }
        self.gamezone.add_widget(newplanet)
        self.currindex += 1

    def reset_planets(self):
        pass

    def move_planets(self, dt):
        D = self.planets
        for index in D:
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
                # collision
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

    def calc_planetsize(self):
        pass

    # build separate module for canvas-shizzle?
    def draw_trajectory(self):
        pass

    def draw_hillbodies(self):
        pass

    def load_textures(self):
        pass
