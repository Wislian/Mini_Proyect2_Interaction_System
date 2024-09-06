import csv
import ast

import sound_functions

def parse_parameter(param):
    """
    Transform a string value to a correct type value
    """
    try:
        return ast.literal_eval(param)
    except (ValueError, SyntaxError):
        return param


def execute_action(function_name, params):

    """
    Take a string function_name and list of params, search it among all functions and execution it with their
    params
    """
    function = globals().get(function_name)
    if not function:
        function = getattr(sound_functions, function_name, None)
    if function:
        processed_params = [
            param if not isinstance(param, str) else parse_parameter(param.strip()) 
            for param in params
        ]
        function(*processed_params)
    else:
        print(f"Function '{function_name}' not found!")

def load_story(file_path):
    """
    Load information from .csv file to dict
    """
    story_nodes = {}
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cleaned_row = {key.strip(): value.strip() for key, value in row.items()}
            story_nodes[int(cleaned_row['node_id'])] = cleaned_row
    return story_nodes
