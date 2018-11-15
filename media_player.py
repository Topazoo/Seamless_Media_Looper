import os
from subprocess import Popen

class Media_Player(object):

    def __init__(self):
        pass

    def run(self):
        print "Run"

    def find_files(self, ext):
        ''' Collect files based on extension
            @ext - The extension to search for '''

    def play_MP4(self, path):
        print "Playing MP4"

        os.system('killall omxplayer.bin')
        omxc = Popen(['omxplayer', '-b', path])