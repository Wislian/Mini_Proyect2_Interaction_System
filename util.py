import os
import ast
import sound_functions
from openal import *

def parse_parameter(param):
    try:
        return ast.literal_eval(param)
    except (ValueError, SyntaxError):
        return param

def execute_action2(function_name, params_str):
    function = globals().get(function_name) or globals().get(f"sound_functions.{function_name}")
    if function:
        params = [parse_parameter(param.strip()) for param in params_str.split(' ')]
        print(params)
        function(*params)
    else:
        print(f"Function '{function_name}' not found!")

def execute_action(function_name, params_str):
    function = globals().get(function_name)
    if not function:
        function = getattr(sound_functions, function_name, None)
    if function:
        params = [parse_parameter(param.strip()) for param in params_str.split(' ')]
        #print(params)
        #function(*params)
        return function, params
    else:
        print(f"Function '{function_name}' not found!")


def get_path(dir):
    path = os.path.join(*dir)
    #os.path.abspath(path)
    return path 

def build_path(path, sound_name):
    file_path = os.path.join([path, f'{sound_name}.wav'])
    return file_path

def fill_path_sound_files(path, shared_data) -> None:
    """
    Fill the sound_files dictionary with sound names and file paths
    """
    sound_files = {}
    try:
        for file_name in os.listdir(path):
            sound_name = os.path.splitext(file_name)[0]
            file_path = os.path.join(path, file_name)
            sound_files[sound_name] = file_path
            shared_data['sound_files'] = sound_files
            shared_data['loaded_sounds'] = {}
    except FileNotFoundError:
        print(f"Error: no se encontro el directorio {path}")
    except Exception as e:
        print(f"Error inesperado o de nisvia: {e}")  
    print('entro')

def clear_buffer():
    sys.stdout.flush()

