import math
import threading
from typing import Dict
from openal import *
from openal import _check
import time
import os

sound_files: Dict[str,str]= {}
loaded_sounds: Dict[str, any] = {}

def get_path(dir):
    path = os.path.join(*dir)
    return path

def fill_path_sound_files(path) -> None:
        try:
            for file_name in os.listdir(path):
                sound_name = os.path.splitext(file_name)[0]
                file_path = os.path.join(path, file_name)
                sound_files[sound_name] = file_path
        except FileNotFoundError:
            print(f"Error: File not found {path}")
        except Exception as e:
            print(f"Error inesperado or from nisvia: {e}")  

def open_file(sound_name:str):
    """
    Load a sound into memory
    """
    if sound_name in sound_files:
        sound_path = sound_files[sound_name]
        source = oalOpen(sound_path)
    return source


def linear_mov(source, final_point:tuple, steps:int, time_alive: float):
        """
        Move the source from source position to final_point in the number of steps

        Args:
            final_point: final position
            steps: number of times the sound is played between the trip
            time_alive: Time in play
        """
        if steps <= 0:
            raise ValueError("The number of steps has to be positive")

        pause_time = time_alive/steps

        x_start, y_start, z_start = source.position
        x_end, y_end, z_end = final_point
        
        x_step = (x_end - x_start) / steps
        y_step = (y_end - y_start) / steps
        z_step = (z_end - z_start) / steps

        for step in range(steps):

            new_x = x_start + (step + 1) * x_step
            new_y = y_start + (step + 1) * y_step
            new_z = z_start + (step + 1) * z_step
        
            source.set_position((new_x, new_y, new_z))

            time.sleep(pause_time) 

        source.set_position(final_point)  

def rotate_mov(source, center =(0,0,0), axis = 'x', angle_degrees = 90,  steps = 100, time_alive = 5):
    
    angle_rad = math.radians(angle_degrees)

    step_angle = angle_rad / steps
    pause_time = time_alive/steps

    x, y, z = source.position
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
            raise ValueError("Axis not valid. Use 'x', 'y' o 'z'.")

        x1 = x_translated +cx
        y1 = y_translated + cy
        z1 = z_translated + cz

        source.set_position((x1, y1, z1))

        time.sleep(pause_time)

def gain_up(source, value):
    source.set_gain(source.gain + (value * 0.01))

def gain_down(source, value):
    source.set_gain(source.gain - (value * 0.01))

def gain_up_soft(source, value, steps = 10):
    delta = value/steps
    while source.gain < 1 and value > 0 :
        source.set_gain(source.gain+(delta * 0.01))
        value -= delta
def gain_down_soft(source,time_stop):
    fade_duration = time_stop/100
    for i in range(100):
        new_gain = source.gain * (1 - (i + 1) / 100)
        source.set_gain(new_gain)
        time.sleep(fade_duration)


def proximation(sound_name, stop,listener_position, sound_position, steps, time_alive, slow_stop, time_stop):
    """
    Place a sound in a position in the plane and move it, increasing its volumen
    progressively as it approaches and can stop it slowly.  
    """
    source = open_file(sound_name)
    source.set_position(sound_position)
    source.set_gain(0.5)
    source.play()

    linear_thread = threading.Thread(target = linear_mov, args=(source, listener_position, steps, time_alive))
    gain_thread = threading.Thread(target = gain_up_soft, args = (source, 50))
    linear_thread.start()
    gain_thread.start()

    time.sleep(time_alive)

    if stop == True:
        if slow_stop:
            gain_down_soft(source, time_stop)
            source.stop()
        else:
            source.stop()
            
def rotate(sound_name, stop, listener_position,  sound_position, axis, angle_degrees, steps, time_alive, slow_stop, time_stop):
    """
    Place a sound in a position in the plane and rotate it around the given axis, and can stop it slowly.
    """
    source = open_file(sound_name)
    source.set_position(sound_position)
    source.play()

    rotate_mov(source, listener_position, axis, angle_degrees, steps, time_alive)

    if stop == True:
        if slow_stop:
            gain_down_soft(source, time_stop)
            source.stop()
        else:
            source.stop()

def change_listener_orientation(listener:Listener, direction, degrees, duration):
    """
    Change the orientation position with direction and degree.


    direction: direction to rotate ('up', 'down', 'right', 'left').
    degrees: degrees to rotate.
    duration: Time to do the rotation.
    """

    frontX, frontY, frontZ, upX, upY, upZ = listener.orientation
    radians = math.radians(degrees)

    steps = 100
    step_duration = duration / steps
    delta_radians = radians / steps

    for i in range(steps):
        if direction == 'right':

            new_frontX = frontX * math.cos(delta_radians) - frontZ * math.sin(delta_radians)
            new_frontZ = frontX * math.sin(delta_radians) + frontZ * math.cos(delta_radians)
            frontX, frontZ = new_frontX, new_frontZ

        elif direction == 'left':
            
            new_frontX = frontX * math.cos(-delta_radians) - frontZ * math.sin(-delta_radians)
            new_frontZ = frontX * math.sin(-delta_radians) + frontZ * math.cos(-delta_radians)
            frontX, frontZ = new_frontX, new_frontZ

        elif direction == 'up':
            
            new_frontY = frontY * math.cos(delta_radians) - frontZ * math.sin(delta_radians)
            new_frontZ = frontY * math.sin(delta_radians) + frontZ * math.cos(delta_radians)
            frontY, frontZ = new_frontY, new_frontZ

        elif direction == 'down':
            
            new_frontY = frontY * math.cos(-delta_radians) - frontZ * math.sin(-delta_radians)
            new_frontZ = frontY * math.sin(-delta_radians) + frontZ * math.cos(-delta_radians)
            frontY, frontZ = new_frontY, new_frontZ

        listener.set_orientation((frontX, frontY, frontZ, upX, upY, upZ))

        time.sleep(step_duration) 


def play(sound_name, sound_position):
    source = open_file(sound_name)
    source.set_position(sound_position)
    source.play()
