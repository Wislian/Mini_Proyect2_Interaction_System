import csv


def load_story(file_path):
    story_nodes = {}
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cleaned_row = {key.strip(): value.strip() for key, value in row.items()}
            story_nodes[int(cleaned_row['node_id'])] = cleaned_row
    return story_nodes

