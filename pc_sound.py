'''
Sound handling module of PocketCosmos app.
'''
# KIVY
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

# BUILTIN
import os
import random


def no_sound_d(func):
    '''decorator to be used on methods from SoundManager to avoid crashing if
    sound support is unavailable on current system'''
    def inner(instance, *args):
        if instance.no_sound:
            return
        func(instance, *args)

    return inner


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
                self.sound_map[sound_file] = sound
            except:  # well, forgot the Exceptions name. but...who cares?!
                # this happens on OX X due to my incapability (and will) to
                # compile audio libs on apple devices
                self.no_sound = True
                break

        # will crash if no sound files were found
        self.next()

    @no_sound_d
    def next(self):
        '''pick next track from sound_map'''

        self.curkey = random.choice(self.sound_map.keys())
        self.cursound = self.sound_map[self.curkey]
        if hasattr(self, 'logic'):
            self.logic.show_track(self.curkey)

    @no_sound_d
    def autoplay(self, dt):
        '''called periodically from logic to check if next track has to be
        played'''

        # check if current track has finished, pick new track if so
        if self.cursound.state == 'stop' and self.do_autoplay:
            self.next()
            self.play()

    @no_sound_d
    def play(self):
        '''called from mainscreen sound widget or logic module'''
        if self.cursound.state == 'stop':
            self.cursound.volume = self.settings['music_volume']
            self.cursound.play()

    @no_sound_d
    def stop(self):
        '''called from mainscreen sound widget or logic module'''
        if self.cursound.state == 'play':
            self.cursound.stop()


if __name__ == '__main__':
    '''simple test using config module
    '''
    import pc_config
    c = pc_config.ConfigController('settings.json')
    a = SoundManager(settings=c)
    print(a.sound_map, a.curkey)
