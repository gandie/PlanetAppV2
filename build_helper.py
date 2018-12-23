'''
Helper module to simplify build process for android and windows builds.
Bascially types shell commands to build / install stuff and clears directories
afterwads.

Very unsecure and untested. Use at ur own risk!

THINGS TO DO:

TASK ONE:
delete parts from .buildozer folder to force rebuilding:
    -only remove custom packages

.buildozer/android/platform/build
~/D/P/.b/a/p/build (master) $ rm -rf dists/
~/D/P/.b/a/p/build (master) $ rm -rf build/
~/D/P/.b/a/p/build (master) $ rm -rf packages/cplanet/
~/D/P/.b/a/p/build (master) $ rm -rf packages/crk4engine/

TASK TWO:
Build cplanet and crk4engine.
python engine_src/cplanet/src/setup.py build install

Then put copies to:
engine_src/tests
Run test files for each engine
After succesful tests put another copy of each engine to root folder for
testing in app


TASK THREE:
If testing with new engines in app was succesful, put engines from engine_src
folder to python for android recipes folder

--> this should also trigger task one to be done!

TASK FIVE:
Build Windows exe files and structure arround it usinng a virtualwine containing
Python27, Kivy and pyInstaller in a windows-like environment.
Zip new dist/main folder into a file named "PocketCosmos-<VERSION>_win.zip".
Fetch version from buildoer.spec

wine C:/Python27/python.exe setup.py build --compiler=mingw32
wine C:/Python27/python.exe setup.py install -f

wine C:/Python27/python.exe -m PyInstaller main.spec

# TODO:
TASK FOUR:
Get fresh copies of all png assets from raw images, scaled down to X
Something like this:
In [8]: for item in a:
   ...:     print(item)
   ...:     os.system("convert -resize 250x250 %s %s" % (item, item))

# TODO:
avoid using os.system, add some safety
'''

import shutil
import argparse
import os

CUSTOM_ENGINES = ['cplanet', 'crk4engine']

HOME = os.getenv('HOME')

WINE_BIN = HOME + '/Dev/KivyBuild/bin'
WINE_PLANETAPPV2_SRC = HOME + '/Dev/KivyBuild/drive_c/PlanetAppV2'

PATH = os.getenv('PATH')


def winebuild():
    '''TASK FIVE
    Use wine + pyinstaller to build windows EXE file (and assets required).
    Build engines and install to wine-python first, then call pyinstaller to
    create EXE file.
    '''
    wine_activate()

    wine_build_engines()
    wine_pyinstaller()

    wine_deactivate()


def wine_pyinstaller():
    '''call wine-python pyinstaller on main.spec to create EXE file from
    PocketCosmos app'''
    cd_command = 'cd %s;' % WINE_PLANETAPPV2_SRC
    build_command = 'wine C:/Python27/python.exe -m PyInstaller main.spec'

    call = cd_command + build_command
    print('Will now build EXE file using wine...: %s' % call)
    os.system(call)


def wine_build_engines():
    '''build and install engines into wine environment to be consmed by
    pyInstaller later
    - git pull from master in WINE_PLANETAPPV2_SRC
    - build and install all engines from now up-to-date WINE_PLANETAPPV2_SRC
      directory
    '''
    # activate_wine()

    cd_command = 'cd %s;' % WINE_PLANETAPPV2_SRC

    pull_command = cd_command + 'git pull origin master'

    print('pulling from master branch: %s' % pull_command)
    os.system(pull_command)

    for engine in CUSTOM_ENGINES:
        engine_path = '/'.join([WINE_PLANETAPPV2_SRC, 'engine_src', engine, 'src'])
        build_path = engine_path + '/build'

        change_dir_command = 'cd %s;' % engine_path
        build_command = 'wine C:/Python27/python.exe setup.py build --compiler=mingw32;'
        install_command = 'wine C:/Python27/python.exe setup.py install -f'

        call = change_dir_command + build_command + install_command

        print('Building and installing engine into wine...: %s' % call)
        os.system(call)


def wine_activate():
    '''activate virtualwine instance by altering PATH environment variable'''

    # add virtualwine bin folder containing the wine executable to be used
    new_path = WINE_BIN + ':' + PATH

    os.putenv('PATH', new_path)

    print('activated. "which wine" output:')
    test_call = 'which wine'
    os.system(test_call)


def wine_deactivate():
    '''remove WINE_BIN from PATH environment variable'''

    os.putenv('PATH', PATH)

    print('deactivated. "which wine" output:')
    test_call = 'which wine'
    os.system(test_call)


def parse_spec():
    keys = ['p4a.source_dir', 'requirements', 'version']
    with open('buildozer.spec', 'r') as specfile:
        lines = specfile.readlines()
    key_lines = dict(
        (key, line.split(' = ')[1].strip())
        for line in lines
        for key in keys
        if key in line and not line.startswith('#')
    )
    return key_lines


def clear_build(auto=False):
    '''
    TASK ONE
    '''
    if not auto:
        uinput = ''
        while not (uinput == 'y' or uinput == 'n'):
            print('This may be helpful if requirements in buildozer.spec have changed')
            uinput = raw_input('THIS WILL FORCE REBUILDING THE APP! Sure? (y/n) ')
        if uinput == 'n':
            return
        print('Your choice...')
    build_path = '.buildozer/android/platform/build/build'
    dists_path = '.buildozer/android/platform/build/dists'
    packages_path = '.buildozer/android/platform/build/packages/'
    print('Deleting %s' % build_path)
    shutil.rmtree(build_path)
    print('Deleting %s' % dists_path)
    shutil.rmtree(dists_path)
    for engine in CUSTOM_ENGINES:
        engine_path = packages_path + engine
        print('Deleting %s' % engine_path)
        try:
            shutil.rmtree(engine_path)
        except Exception as e:
            print('Deleting %s failed' % engine_path)


def build_engines(tests=True):
    '''
    TASK TWO
    '''
    cleanup_engine_src()
    tests_folder = 'engine_src/tests'
    for engine in CUSTOM_ENGINES:
        engine_path = '/'.join(['engine_src', engine, 'src'])
        build_path = engine_path + '/build'
        '''
        print('Will remove build...: %s' % build_path)
        shutil.rmtree(build_path)
        '''

        call = 'cd %s;python setup.py build' % engine_path
        print('Building engine...: %s' % call)
        os.system(call)
        new_build_path = build_path + '/lib.linux-x86_64-2.7/%s.so' % engine

        if tests:
            print('NEW ENGINE, copying to tests folder...: %s' % new_build_path)
            shutil.copy(new_build_path, tests_folder)
            test_call = 'cd %s;python %s.py' % (tests_folder, engine)
            print('Testing...: %s' % test_call)
            os.system(test_call)

        question = 'Copy new engine to root folder? (y/n) :'
        uinput = ''
        while not (uinput == 'y' or uinput == 'n'):
            uinput = raw_input(question)
        if uinput == 'n':
            print('ABORTED. NOT copying...')
            return
        print('Copying %s.so to root folder...' % engine)
        shutil.copy(new_build_path, '.')


def copy_engines(p4a_dir):
    '''
    TASK THREE
    '''
    cleanup_engine_src()
    p4a_recipes_path = '/'.join([p4a_dir[:-1], 'pythonforandroid', 'recipes']) + '/'
    for engine in CUSTOM_ENGINES:
        # print('p4a_source.dir recipe path is: %s' % p4a_recipe_path)
        # print('Will delete...')
        # p4a_recipe_path = '/'.join([p4a_dir[:-1], 'recipes', engine])
        # shutil.rmtree(p4a_recipe_path)
        p4a_engine_path = p4a_recipes_path + engine
        print('Clearing engine in p4a folder: %s' % p4a_engine_path)
        try:
            shutil.rmtree(p4a_engine_path)
        except Exception as e:
            print('Clearing %s failed.')
        source_recipe_path = '/'.join(['engine_src', engine])
        print('Copying engine %s to p4a recipes folder %s ...' % (source_recipe_path, p4a_recipes_path))
        call = 'cp -r %s %s' % (source_recipe_path, p4a_recipes_path)
        print('WILL CALL %s' % call)
        os.system(call)


def cleanup_engine_src():
    for engine in CUSTOM_ENGINES:
        source_path = '/'.join(['engine_src', engine, 'src'])
        build_folder = source_path + '/build'
        print('Will delete build folder: %s' % build_folder)
        try:
            shutil.rmtree(build_folder)
        except Exception as e:
            print('Deleting build folder %s failed' % build_folder)
        compiled_engine = '%s/%s.c' % (source_path, engine)
        print('Will delete compiled engine: %s' % compiled_engine)
        try:
            os.remove(compiled_engine)
        except Exception as e:
            print('Deleting file %s failed' % compiled_engine)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-b',
        '--build',
        help='Build engines and copy to current directory',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '-p',
        '--p4a',
        help='Copy new engines to p4a recipes dir',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '-c',
        '--clear',
        help='Clear build to force rebuilding app',
        action='store_true',
        default=False
    )

    parser.add_argument(
        '-w',
        '--winebuild',
        help='Build windows release using wine.',
        action='store_true',
        default=False
    )

    args_d = parser.parse_args().__dict__  # i want a dict, not a namespace
    spec_data = parse_spec()

    if args_d['build']:
        build_engines()
        cleanup_engine_src()
    if args_d['p4a']:
        copy_engines(spec_data['p4a.source_dir'])
    if args_d['clear']:
        clear_build()
    if args_d['winebuild']:
        winebuild()
