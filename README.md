![Pocket Cosmos Splashscreen](https://github.com/gandie/PlanetAppV2/blob/master/media/splashscreen/splashscreen.jpg)

# PocketCosmos

A gravity simulation sandbox running on multiple platforms:

Windows, Linux, Android

Intended to run on mobile devices with touch screen.

Requirements:
-Python 2.7*
-Kivy 1.10
-buildozer (to build for android)
-pyinstaller (to build for windows)

See [Releases](https://github.com/gandie/PlanetAppV2/releases) for prebuilt versions.

# Packaging

Can be built into apk for android using buildozer, for windows (EXE-file) using
pyinstaller.

buildozer.spec is part of this repository and must be slightly altered to work
on your system. See comments in buildozer.spec for more detail.

Windows build has been tested using pyinstaller installed into a wine environment.
main.spec can be altered and used with pyinstaller to build EXE-files.
