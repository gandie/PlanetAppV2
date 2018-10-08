'''
Sound handling module of PocketCosmos app.
'''
# KIVY
from kivy.core.audio import SoundLoader
from kivy.uix.floatlayout import FloatLayout

# BUILTIN
import os
import random


class SoundManager(object):
    '''loads sound files from media directory and provides basic functions to
    play / stop tracks loaded while ingame'''

    '''
    self.sound_map['alpha'].volume = self.settings['music_volume']
    '''

    def __init__(self, settings, path='./media/sound/music/', endings=None):

        self.settings = settings
        self.path = path

        # default valid sound file endings
        if not endings:
            self.endings = ['ogg']

        self.import_sounds()

    def import_sounds(self):
        '''use kivy SoundLoader to load all audio files from given folder and
        store them in sound_map dict'''
        self.sound_map = {}
        sound_files = os.listdir(self.path)
        for sound_file in sound_files:
            if not sound_file.split('.')[-1] in self.endings:
                continue
            sound = SoundLoader.load(os.path.join(self.path,sound_file))
            self.sound_map[sound_file] = sound

        # will crash if no sound files were found
        self.curkey = random.choice(self.sound_map.keys())
        self.cursound = self.sound_map[self.curkey]

    def next(self):
        '''pick next track from sound_map'''
        self.curkey = random.choice(self.sound_map.keys())
        self.cursound = self.sound_map[self.curkey]

    def autoplay(self):
        '''called periodically from logic to check if next track has to be
        played'''

        # check if current track has finished, pick new track if so
        if self.cursound.state == 'stop':
            self.next()
            self.play()

    def play(self):
        '''called from mainscreen sound widget or logic module'''
        if self.cursound.state == 'stop':
            self.cursound.volume = self.settings['music_volume']
            self.cursound.play()

    def stop(self):
        '''called from mainscreen sound widget or logic module'''
        if self.cursound.state == 'play':
            self.cursound.stop()


if __name__ == '__main__':
    '''simple test
    '''
    import pc_config
    c = pc_config.ConfigController('settings.json')
    a = SoundManager(settings=c)
    print(a.sound_map, a.curkey)
