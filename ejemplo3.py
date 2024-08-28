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
source.set_position((100, 0, 0))  # Comienza lejos
source.set_gain(0.25)
source.play()
steps = 10
step_duration = duration/steps
print(duration, step_duration)
# Acercar la fuente al oyente
for x in range(10, 0,-1):
    source.set_position((x, 0, 0))
    #source.play()
    time.sleep(step_duration)  # Espera para escuchar el cambio en la posición
    print(f"Fuente en posición: {x}")

# Esperar a que termine la reproducción
while source.get_state() == AL_PLAYING:
    time.sleep(1)

# 2. Rotación del oyente durante la reproducción del sonido
print("Rotación del oyente mientras se reproduce el sonido...")
source.set_position((0, 0, 10))  # Coloca la fuente en frente del oyente
source.play()

# Cambiar la orientación del oyente
for angle in range(0, 360, 45):
    rad = angle * 3.14159 / 180
    listener.set_orientation((math.cos(rad), 0, -math.sin(rad), 0, 1, 0))  # Rotar en el plano horizontal
    source.play()
    time.sleep(0.5)
    print(f"Oyente orientado a {angle} grados")

# Esperar a que termine la reproducción
while source.get_state() == AL_PLAYING:
    time.sleep(1)

# 3. Ajuste de la velocidad del oyente (efecto Doppler)
print("Configurando la velocidad del oyente...")
listener.set_velocity((5, 0, 0))  # Movimiento rápido hacia adelante en el eje X
source.set_position((-10, 0, 0))  # Fuente detrás del oyente
for i in range(10):
    source.play()
    time.sleep(0.2)

# Esperar a que termine la reproducción
while source.get_state() == AL_PLAYING:
    time.sleep(1)

source.set_position((0, 10, 0))  # Coloca la fuente en frente del oyente
source.set_looping(True)
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
