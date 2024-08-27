from openal import *
import time
import math

# Inicialización de OpenAL
device = oalOpenDevice(None)  # Abre el dispositivo por defecto
if device:
    context = oalCreateContext(device)  # Crea un contexto
    if context:
        oalMakeContextCurrent(context)  # Hace el contexto actual
    else:
        print("Error al crear el contexto")
else:
    print("Error al abrir el dispositivo de audio")

# Cargar el archivo de sonido
sound = oalOpen("sound.wav")
sound.set_looping(True)  # Hacer que el sonido se reproduzca en bucle

# Configuración inicial del oyente
listener_pos = [0.0, 0.0, 0.0]  # Posición inicial del oyente
listener_angle = 0.0  # Ángulo inicial del oyente

alListener3f(AL_POSITION, *listener_pos)  # Posición inicial del oyente

direction_vect = [
    math.sin(listener_angle), 0.0, math.cos(listener_angle),  # Orientación del oyente
    0.0, 1.0, 0.0  # Vector "arriba" del oyente
]
alListenerfv(AL_ORIENTATION, direction_vect)

# Configuración de la fuente de sonido
sound_source = sound.source
sound_source.set_position(0.0, 0.0, -5.0)  # Coloca la fuente a 5 unidades por detrás del oyente

# Reproducir el sonido
sound.play()

def update_listener():
    global listener_angle

    # Movimiento del oyente en un círculo alrededor de la fuente de sonido
    listener_pos[0] = 5.0 * math.sin(listener_angle)
    listener_pos[2] = 5.0 * math.cos(listener_angle)
    listener_angle += 0.05  # Incrementa el ángulo para simular movimiento

    # Actualizar posición del oyente en OpenAL
    alListener3f(AL_POSITION, *listener_pos)

    # Actualizar la orientación del oyente
    direction_vect[0] = -math.sin(listener_angle)
    direction_vect[2] = -math.cos(listener_angle)
    alListenerfv(AL_ORIENTATION, direction_vect)

# Bucle de procesamiento
try:
    while True:
        update_listener()
        time.sleep(0.01)  # Controla la velocidad del bucle
except KeyboardInterrupt:
    pass  # Permite salir del bucle con Ctrl+C

# Limpiar
sound.stop()
oalQuit()
