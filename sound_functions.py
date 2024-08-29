import math
from typing import Dict
from openal import *
from openal import _check
from pydub import AudioSegment
import time


sound_files: Dict[str,str]= {}
loaded_sounds: list = []
class SoundManager:
    """Manage the input of the sounds"""

    def __init__(self, path: str):
        """
        Load the sounds into the code
        

        Args:
            path (str) : Path where the sounds located
        """
        self.path = path
        self.fill_path_sound_files()

    def fill_path_sound_files(self) -> None:
        """
        Fill the sound_files dictionary with sound names and file paths
        """
        try:
            for file_name in os.listdir(self.path):
                sound_name = os.path.splitext(file_name)[0]
                sound_files[sound_name] = '/'.join([self.path, file_name])
        except FileNotFoundError:
            print(f"Error: no se encontro el directorio {self.path}")
        except Exception as e:
            print(f"Error inesperado o de nisvia: {e}")  
    def sounds_in_sys(self):
        print(loaded_sounds) 
    def available_sounds(self):
        print(sound_files)

def open_short(sound_name:str):
    """
    Load a sound into memory
    """
    if sound_name in sound_files:
        sound_path = sound_files[sound_name]
        _check()
        file_ = WaveFile(sound_path)
        buffer_ = Buffer(file_)
        source = ShortSound(buffer_, True)
    return source
class ShortSound(Source):
    """
    Combination of source functions
    """
    def __init__(self, buffer_, destroy_buffer):
        super().__init__(buffer_, destroy_buffer)
    def linear_mov(self, start_point:tuple, final_point:tuple, steps:int, pause_time: float):
        """
        Move the source from start_point to final_point in the number of steps

        Args:
            start_point: initial position
            final_point: final position
            steps: number of times the sound is played between the trip
            pause_time: Time to wait between position changes
        """
        if steps <= 0:
            raise ValueError("el numero de pasos debe ser positivo")

        x_start, y_start, z_start = start_point
        x_end, y_end, z_end = final_point
        
        x_step = (x_end - x_start) / steps
        y_step = (y_end - y_start) / steps
        z_step = (z_end - z_start) / steps
        
        for step in range(steps):
            new_x = x_start + (step + 1) * x_step
            new_y = y_start + (step + 1) * y_step
            new_z = z_start + (step + 1) * z_step
        
            self.set_position((new_x, new_y, new_z))
            
            print(self.position)
            self.play() 
            time.sleep(pause_time)
        self.set_position(final_point)
        self.play()     

device = alc.alcOpenDevice(None)
context = alc.alcCreateContext(device, None)
alc.alcMakeContextCurrent(context)

manager = SoundManager('resources/wav')
source = open_short('bottle_pop')
listener = oalGetListener()

source.play()
source.set_position((-10,10,10))
source.linear_mov(source.position,(10,-10,-10),15,0.5)
source.linear_mov(source.position,(0,0,0),5,0.5)

oalQuit()
alc.alcDestroyContext(context)
alc.alcCloseDevice(device)