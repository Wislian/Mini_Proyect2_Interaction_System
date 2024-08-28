
def read_story(file_path):
    """
    Read the story from text file.

    Args:
        file_path (str): The path of the text file that has the story.

    Returns:
        list of str: List of lines of the story.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return [lines.strip() for line in lines]
