from os import system
from time import time, sleep
from random import choice
from unicurses import *
from msvcrt import kbhit
from constant import *
from utils import rectangle



class Tetris:
    def __init__(self) -> None:
        self.grille = [[0 for _ in range(10)] for _ in range(20)]
        self.next_block = bricks[choice(list(bricks.keys()))]
        self.block = None
        self.pos = None
        self.run = True
        self.score = 0
        
        self.first_block = True # pas trouvé d'autre soltion
    
    def print_grille(self):
        for y, row in enumerate(self.grille):
            for x, value in enumerate(row):
                if value:
                    attron(COLOR_PAIR(value))
                    mvaddch(y + 2, x + 1, " ")
                    attroff(COLOR_PAIR(value))
        rectangle(1, 0, len(self.grille) + 1, len(self.grille[0]) + 1)

    def collision(self, position, forme):
        for y in range(len(forme)):
            for x in range(len(forme[y])):
                if forme[y][x]:
                    grid_y = position[0] + y
                    grid_x = position[1] + x
                    if grid_y < 0 or grid_y >= len(self.grille) or grid_x < 0 or grid_x >= len(self.grille[0]):
                        return True
                    if self.grille[grid_y][grid_x]:
                        return True
        return False

    def add_forme(self, position, forme):
        for y, row in enumerate(forme):
            for x, value in enumerate(row):
                if value:
                    self.grille[position[0] + y][position[1] + x] = value

    def del_forme(self, position, forme):
        for y, row in enumerate(forme):
            for x, value in enumerate(row):
                if value:
                    self.grille[position[0] + y][position[1] + x] = 0

    def add_block(self):
        self.pos = [0, 3]
        self.block = self.next_block
        self.next_block = bricks[choice(list(bricks.keys()))]
        if not self.collision(self.pos, self.block):
            self.add_forme(self.pos, self.block)
            if self.first_block:
                self.first_block = False
            else:
                self.score +=10
        else:
            self.run = False
       
    """     
    # def pos_possible_la_plus_bas(self):
    #     if self.block is not None:
    #         temp_pos = self.pos.copy()
    #         self.del_forme(self.pos, self.block)
    #         while True:
    #             temp_pos[0] += 1
    #             if temp_pos[0] > len(self.grille) - 3:
    #                 temp_pos[0] -= 1 
    #                 break
    #             elif not self.collision(temp_pos, self.block):
    #                 pass
    #             else:
    #                 temp_pos[0] -= 1 
    #                 break
    #         self.add_forme(self.pos, self.block)
    #         for i in range(len(self.block)):
    #             for j in range(len(self.block[i])):
    #                 obj = self.block[i][j]
                    
    #                 if obj != 0:
    #                     mvaddch(i + 2 + temp_pos[0], j + 1 + temp_pos[1], '#')
    #         return temp_pos[0] + len(self.block[0])
    #     return 0
    """
            
    def update(self):
        if self.block:
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

    def update_score(self, nbr_full_line):
        match nbr_full_line:
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

    def check_full_line(self):
        full_lines = []
        for i in range(len(self.grille)):
            if self.grille[i].count(0) == 0:
                full_lines.append(i)
        self.update_score(len(full_lines))        

        for line in full_lines:
            for j in range(line, 0, -1):
                self.grille[j] = self.grille[j - 1]
            self.grille[0] = [0 for _ in range(len(self.grille[0]))]

    def move_left(self):
        if self.block:
            if self.pos[1] - 1 >= 0:
                self.del_forme(self.pos, self.block)
                if not self.collision((self.pos[0], self.pos[1] - 1), self.block):
                    self.pos[1] -= 1
                self.add_forme(self.pos, self.block)

    def move_right(self):
        if self.block:
            if self.pos[1] < len(self.grille[0]) - len(self.block[0]):
                self.del_forme(self.pos, self.block)
                if not self.collision((self.pos[0], self.pos[1] + 1), self.block):
                    self.pos[1] += 1
                self.add_forme(self.pos, self.block)

    def move_down(self):
        if self.block:
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
        if self.block:
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
        for y, row in enumerate(block):
            for x, value in enumerate(row):
                if value:
                    attron(COLOR_PAIR(value))
                    mvaddch(y + position[1], x + position[0], " ")
                    attroff(COLOR_PAIR(value))

    def init_display(self):
        stdscr = initscr()
        noecho()
        cbreak()
        curs_set(0)
        keypad(stdscr, True)
        start_color()
        init_pair(1, COLOR_RED, COLOR_RED)
        for key in colors.keys():
            init_pair(key, colors[key], colors[key])

    def close_display(self):
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

    def check_input(self):
        if kbhit():
            k = getch()
            if k == KEY_LEFT:
                self.move_left()
            elif k == KEY_RIGHT:
                self.move_right()
            elif k == KEY_UP:
                self.rotate()
            elif k == KEY_DOWN:
                self.move_down()
    
    def print_info(self):
        mvaddstr(1, 13, "NEXT")
        rectangle(2, 12, 3, 5)
        self.draw_next_bloc((13, 3), self.next_block)
        mvaddstr(6, 13, "SCORE")
        mvaddstr(7, 13, str(self.score))
        
    def loop(self):
        self.init_display()
        
        previous_time = time()
        while self.run:
            new_time = time()
            if new_time - previous_time > 1:
                previous_time = new_time
                self.update()
                
            self.check_input()
            
            clear()
            self.print_info()
            self.print_grille()
            refresh()
            

        self.close_display()

if __name__ == "__main__":
    t = Tetris()
    t.loop()
    
"""
a rajouter : 
- si on appuie sur espace ça va direct tout en bas
- aussi prechote la prochaine position
"""