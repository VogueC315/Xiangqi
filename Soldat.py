# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 17:36:09 2024

@author: jlbou
"""

import pygame
from Piece import *

class Soldat(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.type=Soldat
        
    def possible_moves(self,game):
        moves=[]
        positions=[]
        if self.color == 'white':
            if self.position[0] <= 4:
                positions.append((self.position[0]+1,self.position[1]))
            else :
                positions.append((self.position[0]+1,self.position[1]))
                positions.append((self.position[0]+1,self.position[1]+1))
                positions.append((self.position[0]+1,self.position[1]-1))
        elif self.color == 'black' :
            if self.position[0] >= 5:
                positions.append((self.position[0]-1,self.position[1]))
            else :
                positions.append((self.position[0]-1,self.position[1]))
                positions.append((self.position[0]+1,self.position[1]+1))
                positions.append((self.position[0]+1,self.position[1]-1))
        for pos in positions:
            if (game.get_piece(pos)==None) or (game.get_piece(pos).color!=self.color):
                moves.append(pos)
        return moves
