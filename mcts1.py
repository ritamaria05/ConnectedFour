import numpy as np

class Node:
    def __init__(self, move, parent, player='O'):
        self.move = move
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0
        self.player = player