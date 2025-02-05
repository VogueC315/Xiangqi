# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 16:33:37 2024

@author: jlbou
"""


import pygame
from Piece import *
from General import *
from Conseiller import *
from Char import *
from Canon import *
from Cavalier import *
from Soldat import *
from Board import *
from Elephant import *

class Game:
    """Classe principale qui gère le jeu."""
    def __init__(self,plateau):
        
        self.ecran = pygame.display.set_mode((TAILLE_FENETRE_LARGEUR, TAILLE_FENETRE_HAUTEUR))
        pygame.display.set_caption("Jeu de plateau avec pièces")
        
        self.plateau = plateau
        self.m = [[None for _ in range(9)] for _ in range(10)]
        
        # Initialiser les pièces des joueurs
        
        self.m[0][0]=Char("white", [0, 0])
        self.m[0][1]=Cavalier("white", [0, 1])
        self.m[0][2]=Elephant("white", [0, 2])
        self.m[0][3]=Conseiller("white", [0, 3])
        self.m[0][4]=General("white", [0, 4])
        self.m[0][5]=Conseiller("white", [0, 5])
        self.m[0][6]=Elephant("white", [0, 6])
        self.m[0][7]=Cavalier("white", [0, 7])
        self.m[0][8]=Char("white", [0, 8])
        
        self.m[9][0]=Char("black", [9, 0])
        self.m[9][1]=Cavalier("black", [9, 1])
        self.m[9][2]=Elephant("black", [9, 2])
        self.m[9][3]=Conseiller("black", [9, 3])
        self.m[9][4]=General("black", [9, 4])
        self.m[9][5]=Conseiller("black", [9, 5])
        self.m[9][6]= Elephant("black", [9, 6])
        self.m[9][7]=Cavalier("black", [9, 7])
        self.m[9][8]=Char("black", [9, 8])
        
                
        for i in range(0, 9, 2):
            self.m[3][i]=Soldat("white", [3, i])
            self.m[6][i]=Soldat("black", [6, i])
        
        self.m[2][1]=Canon("white", [2, 1])
        self.m[2][7]=Canon("white", [2, 7])
        self.m[7][1]=Canon("black", [7, 1])
        self.m[7][7]=Canon("black", [7, 7])
        
        self.current_turn='white'
        self.piece_selectionnee=None
        self.historique=[self.m]
        self.piece_capturee=None
        
    def get_piece(self,pos):
        return self.m[pos[0]][pos[1]]
    
    def set_piece(self,pos,p):
        self.m[pos[0]][pos[1]]=p
        if p:
            p.position=pos
    
    def line_of_sight(self):
        boole=True
        pos1=self.find_general('white')
        pos2=self.find_general('black')
        if pos1[1]==pos2[1]:
            for i in range(pos1[0]+1,pos2[0]):
                if self.m[i][pos1[1]]:
                    boole=False
        else : 
            boole=False
        return boole
    
    def is_check(self):
        pos=self.find_general(self.current_turn)
        for row in self.m:
            for piece in row:
                if piece and piece.color!=self.current_turn:
                    if pos in piece.valid_moves(self):
                        return True
        return False
    
    def find_general(self,color):
        for row in self.m:
            for piece in row:
                if piece and piece.type=='General' and piece.color==color:
                    return piece.position
    
    def check_mate(self):
        for row in self.m:
            for piece in row:
                if (piece and piece.color==self.current_turn):
                    if piece.valid_moves(self):
                        return False
    
    
    def get_mouse_location(self, pos_souris):
        """Convertit la position de la souris en la position de la case sélectionnée (ligne et colonne)."""
        x, y = pos_souris           # Récupération des coordonnées de la souris
        colonne = x // TAILLE_CASE  # Convertit l'abscisse en numéro de colonne
        ligne = y // TAILLE_CASE    # Convertit l'ordonnée en numéro de ligne
        return ligne, colonne
    
    def handle_click(self):
        """Gère les événements du jeu, comme les clics de souris."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos_souris = pygame.mouse.get_pos()
                row, col = self.get_mouse_location(pos_souris)
                pos=[row,col]
                print(pos)
                # Vérifie si une pièce est sélectionnée
                if self.piece_selectionnee:
                    print("Deuxième boucle")
                    print(self.m[3][4])
                    print(self.m[4][4])
                    # Vérifie la validité du déplacement
                    if pos in self.piece_selectionnee.valid_moves(self):
                        old_pos=self.piece_selectionnee.position
                        self.set_piece(pos,self.piece_selectionnee)
                        self.set_piece(old_pos,None)
                        if self.current_turn == "white":
                            self.current_turn = "black"
                        else:
                            self.current_turn = "white"
                        self.historique.append(self.m)
                        print(self.m[3][4])
                        print(self.m[4][4])
                    else:
                        self.piece_selectionnee=None
                        
                else:
                    # Sélectionner une pièce si elle appartient au joueur actuel
                    print("Première boucle")
                    piece=self.get_piece(pos)
                    if piece and piece.color == self.current_turn:
                            self.piece_selectionnee = piece
                            break
        

    def mettre_a_jour(self):
        """Actualise le plateau."""
        self.plateau.dessiner(self.ecran)
        for row in self.m:
            for piece in row:
                if piece:
                    piece.dessiner(self.ecran)
        
        pygame.display.flip()

    def lancer(self):
        while True:
            self.handle_click()
            self.mettre_a_jour()
            
            
# Démarrer le jeu
if __name__ == "__main__":
    plateau=Board()
    jeu = Game(plateau)
    jeu.lancer()
            
    