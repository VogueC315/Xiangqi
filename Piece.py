# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 14:45:43 2024

@author: jlbou
"""
import pygame



# Constantes globales
NOMBRE_LIGNES = 10       # Nombre de lignes 
NOMBRE_COLONNES = 9      # Nombre de colonnes 
TAILLE_CASE = 50        # Taille d'une case en pixels
TAILLE_FENETRE_LARGEUR = NOMBRE_COLONNES * TAILLE_CASE
TAILLE_FENETRE_HAUTEUR = NOMBRE_LIGNES * TAILLE_CASE


# Couleurs
COULEUR_FOND = (255, 255, 255)   # Blanc pour le fond
COULEUR_LIGNE = (0, 0, 0)        # Noir pour les lignes



class Piece:
    def __init__(self,color,pos):
        self.color = color
        self.position = pos
        self.type = None
        self.selection = False
    
    def possible_moves(self,game):
        pass
    
    def valid_moves(self,game):
        valid_moves=[]
        moves=self.possible_moves(game)
        for pos in moves:
            captured=game.get_piece(pos)
            game.set_piece(pos,self)
            game.set_piece(self.position,None)
            if not game.is_check() and not game.line_of_sight():
                valid_moves.append(pos)
            game.set_piece(pos, captured)
            game.set_piece(pos, self)
        return valid_moves
    
    def move(self,pos,game):
        captured=game.get_piece(pos)
        game.set_piece(pos,self)
        game.set_piece(self.position,None)
        self.position=pos
        
    def dessiner(self, ecran):
        """Dessine la pièce sous forme de cercle au centre de la case."""
        x = self.position[1] * TAILLE_CASE + TAILLE_CASE // 2
        y = self.position[0] * TAILLE_CASE + TAILLE_CASE // 2
        rayon = TAILLE_CASE // 3
        if self.color=="white":  
            pygame.draw.circle(ecran, "blue", (x, y), rayon)
        else:
            pygame.draw.circle(ecran, "black", (x, y), rayon)
        