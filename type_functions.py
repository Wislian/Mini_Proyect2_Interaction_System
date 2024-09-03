import textwrap
import time

line_lenth = 40

def print_typing(text, delay = 0.1):
    wrapped_text = textwrap.fill(text, width = line_lenth)
    for char in wrapped_text:
        print(char, end='', flush = True)
        time.sleep(delay)
    print()

def print_w(text):
    wrapped_text = textwrap.fill(text, width = line_lenth)
    print(wrapped_text)

