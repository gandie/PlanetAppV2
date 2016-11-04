# KIVY
from kivy.uix.image import Image
from kivy.properties import *
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.core.window import Window

# CUSTOM
from planet import Planet

# ENGINE
from cplanet import CPlanetKeeper

# BUILTIN
from random import choice, randint
from os import listdir

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

    # GUI DATA
    add_planet_mode = BooleanProperty(None)
    add_sun_mode = BooleanProperty(None)
    zoom_mode = BooleanProperty(None)
    del_mode = BooleanProperty(None)
    multi_mode = BooleanProperty(None)
    fixview_mode = BooleanProperty(None)

    # SELECTED PLANET
    selplanet = ObjectProperty(None, allownone = True)
    selplanet_index = NumericProperty(None, allownone = True)

    # this is called when app is built!
    def __init__(self):

        # set up dicts to be filled
        self.planets = {}
        self.settings = {}

        # initialize planetkeeper
        self.keeper = CPlanetKeeper()

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
        Clock.schedule_interval(self.update_game, 1.0 / 25.0)
        Clock.schedule_interval(self.tick_engine, 1.0 / 25.0)

    def stop_game(self):
        Clock.unschedule(self.update_game)
        Clock.unschedule(self.tick_engine)

    def register_gamezone(self, gamezone):
        self.gamezone = gamezone

    def register_mainscreen(self, mainscreen):
        self.mainscreen = mainscreen

    def add_body(self, body = 'planet', pos = (0,0), texture_index = None,
                 vel = (0, 0), density = 1, mass = 100, fixed = False,
                 light = 0, temperature = 0, **kwargs):

        # create new widget
        newplanet = Planet()

        # texture of new body, defaults to planet
        texture_list = self.texture_mapping.get(body, self.planet_textures)
        texture_index = texture_index or randint(0, len(texture_list) - 1)
        newplanet_texture = texture_list[texture_index]
        newplanet.set_base_image(newplanet_texture)

        # inform the keeper
        newindex = self.keeper.create_planet(
            pos_x = pos[0],
            pos_y = pos[1],
            vel_x = vel[0],
            vel_y = vel[1],
            mass = mass,
            density = density
        )

        # if keeper says no, do nothing
        if newindex == -1:
            return

        radius = self.keeper.get_planet_radius(newindex)
        planet_d = {
            'position_x' : pos[0],
            'position_y' : pos[1],
            'velocity_x' : vel[0],
            'velocity_y' : vel[1],
            'density' : density,
            'mass' : mass,
            'fixed' : fixed,
            'widget' : newplanet,
            'texture_index' : texture_index,
            'body' : body
        }

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
        if not index in self.planets:
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
        self.keeper.tick()

    def update_game(self, dt):

        del_indexes = []

        for index in self.planets:
            if self.keeper.planet_exists(index):
                # fetch data from keeper
                pos_x = self.keeper.get_planet_pos_x(index)
                pos_y = self.keeper.get_planet_pos_y(index)
                mass = self.keeper.get_planet_mass(index)
                radius = self.keeper.get_planet_radius(index)
                density = self.keeper.get_planet_density(index)

                # update data
                self.planets[index]['position_x'] = pos_x
                self.planets[index]['position_y'] = pos_y
                self.planets[index]['mass'] = mass
                self.planets[index]['density'] = density
                self.planets[index]['widget'].center_x = pos_x
                self.planets[index]['widget'].center_y = pos_y
                self.planets[index]['widget'].size = (radius * 2, radius * 2)

                transition = self.planet_transitions.get(self.planets[index]['body'], None)
                if transition:
                    if self.planets[index]['mass'] > transition['mass']:
                        self.planets[index]['widget'].set_color(0, 0, 0)
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

        if self.selplanet_index and self.fixview_mode:
            self.center_planet(self.selplanet_index)

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
        if self.selplanet_index != None:
            P = self.planets
            D = P[self.selplanet_index]
            self.mainscreen.infobox.update(**D)

    def update_seltoggles(self, dt):
        if self.selplanet_index != None:
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
        if index != None:
            if self.planets[index]['fixed']:
                self.keeper.unfix_planet(index)
                self.planets[index]['fixed'] = False
            else:
                self.keeper.fix_planet(index)
                self.planets[index]['fixed'] = True

    def addmass_selected(self, instance):
        index = self.selplanet_index
        if index != None:
            newmass = self.planets[index]['mass'] * 1.1
            self.keeper.set_planet_mass(index, newmass)

    def submass_selected(self, instance):
        index = self.selplanet_index
        if index != None:
            newmass = self.planets[index]['mass'] * 0.9
            self.keeper.set_planet_mass(index, newmass)

    # delete planets far away from anything else
    # TO BE DONE
    def collect_garbage(self):
        pass

    def center_planet(self, index):

        pos_x = self.planets[index]['position_x']
        pos_y = self.planets[index]['position_y']

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
