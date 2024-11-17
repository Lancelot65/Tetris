from unicurses import COLOR_CYAN, COLOR_YELLOW, COLOR_MAGENTA, COLOR_WHITE, COLOR_BLUE, COLOR_RED, COLOR_GREEN

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

loser_text = r"""
  _                         
 | |                        
 | |     ___  ___  ___ _ __ 
 | |    / _ \/ __|/ _ \ '__|
 | |___| (_) \__ \  __/ |   
 |______\___/|___/\___|_|   
"""