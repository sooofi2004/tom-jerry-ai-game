import numpy as np
from interface import Interface

with open('matrix.txt', 'r') as f:
    board_txt = ''.join(f.readlines()).replace('\n', ';')

world = np.matrix(board_txt)

interface = Interface(world)
interface.showInterface()
