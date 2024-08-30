import math
from typing import Dict
from openal import *
from openal import _check
from pydub import AudioSegment
import time

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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
    
    """
    def __init__(self, buffer_, destroy_buffer):
        super().__init__(buffer_, destroy_buffer)

    def linear_mov(self, final_point:tuple, steps:int, pause_time: float):
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

        x_start, y_start, z_start = self.position
        x_end, y_end, z_end = final_point
        
        x_step = (x_end - x_start) / steps
        y_step = (y_end - y_start) / steps
        z_step = (z_end - z_start) / steps
        self.play()
        self.set_looping(True)
        for step in range(steps):
            new_x = x_start + (step + 1) * x_step
            new_y = y_start + (step + 1) * y_step
            new_z = z_start + (step + 1) * z_step
        
            self.set_position((new_x, new_y, new_z))
            
            print(self.position)
            time.sleep(pause_time)
        self.set_position(final_point)
        self.set_looping(False)   

    def rotate(self, center, axis, angle_degrees,  steps = 100):
        angle_rad = math.radians(angle_degrees)
        step_angle = angle_rad / steps

        x, y, z = self.position
        cx, cy, cz = center

        self.play()
        self.set_looping(True)

        for i in range(steps + 1):
            current_angle = i * step_angle
            x_translated = x - cx
            y_translated = y - cy
            z_translated = z - cz

            if axis == 'x':
                new_y = y_translated * math.cos(current_angle) - z_translated * math.sin(current_angle)
                new_z = y_translated * math.sin(current_angle) + z_translated * math.cos(current_angle)
                y_translated, z_translated = new_y, new_z
            elif axis == 'y':
                new_x = x_translated * math.cos(current_angle) + z_translated * math.sin(current_angle)
                new_z = -x_translated * math.sin(current_angle) + z_translated * math.cos(current_angle)
                x_translated, z_translated = new_x, new_z
            elif axis == 'z':
                new_x = x_translated * math.cos(current_angle) - y_translated * math.sin(current_angle)
                new_y = x_translated * math.sin(current_angle) + y_translated * math.cos(current_angle)
                x_translated, y_translated = new_x, new_y
            else:
                raise ValueError("Eje no válido. Use 'x', 'y' o 'z'.")

            x1 = x_translated +cx
            y1 = y_translated + cy
            z1 = z_translated + cz

            self.set_position((x1, y1, z1))

            time.sleep(0.1)

        self.set_looping(False)
        plt.show()




def wait_for_keypress():
    input("Presiona cualquier tecla para continuar...")


device = alc.alcOpenDevice(None)
context = alc.alcCreateContext(device, None)
alc.alcMakeContextCurrent(context)

manager = SoundManager('resources/wav')
source = open_short('bottle_pop')
#source = open_short('Psychosocial-mono')
listener = oalGetListener()

source.set_position((-10,0,0))
source.linear_mov(source.position,(10,-10,-10),15,0.5)
source.linear_mov(source.position,(0,0,0),5,0.5)
source.set_position((-10,0,0))
#pasa por atras
source.rotate(listener.position, "y", 90)
wait_for_keypress()
source.set_position((-10,0,0))
#pasa por adelante
source.rotate(listener.position, "y", -90)

oalQuit()
alc.alcDestroyContext(context)
alc.alcCloseDevice(device)