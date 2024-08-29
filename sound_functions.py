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


    def rotate(self, center_point, radius, speed, duration, tilt_angle=0):
        """
        Rota una fuente alrededor de un punto central en un círculo de radio 'radius', 
        permitiendo una inclinación adicional en el eje Y.

        :param source: Objeto fuente que se moverá (debe tener un método set_position).
        :param center_point: Punto alrededor del cual girará la fuente, en formato (x, y, z).
        :param radius: Radio del círculo alrededor del punto central.
        :param speed: Velocidad de rotación en grados por segundo.
        :param duration: Duración total de la rotación en segundos.
        :param tilt_angle: Ángulo de inclinación alrededor del eje Y en grados (opcional).
        """
        angle_step = speed * 0.1  # Incremento del ángulo para cada actualización
        start_time = time.time()
        self.set_looping(True)
        while time.time() - start_time < duration:
            elapsed_time = time.time() - start_time
            angle = (elapsed_time * speed) % 360
            rad = math.radians(angle)
            
            # Calcula la nueva posición de la fuente
            x_center, y_center, z_center = center_point
            
            # Posición en el plano XY después de la rotación
            x = x_center + radius * math.cos(rad)
            z = z_center + radius * math.sin(rad)
            
            # Si se desea una inclinación en el eje Y
            if tilt_angle != 0:
                # Calcula la nueva posición y la inclinación
                tilt_rad = math.radians(tilt_angle)
                y = y_center + radius * math.sin(tilt_rad)
            else:
                y = y_center
            
            self.set_position((x, y, z))
            
            time.sleep(0.1)  # Espera para permitir la actualización visual del cambio en la posición
            print(f"Fuente en posición: ({x:.2f}, {y:.2f}, {z:.2f})")
        
        self.set_looping(False)


    def rotate(self, center_point, initial_position, axis, speed, duration, direction='clockwise'):
        """
        Rota una fuente alrededor de un punto central en un círculo sobre un eje especificado.

        :param source: Objeto fuente que se moverá (debe tener un método set_position).
        :param center_point: Punto alrededor del cual girará la fuente, en formato (x, y, z).
        :param initial_position: Posición inicial de la fuente, en formato (x, y, z).
        :param axis: Eje alrededor del cual girará la fuente ('x', 'y' o 'z').
        :param speed: Velocidad de rotación en grados por segundo.
        :param duration: Duración total de la rotación en segundos.
        :param direction: Dirección de la rotación ('clockwise' para horario, 'counterclockwise' para antihorario).
        """
        if direction not in ['clockwise', 'counterclockwise']:
            raise ValueError("direction debe ser 'clockwise' o 'counterclockwise'")
        
        angle_step = speed * 0.1  # Incremento del ángulo para cada actualización
        start_time = time.time()
        
        # Definir el sentido de rotación
        direction_multiplier = -1 if direction == 'clockwise' else 1
        self.play()
        self.set_looping(True)
        while time.time() - start_time < duration:
            elapsed_time = time.time() - start_time
            angle = (elapsed_time * speed * direction_multiplier) % 360
            print(angle)
            rad = math.radians(angle)
            
            # Obtén las coordenadas iniciales
            x0, y0, z0 = initial_position
            cx, cy, cz = center_point
            
            if axis == 'x':
                # Rotación alrededor del eje X
                y = cy + (y0 - cy) * math.cos(rad) - (z0 - cz) * math.sin(rad)
                z = cz + (y0 - cy) * math.sin(rad) + (z0 - cz) * math.cos(rad)
                x = x0
            elif axis == 'y':
                # Rotación alrededor del eje Y
                x = cx + (x0 - cx) * math.cos(rad) + (z0 - cz) * math.sin(rad)
                y = y0
                z = cz - (x0 - cx) * math.sin(rad) + (z0 - cz) * math.cos(rad)
            elif axis == 'z':
                # Rotación alrededor del eje Z
                x = cx + (x0 - cx) * math.cos(rad) - (y0 - cy) * math.sin(rad)
                y = cy + (x0 - cx) * math.sin(rad) + (y0 - cy) * math.cos(rad)
                z = z0
            else:
                raise ValueError("axis debe ser 'x', 'y' o 'z'")
            
            self.set_position((x, y, z))
            
            time.sleep(0.1)  # Espera para permitir la actualización visual del cambio en la posición
            print(f"Fuente en posición: ({x:.2f}, {y:.2f}, {z:.2f})")
        
        self.set_looping(False)

    def rotate2(self, center_point, initial_position, axis, speed, duration, angle_range:float, direction='clockwise'):
        """
        Rota una fuente alrededor de un punto central en un círculo sobre un eje especificado y grafica las posiciones en tiempo real.

        :param center_point: Punto alrededor del cual girará la fuente, en formato (x, y, z).
        :param initial_position: Posición inicial de la fuente, en formato (x, y, z).
        :param axis: Eje alrededor del cual girará la fuente ('x', 'y' o 'z').
        :param speed: Velocidad de rotación en grados por segundo.
        :param duration: Duración total de la rotación en segundos.
        :param angle_range: Ángulo máximo de rotación en grados.
        :param direction: Dirección de la rotación ('clockwise' para horario, 'counterclockwise' para antihorario).
        """
        if direction not in ['clockwise', 'counterclockwise']:
            raise ValueError("direction debe ser 'clockwise' o 'counterclockwise'")
        
        if angle_range <= 0:
            raise ValueError("angle_range debe ser positivo")
        
        angle_step = speed * 0.1  # Incremento del ángulo para cada actualización
        start_time = time.time()
        
        # Definir el sentido de rotación
        direction_multiplier = -1 if direction == 'clockwise' else 1

        cx, cy, cz = center_point
        self.play()
        self.set_looping(True)
        if direction != 'clockwise':
            limit = 360 - angle_range
        else:
            limit = angle_range
        while time.time() - start_time < duration:
            elapsed_time = time.time() - start_time
            angle = (elapsed_time * speed * direction_multiplier) % 360
            print(angle)

            if (direction == 'clockwise'):
                if angle >= limit:
                    break
            else:
                if angle <=limit:
                    break

            rad = math.radians(angle)
            
            # Obtén las coordenadas iniciales
            x0, y0, z0 = initial_position
            
            if axis == 'x':
                # Rotación alrededor del eje X
                y = cy + (y0 - cy) * math.cos(rad) - (z0 - cz) * math.sin(rad)
                z = cz + (y0 - cy) * math.sin(rad) + (z0 - cz) * math.cos(rad)
                x = x0
            elif axis == 'y':
                # Rotación alrededor del eje Y
                x = cx + (x0 - cx) * math.cos(rad) + (z0 - cz) * math.sin(rad)
                y = y0
                z = cz - (x0 - cx) * math.sin(rad) + (z0 - cz) * math.cos(rad)
            elif axis == 'z':
                # Rotación alrededor del eje Z
                x = cx + (x0 - cx) * math.cos(rad) - (y0 - cy) * math.sin(rad)
                y = cy + (x0 - cx) * math.sin(rad) + (y0 - cy) * math.cos(rad)
                z = z0
            else:
                raise ValueError("axis debe ser 'x', 'y' o 'z'")
            
            self.set_position((x, y, z))
            
            print(f"Fuente en posición: ({x:.2f}, {y:.2f}, {z:.2f})")
        
        self.set_looping(False)

def wait_for_keypress():
    input("Presiona cualquier tecla para continuar...")


device = alc.alcOpenDevice(None)
context = alc.alcCreateContext(device, None)
alc.alcMakeContextCurrent(context)

manager = SoundManager('resources/wav')
source = open_short('bottle_pop')
listener = oalGetListener()

source.set_position((-10,10,10))
#source.linear_mov(source.position,(10,-10,-10),15,0.5)
#source.linear_mov(source.position,(0,0,0),5,0.5)
#source.rotate(listener.position, 10, 20, 10, 15)
#source.rotate(listener.position, source.position, "y", 20, 20, 90, "clockwise")
source.rotate2(listener.position, source.position, "y", 20, 20, angle_range= 180)
wait_for_keypress()
print('CAmbio de sentido')
source.rotate(listener.position, source.position, "x", 20, 20, "counterclockwise")
print('Cambio de sentido')
source.rotate(listener.position, source.position, "y", 20, 20, "clockwise")
print('CAmbio de sentido')
source.rotate(listener.position, source.position, "y", 20, 20, "counterclockwise")

print('cambio de sentido')
source.rotate(listener.position, source.position, "z", 20, 20, "clockwise")
print('CAmbio de sentido')
source.rotate(listener.position, source.position, "z", 20, 20, "counterclockwise")


oalQuit()
alc.alcDestroyContext(context)
alc.alcCloseDevice(device)