# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 15:12:01 2024

@author: jlbou
"""

import pygame
from Piece import * 

class General(Piece):
    """Classe qui représente la pièce General sur le plateau."""
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.type=General
    
    def possible_moves(self,game):
        moves=[]
        positions_white=[(0,3),(0,4),(0,5),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5)]
        positions_black=[(7,3),(7,4),(7,5),(8,3),(8,4),(8,5),(9,3),(9,4),(9,5)]
        if self.color == 'white':
            for pos in positions_white:
                dx = abs(self.position[1] - nouvelle_colonne)
                dy = abs(self.position[0] - nouvelle_ligne)
                if ((dx == 1 and dy == 0) or (dx == 0 and dy == 1)) and ((game.get_piece(pos)==None) or (game.get_piece(pos).color=="black")):
                    moves.append(pos)        
        elif self.color == 'black':
            for pos in positions_black:
                dx = abs(self.position[1] - nouvelle_colonne)
                dy = abs(self.position[0] - nouvelle_ligne)
                if ((dx == 1 and dy == 0) or (dx == 0 and dy == 1)) and (game.get_piece(pos)==None or game.get_piece(pos).color=="white"):
                    moves.append(pos)
        return moves