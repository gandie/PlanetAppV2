from pythonforandroid.toolchain import *
from pythonforandroid.recipe import *

class CplanetRecipe(IncludedFilesBehaviour, CythonRecipe):
    version = ''
    url = ''
    name = 'cplanet'
    src_filename = 'src'
    depends = [('python3')]

recipe = CplanetRecipe()
