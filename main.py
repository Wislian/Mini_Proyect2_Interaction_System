from sound_functions import *
from csv_reader import *
from type_functions import *
from utils import clear_screen


END_NODE = 0
def main():
    oalInit()
    device = alc.alcOpenDevice(None)
    context = alc.alcCreateContext(device, None)
    alc.alcMakeContextCurrent(context)
    fill_path_sound_files(get_path(["resources","wav"]))
    listener = oalGetListener()
    story_nodes = load_story(get_path(["resources","story","story.csv"]))
    current_node = 1
    threads= []
    try:
        input("Enter to start")
        while current_node != END_NODE:

            options = story_nodes[current_node]['story_options'].split('/')
            func, params = story_nodes[current_node]['function'], story_nodes[current_node]['function_parameters'] 
            
            if func == "Exit":
                time.sleep(8)
                current_node = END_NODE

            elif func =="Text":
                lines = story_nodes[current_node]['text'].split('.')
                #clear_screen()
                print_w(lines[1])
                print_typing(lines[0])
                time.sleep(1)
                threads.clear()
                current_node += 1

            elif func == "Decision":
                lines = story_nodes[current_node]['text'].split('.')
                #clear_screen()
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
                        current_node = int(op1[2])
                    elif option == 2:
                        current_node = int(op2[2])
                    elif options == 0:
                        for thread in threads:
                            thread.join()
                threads.clear()

            else:
                params = params.split()
                if func == "change_listener_orientation":
                    params.insert(0,listener)
                time.sleep(int(story_nodes[current_node]["time_until_play"]))
                thread = threading.Thread(target = execute_action, args=(func, params))
                threads.append(thread)
                current_node += 1
                thread.start() 
    finally:
        for thread in threads:
            thread.join()
        oalQuit()
        print('Exit.............')
if __name__ == '__main__':
    main()
