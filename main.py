from sound_functions import *
from csv_reader import *
import asyncio
from type_functions import *

async def main():
    oalInit()
    device = alc.alcOpenDevice(None)
    context = alc.alcCreateContext(device, None)
    alc.alcMakeContextCurrent(context)
    manager = SoundManager(get_path())
    listener = oalGetListener()
    story_nodes = load_story(get_path(["resources","story","story.csv"]))
    current_node = 1
    tasks = []
    while True:
        options = story_nodes[current_node]['story_options'].split('/')
        func, params = story_nodes[current_node]['function'], story_nodes[current_node]['function_parameters'] 
        if func != "Text":
            if options[0] =='task':

                task = asyncio.create_task(execute_action(func, params))
                tasks.append(task)
            else:
                pass
        else:
            await asyncio.gather(*tasks)
            lines = story_nodes[current_node]['text'].split('.')
            print_w(lines[0])
            print_typing(lines[1])
            op1, op2 = options[0].split(' '), options[1].split(" ")
            option = -1
            while option != 1 and option != 2:
                option = int(input("---"))
                if option == 1:
                    print(f'se presiono 1 {op1[2]}')
                    current_node = op1[2]
                elif option == 2:
                    print(f'se presiono 2 {op2[2]}')
                    current_node = op1[2]
            tasks.clear()
if __name__ == '__main__':
    asyncio.run(main())
