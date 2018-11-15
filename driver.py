from media_player import Media_Player
import os

def __main__():
    player = Media_Player()
    cwd = os.getcwd()
    player.play_MP4(cwd + '/small.mp4')


__main__()
