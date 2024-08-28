from pydub import AudioSegment

# Cargar el archivo de audio
audio = AudioSegment.from_file('wav/sound.wav')

# Verificar si es mono o estéreo
if audio.channels == 1:
    print("El archivo de audio es mono.")
elif audio.channels == 2:
    print("El archivo de audio es estéreo.")
else:
    print(f"El archivo de audio tiene {audio.channels} canales.")
