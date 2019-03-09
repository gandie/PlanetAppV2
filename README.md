![Pocket Cosmos Splashscreen](https://github.com/gandie/PlanetAppV2/blob/master/media/splashscreen/splashscreen.jpg)

# PocketCosmos

A gravity simulation sandbox running on multiple platforms:

Windows, Linux, Android

Intended to run on mobile devices with touch screen.

Requirements:
* Python 2.7*
* Kivy 1.10
* buildozer (to build for android)
* pyinstaller (to build for windows)

Currently using versions (Python2):
* Cython version 0.25.1
* Kivy version 1.10.0
* Buildozer version 0.34
* python-for-android version > 0.6.0 (`a036f4442b6a232d0c3a96c0b9d223e1b8cfe1d4`)
* wine version 1.6.2

Currently using versions (Python3):
* Cython version 0.29.6
* Kivy version 1.10.0
* Buildozer version 0.39
* python-for-android version > 0.7.0 (`25e5acce19cf53119f0be94f2a8c0cebcfe78353`)

# Installation

See [Releases](https://github.com/gandie/PlanetAppV2/releases) for prebuilt versions.

## Windows

Unzip the windows release to a place you trust. Then Navigate into the `main`
folder and start `main.exe`.

Expect missing `missing *.dll` errors on startup, these are caused by the sound
module and must be investigated in future releases.

## Android

Download the android release (apk) to your device. Then make sure you allow the
installation of untrusted software (and disallow it after installation!).

Use a file explorer app of your choice, navigate to your downloads folders and
install the app by executing the apk file.

# Packaging / Building

PocketCosmos can be built into an android app using buildozer (apk) and into
a windows EXE-file using pyinstaller.

Each engine found in the `engine_src` directory represents a python-for-android
recipe which must be accessible for p4a during the build process invoked by
buildozer.

To build EXE files these engines must be installed into the python environment
calling PyInstaller.

Some of the tasks neccessary to build PocketCosmos have been automated in
the `build_helper.py` script. Alter its global variables depending on your
build environment. The docstring may be helpful to reproduce these steps or
alter the script depending on your setup and needs.

```bash
python build_helper.py -h
usage: build_helper.py [-h] [-b] [-p] [-c] [-w]

optional arguments:
  -h, --help       show this help message and exit
  -b, --build      Build engines copy to current directory
  -p, --p4a        Copy new engines to p4a recipes dir
  -c, --clear      Clear build to force rebuilding app
  -w, --winebuild  Build windows release using wine.
```

## Buildozer (APK)

`buildozer.spec` is part of this repository and must be slightly altered to work
on your system. See comments for more detail.

Make sure to copy both engines from `engine_src` directory to your
python-for-android `recipes` folder and add `cplanet,crk4engine` to buildozer
requirements.

## PyInstaller (EXE)

Windows build has been tested using pyinstaller installed into a virtualwine
environment. `main.spec` can be altered and used with pyinstaller to build EXE-files.

Make sure your wine environment has following components installed:
+ Python (2.7 / 3.4.4)
+ MinGW

### virtualwine + Python3.4 setup

First set up your new wine environment and activate it:

```bash
cd path/where/ur/wines/live
vwine-setup python3wine
. python3wine/bin/activate.fish
```

All commands mentioned from here must run inside the `(python3wine)` environment.
Now install Python3.4:

```bash
cd path/where/u/keep/python34
wine msiexec -i python-3.4.4.msi
```

Install MinGW C / C++ compiler which is needed to build engines:

```bash
cd path/where/u/keep/MinGW
wine mingw-get-setup.exe
```

If you experience any trouble with MinGW usage, try step mentioned [here](https://stackoverflow.com/questions/24683305/python-cant-install-packages-typeerror-unorderable-types-nonetype-str)

Editing `PATH` variable in wine is explained [here](https://wiki.winehq.org/Wine_User%27s_Guide#Setting_Windows.2FDOS_environment_variables)

It may be useful to add `C:\Python34\` and `C:\Python34\scripts\` to `PATH` as well
for easier `python.exe` and `pip.exe` invocation.

Now start installing python packages:

```bash
cd path/where/ur/wines/live/python3wine/drive_c/Python34/ # ..or your add "C:\Python34\" to PATH
wine python.exe -m pip install cython
wine python.exe -m pip install kivy==1.10.0
wine python.exe -m pip install pyInstaller
wine python.exe -m pip install docutils pygments kivy.deps.sdl2 kivy.deps.glew
```

Now go to a place familiar (i recommend the `drive_c` folder) and get a fresh
PocketCosmos checkout:

```bash
cd path/where/ur/wines/live/python3wine/drive_c/
git clone https://github.com/gandie/PlanetAppV2
```

Install engines, start with `cplanet`:

```bash
cd place/to/your/PlanetAppV2/engine_src/cplanet/src/
wine C:/Python34/python.exe setup.py build --compiler=mingw32
wine C:/Python34/python.exe setup.py install
```

... and same procedure to install `crk4engine`:

```bash
cd place/to/your/PlanetAppV2/engine_src/crk4engine/src/
wine C:/Python34/python.exe setup.py build --compiler=mingw32
wine C:/Python34/python.exe setup.py install
```

Now we have everything we need, we can build the EXE file:

```bash
cd place/to/your/PlanetAppV2/
wine C:/Python34/python.exe -m PyInstaller main.spec
```

You can find the `main.exe` file in the `dist/main/` directory bundled with all
file assets needed. Test call:

```bash
cd place/to/your/PlanetAppV2/dist/main
wine main.exe
```

# Links

## Tech
* [Kivy Docs](https://kivy.org/doc/stable/)
* [Buildozer Docs](https://buildozer.readthedocs.io/en/latest/)
* [python-for-android](https://github.com/kivy/python-for-android)
* [MinGW](http://www.mingw.org/wiki/Getting_Started)
* [virtualwine](https://github.com/htgoebel/virtual-wine)

## Artists
* [rafikibeats music](https://soundcloud.com/rafikibeats)
* [IKONE graphics](https://www.instagram.com/ikone.official/)
