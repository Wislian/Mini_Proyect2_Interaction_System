from openal import *
import time


source = oalOpen('wav/bottle_pop.wav')
listener = oalGetListener()
source.play()
while source.get_state() == AL_PLAYING:
    time.sleep(1)
listener.move_to((5,0,0))
listener.set_orientation((0,0,-1,0,1,0))
source.play()
while source.get_state() == AL_PLAYING:
    time.sleep(1)

listener.set_gain(0.5)
source.play()
while source.get_state() == AL_PLAYING:
    time.sleep(1)

oalQuit()