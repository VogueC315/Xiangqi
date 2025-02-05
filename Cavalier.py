# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 17:02:58 2024

@author: jlbou
"""

import pygame
from Piece import *

class Cavalier(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.type=Cavalier
    
    def possible_moves(self,game):
        moves=[]
        positions={(self.position[0]+1,self.position[1]-2),(self.position[0]+1,self.position[1]+2),(self.position[0]+2,self.position[1]-1),(self.position[0]+2,self.position[1]+1),(self.position[0]-1,self.position[1]+2),(self.position[0]-1,self.position[1]-2),(self.position[0]-2,self.position[1]+1),(self.position[0]-2,self.position[1]-1)}
        for pos in positions:
            if (game.get_piece(pos)==None) or (game.get_piece(pos).color=="black"):
                if abs(dx)==min(abs(dx),abs(dy)):
                    if (game.get_piece((self.position[0]+int(dy/abs(dy)),self.position[1]))==None) and (game.get_piece(pos)==None or game.get_piece(pos).color!=self.color):
                        moves.append(pos)
                elif abs(dy)==min(abs(dx),abs(dy)):
                    if (game.get_piece((self.position[0],self.position[1]+int(dx/abs(dx))))==None) and (game.get_piece(pos)==None or game.get_piece(pos).color!=self.color):
                        moves.append(pos)
                        
        return moves
        
