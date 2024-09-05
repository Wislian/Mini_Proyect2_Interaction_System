from sound_functions import *
from csv_reader import *
from type_functions import *
from utils import clear_screen

def main():
    oalInit()
    device = alc.alcOpenDevice(None)
    context = alc.alcCreateContext(device, None)
    alc.alcMakeContextCurrent(context)
    manager = SoundManager(get_path(["resources","wav"]))
    listener = oalGetListener()
    story_nodes = load_story(get_path(["resources","story","story.csv"]))
    current_node = 1
    threads= []
    print(story_nodes)
    input()
    while current_node != 0:
        print(current_node)
        print(story_nodes[current_node])
        options = story_nodes[current_node]['story_options'].split('/')
        func, params = story_nodes[current_node]['function'], story_nodes[current_node]['function_parameters'] 
        
        if func != "Decision" and func != "Text":
            if options[0] =='task':
                params = params.split()
                if func == "change_listener_orientation":
                    params.insert(0,listener)
                print(params)
                time.sleep(int(story_nodes[current_node]["time_until_play"]))
                #func_exe, params_exe = execute_action(func, params)
                #thread = threading.Thread(target=func_exe, args=(params_exe))
                thread = threading.Thread(target = execute_action, args=(func, params))
                threads.append(thread)
                current_node += 1
                thread.start()
            #time.sleep(2)
        elif func =="Text":
            lines = story_nodes[current_node]['text'].split('.')
            clear_screen()
            print_w(lines[1])
            print_typing(lines[0])
            time.sleep(1)
            threads.clear()
            current_node += 1
        else:
            lines = story_nodes[current_node]['text'].split('.')
            clear_screen()
            print_w(lines[0])
            print_typing(lines[1])
            time.sleep(1)
            op1, op2 = options[0].split(' '), options[1].split(" ")
            option = -1
            print(f"1. {op1[1]}")
            print(f"2. {op2[1]}")
            while option != 1 and option != 2:
                option = int(input("---"))
                if option == 1:
                    print(f'se presiono 1 {op1[2]}')
                    current_node = int(op1[2])
                elif option == 2:
                    print(f'se presiono 2 {op2[2]}')
                    current_node = int(op2[2])
                elif options == 0:
                    for thread in threads:
                        thread.join()
            threads.clear()
    print('Exit.............')
    alc.alcMakeContextCurrent(None)
    alc.alcDestroyContext(context)
    alc.alcCloseDevice(device)
if __name__ == '__main__':
    main()
