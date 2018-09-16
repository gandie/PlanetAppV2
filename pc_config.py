import json

'''
Configuration module of pocketcosmos. Defaults Configuration and stuff live
here.
'''

SETTING_TYPES = ['bool', 'number', 'select']


class ConfigType(object):

    def __init__(self, name, settings_type, label, defaultvalue, min_value=None,
                 max_value=None, values=None, show=True, seqnum=None):

        assert settings_type in SETTING_TYPES, 'invalid setting_type'

        self.name = name
        self.settings_type = settings_type
        self.label = label
        self.defaultvalue = defaultvalue

        self.min_value = min_value
        self.max_value = max_value
        self.values = values
        self.show = show

        self.seqnum = seqnum

        # do some validation to sleep better
        if self.settings_type == 'number':
            valid = (self.min_value is not None) and (self.max_value is not None)
            assert valid, 'number type needs min/max for slider borders!'
            assert self.defaultvalue >= self.min_value, 'default lower than min'
            assert self.defaultvalue <= self.max_value, 'default higher than max'
        elif self.settings_type == 'select':
            valid = self.values is not None
            assert valid, 'select type needs values to select from!'
            assert self.defaultvalue in self.values, 'default not in values!'
        elif self.settings_type == 'bool':
            valid = isinstance(self.defaultvalue, bool)
            assert valid, 'bool default must be a bool!'

        self.value = defaultvalue

    def validate(self, value):
        '''simple input validation calld from model when value is set'''
        if self.settings_type == 'number':
            assert value >= self.min_value, '%s lower than min in %s' % (value, self.name)
            assert value <= self.max_value, '%s higher than max %s' % (value, self.name)
        elif self.settings_type == 'select':
            assert value in self.values, 'not in values!'
        elif self.settings_type == 'bool':
            valid = isinstance(value, bool)
            assert valid, 'bool default must be a bool!'


class ConfigModel(object):

    def __init__(self):
        self.config = {
            # Minimum mass START
            'min_moon_mass': ConfigType(
                name='min_moon_mass',
                settings_type='number',
                label='Minimum moon mass',
                defaultvalue=9,
                min_value=6,
                max_value=11,
                seqnum=80
            ),
            'min_planet_mass': ConfigType(
                name='min_planet_mass',
                settings_type='number',
                label='Minimum planet mass',
                defaultvalue=15,
                min_value=10,
                max_value=20,
                seqnum=90
            ),
            'min_gasgiant_mass': ConfigType(
                name='min_gasgiant_mass',
                settings_type='number',
                label='Minimum gasgiant mass',
                defaultvalue=50,
                min_value=40,
                max_value=100,
                seqnum=100
            ),
            'min_sun_mass': ConfigType(
                name='min_sun_mass',
                settings_type='number',
                label='Minimum sun mass',
                defaultvalue=50000,
                min_value=40000,
                max_value=60000,
                seqnum=110
            ),
            'min_bigsun_mass': ConfigType(
                name='min_bigsun_mass',
                settings_type='number',
                label='Minimum bigsun mass',
                defaultvalue=100000,
                min_value=80000,
                max_value=120000,
                seqnum=120
            ),
            'min_giantsun_mass': ConfigType(
                name='min_giantsun_mass',
                settings_type='number',
                label='Minimum giantsun mass',
                defaultvalue=250000,
                min_value=200000,
                max_value=400000,
                seqnum=130
            ),
            'min_blackhole_mass': ConfigType(
                name='min_blackhole_mass',
                settings_type='number',
                label='Minimum blackhole mass',
                defaultvalue=600000,
                min_value=500000,
                max_value=700000,
                seqnum=140
            ),

            'min_blackhole_mass': ConfigType(
                name='min_blackhole_mass',
                settings_type='number',
                label='Minimum blackhole mass',
                defaultvalue=600000,
                min_value=500000,
                max_value=700000,
                seqnum=150
            ),
            # Minimum mass END
            # Density START
            'moon_density': ConfigType(
                name='moon_density',
                settings_type='number',
                label='Moon density',
                defaultvalue=.1,
                min_value=.05,
                max_value=.15,
                seqnum=160
            ),
            'planet_density': ConfigType(
                name='planet_density',
                settings_type='number',
                label='Planet density',
                defaultvalue=.1,
                min_value=.05,
                max_value=.15,
                seqnum=170
            ),
            'gasgiant_density': ConfigType(
                name='gasgiant_density',
                settings_type='number',
                label='Gasgiant density',
                defaultvalue=.1,
                min_value=.05,
                max_value=.15,
                seqnum=180
            ),
            'sun_density': ConfigType(
                name='sun_density',
                settings_type='number',
                label='Sun density',
                defaultvalue=.5,
                min_value=.2,
                max_value=1,
                seqnum=190
            ),
            'bigsun_density': ConfigType(
                name='bigsun_density',
                settings_type='number',
                label='Big sun density',
                defaultvalue=2,
                min_value=1,
                max_value=4,
                seqnum=200
            ),
            'giantsun_density': ConfigType(
                name='giantsun_density',
                settings_type='number',
                label='Giant sun density',
                defaultvalue=4,
                min_value=3,
                max_value=6,
                seqnum=210
            ),
            'blackhole_density': ConfigType(
                name='blackhole_density',
                settings_type='number',
                label='Blackhole density',
                defaultvalue=100,
                min_value=50,
                max_value=500,
                seqnum=220
            ),
            # Density END
            # Game setting START
            'background': ConfigType(
                name='background',
                settings_type='bool',
                label='Show background',
                defaultvalue=True,
                seqnum=70
            ),
            'show_tutorial': ConfigType(
                name='show_tutorial',
                settings_type='bool',
                label='Show tutorial',
                defaultvalue=False,
                show=False,
                seqnum=60
            ),
            'multi_shot_min': ConfigType(
                name='multi_shot_min',
                settings_type='number',
                label='Minimum bodies multishot',
                defaultvalue=10,
                min_value=5,
                max_value=50,
                seqnum=40
            ),
            'multi_shot_max': ConfigType(
                name='multi_shot_max',
                settings_type='number',
                label='Maximum bodies multishot',
                defaultvalue=50,
                min_value=45,
                max_value=100,
                seqnum=50
            ),
            'engine': ConfigType(
                name='engine',
                settings_type='select',
                label='Engine to use for gravity calculations',
                defaultvalue='crk4engine',
                values=['crk4engine', 'cplanet', 'pythonrk4'],
                seqnum=10
            ),
            'ticks_ahead': ConfigType(
                name='ticks_ahead',
                settings_type='number',
                label='Ticks to calculate into future when showing orbits',
                defaultvalue=500,
                min_value=100,
                max_value=1000,
                seqnum=20
            ),
            'music_volume': ConfigType(
                name='music_volume',
                settings_type='number',
                label='Music volume',
                defaultvalue=0.0,
                min_value=0.0,
                max_value=1.0,
                seqnum=30
            ),
        }

    def __iter__(self):
        return self.config.__iter__()

    def __getitem__(self, key):
        return self.config[key]

    def __setitem__(self, key, value):
        if key in self.config:
            configitem = self.config[key]
            configitem.validate(value)
            configitem.value = value
        else:
            raise KeyError('Key not found in config: %s' % key)


class ConfigController(object):
    '''app will talk to this
    '''

    def __init__(self, path):
        self.path = path
        self.model = ConfigModel()
        self.load()

    def __getitem__(self, key):
        return self.model[key].value

    def __setitem__(self, key, value):
        self.model[key] = value

    def __iter__(self):
        return self.model.config.iterkeys()

    def load(self):
        try:
            with open(self.path, 'r') as settingsfile:
                json_d = settingsfile.readline()
            settings = json.loads(json_d)
            for key, value in settings.items():
                # self.model[key].value = value
                self.model[key] = value
        except IOError:
            print('Unable to open settings file. Using defaults.')

    def save(self):
        '''safe current model state into json file'''
        save_dict = {key: self.model[key].value for key in self.model}
        save_json = json.dumps(save_dict)
        with open(self.path, 'w') as settingsfile:
            settingsfile.write(save_json)

    def showconfig(self):
        '''Debug function to display config'''
        import pprint
        save_dict = {key: self.model[key].value for key in self.model}
        pprint.pprint(save_dict)


if __name__ == '__main__':
    '''simple test for new config machine'''

    controller = ConfigController('another_settings.json')
    controller.showconfig()

    for key in controller:
        print(key, controller[key])

    controller.save()
