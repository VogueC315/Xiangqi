# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 16:20:40 2024

@author: jlbou
"""

import pygame
from Piece import *

class Char(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.type=Char
    
    def possible_moves(self,game):
        moves=[]
        positions={(self.position[0],i) for i in range(0,10)}|{(i,self.position[1]) for i in range(0,11)}
        for pos in positions:
            if pos[0]==self.position[0]:
                if (game.get_piece((self.position[0],i))==None for i in range(min(pos[1],self.position[1])+1,max(pos[1],self.position[1]))):
                    if ((game.get_piece(pos)==None) or (game.get_piece(pos).color!=self.color)):
                        moves.append(pos)
            elif pos[1]==self.position[1]:
                if (game.get_piece((i,self.position[1]))==None for i in range(min(pos[0],self.position[0])+1,max(pos[0],self.position[0]))):
                    if ((game.get_piece(pos)==None) or (game.get_piece(pos).color!=self.color)):
                        moves.append(pos)
        return moves
