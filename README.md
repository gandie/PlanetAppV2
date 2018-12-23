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


Currently using versions:
* Cython version 0.25.1
* Kivy version 1.10.0
* Buildozer version 0.34

# Installation

See [Releases](https://github.com/gandie/PlanetAppV2/releases) for prebuilt versions.

## Windows

Unzip the windows release to a place you trust. Then Navigate into the `main`
folder and start `main.exe`.

Expect missing `missing *.dll` errors on startup, these are caused by the sound
module and must be investigated in future releases. Currenty all windows releases
work with debug console activated, so expect one window showing the app and another
one showing a terminal showing strange errors.

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

## PyInstaller (EXE)

Windows build has been tested using pyinstaller installed into a virtualwine
environment. `main.spec` can be altered and used with pyinstaller to build EXE-files.

# Links

## Tech
* [Kivy Docs](https://kivy.org/doc/stable/)
* [Buildozer Docs](https://buildozer.readthedocs.io/en/latest/)
* [python-for-android](https://github.com/kivy/python-for-android)
* [virtualwine](https://github.com/htgoebel/virtual-wine)

## Artists
* [rafikibeats music](https://soundcloud.com/rafikibeats)
* [IKONE graphics](https://www.instagram.com/ikone.official/)
