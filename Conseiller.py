# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 16:04:16 2024

@author: jlbou
"""

import pygame
from Piece import *

class Conseiller(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.type=Conseiller
    
    def possible_moves(self,game):
        moves=[]
        positions_white=[(0,3),(0,5),(1,4),(2,3),(2,5)]
        positions_black=[(7,3),(7,5),(8,4),(9,3),(9,5)]
        if self.color == 'white':
            for pos in positions_white:
                dx = abs(self.position[1] - pos[1])
                dy = abs(self.position[0] - pos[0])
                if (dx == 1 and dy == 1) and ((game.get_piece(pos)==None) or (game.get_piece(pos).color=="black")):
                    moves.append(pos)        
        elif self.color == 'black':
            for pos in positions_black:
                dx = abs(self.position[1] - pos[1])
                dy = abs(self.position[0] - pos[0])
                if (dx == 1 and dy == 1) and (game.get_piece(pos)==None or game.get_piece(pos).color=="white"):
                    moves.append(pos)
        return moves