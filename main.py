from sound_functions import *
from type_functions import *
import keyboard
from csv_reader import *
from util import *
import sys
import multiprocessing


def main():
    manager = multiprocessing.Manager()
    shared_data = manager.dict()
    init(shared_data)
    sound_task_queue = multiprocessing.Queue()
    sound_process = multiprocessing.Process(target = sound_worker, args=(sound_task_queue, shared_data))
    sound_process.start()
    story_nodes = load_story(get_path(["resources", "story","story.csv"]))
    #print(story_nodes)
    current_node = 1
    while True:
        #source = open_file('bomb', shared_data)
        #source.play()
        func, params = execute_action(story_nodes[current_node]['function'], story_nodes[current_node]["function_parameters"])
        params.append(shared_data)
        sound_task_queue.put((func, params))
        #sound_task_queue.put((execute_action(story_nodes[current_node]['function'], story_nodes[current_node]['function_parameters'])))
        lines = story_nodes[current_node]['text'].split('.')
        print_w(lines[0])
        print_typing(lines[1])
        band = 0 
        if story_nodes[current_node]['story_options'] != '':
            options = story_nodes[current_node]['story_options'].split('/')
            print(options)
            op1, op2 = options[0].split(' '), options[1].split(' ')
            print(f"{op1[0]}. {op1[1]}")
            print(f"{op2[0]}. {op2[1]}")
            
            clear_buffer()
            while band == 0:

                if keyboard.is_pressed('1'):
                    print(f'se presiono 1 {op1[2]}')
                    current_node = op1[2]
                    band = 1
                elif keyboard.is_pressed('2'):
                    print(f'se presiono 2 {op2[2]}')
                    current_node = op1[2]
                    band = 2
        else:
            clear_buffer()
            keyboard.read_event()
            print('continua')
            current_node = 2



        clear_buffer()

    clear_buffer()
    keyboard.read_event()
    clear_buffer()
    


async def main2():

    sources[0].set_position((0,0,20))
    sources[1].set_position((-3,0,0))
    sources[2].set_position((-4,0,0))

    sources[0].set_looping(True)
    sources[1].set_looping(True)
    sources[2].set_looping(True)

    sources[0].set_gain(0.5)

    async def movement(source):
         await source.linear_mov((10,-10,-10),15,0.5)
         await source.linear_mov((0,0,0),5,0.5)
        
    for sound in sources:
        sound.play()
    task3 = asyncio.create_task(sources[0].linear_mov((0,0,3),15,0.5))
    task4 = asyncio.create_task(sources[0].gain_up_soft(50))
    task1 = asyncio.create_task(sources[1].rotate2(listener.position, "y", -90, 100))
    task2 = asyncio.create_task(movement(sources[2]))
    await task1
    await task2
    await task3
    await task4
    for sound in sources:
        sound.set_looping(False)
    #pasa por atras
    #source.rotate(listener.position, "y", 90)
    #wait_for_keypress()
    #source.set_position((-10,0,0))
    #pasa por adelante
    #source.rotate(listener.position, "y", -90)

    oalQuit()
    alc.alcDestroyContext(context)
    alc.alcCloseDevice(device)

if __name__ == "__main__":
    main()