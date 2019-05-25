'''
Sound handling module of PocketCosmos app.
'''
# KIVY
from kivy.core.audio import SoundLoader

# BUILTIN
import os
import random


class SoundManager(object):
    '''loads sound files from media directory and provides basic functions to
    play / stop tracks loaded while ingame'''

    def __init__(self, settings, path='./media/sound/music/', endings=None):

        self.settings = settings
        self.path = path

        self.do_autoplay = True

        # this flag is set when import fails to avoid breaking the whole app
        # due to sound problems
        self.no_sound = False

        # default valid sound file endings
        if not endings:
            self.endings = ['ogg']

        self.import_sounds()

    def import_sounds(self):
        '''use kivy SoundLoader to load all audio files from given folder and
        store them in sound_map dict. detect if sound is unavailable and set
        no_sound flag accordingly'''
        self.sound_map = {}
        sound_files = os.listdir(self.path)
        for sound_file in sound_files:
            if not sound_file.split('.')[-1] in self.endings:
                continue
            try:
                sound = SoundLoader.load(
                    os.path.join(self.path, sound_file)
                )
                if not sound:
                    self.no_sound = True
                    return
                print('adding sound: %s' % sound_file)
                self.sound_map[sound_file] = sound
            except:  # well, forgot the Exceptions name. but...who cares?!
                # this happens on OX X due to my incapability (and will) to
                # compile audio libs on apple devices
                self.no_sound = True
                return

        # will crash if no sound files were found
        self.next()

    def next(self):
        '''pick next track from sound_map'''

        if self.no_sound:
            return

        self.curkey = random.choice(list(self.sound_map.keys()))
        self.cursound = self.sound_map[self.curkey]
        if hasattr(self, 'logic'):
            self.logic.show_track(self.curkey)

    def autoplay(self, dt):
        '''called periodically from logic to check if next track has to be
        played'''
        if self.no_sound:
            return

        # check if current track has finished, pick new track if so
        if self.cursound.state == 'stop' and self.do_autoplay:
            self.next()
            self.play()

    def play(self):
        '''called from mainscreen sound widget or logic module'''
        if self.no_sound:
            return

        if self.cursound.state == 'stop':
            self.cursound.volume = self.settings['music_volume']
            self.cursound.play()

    def stop(self):
        '''called from mainscreen sound widget or logic module'''
        if self.no_sound:
            return

        if self.cursound.state == 'play':
            self.cursound.stop()


if __name__ == '__main__':
    '''simple test using config module
    '''
    import pc_config
    c = pc_config.ConfigController('settings.json')
    a = SoundManager(settings=c)
    print(a.sound_map, a.curkey)
