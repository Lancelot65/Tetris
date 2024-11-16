
from keyboard import on_press_key
from os import system
from time import time, sleep
from random import choice

bricks = {
  'Tétrimino I': [[1, 1, 1, 1]],
  'Tétrimino O': [[1, 1], [1, 1]],
  'Tétrimino T': [[0, 1, 1, 1], [0, 0, 1, 0]],
  'Tétrimino L': [[1, 1, 1], [1, 0, 0]],
  'Tétrimino J': [[1, 1, 1], [0, 0, 1]],
  'Tétrimino Z': [[1, 1, 0], [0, 1, 1]],
  'Tétrimino S': [[0, 1, 1], [1, 1, 0]],
}

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
        self.grille = [[0 for _ in range(10)] for _ in range(10)]
        self.block = None
        self.pos = None
        
        
        on_press_key("gauche", self.move_left)
        on_press_key("droite", self.move_right)
        on_press_key("bas", self.move_down)
        on_press_key("up", self.rotate)

    
    def print(self):
        for row in self.grille: 
            print('[', end=' ')
            for column in row:
                if column == 1:
                    print('#', end=' ')
                else:
                    print(' ', end=' ')
            print(']')
        
        print('\n')
           
    def collision(self, position, forme):
        for y in range(len(forme)):
            for x in range(len(forme[y])):
                if self.grille[position[0] + y][position[1] + x] == 1:
                    if forme[y][x] == 1:
                        return True
        return False
    
    def del_forme(self, position, forme):
        for y in range(len(self.block)):
            for x in range(len(self.block[y])):
                if forme[y][x] == 1:
                    index_y = position[0] + y
                    index_x = position[1] + x
                    self.grille[index_y][index_x] = 0

    def add_forme(self, position, forme):
        for y in range(len(self.block)):
            for x in range(len(self.block[y])):
                if forme[y][x] == 1:
                    index_y = position[0] + y
                    index_x = position[1] + x
                    self.grille[index_y][index_x] = 1

    def add_block(self): # check si possible
        self.pos = [0, 3]
        self.block = bricks[choice(list(bricks.keys()))]
        if not self.collision(self.pos, self.block):
            for y in range(len(self.block)):
                for x in range(len(self.block[y])):
                    if self.block[y][x] == 1:
                        index_y = self.pos[0] + y
                        index_x = self.pos[1] + x
                        self.grille[index_y][index_x] = 1
        else:
            self.run = False

    def update(self):
        if self.block is not None:
            if self.pos[0] + len(self.block) + 1 > 10:
                self.block = None
                return    
            self.del_forme(self.pos, self.block)
            if not self.collision((self.pos[0] + 1, self.pos[1]), self.block):
                self.pos[0] +=1
                self.add_forme(self.pos, self.block)
            else:
                self.add_forme(self.pos, self.block)
                self.block = None
                self.check_full_line()
                self.add_block()
            
        else:
            self.add_block()
    
    def check_full_line(self):
        full_lines = []
        for i in range(len(self.grille)):
            if sum(self.grille[i]) == len(self.grille[0]):  # Check if the line is full
                full_lines.append(i)  # Store the index of the full line

        # Clear full lines and shift down
        for line in full_lines:
            for j in range(line, 0, -1):  # Move lines down
                self.grille[j] = self.grille[j - 1]
            self.grille[0] = [0 for _ in range(len(self.grille[0]))] 
    
    def move_left(self, event):
        if self.block is not None:
            if self.pos[1] - 1 >= 0:
                self.del_forme(self.pos, self.block)
                if not self.collision((self.pos[0], self.pos[1] - 1), self.block):
                    self.pos[1] -= 1
                    self.add_forme(self.pos, self.block)
                else:
                    self.add_forme(self.pos, self.block)
                
    def move_right(self, event):
        if self.block is not None:
            if self.pos[1] < len(self.grille[0]) - len(self.block[0]):
            
                self.del_forme(self.pos, self.block)
                if not self.collision((self.pos[0], self.pos[1] + 1), self.block):
                    self.pos[1] += 1
                    self.add_forme(self.pos, self.block)
                else:
                    self.add_forme(self.pos, self.block)
    def move_down(self, event):
        if self.block is not None:
            if self.pos[0] + len(self.block) + 1 > 10:
                self.block = None
                self.check_full_line()
                return    
            self.del_forme(self.pos, self.block)
            if not self.collision((self.pos[0] + 1, self.pos[1]), self.block):
                self.pos[0] +=1
                self.add_forme(self.pos, self.block)
    
    def rotate(self, event):
        if self.block is not None:
            rotate_form = self.rotate_horaire(self.block)
            if self.pos[0] + len(rotate_form) + 1 > 10:
                return
            self.del_forme(self.pos, self.block)
            if not self.collision(self.pos, rotate_form):
                self.block = rotate_form
                self.add_forme(self.pos, self.block)
            else:
                self.add_forme(self.pos, self.block)
            
    
    def rotate_horaire(self, forme):
        rotated = [[0] * len(forme) for _ in range(len(forme[0]))]

        for i in range(len(forme)):
            for j in range(len(forme[0])):
                rotated[j][len(forme) - 1 - i] = forme[i][j]
        return rotated

    def loop(self):
        self.run = True
        previous_time = time() - 1
        while self.run:
            new_time = time()
            if new_time - previous_time > 1:
                previous_time = new_time
                self.update()
                i=0
            system('cls')
            self.print()  
        system('cls')
        print(loser_text)

t = Tetris()
t.loop()