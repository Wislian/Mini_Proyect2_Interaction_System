import math
from openal import *
import time
from pydub import AudioSegment

def get_audio_duration(filename):
    audio = AudioSegment.from_file(filename)
    return len(audio)/1000.0
# Inicializa el dispositivo de audio y el contexto
device = alc.alcOpenDevice(None)
if not device:
    print("Error al abrir el dispositivo de audio.")
    exit(1)

context = alc.alcCreateContext(device, None)
alc.alcMakeContextCurrent(context)

# Cargar el sonido y obtener el oyente
source = oalOpen('wav/Psychosocial-mono.wav')
duration = get_audio_duration('wav/Psychosocial-mono.wav')
listener = oalGetListener()

# 1. Simulación de acercamiento de pasos hacia el oyente
print("Simulación de acercamiento de pasos hacia el oyente...")
 # Comienza lejos
source.set_gain(0.50)
steps = 10
step_duration = duration/steps
print(duration, step_duration)
# Acercar la fuente al oyente
source.set_position((0, 10, 0))  # Coloca la fuente en frente del oyente
source.play()

# Parámetros para la rotación
radius = 10  # Radio del círculo alrededor del oyente
speed = 10    # Velocidad de rotación en grados por segundo
duration = 10 # Duración total de la rotación en segundos
angle_step = speed * 0.1  # Incremento del ángulo para cada actualización

start_time = time.time()
while time.time() - start_time < duration:
    elapsed_time = time.time() - start_time
    angle = (elapsed_time * speed) % 360
    rad = math.radians(angle)
    
    # Calcula la nueva posición de la fuente
    x = radius * math.cos(rad)
    z = radius * math.sin(rad)
    source.set_position((x, 0, z))
    
    time.sleep(0.1)  # Espera para permitir la actualización visual del cambio en la posición
    print(f"Fuente en posición: ({x:.2f}, 0, {z:.2f})")
source.set_looping(False)
# Esperar a que termine la reproducción
while source.get_state() == AL_PLAYING:
    time.sleep(1)

# Limpiar recursos
oalQuit()
alc.alcDestroyContext(context)
alc.alcCloseDevice(device)
