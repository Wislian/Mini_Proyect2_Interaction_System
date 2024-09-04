import os

def clear_screen():
    # Verifica el sistema operativo
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Unix/Linux/MacOS
        os.system('clear')
