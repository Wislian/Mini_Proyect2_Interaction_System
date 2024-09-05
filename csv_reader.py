import csv
import ast

import sound_functions

def parse_parameter(param):
    try:
        return ast.literal_eval(param)
    except (ValueError, SyntaxError):
        return param


def execute_action(function_name, params):
    function = globals().get(function_name)
    if not function:
        function = getattr(sound_functions, function_name, None)
    if function:
        #params = [parse_parameter(param.strip()) for param in params_str.split(' ')]
        #function(*params)
        processed_params = [
            param if not isinstance(param, str) else parse_parameter(param.strip()) 
            for param in params
        ]
        function(*processed_params)
    else:
        print(f"Function '{function_name}' not found!")

def load_story(file_path):
    story_nodes = {}
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cleaned_row = {key.strip(): value.strip() for key, value in row.items()}
            story_nodes[int(cleaned_row['node_id'])] = cleaned_row
    return story_nodes

def load_story2(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        story = []
        for row in reader:
            # Filtrar filas con valores None
            cleaned_row = {
                key.strip() if key else key: value.strip() if value else value
                for key, value in row.items() if key is not None and value is not None
            }
            story.append(cleaned_row)
    return story

#print(load_story2(sound_functions.get_path(["resources","story","story.csv"])))