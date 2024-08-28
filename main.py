from sound_functions import *
from text_reader import *


def main():
    sounds_path = '/resources/wav'
    story_path = '/resources/story'

    story_lines = read_story(story_path)

    for line in story_lines:
        print(line)
        #any sound function

if __name__ == '__main__':
    main()
