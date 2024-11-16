from os import system
from time import time, sleep
from random import choice
from unicurses import *
import msvcrt

colors = {
    1 : COLOR_CYAN,
    2 : COLOR_YELLOW,
    3 : COLOR_MAGENTA,
    4 : COLOR_WHITE,
    5 : COLOR_BLUE,
    6 : COLOR_RED,
    7 : COLOR_GREEN
}

bricks = {
    'Tétrimino I': [[1, 1, 1, 1]], 
    'Tétrimino O': [[2, 2], [2, 2]],
    'Tétrimino T': [[3, 3, 3], [0, 3, 0]],
    'Tétrimino L': [[4, 4, 4], [4, 0, 0]],
    'Tétrimino J': [[5, 5, 5], [0, 0, 5]],
    'Tétrimino Z': [[6, 6, 0], [0, 6, 6]],
    'Tétrimino S': [[0, 7, 7], [7, 7, 0]],
}

def rectangle(y1, x1, height, width):
    mvhline(y1, x1, 0, width)
    mvhline(y1 + height, x1, 0, width)
    mvvline(y1, x1, 0, height)
    mvvline(y1, x1+width, 0, height)
    mvaddch(y1, x1, ACS_ULCORNER)
    mvaddch(y1+height, x1, ACS_LLCORNER)
    mvaddch(y1, x1+width, ACS_URCORNER)
    mvaddch(y1+height, x1+width, ACS_LRCORNER)

loser_text = r"""
  _                         
 | |                        
 | |     ___  ___  ___ _ __ 
 | |    / _ \/ __|/ _ \ '__|
 | |___| (_) \__ \  __/ |   
 |______\___/|___/\___|_|   
"""



class Tetris:
    def __init__(self) -> None:
        self.grille = [[0 for _ in range(10)] for _ in range(20)]
        self.next_block = bricks[choice(list(bricks.keys()))]
        self.block = None
        self.pos = None
        self.run = True
        self.score = 0

    def print(self):
        for row in self.grille: 
            print('[', end=' ')
            for column in row:
                if column == 1:
                    print('#', end='')
                else:
                    print(' ', end='')
            print(']')
        print('\n')

    
    
    def new_print(self):
        for i in range(len(self.grille)):
            for j in range(len(self.grille[i])):
                obj = self.grille[i][j]
                if obj != 0:
                    attron(COLOR_PAIR(obj))
                    mvaddch(i + 2, j + 1, str(obj))
                    attroff(COLOR_PAIR(obj))
                else:
                    mvaddch(i + 2, j + 1, ' ')
        rectangle(1, 0, len(self.grille) + 1, len(self.grille[0]) + 1)

    def collision(self, position, forme):
        for y in range(len(forme)):
            for x in range(len(forme[y])):
                if self.grille[position[0] + y][position[1] + x] != 0:
                    if forme[y][x] != 0:
                        return True
        return False

    def del_forme(self, position, forme):
        for y in range(len(forme)):
            for x in range(len(forme[y])):
                if forme[y][x] != 0:
                    index_y = position[0] + y
                    index_x = position[1] + x
                    self.grille[index_y][index_x] = 0

    def add_forme(self, position, forme):
        color = None
        for y in forme:
            for x in y:
                if x!=0:
                    color = x
                    break
        for y in range(len(forme)):
            for x in range(len(forme[y])):
                if forme[y][x] != 0:
                    index_y = position[0] + y
                    index_x = position[1] + x
                    self.grille[index_y][index_x] = color

    def add_block(self):
        self.pos = [0, 3]
        self.block = self.next_block
        self.next_block = bricks[choice(list(bricks.keys()))]
        if not self.collision(self.pos, self.block):
            self.add_forme(self.pos, self.block)
            self.score +=10
        else:
            self.run = False
            
    # def pos_possible_la_plus_bas(self):
    #     if self.block is not None:
    #         temp_pos = self.pos.copy()
    #         self.del_forme(self.pos, self.block)
    #         while True:
    #             if temp_pos[0] > len(self.grille) - 3:
    #                 break
    #             if not self.collision(temp_pos, self.block):
    #                 temp_pos[0] += 1
    #             else:
    #                 break
    #         self.add_forme(self.pos, self.block)
    #         for i in range(len(self.block)):
    #             for j in range(len(self.block[i])):
    #                 obj = self.block[i][j]
    #                 if obj != 0:
    #                     mvaddch(i + 2 + temp_pos[0], j + 1 + temp_pos[1], '#')
    #                 else:
    #                     mvaddch(i + 2 + temp_pos[0], j + 1 + temp_pos[1], ' ')
            

    def update(self):
        if self.block is not None:
            if self.pos[0] + len(self.block) >= len(self.grille):
                self.block = None
                return    
            self.del_forme(self.pos, self.block)
            if not self.collision((self.pos[0] + 1, self.pos[1]), self.block):
                self.pos[0] += 1
                self.add_forme(self.pos, self.block)
            else:
                self.add_forme(self.pos, self.block)
                self.block = None
                self.check_full_line()
                self.add_block()

        else:
            self.check_full_line()
            self.add_block()

    def check_full_line(self):
        full_lines = []
        for i in range(len(self.grille)):
            count = 0
            for value in self.grille[i]:
                if value == 0:
                    count +=1
            if count == 0:
                full_lines.append(i)
        a = len(full_lines)
        match a:
            case 1:
                self.score += 40
            case 2:
                self.score += 100
            case 3:
                self.score += 300
            case 4:
                self.score += 1200
            case _:
                pass

        for line in full_lines:
            for j in range(line, 0, -1):
                self.grille[j] = self.grille[j - 1]
            self.grille[0] = [0 for _ in range(len(self.grille[0]))]

    def move_left(self):
        if self.block is not None:
            if self.pos[1] - 1 >= 0:
                self.del_forme(self.pos, self.block)
                if not self.collision((self.pos[0], self.pos[1] - 1), self.block):
                    self.pos[1] -= 1
                self.add_forme(self.pos, self.block)

    def move_right(self):
        if self.block is not None:
            if self.pos[1] < len(self.grille[0]) - len(self.block[0]):
                self.del_forme(self.pos, self.block)
                if not self.collision((self.pos[0], self.pos[1] + 1), self.block):
                    self.pos[1] += 1
                self.add_forme(self.pos, self.block)

    def move_down(self):
        if self.block is not None:
            if self.pos[0] + len(self.block) >= len(self.grille):
                self.block = None
                return    
            self.del_forme(self.pos, self.block)
            if not self.collision((self.pos[0] + 1, self.pos[1]), self.block):
                self.pos[0] += 1
                self.add_forme(self.pos, self.block)
            else:
                self.add_forme(self.pos, self.block)
                self.check_full_line()
                self.block = None
                self.add_block()

    def rotate(self):
        if self.block is not None:
            rotate_form = self.rotate_horaire(self.block)
            self.del_forme(self.pos, self.block)
            if self.pos[1] + len(rotate_form[0]) > len(self.grille[0]):
                pass
            elif not self.collision(self.pos, rotate_form):
                self.block = rotate_form
            self.add_forme(self.pos, self.block)

    def rotate_horaire(self, forme):
        rotated = [[0] * len(forme) for _ in range(len(forme[0]))]
        for i in range(len(forme)):
            for j in range(len(forme[0])):
                rotated[j][len(forme) - 1 - i] = forme[i][j]
        return rotated

    def draw_next_bloc(self, position, block):
        """
        (y, x)
        """
        for i in range(len(block)):
            for j in range(len(block[i])):
                obj = block[i][j]
                if obj != 0:
                    attron(COLOR_PAIR(obj))
                    mvaddch(i + position[1], j + position[0], str(obj))
                    attroff(COLOR_PAIR(obj))
                else:
                    mvaddch(i + position[1], j + position[0], ' ')

    def loop(self):
        stdscr = initscr()
        noecho()
        cbreak()
        curs_set(0)
        keypad(stdscr, True)
        start_color()
        init_pair(1, COLOR_RED, COLOR_RED)
        for key in colors.keys():
            init_pair(key, colors[key], colors[key])
        
        
        previous_time = time()
        while self.run:
            new_time = time()
            if new_time - previous_time > 1:
                previous_time = new_time
                self.update()
            if msvcrt.kbhit():
                k = getch()
                if k == KEY_LEFT:
                    self.move_left()
                elif k == KEY_RIGHT:
                    self.move_right()
                elif k == KEY_UP:
                    self.rotate()
                elif k == KEY_DOWN:
                    self.move_down()
            clear()
            mvaddstr(1, 13, "NEXT")
            rectangle(2, 12, 3, 5)
            self.draw_next_bloc((13, 3), self.next_block)
            mvaddstr(6, 13, "SCORE")
            mvaddstr(7, 13, str(self.score))
            self.new_print()
            # self.pos_possible_la_plus_bas()
            refresh()
            

        clear()
        move(0, 0)
        attron(A_BOLD)
        addstr(loser_text)
        attroff(A_BOLD)
        attron(A_DIM)
        addstr("        press any key")
        attroff(A_DIM)
        refresh()
        getch()
        clear()
        refresh()
        endwin()
        print("See you soon")

if __name__ == "__main__":
    t = Tetris()
    t.loop()
    
"""
a rajouter : 
si on appuie sur espace ça va direct tout en bas
aussi prechote la prochaine position
"""