# OSRS Flipping Tool

## Table of Contents
1. [About this project](#about)
2. [Features](#features)
3. [Building and running](#building-and-running)

<a name="about"></a>
## About this Project
I'm hoping that this tool will be useful to people who are interested in
flipping on the Oldschool Runescape Grand Exchange. I started off with
attempting to write python scripts that I embedded in a LibreOffice Calc
document, but that turned out to be slow and ugly. After, I considered Tkinter,
but decided against it because UI toolkits scare me. While I was looking, I
realized that I could just call up a webkit window and use HTML and Javascript
to make a pretty interface. That's where we are now. The project is in *very*
early stages, and basically none of the user-facing features are implemented,
but I'm making a lot of progress on the underside of the application. Hopefully
these efforts will pay off in the long run.

<a name="features"></a>
## Features
Nuthin yet :(

<a name="building-and-running"></a>
## Building and running
In order to build this project, you must install the following
platform-specific dependencies:

### Linux
* Nothing at this time

### macOS
* [Brew](https://brew.sh/)
* magic

    brew install libmagic
    pip3 install python-magic

* magic

    pip3 install pywebview
    pip3 install python-magic

After you have installed the dependencies, it's just a simple matter of running the following from the project root:
    make
    dist/merching.py

Note: I was unable to get this to build in Windows as it depends on gnu make,
which didn't seem to have much support for Windows. Additionally, I couldn't
figure out how to get the python dependencies to install correctly on my
Windows VM. Because of these two things, I've decided that I do not offer
Windows compatibility at this time. 
