from unicurses import *

def rectangle(y1, x1, height, width):
    mvhline(y1, x1, 0, width)
    mvhline(y1 + height, x1, 0, width)
    mvvline(y1, x1, 0, height)
    mvvline(y1, x1+width, 0, height)
    mvaddch(y1, x1, ACS_ULCORNER)
    mvaddch(y1+height, x1, ACS_LLCORNER)
    mvaddch(y1, x1+width, ACS_URCORNER)
    mvaddch(y1+height, x1+width, ACS_LRCORNER)