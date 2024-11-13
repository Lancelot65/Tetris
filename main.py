import numpy as np
import random
import time
import keyboard
import os


bricks = {
  'Tétrimino I': np.array([[1], [1], [1], [1]], dtype=bool),
  'Tétrimino O': np.array([[0, 1, 1, 0], [0, 1, 1, 0]], dtype=bool),
  'Tétrimino T': np.array([[0, 1, 1, 1], [0, 0, 1, 0]], dtype=bool),
  'Tétrimino L': np.array([[0, 1, 1, 1], [0, 1, 0, 0]], dtype=bool),
  'Tétrimino J': np.array([[0, 1, 1, 1], [0, 0, 0, 1]], dtype=bool),
  'Tétrimino Z': np.array([[0, 1, 1, 0], [0, 0, 1, 1]], dtype=bool),
  'Tétrimino S': np.array([[0, 0, 1, 1], [0, 1, 1, 0]], dtype=bool),
}

class Tetris:
    def __init__(self):
        self.grille = np.zeros((20, 10), dtype=bool)
        self.grille_dur = np.zeros((20, 10), dtype=bool)
        self.last_block = None
        self.position = None


    def check_full_line(self):
        for row in range(self.grille.shape[0]):
            if np.sum(self.grille[row]) == 10:
                self.grille_dur[0:row+1] = np.vstack([np.zeros((1, 10), dtype=bool), self.grille_dur[0:row]])
                self.grille = self.grille_dur.copy()

  #  def check_collision(self, patern, position):
  #      return not np.any(np.any(self.grille_dur[position[0]:position[0] + self.last_block.shape[0], position[1]:position[1] + self.last_block.shape[1]] & patern))

    def check_collision(self, patern, position):
        end_row = position[0] + patern.shape[0]
        end_col = position[1] + patern.shape[1]

        if end_row > self.grille_dur.shape[0] or end_col > self.grille_dur.shape[1]:
            return False

        return not np.any(np.any(self.grille_dur[position[0]:end_row, position[1]:end_col] & patern))

    def add_tretris(self):
        self.grille = self.grille_dur.copy()
        # self.last_block = bricks[random.choice(list(bricks.keys()))]
        self.last_block = bricks['Tétrimino I']
        self.position = (0, 3)
        if self.check_collision(self.last_block, self.position):
            self.grille[self.position[0]:self.position[0] + self.last_block.shape[0], self.position[1]:self.position[1] + self.last_block.shape[1]] = self.last_block

        else:
            self.last_block = None


    def update(self):
        if self.last_block is not None:
            if self.check_collision(self.last_block, (self.position[0] + 1, self.position[1])) and self.position[0] != 20 - self.last_block.shape[0]:
                self.grille[self.position[0]:self.position[0] + self.last_block.shape[0], self.position[1]:self.position[1] + self.last_block.shape[1]] = False ## a modifier car ça enlève les ancien
                self.position = (self.position[0] + 1, self.position[1])
                self.grille[self.position[0]:self.position[0] + self.last_block.shape[0], self.position[1]:self.position[1] + self.last_block.shape[1]] = self.grille[self.position[0]:self.position[0] + self.last_block.shape[0], self.position[1]:self.position[1] + self.last_block.shape[1]] | self.last_block
            else:
                self.grille_dur[self.position[0]:self.position[0] + self.last_block.shape[0], self.position[1]:self.position[1] + self.last_block.shape[1]] = self.last_block | self.grille[self.position[0]:self.position[0] + self.last_block.shape[0], self.position[1]:self.position[1] + self.last_block.shape[1]]
                self.last_block = None
        else:
            self.add_tretris()
            #ouvrir un nouveau bloc