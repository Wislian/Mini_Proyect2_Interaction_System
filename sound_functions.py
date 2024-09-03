import math
import multiprocessing
from typing import Dict
from openal import *
from openal import _check
import time
import os
import threading
from util import fill_path_sound_files, get_path


def open_file(sound_name:str, shared_data):
    """
    Load a sound into memory
    """
    #print('este es el otro proceso')
    #print( shared_data['sound_files'])
    #print(shared_data['loaded_sounds'])
    if sound_name not in shared_data['loaded_sounds']:
        if sound_name in  shared_data['sound_files']:
            sound_path =  shared_data['sound_files'][sound_name]
            _check()
            file_ = WaveFile(sound_path)
            buffer_ = Buffer(file_)
            source = Sound(buffer_, True)
            shared_data['loaded_sounds'][sound_name] = buffer_
        else:
            raise ValueError("Archivo no encontrado")
    else:
        source = Sound(shared_data['loaded_sounds'][sound_name], True)
        
    return source

class Sound(Source):
    """
    
    """
    def __init__(self, buffer_, destroy_buffer):
        super().__init__(buffer_, destroy_buffer)
    def copy(self):
        return Sound(self.buffer, True)

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
        for step in range(steps):
            new_x = x_start + (step + 1) * x_step
            new_y = y_start + (step + 1) * y_step
            new_z = z_start + (step + 1) * z_step
        
            self.set_position((new_x, new_y, new_z))
            
            print(self.position)
            #await asyncio.sleep(pause_time)
        self.set_position(final_point)  

    def rotate(self, center, axis, angle_degrees,  steps = 100):
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



def play(sound_name, sound_position, stop = False):
    source = open_file(sound_name)
    source.set_position(sound_position)
    source.play()
    if stop == False:
        pass
        #await asyncio.sleep(0.1)
    return stop



def proximation_worker(sound_name, stop,listener_position, sound_position, steps, time_alive, slow_stop, steps_alive, shared_data):
        source = open_file(sound_name, shared_data)
        source.set_position(sound_position)
        source.set_looping(True)
        source.set_gain(0.5)
        source.play()
        def linear_mov():
            source.linear_mov(listener_position, steps, 0.5)
        def gain_up_soft():
            source.gain_up_soft(50)
        thread_1 = threading.Thread(target=linear_mov)
        thread_2 = threading.Thread(target=gain_up_soft)
        thread_1.start()
        thread_2.start()
        thread_1.join()
        thread_2.join()
        if stop == True:
            if slow_stop:
                fade_duration = time_alive/steps_alive
                for i in range(steps_alive):
                    new_gain = source.gain * (1 - (i + 1) / steps_alive)
                    source.set_gain(new_gain)
                    time.sleep(fade_duration)
        return stop
def proximation(sound_name, stop,listener_position, sound_position, steps, time_alive, slow_stop, steps_alive, shared_data):
    process = multiprocessing.Process(target = proximation_worker, args = (sound_name, stop,listener_position, sound_position, steps, time_alive, slow_stop, steps_alive, shared_data))
    process.start()

def rotate_worker(sound_name, stop,listener_position, sound_position, axis, angle_degrees, steps, time_alive, slow_stop, steps_alive, shared_data):
    source = open_file(sound_name, shared_data)
    source.set_position(sound_position)
    source.set_looping(True)
    source.play()
    #def rotate_in():
    source.rotate(listener_position, axis, angle_degrees, steps)
    #thread_1 = threading.Thread(target=rotate_in)
    #thread_1.start()
    if stop == True:
        if slow_stop:
            fade_duration = time_alive/steps_alive
            for i in range(steps_alive):
                new_gain = source.gain * (1 - (i + 1) / steps_alive)
                source.set_gain(new_gain)
                time.sleep(fade_duration)
    return stop

def rotate(sound_name, stop,listener_position, sound_position, axis, angle_degrees, steps, time_alive, slow_stop, steps_alive, shared_data):
    process = multiprocessing.Process(target=rotate_worker, args=(sound_name, stop,listener_position, sound_position, axis, angle_degrees, steps, time_alive, slow_stop, steps_alive, shared_data))
    process.start()

def change_listener_orientation(direction, degrees, duration):
    global listener
    """
    Rota al jugador en la dirección dada ('up', 'down', 'right', 'left').
    
    :param direction: String que representa la dirección ('up', 'down', 'right', 'left').
    :param degrees: Grados a rotar.
    :param duration: Duración de la rotación en segundos.
    """
    # Descomponemos la orientación actual y la dirección de "arriba"
    frontX, frontY, frontZ, upX, upY, upZ = listener.orientation
    
    # Convertimos grados a radianes
    radians = math.radians(degrees)

    # Calculamos el número de pasos para suavizar la rotación
    steps = 100
    step_duration = duration / steps
    delta_radians = radians / steps

    for i in range(steps):
        if direction == 'right':
            # Rotación alrededor del eje Y (hacia la derecha)
            new_frontX = frontX * math.cos(delta_radians) - frontZ * math.sin(delta_radians)
            new_frontZ = frontX * math.sin(delta_radians) + frontZ * math.cos(delta_radians)
            frontX, frontZ = new_frontX, new_frontZ
        elif direction == 'left':
            # Rotación alrededor del eje Y (hacia la izquierda, rotación inversa)
            new_frontX = frontX * math.cos(-delta_radians) - frontZ * math.sin(-delta_radians)
            new_frontZ = frontX * math.sin(-delta_radians) + frontZ * math.cos(-delta_radians)
            frontX, frontZ = new_frontX, new_frontZ
        elif direction == 'up':
            # Rotación alrededor del eje X (hacia arriba)
            new_frontY = frontY * math.cos(delta_radians) - frontZ * math.sin(delta_radians)
            new_frontZ = frontY * math.sin(delta_radians) + frontZ * math.cos(delta_radians)
            frontY, frontZ = new_frontY, new_frontZ
        elif direction == 'down':
            # Rotación alrededor del eje X (hacia abajo, rotación inversa)
            new_frontY = frontY * math.cos(-delta_radians) - frontZ * math.sin(-delta_radians)
            new_frontZ = frontY * math.sin(-delta_radians) + frontZ * math.cos(-delta_radians)
            frontY, frontZ = new_frontY, new_frontZ

        # Actualizamos la orientación
        listener.set_orientation((frontX, frontY, frontZ, upX, upY, upZ))

        # Esperamos el tiempo de un paso
        #await asyncio.sleep(step_duration) 

def init(shared_data):
    global listener
    oalInit()
    listener = oalGetListener()
    device = alc.alcOpenDevice(None)
    context = alc.alcCreateContext(device, None)
    alc.alcMakeContextCurrent(context)
    fill_path_sound_files(get_path(["resources","wav"]), shared_data)

def sound_worker(task_queue, shared_data):
    while True:
        task = task_queue.get()
        if task == "STOP":
            break
        function, args = task
        function(*args)