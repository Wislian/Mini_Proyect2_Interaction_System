import csv




def execute_action(function_name, params):
    function = globals().get(function_name)
    if function:
        function(*params)
    else:
        print(f"Function '{function_name}' not found!")

def load_story(file_path):
    with open(file_path, mode = 'r', encoding = 'utf-8') as file:
        reader = csv.DictReader(file)
        story_nodes = {row['node_id']: row for row in reader}
    return story_nodes

