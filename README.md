# Seamless Media Player
### Author: Peter Swanson
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 2.7](https://img.shields.io/badge/Python-2.7-brightgreen.svg)](https://www.python.org/downloads/release/python-2714/)
[![Pillow 5.3.0](https://img.shields.io/badge/Pillow-5.3.0-brightgreen.svg)](https://pypi.org/project/Pillow/5.3.0/)
[![python-vlc 3.0.4106](https://img.shields.io/badge/python–vlc-3.0.4106-brightgreen.svg)](https://pypi.org/project/python-vlc/3.0.4106/)

## Background:
A friend of mine who works in the entertainment industry told me he was thinking
about using a Raspberry Pi to loop media for the scenes he was shooting. We couldn't find
any good pre-built programs to display images or loop media so I decided to build the 
application myself with an easy to use GUI. 

<b>This application can be installed on a Raspberry Pi to seamlessly loop videos and display images.</b>

Note: This application is Linux and Windows compatible, but far more robust media applications exist.

## Using the Application:
### Install Dependencies:
Ensure the following are installed on the machine you are running the application on:
- Python 2.7 with pip
- virtualenv for Python 2.7
- vlc
    - Windows: https://get.videolan.org/vlc/3.0.4/win32/vlc-3.0.4-win32.exe
    - Linux: ``` $ sudo apt-get install vlc ```

Create a virtualenv and install the requirements from <i>requirements.txt</i> with pip
```
$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip install -r "requirements.txt"
``` 
### Run the Application:
Clone this repository to a folder of your choice, navigate to the folder containing
<i>driver.py</i> and run it.
```
(venv) $ git clone https://github.com/Topazoo/Seamless_Media_Looper.git
(venv) $ cd Seamless_Media_Looper
(venv) $ python driver.py
```
If all dependencies are installed correctly, the GUI will open.

### Navigating the GUI: 
Each GUI tab represents a different storage device. All attached USB drives are
displayed.
- Click on a tab or press tab then an arrow key to change tabs. 
- Double click or press Enter on any directory to display its contents.
- Double click or press Enter on any image file to display it in fullscreen.
- Double click or press Enter on any video file to loop it in fullscreen.
- Alt + double click or press Alt + Enter on any video to play it in fullscreen. 
- Press Escape to exit any media being displayed.
- Press Alt + F4 to exit the program.
