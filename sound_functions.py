import math
import threading
from typing import Dict
from openal import *
from openal import _check
from pydub import AudioSegment
import time
import asyncio
import os

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

sound_files: Dict[str,str]= {}
loaded_sounds: Dict[str, any] = {}
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
                file_path = os.path.join(self.path, file_name)
                sound_files[sound_name] = file_path
        except FileNotFoundError:
            print(f"Error: no se encontro el directorio {self.path}")
        except Exception as e:
            print(f"Error inesperado o de nisvia: {e}")  
    def list_sounds(self):
        for i in loaded_sounds.keys():
            print(f"{i} :, {loaded_sounds[i]}") 
    def available_sounds(self):
        print(sound_files)
    

def open_file(sound_name:str):
    """
    Load a sound into memory
    """
    if sound_name not in loaded_sounds:
        if sound_name in sound_files:
            sound_path = sound_files[sound_name]
            _check()
            file_ = WaveFile(sound_path)
            buffer_ = Buffer(file_)
            source = Sound(buffer_, True)
            loaded_sounds[sound_name] = buffer_
        else:
            raise ValueError("Archivo no encontrado")
    else:
        source = Sound(loaded_sounds[sound_name], True)
        
    return source

class Sound(Source):
    """
    
    """
    def __init__(self, buffer_, destroy_buffer):
        super().__init__(buffer_, destroy_buffer)
    def copy(self):
        return Sound(self.buffer, True)
    #def destroy(self):
    #    super.destroy()

    def linear_mov(self, final_point:tuple, steps:int, pause_time: float):
        """
        Move the source from source position to final_point in the number of steps

        Args:
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
        for step in range(steps):
            new_x = x_start + (step + 1) * x_step
            new_y = y_start + (step + 1) * y_step
            new_z = z_start + (step + 1) * z_step
        
            self.set_position((new_x, new_y, new_z))
            
            #print(self.position)
            time.sleep(pause_time) 
            #await asyncio.sleep(pause_time)
        self.set_position(final_point)  

    def rotate(self, center =(0,0,0), axis = 'x', angle_degrees = 90,  steps = 100):
        angle_rad = math.radians(angle_degrees)
        step_angle = angle_rad / steps

        x, y, z = self.position
        cx, cy, cz = center

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
            #await asyncio.sleep(0.1)

    def gain_up(self, value):
        self.set_gain(self.gain + (value * 0.01))

    def gain_down(self, value):
        self.set_gain(self.gain - (value * 0.01))

    def gain_up_soft(self, value, steps = 10):
        delta = value/steps
        while self.gain < 1 and value > 0 :
            self.set_gain(self.gain+(delta * 0.01))
            value -= delta

    def gain_down_soft(self, value, steps = 10):
        while self.gain > 0 and value > 0 :
            delta = value/steps
            self.set_gain(self.gain-(delta * 0.01))
            value -= delta



def wait_for_keypress():
    input("Presiona cualquier tecla para continuar...")


def get_path(dir):
    path = os.path.join(*dir)
    #os.path.abspath(path)
    return path 

def proximation(sound_name, stop,listener_position, sound_position, steps, time_alive, slow_stop, steps_alive):
    source = open_file(sound_name)
    source.set_position(sound_position)
    source.set_looping(True)
    source.set_gain(0.5)
    source.play()
    linear_thread = threading.Thread(target = source.linear_mov, args=(listener_position, steps, 0.5))
    gain_thread = threading.Thread(target = source.gain_up_soft, args = (50,))
    linear_thread.start()
    gain_thread.start()
    linear_thread.join()
    gain_thread.join()
    if stop == True:
        if slow_stop:
            fade_duration = time_alive/steps_alive
            for i in range(steps_alive):
                new_gain = source.gain * (1 - (i + 1) / steps_alive)
                source.set_gain(new_gain)
                time.sleep(fade_duration)
        else:
            source.stop()
            
def rotate(sound_name, stop, listener_position,  sound_position, axis, angle_degrees, steps, time_alive, slow_stop, steps_alive):
    source = open_file(sound_name)
    source.set_position(sound_position)
    source.set_looping(True)
    source.play()
    rotate_thread = threading.Thread(target= source.rotate, args=(listener_position, axis, angle_degrees, steps))
    rotate_thread.start()
    rotate_thread.join()
    if stop == True:
        if slow_stop:
            fade_duration = time_alive/steps_alive
            for i in range(steps_alive):
                new_gain = source.gain * (1 - (i + 1) / steps_alive)
                source.set_gain(new_gain)
                time.sleep(fade_duration)
        else:
            source.stop()

async def main():
    oalInit()
    device = alc.alcOpenDevice(None)
    context = alc.alcCreateContext(device, None)
    alc.alcMakeContextCurrent(context)

    sources = []
    manager = SoundManager(get_path(["resources","wav"]))
    sources.append(open_file('dripping-water-in-cave-mono'))
    #source = open_short('Psychosocial-mono')
    listener = oalGetListener()
    sources.append(open_file('bird-short'))
    sources.append(open_file('bottle_pop'))
    manager.list_sounds()
    for i in sources:
        print(i)

    sources[0].set_position((0,0,20))
    sources[1].set_position((-3,0,0))
    sources[2].set_position((-4,0,0))

    sources[0].set_looping(True)
    sources[1].set_looping(True)
    sources[2].set_looping(True)

    sources[0].set_gain(0.5)

    async def movement(source):
         await source.linear_mov((10,-10,-10),15,0.5)
         await source.linear_mov((0,0,0),5,0.5)
        
    for sound in sources:
        sound.play()
    #task3 = asyncio.create_task(sources[0].linear_mov((0,0,3),15,0.5))
    #task4 = asyncio.create_task(sources[0].gain_up_soft(50))
    task1 = asyncio.create_task(sources[1].rotate(listener.position, "y", -180, 100))
    #task2 = asyncio.create_task(movement(sources[2]))
    await task1
    #await task2
    #await task3
    #await task4
    for sound in sources:
        sound.set_looping(False)
    #pasa por atras
    #source.rotate(listener.position, "y", 90)
    #wait_for_keypress()
    #source.set_position((-10,0,0))
    #pasa por adelante
    #source.rotate(listener.position, "y", -90)

    oalQuit()
    alc.alcDestroyContext(context)
    alc.alcCloseDevice(device)

#if __name__ == "__main__":
#    asyncio.run(main())