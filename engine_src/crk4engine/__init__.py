from pythonforandroid.toolchain import *
from pythonforandroid.recipe import *


class CRk4EngineRecipe(IncludedFilesBehaviour, CythonRecipe):
    version = ''
    url = ''
    name = 'crk4engine'
    src_filename = 'src'
    depends = [('python3')]


recipe = CRk4EngineRecipe()
