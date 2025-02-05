# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 16:44:29 2024

@author: jlbou
"""

import pygame
from Piece import *

class Elephant(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.type=Elephant
    
    def possible_moves(self,game):
        moves=[]
        positions_white=[(0,2),(0,6),(2,0),(2,4),(2,8),(4,2),(4,6)]
        positions_black=[(5,2),(5,6),(7,0),(7,4),(7,8),(9,2),(9,6)]
        if self.color == 'white':
            for pos in positions_white:
                dx = abs(self.position[1] - pos[1])
                dy = abs(self.position[0] - pos[0])
                if (dx == 2 and dy == 2) and ((game.get_piece(pos)==None) or (game.get_piece(pos).color=="black")):
                    if game.get_piece((int((nouvelle_ligne+self.ligne)/2),int((nouvelle_colonne+self.colonne)/2)))==None:
                        moves.append(pos)        
        elif self.color == 'black':
            for pos in positions_black:
                dx = abs(self.position[1] - pos[1])
                dy = abs(self.position[0] - pos[0])
                if (dx == 2 and dy == 2) and (game.get_piece(pos)==None or game.get_piece(pos).color=="white"):
                    if game.get_piece((int((nouvelle_ligne+self.ligne)/2),int((nouvelle_colonne+self.colonne)/2)))==None:
                        moves.append(pos)
        return moves
    