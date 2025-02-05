# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 16:41:48 2024

@author: jlbou
"""

import pygame
import sys

# Constantes globales
NOMBRE_LIGNES = 10       # Nombre de lignes 
NOMBRE_COLONNES = 9      # Nombre de colonnes 
TAILLE_CASE = 50        # Taille d'une case en pixels
TAILLE_FENETRE_LARGEUR = NOMBRE_COLONNES * TAILLE_CASE
TAILLE_FENETRE_HAUTEUR = NOMBRE_LIGNES * TAILLE_CASE


# Couleurs
COULEUR_FOND = (255, 255, 255)   # Blanc pour le fond
COULEUR_LIGNE = (0, 0, 0)        # Noir pour les lignes
COULEUR_PIECE_J1 = (0, 128, 255) # Bleu pour les pièces du joueur 1
COULEUR_PIECE_J2 = (0, 0, 0)     # Noir pour les pièces du joueur 2

class Board:
    """Classe qui représente le plateau de jeu."""
    def __init__(self):
        self.largeur = TAILLE_FENETRE_LARGEUR
        self.hauteur = TAILLE_FENETRE_HAUTEUR

    def dessiner(self, ecran):
        """Dessine la grille du plateau."""
        ecran.fill(COULEUR_FOND)
        # Tracé des lignes horizontales
        for ligne in range(NOMBRE_LIGNES + 1):
            pygame.draw.line(ecran, COULEUR_LIGNE, (0, ligne * TAILLE_CASE), (self.largeur, ligne * TAILLE_CASE), 2)
        # Tracé des lignes verticales
        for colonne in range(NOMBRE_COLONNES + 1):
            pygame.draw.line(ecran, COULEUR_LIGNE, (colonne * TAILLE_CASE, 0), (colonne * TAILLE_CASE, self.hauteur), 2)
