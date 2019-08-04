from pythonforandroid.toolchain import *
from pythonforandroid.recipe import *


class Pyrk4EngineRecipe(IncludedFilesBehaviour, CythonRecipe):
    version = ''
    url = ''
    name = 'pyrk4engine'
    src_filename = 'src'
    depends = [('python3')]


recipe = Pyrk4EngineRecipe()
