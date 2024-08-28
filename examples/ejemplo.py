import time
from openal import *

# Inicializar dispositivo y contexto
device = alc.alcOpenDevice(None)
context = alc.alcCreateContext(device, None)
alc.alcMakeContextCurrent(context)

# Cargar el sonido y configurar el oyente
source = oalOpen('wav/dripping-water-in-cave-mono.wav')
listener = oalGetListener()
listener.set_position((0, 0, 0))
listener.set_orientation((0, 0, -1, 0, 1, 0))  # Mirando hacia adelante

# Configuración de la fuente de sonido
source.set_position((-10, 0, 0))  # Comienza a la izquierda
source.set_gain(1.0)
source.set_rolloff_factor(1.0)

# Reproducir sonido
source.play()

# Mover la fuente lentamente de izquierda a derecha
for x in range(-10, 11):
    source.set_position((x, 0, 0))
    time.sleep(1)
    print(f"Fuente en posición: {x}")

# Esperar a que termine la reproducción
while source.get_state() == AL_PLAYING:
    time.sleep(1)

# Limpiar
alc.alcDestroyContext(context)
alc.alcCloseDevice(device)
