import csv
import ast

def parse_parameter(param):
    try:
        return ast.literal_eval(param)
    except (ValueError, SyntaxError):
        return param


def execute_action(function_name, params_str):
    function = globals().get(function_name)
    #if not function:
    #   function = getattr(sound_functions, function_name, None)
    if function:
        params = [parse_parameter(param.strip()) for param in params_str.split(' ')]
        #print(params)
        #function(*params)
        return function, params
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

