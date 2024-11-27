# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 16:26:58 2024

@author: jlbou
"""

##################
# Echecs chinois #
##################

################################
# Quelques importations utiles #
################################

import pygame
import sys


# Initialiser pygame
pygame.init()

# Constantes globales
NOMBRE_LIGNES = 10       # Nombre de lignes 
NOMBRE_COLONNES = 9      # Nombre de colonnes 
TAILLE_CASE = 72    # Taille d'une case en pixels
TAILLE_FENETRE_LARGEUR = NOMBRE_COLONNES * TAILLE_CASE
TAILLE_FENETRE_HAUTEUR = NOMBRE_LIGNES * TAILLE_CASE


# Couleurs
COULEUR_FOND = (255, 255, 255)   # Blanc pour le fond
COULEUR_LIGNE = (0, 0, 0)        # Noir pour les lignes
COULEUR_PIECE_J1 = (0, 128, 255) # Bleu pour les pièces du joueur 1
COULEUR_PIECE_J2 = (0, 0, 0)     # Noir pour les pièces du joueur 2

"""VOUS DEVEZ TELECHARGER DES IMAGES SUR INTERNET ET REMPLACER LES CHEMINS DANS LE PROGRAMME CI-DESSOUS"""
image_pion_noir_elephant = pygame.image.load(r"C:\Users\mathi\Downloads\babar-250.jpg")
image_pion_noir_elephant = pygame.transform.scale(image_pion_noir_elephant, (TAILLE_CASE//1.5 , TAILLE_CASE//1.5 ))

image_pion_noir_roi = pygame.image.load(r"C:/Users/mathi/Downloads/png-clipart-clash-royale-clash-of-clans-king-game-clash-of-clans-game-king.png")
image_pion_noir_roi = pygame.transform.scale(image_pion_noir_roi, (TAILLE_CASE//1.5 , TAILLE_CASE//1.5 ))

image_pion_noir_garde = pygame.image.load(r"C:\Users\mathi\Downloads\istockphoto-1336197081-612x612.jpg")
image_pion_noir_garde = pygame.transform.scale(image_pion_noir_garde, (TAILLE_CASE//1.5 , TAILLE_CASE//1.5 ))

image_pion_noir_pion = pygame.image.load(r"C:/Users/mathi/Downloads/télécharger.png")
image_pion_noir_pion = pygame.transform.scale(image_pion_noir_pion, (TAILLE_CASE//1.5 , TAILLE_CASE//1.5 ))

image_pion_noir_canon = pygame.image.load(r"C:\Users\mathi\Downloads\pngtree-military-cannon-ammunition-illustration-png-image_4506459.jpg")
image_pion_noir_canon = pygame.transform.scale(image_pion_noir_canon, (TAILLE_CASE//1.5 , TAILLE_CASE//1.5 ))

image_pion_noir_cheval = pygame.image.load(r"C:\Users\mathi\Downloads\IOMHWR33OPNAC4OWDK2BCLIBKA.jpg")
image_pion_noir_cheval = pygame.transform.scale(image_pion_noir_cheval, (TAILLE_CASE//1.5 , TAILLE_CASE//1.5 ))

image_pion_noir_char = pygame.image.load(r"C:/Users/mathi/Downloads/Zappy.webp")
image_pion_noir_char = pygame.transform.scale(image_pion_noir_char, (TAILLE_CASE//1.5 , TAILLE_CASE//1.5 ))


image_pion_rouge_elephant = pygame.image.load(r"C:/Users/mathi/Downloads/Xiangqi_image/babar-250.jpg")
image_pion_rouge_elephant = pygame.transform.scale(image_pion_rouge_elephant, (TAILLE_CASE//1.5 , TAILLE_CASE//1.5 ))

image_pion_rouge_roi = pygame.image.load(r"C:/Users/mathi/Downloads/Xiangqi_image/png-clipart-clash-royale-clash-of-clans-boom-beach-hay-day-android-clash-royal-game-video-game-thumbnail.png")
image_pion_rouge_roi = pygame.transform.scale(image_pion_rouge_roi, (TAILLE_CASE//1.5 , TAILLE_CASE//1.5 ))

image_pion_rouge_garde = pygame.image.load(r"C:/Users/mathi/Downloads/Xiangqi_image/istockphoto-1336197081-612x612.jpg")
image_pion_rouge_garde = pygame.transform.scale(image_pion_rouge_garde, (TAILLE_CASE//1.5 , TAILLE_CASE//1.5 ))

image_pion_rouge_pion = pygame.image.load(r"C:/Users/mathi/Downloads/Xiangqi_image/Classic_Chess_Pawn_White_1000_0001.jpg")
image_pion_rouge_pion = pygame.transform.scale(image_pion_rouge_pion, (TAILLE_CASE//1.5 , TAILLE_CASE//1.5 ))

image_pion_rouge_canon = pygame.image.load(r"C:/Users/mathi/Downloads/Xiangqi_image/pngtree-military-cannon-ammunition-illustration-png-image_4506459.jpg")
image_pion_rouge_canon = pygame.transform.scale(image_pion_rouge_canon, (TAILLE_CASE//1.5 , TAILLE_CASE//1.5 ))

image_pion_rouge_cheval = pygame.image.load(r"C:/Users/mathi/Downloads/Xiangqi_image/IOMHWR33OPNAC4OWDK2BCLIBKA.jpg")
image_pion_rouge_cheval = pygame.transform.scale(image_pion_rouge_cheval, (TAILLE_CASE//1.5 , TAILLE_CASE//1.5 ))

image_pion_rouge_char = pygame.image.load(r"C:/Users/mathi/Downloads/Xiangqi_image/Zappy.jpg")
image_pion_rouge_char = pygame.transform.scale(image_pion_rouge_char, (TAILLE_CASE//1.5 , TAILLE_CASE//1.5 ))



############################
# Implémentation des class #
############################

class Piece:
    """Classe qui représente une pièce sur le plateau."""
    def __init__(self, couleur, ligne, colonne):
        self.couleur = couleur
        self.ligne = ligne
        self.colonne = colonne
        self.selectionnee = False

    def dessiner(self, ecran):
        """Dessine la pièce sous forme de cercle au centre de la case."""
        x = self.colonne * TAILLE_CASE + TAILLE_CASE // 2
        y = self.ligne * TAILLE_CASE + TAILLE_CASE // 2
        rayon = TAILLE_CASE // 3
        if self.couleur=="white":  

            pygame.draw.circle(ecran, COULEUR_PIECE_J1, (x, y), rayon)
        else:
            
            pygame.draw.circle(ecran, COULEUR_PIECE_J2, (x, y), rayon)
        
    def mouvement_valide(self, nouvelle_ligne, nouvelle_colonne):
        """Vérifie que le mouvement est possible."""
        raise NotImplementedError("This method should be overridden by subclasses")
    
    def zone_autorisee(self, nouvelle_ligne, nouvelle_colonne, colonnes_autorisees=None, lignes_autorisees=None):
        """Vérifie que la pièce se trouve dans une zone autorisée."""
        # Vérifie si une position est dans une zone donnée (colonnes et/ou lignes spécifiques)
        if colonnes_autorisees is not None and nouvelle_colonne not in colonnes_autorisees:
            return False
        if lignes_autorisees is not None and nouvelle_ligne not in lignes_autorisees:
            return False
        return True
    
    def chemin_libre(self, nouvelle_ligne, nouvelle_colonne, jeu):
        """Vérifie que le mouvement est possible."""
        raise NotImplementedError("This method should be overridden by subclasses")
    
    def deplacer(self, nouvelle_ligne, nouvelle_colonne):
        """Met à jour la position de la pièce."""
        self.ligne = nouvelle_ligne
        self.colonne = nouvelle_colonne
        

class General(Piece):
    """Classe qui représente la pièce General sur le plateau."""
    def __init__(self, couleur, ligne, colonne):
        super().__init__(couleur, ligne, colonne)
    def dessiner(self, ecran):
        """Dessine la pièce sous forme de cercle au centre de la case."""
        x = self.colonne * TAILLE_CASE + TAILLE_CASE // 2
        y = self.ligne * TAILLE_CASE + TAILLE_CASE // 2
        rayon = TAILLE_CASE // 3
        if self.couleur=="white":  
            ecran.blit(image_pion_rouge_roi, (x-20, y-20))
            #pygame.draw.circle(ecran, COULEUR_PIECE_J1, (x, y), rayon)
        else:
            ecran.blit(image_pion_noir_roi, (x-20, y-20))
            #pygame.draw.circle(ecran, COULEUR_PIECE_J2, (x, y), rayon)
           
    def mouvement_valide(self, nouvelle_ligne, nouvelle_colonne, plateau):
        """Définie les mouvements valides pour le General."""
        if self.couleur == 'white':
            # Roi blanc restreint aux colonnes 2, 3 et lignes 5, 6
            if not self.zone_autorisee(nouvelle_ligne, nouvelle_colonne, colonnes_autorisees=range(3, 6), lignes_autorisees=range(0, 3)):
                return False
        else:
            # Roi noir restreint aux colonnes 0, 1 et lignes 0, 1
            if not self.zone_autorisee(nouvelle_ligne, nouvelle_colonne, colonnes_autorisees=range(3, 6), lignes_autorisees=range(7, 10)):
                return False
        
        dx = abs(self.colonne - nouvelle_colonne)
        dy = abs(self.ligne - nouvelle_ligne)
        return (dx == 1 and dy == 0) or (dx == 0 and dy == 1) 
    
    def chemin_libre(self, nouvelle_ligne, nouvelle_colonne, jeu):
        return True

    def est_echec(self, jeu):
        """vérifie si le roi est en échec"""
        echec = False
        """on vérifie que le roi n'est pas mis en échec par un Soldat adverse"""
        pos_possibles_soldat = [[self.ligne,self.colonne+1],[self.ligne,self.colonne-1],[self.ligne-1,self.colonne]]
        for pos in pos_possibles_soldat:
            for piece in jeu.pieces_adverses:
                if type(piece)==Soldat and piece.mouvement_valide(self.ligne,self.colonne,self) and piece.ligne == pos[0] and piece.colonne == pos[1]:
                    echec = True
        """on vérifie que le roi n'est pas mis en échec par un éléphant adverse"""
        pos_possibles_elephant = [[self.ligne+2,self.colonne+2],[self.ligne+2,self.colonne-2],[self.ligne-2,self.colonne+2],[self.ligne-2,self.colonne-2]]
        for pos in pos_possibles_elephant:
            for piece in jeu.pieces_adverses:
                if type(piece)==Elephant and piece.mouvement_valide(self.ligne,self.colonne,self) and piece.ligne == pos[0] and piece.colonne == pos[1]:
                    echec = True
        """on vérifie que le roi n'est pas mis en échec par un cavalier adverse"""        
        pos_possibles_cavalier = [[self.ligne+2,self.colonne+1],[self.ligne+2,self.colonne-1],[self.ligne+1,self.colonne+2],[self.ligne+1,self.colonne-2],[self.ligne-1,self.colonne+2],[self.ligne-1,self.colonne-2],[self.ligne-2,self.colonne+1],[self.ligne-2,self.colonne-1]]
        for pos in pos_possibles_cavalier:
            for piece in jeu.pieces_adverses:
                if type(piece)==Cavalier and piece.mouvement_valide(self.ligne,self.colonne,self) and piece.ligne == pos[0] and piece.colonne == pos[1]:
                    echec = True
        """on vérifie que le roi n'est pas mis en échec par un char adverse"""
        pos_possibles_char = [[self.ligne, i] for i in range(9)]+[[i,self.colonne] for i in range(10)]
        for pos in pos_possibles_char:
            for piece in jeu.pieces_adverses:
                if type==Char and piece.mouvement_valide(self.ligne,self.colonne,self) and piece.ligne == pos[0] and piece.colonne == pos[1]:
                    echec = True
        
        """on vérifie que le roi n'est pas mis en échec par un canon adverse"""
        """à compléter"""
        
        if jeu.tour_actuel == 'white':
            for piece in self.pieces_J2:
                if isinstance(piece, Canon):
                    ligne_canon_adverse, colonne_canon_adverse = piece.ligne,piece.colonne
            nombre_pieces_interposees = 0
            if ligne_canon_adverse == self.ligne:
                if colonne_canon_adverse < self.colonne:
                    for i in range(colonne_canon_adverse,self.colonne-1):
                        if jeu.matrice[self.ligne][i] ==1:
                            nombre_pieces_interposees+=1
                else:
                    for i in range(self.colonne,colonne_canon_adverse-1):
                        if jeu.matrice[self.ligne][i] ==1:
                            nombre_pieces_interposees+=1
            elif colonne_canon_adverse ==self.colonne:
                if ligne_canon_adverse < self.ligne:
                    for i in range(ligne_canon_adverse,self.ligne-1):
                        if jeu.matrice[self.colonne][i] ==1:
                            nombre_pieces_interposees+=1
                else:
                    for i in range(self.ligne,ligne_canon_adverse-1):
                        if jeu.matrice[self.colonne][i] ==1:
                            nombre_pieces_interposees+=1
            if nombre_pieces_interposees ==1:
                echec = True
                
        if jeu.tour_actuel == 'black':
            for piece in self.pieces_J1:
                if isinstance(piece, Canon):
                    ligne_canon_adverse, colonne_canon_adverse = piece.ligne,piece.colonne
            nombre_pieces_interposees = 0
            if ligne_canon_adverse == self.ligne:
                if colonne_canon_adverse < self.colonne:
                    for i in range(colonne_canon_adverse,self.colonne-1):
                        if jeu.matrice[self.ligne][i] ==1:
                            nombre_pieces_interposees+=1
                else:
                    for i in range(self.colonne,colonne_canon_adverse-1):
                        if jeu.matrice[self.ligne][i] ==1:
                            nombre_pieces_interposees+=1
            elif colonne_canon_adverse ==self.colonne:
                if ligne_canon_adverse < self.ligne:
                    for i in range(ligne_canon_adverse,self.ligne-1):
                        if jeu.matrice[self.colonne][i] ==1:
                            nombre_pieces_interposees+=1
                else:
                    for i in range(self.ligne,ligne_canon_adverse-1):
                        if jeu.matrice[self.colonne][i] ==1:
                            nombre_pieces_interposees+=1
            if nombre_pieces_interposees ==1:
                echec = True
        
        """on verifie que le roi n'est pas mis en échec par la ligne de mire du roi adverse"""
        ligne_mire = True
        if jeu.tour_actuel =='white':
            for piece in self.pieces_J2:
                if isinstance(piece, General):
                    ligne_general_adverse, colonne_general_adverse = piece.ligne, piece.colonne
            if colonne_general_adverse == self.colonne:
                for i in range(ligne_general_adverse,self.ligne-1):
                    if jeu.matrice[i][self.colonne] ==1:
                        ligne_mire = False
        if jeu.tour_actuel =='black':
            for piece in self.pieces_J1:
                if isinstance(piece, General):
                    ligne_general_adverse, colonne_general_adverse = piece.ligne, piece.colonne
            if colonne_general_adverse == self.colonne:
                for i in range(self.ligne,ligne_general_adverse-1):
                    if jeu.matrice[i][self.colonne] ==1:
                        ligne_mire = False
        if ligne_mire == True:
            echec = True
        return echec    

    
    def est_echec(self, jeu, pieces_adverses):
        """vérifie si le roi est en échec"""
        echec = False
        """on vérifie que le roi n'est pas mis en échec par un Soldat adverse"""
        pos_possibles_soldat = [[self.ligne,self.colonne+1],[self.ligne,self.colonne-1],[self.ligne-1,self.colonne]]
        for pos in pos_possibles_soldat:
            for piece in pieces_adverses:
                if type(piece)==Soldat and piece.mouvement_valide(self.ligne,self.colonne,self) and piece.ligne == pos[0] and piece.colonne == pos[1]:
                    echec = True
        """on vérifie que le roi n'est pas mis en échec par un éléphant adverse"""
        pos_possibles_elephant = [[self.ligne+2,self.colonne+2],[self.ligne+2,self.colonne-2],[self.ligne-2,self.colonne+2],[self.ligne-2,self.colonne-2]]
        for pos in pos_possibles_elephant:
            for piece in pieces_adverses:
                if type(piece)==Elephant and piece.mouvement_valide(self.ligne,self.colonne,self) and piece.ligne == pos[0] and piece.colonne == pos[1]:
                    echec = True
        """on vérifie que le roi n'est pas mis en échec par un cavalier adverse"""        
        pos_possibles_cavalier = [[self.ligne+2,self.colonne+1],[self.ligne+2,self.colonne-1],[self.ligne+1,self.colonne+2],[self.ligne+1,self.colonne-2],[self.ligne-1,self.colonne+2],[self.ligne-1,self.colonne-2],[self.ligne-2,self.colonne+1],[self.ligne-2,self.colonne-1]]
        for pos in pos_possibles_cavalier:
            for piece in pieces_adverses:
                if type(piece)==Cavalier and piece.mouvement_valide(self.ligne,self.colonne,self) and piece.ligne == pos[0] and piece.colonne == pos[1]:
                    echec = True
        """on vérifie que le roi n'est pas mis en échec par un char adverse"""
        pos_possibles_char = [[self.ligne, i] for i in range(9)]+[[i,self.colonne] for i in range(10)]
        for pos in pos_possibles_char:
            for piece in pieces_adverses:
                if type==Char and piece.mouvement_valide(self.ligne,self.colonne,self) and piece.ligne == pos[0] and piece.colonne == pos[1]:
                    echec = True
        
        """on vérifie que le roi n'est pas mis en échec par un canon adverse"""
        
        
        if jeu.tour_actuel == 'white':
            for piece in jeu.pieces_J2:
                if isinstance(piece, Canon):
                    ligne_canon_adverse, colonne_canon_adverse = piece.ligne,piece.colonne
            nombre_pieces_interposees = 0
            if ligne_canon_adverse == self.ligne:
                if colonne_canon_adverse < self.colonne:
                    for i in range(colonne_canon_adverse,self.colonne-1):
                        if jeu.matrice[self.ligne][i] ==1:
                            nombre_pieces_interposees+=1
                else:
                    for i in range(self.colonne,colonne_canon_adverse-1):
                        if jeu.matrice[self.ligne][i] ==1:
                            nombre_pieces_interposees+=1
            elif colonne_canon_adverse ==self.colonne:
                if ligne_canon_adverse < self.ligne:
                    for i in range(ligne_canon_adverse,self.ligne-1):
                        if jeu.matrice[self.colonne][i] ==1:
                            nombre_pieces_interposees+=1
                else:
                    for i in range(self.ligne,ligne_canon_adverse-1):
                        if jeu.matrice[self.colonne][i] ==1:
                            nombre_pieces_interposees+=1
            if nombre_pieces_interposees ==1:
                echec = True
                
        if jeu.tour_actuel == 'black':
            for piece in jeu.pieces_J1:
                if isinstance(piece, Canon):
                    ligne_canon_adverse, colonne_canon_adverse = piece.ligne,piece.colonne
            nombre_pieces_interposees = 0
            if ligne_canon_adverse == self.ligne:
                if colonne_canon_adverse < self.colonne:
                    for i in range(colonne_canon_adverse,self.colonne-1):
                        if jeu.matrice[self.ligne][i] ==1:
                            nombre_pieces_interposees+=1
                else:
                    for i in range(self.colonne,colonne_canon_adverse-1):
                        if jeu.matrice[self.ligne][i] ==1:
                            nombre_pieces_interposees+=1
            elif colonne_canon_adverse ==self.colonne:
                if ligne_canon_adverse < self.ligne:
                    for i in range(ligne_canon_adverse,self.ligne-1):
                        if jeu.matrice[self.colonne][i] ==1:
                            nombre_pieces_interposees+=1
                else:
                    for i in range(self.ligne,ligne_canon_adverse-1):
                        if jeu.matrice[self.colonne][i] ==1:
                            nombre_pieces_interposees+=1
            if nombre_pieces_interposees ==1:
                echec = True
        
        """on verifie que le roi n'est pas mis en échec par la ligne de mire du roi adverse"""
        ligne_mire = True
        if jeu.tour_actuel =='white':
            for piece in jeu.pieces_J2:
                if isinstance(piece, General):
                    ligne_general_adverse, colonne_general_adverse = piece.ligne, piece.colonne
            if colonne_general_adverse == self.colonne:
                for i in range(ligne_general_adverse,self.ligne-1):
                    if jeu.matrice[i][self.colonne] ==1:
                        ligne_mire = False
        if jeu.tour_actuel =='black':
            for piece in jeu.pieces_J1:
                if isinstance(piece, General):
                    ligne_general_adverse, colonne_general_adverse = piece.ligne, piece.colonne
            if colonne_general_adverse == self.colonne:
                for i in range(self.ligne,ligne_general_adverse-1):
                    if jeu.matrice[i][self.colonne] ==1:
                        ligne_mire = False
        if ligne_mire == True:
            echec = True
        return echec        
      

class Conseiller(Piece):
    """Classe qui représente la pièce Conseiller sur le plateau."""
    def __init__(self, couleur, ligne, colonne):
        super().__init__(couleur, ligne, colonne)
    def dessiner(self, ecran):
        """Dessine la pièce sous forme de cercle au centre de la case."""
        x = self.colonne * TAILLE_CASE + TAILLE_CASE // 2
        y = self.ligne * TAILLE_CASE + TAILLE_CASE // 2
        rayon = TAILLE_CASE // 3
        if self.couleur=="white":  
            ecran.blit(image_pion_rouge_garde, (x-20, y-20))
            #pygame.draw.circle(ecran, COULEUR_PIECE_J1, (x, y), rayon)
        else:
            ecran.blit(image_pion_noir_garde, (x-20, y-20))
            #pygame.draw.circle(ecran, COULEUR_PIECE_J2, (x, y), rayon)
        
    def mouvement_valide(self, nouvelle_ligne, nouvelle_colonne, plateau):
        """Définie les mouvements valides pour le Conseiller."""
        if self.couleur == 'white':
            # Roi blanc restreint aux colonnes 2, 3 et lignes 5, 6
            if not self.zone_autorisee(nouvelle_ligne, nouvelle_colonne, colonnes_autorisees=range(3, 6), lignes_autorisees=range(0, 3)):
                return False
        else:
            # Roi noir restreint aux colonnes 0, 1 et lignes 0, 1
            if not self.zone_autorisee(nouvelle_ligne, nouvelle_colonne, colonnes_autorisees=range(3, 6), lignes_autorisees=range(7, 10)):
                return False
        
        dx = abs(self.colonne - nouvelle_colonne)
        dy = abs(self.ligne - nouvelle_ligne)
        return dx == 1 and dy == 1
    
    def chemin_libre(self, nouvelle_ligne, nouvelle_colonne, jeu):
        return True

class Elephant(Piece):
    """Classe qui représente la pièce Elephant sur le plateau."""
    
    def __init__(self, couleur, ligne, colonne):
        super().__init__(couleur, ligne, colonne)
    def dessiner(self, ecran):
        """Dessine la pièce sous forme de cercle au centre de la case."""
        x = self.colonne * TAILLE_CASE + TAILLE_CASE // 2
        y = self.ligne * TAILLE_CASE + TAILLE_CASE // 2
        rayon = TAILLE_CASE // 3
        if self.couleur=="white":  
            ecran.blit(image_pion_rouge_elephant, (x-20, y-20))
            #pygame.draw.circle(ecran, COULEUR_PIECE_J1, (x, y), rayon)
        else:
            ecran.blit(image_pion_noir_elephant, (x-20, y-20))
            #pygame.draw.circle(ecran, COULEUR_PIECE_J2, (x, y), rayon)
        
    def mouvement_valide(self, nouvelle_ligne, nouvelle_colonne, plateau):
        """Définie les mouvements valides pour l'Elephant."""
        if self.couleur == 'white':
            # Elephant blanc restreint aux colonnes 2, 3 et lignes 5, 6
            if not self.zone_autorisee(nouvelle_ligne, nouvelle_colonne, lignes_autorisees=range(0, 5)):
                return False
        else:
            # Elephant noir restreint aux colonnes 0, 1 et lignes 0, 1
            if not self.zone_autorisee(nouvelle_ligne, nouvelle_colonne, lignes_autorisees=range(5, 10)):
                return False
        
        dx = abs(self.colonne - nouvelle_colonne)
        dy = abs(self.ligne - nouvelle_ligne) 
        return dx == 2 and dy == 2

    def chemin_libre(self, nouvelle_ligne, nouvelle_colonne,jeu):
        if jeu.matrice[int((nouvelle_ligne+self.ligne)/2)][int((nouvelle_colonne+self.colonne)/2)]==1:
            return False
        return True

class Cavalier(Piece):
    """Classe qui représente la pièce Cavalier sur le plateau."""
    def __init__(self, couleur, ligne, colonne):
        super().__init__(couleur, ligne, colonne)
    def dessiner(self, ecran):
        """Dessine la pièce sous forme de cercle au centre de la case."""
        x = self.colonne * TAILLE_CASE + TAILLE_CASE // 2
        y = self.ligne * TAILLE_CASE + TAILLE_CASE // 2
        rayon = TAILLE_CASE // 3
        if self.couleur=="white":  
            ecran.blit(image_pion_rouge_cheval, (x-20, y-20))
            #pygame.draw.circle(ecran, COULEUR_PIECE_J1, (x, y), rayon)
        else:
            ecran.blit(image_pion_noir_cheval, (x-20, y-20))
            #pygame.draw.circle(ecran, COULEUR_PIECE_J2, (x, y), rayon)
        
    def mouvement_valide(self, nouvelle_ligne, nouvelle_colonne, plateau):
        """Définie les mouvements valides pour le Cavalier."""
        dx = abs(self.colonne - nouvelle_colonne)
        dy = abs(self.ligne - nouvelle_ligne) 
        return (dx == 2 and dy == 1) or (dx == 1 and dy == 2) 

    def chemin_libre(self, nouvelle_ligne, nouvelle_colonne, jeu):
        dx = nouvelle_colonne - self.colonne
        dy = nouvelle_ligne - self.ligne 
        if abs(dx)==min(abs(dx),abs(dy)):
            if jeu.matrice[self.ligne+int(dy/abs(dy))][self.colonne]==1:
                return False
        elif abs(dy)==min(abs(dx),abs(dy)):
            if jeu.matrice[self.ligne][self.colonne+int(dx/abs(dx))]==1:
                return False
        return True
    

class Char(Piece):
    """Classe qui représente la pièce Char sur le plateau."""
    def __init__(self, couleur, ligne, colonne):
        super().__init__(couleur, ligne, colonne)
    def dessiner(self, ecran):
        """Dessine la pièce sous forme de cercle au centre de la case."""
        x = self.colonne * TAILLE_CASE + TAILLE_CASE // 2
        y = self.ligne * TAILLE_CASE + TAILLE_CASE // 2
        rayon = TAILLE_CASE // 3
        if self.couleur=="white":  
            ecran.blit(image_pion_rouge_char, (x-20, y-20))
            #pygame.draw.circle(ecran, COULEUR_PIECE_J1, (x, y), rayon)
        else:
            ecran.blit(image_pion_noir_char, (x-20, y-20))
            #pygame.draw.circle(ecran, COULEUR_PIECE_J2, (x, y), rayon)
         
    def mouvement_valide(self, nouvelle_ligne, nouvelle_colonne, plateau):
        """Définie les mouvements valides pour le Char."""
        return self.colonne == nouvelle_colonne or self.ligne == nouvelle_ligne
   
    def chemin_libre(self, nouvelle_ligne, nouvelle_colonne, jeu):
        if nouvelle_ligne==self.ligne:
            for i in range(min(nouvelle_colonne,self.colonne)+1,max(nouvelle_colonne,self.colonne)):
                if jeu.matrice[self.ligne][i]==1:
                    return False
        elif nouvelle_colonne==self.colonne:
            for i in range(min(nouvelle_ligne,self.ligne)+1,max(nouvelle_ligne,self.ligne)):
                if jeu.matrice[i][self.colonne]==1:
                    return False
        return True 
    
    
class Canon(Piece):
    """Classe qui représente la pièce Canon sur le plateau."""
    def __init__(self, couleur, ligne, colonne):
        super().__init__(couleur, ligne, colonne)
    def dessiner(self, ecran):
        """Dessine la pièce sous forme de cercle au centre de la case."""
        x = self.colonne * TAILLE_CASE + TAILLE_CASE // 2
        y = self.ligne * TAILLE_CASE + TAILLE_CASE // 2
        rayon = TAILLE_CASE // 3
        if self.couleur=="white":  
            ecran.blit(image_pion_rouge_canon, (x-20, y-20))
            #pygame.draw.circle(ecran, COULEUR_PIECE_J1, (x, y), rayon)
        else:
            ecran.blit(image_pion_noir_canon, (x-20, y-20))
            #pygame.draw.circle(ecran, COULEUR_PIECE_J2, (x, y), rayon)
        
    def mouvement_valide(self, nouvelle_ligne, nouvelle_colonne, plateau):
        """Définie les mouvements valides pour le Canon."""
        return self.colonne == nouvelle_colonne or self.ligne == nouvelle_ligne

    def chemin_libre(self, nouvelle_ligne, nouvelle_colonne, jeu):
        return True


class Soldat(Piece):
    """Classe qui représente la pièce Soldat sur le plateau."""
    def __init__(self, couleur, ligne, colonne):
        super().__init__(couleur, ligne, colonne)
    def dessiner(self, ecran):
        """Dessine la pièce sous forme de cercle au centre de la case."""
        x = self.colonne * TAILLE_CASE + TAILLE_CASE // 2
        y = self.ligne * TAILLE_CASE + TAILLE_CASE // 2
        rayon = TAILLE_CASE // 3
        if self.couleur=="white":  
            ecran.blit(image_pion_rouge_pion, (x-20, y-20))
            #pygame.draw.circle(ecran, COULEUR_PIECE_J1, (x, y), rayon)
        else:
            ecran.blit(image_pion_noir_pion, (x-20, y-20))
            #pygame.draw.circle(ecran, COULEUR_PIECE_J2, (x, y), rayon)
        
    def mouvement_valide(self, nouvelle_ligne, nouvelle_colonne, plateau):
        """Définie les mouvements valides pour le Soldat."""
        if self.couleur == 'white':
            if self.ligne <= 4:
                if (nouvelle_ligne == self.ligne + 1) and (nouvelle_colonne==self.colonne):
                    return True
            else :
                dx = abs(nouvelle_colonne - self.colonne)
                dy = nouvelle_ligne - self.ligne
                return (dx == 1 and dy == 0) or (dx == 0 and dy == 1)
        elif self.couleur == 'black' :
            if self.ligne >= 5:
                if (nouvelle_ligne == self.ligne - 1) and (nouvelle_colonne==self.colonne):
                    return True
            else :
                dx = abs(nouvelle_colonne - self.colonne)
                dy = nouvelle_ligne - self.ligne
                return (dx == 1 and dy == 0) or (dx == 0 and dy == -1)
        else :
            return False
        
    def chemin_libre(self, nouvelle_ligne, nouvelle_colonne, jeu):
        return True
    
        

    

class Plateau:
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


class Jeu:
    """Classe principale qui gère le jeu."""
    def __init__(self):
        self.ecran = pygame.display.set_mode((TAILLE_FENETRE_LARGEUR, TAILLE_FENETRE_HAUTEUR))
        pygame.display.set_caption("Jeu de plateau avec pièces")
        
        # Créer le plateau et les pièces
        self.plateau = Plateau()
        self.matrice = [[0 for _ in range(NOMBRE_COLONNES)] for _ in range(NOMBRE_LIGNES)]
        
        # Ajout des positions des pièces dans la matrice
        
        for i in range(NOMBRE_COLONNES):
            self.matrice[0][i]+=1
            self.matrice[-1][i]+=1
        
        for i in range(0, 9, 2):
            self.matrice[3][i]+=1
            self.matrice[6][i]+=1
            
        self.matrice[2][1]+=1
        self.matrice[2][7]+=1
        self.matrice[7][1]+=1
        self.matrice[7][7]+=1
        
        # Initialiser les pièces des joueurs
        self.pieces_J1 = [
            General("white", 0, 4), Char("white", 0, 0), Cavalier("white", 0, 1), Elephant("white", 0, 2),
            Conseiller("white", 0, 3), Conseiller("white", 0, 5),
            Elephant("white", 0, 6), Cavalier("white", 0, 7), Char("white", 0, 8)
        ]
        self.pieces_J2 = [
            General("black", 9, 4), Char("black", 9, 0), Cavalier("black", 9, 1), Elephant("black", 9, 2),
            Conseiller("black", 9, 3), Conseiller("black", 9, 5),
            Elephant("black", 9, 6), Cavalier("black", 9, 7), Char("black", 9, 8)
        ]
        
        for i in range(0, 9, 2):
            self.pieces_J1.append(Soldat("white", 3, i))
            self.pieces_J2.append(Soldat("black", 6, i))
        
        self.pieces_J1.append(Canon("white", 2, 1))
        self.pieces_J1.append(Canon("white", 2, 7))
        self.pieces_J2.append(Canon("black", 7, 1))
        self.pieces_J2.append(Canon("black", 7, 7))

        self.piece_selectionnee = None
        self.tour_actuel = "white"  # Commence avec le joueur blanc

    def obtenir_case_souris(self, pos_souris):
        """Convertit la position de la souris en la position de la case sélectionnée (ligne et colonne)."""
        x, y = pos_souris           # Récupération des coordonnées de la souris
        colonne = x // TAILLE_CASE  # Convertit l'abscisse en numéro de colonne
        ligne = y // TAILLE_CASE    # Convertit l'ordonnée en numéro de ligne
        return ligne, colonne

    def gerer_evenements(self):
        """Gère les événements du jeu, comme les clics de souris."""
        for event in pygame.event.get():
            pieces_adverses = self.pieces_J2 if self.tour_actuel == "white" else self.pieces_J1
            pieces_amies = self.pieces_J1 if self.tour_actuel == "white" else self.pieces_J2
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos_souris = pygame.mouse.get_pos()
                ligne, colonne = self.obtenir_case_souris(pos_souris)
                # Vérifie si une pièce est sélectionnée
                
                
                if self.piece_selectionnee:
                    ligne_actuelle = self.piece_selectionnee.ligne
                    colonne_actuelle = self.piece_selectionnee.colonne
                    # Vérifie la validité du déplacement
                    if self.piece_selectionnee.mouvement_valide(ligne, colonne, self):

                        
                        
                        
                        
                        
                        
                        # Vérifie si une collision a lieu
                        if self.piece_selectionnee.chemin_libre(ligne, colonne, self):
                            # Vérifie s'il y a une pièce adverse sur la case de destination
                            piece_capturee = None
                            for piece in pieces_adverses:
                                if piece.ligne == ligne and piece.colonne == colonne:
                                    piece_capturee = piece
                                    break
                            for piece in pieces_amies:
                                if piece.ligne == ligne and piece.colonne == colonne:
                                    self.piece_selectionnee = None
                                    break
                       
                    
                            
                       
                            
                        
                            # Si une pièce adverse est présente, la capturer
                            if piece_capturee:
                                pieces_adverses.remove(piece_capturee)  # Enlever la pièce adverse
                                self.matrice[piece_capturee.ligne][piece_capturee.colonne] -= 1
                                
                            #Vérifie si le roi du joueur qui joue est en échec à l'issue de son tour
                            
                            general_ami = pieces_amies[0]
                            self.piece_selectionnee.deplacer(ligne,colonne)
                            if general_ami.est_echec(self,pieces_adverses):
                                self.piece_selectionnee.deplacer(ligne_actuelle, colonne_actuelle)
                                if piece_capturee:
                                    pieces_adverses.append(piece_capturee)
                                    self.matrice[piece_capturee.ligne][piece_capturee.colonne] += 1
                                piece.selectionnee = None
                            
                              
                            if self.piece_selectionnee:
                                # Déplace la pièce sélectionnée si la piece est encore sélectionnée
                                self.matrice[self.piece_selectionnee.ligne][self.piece_selectionnee.colonne] -= 1
                                self.matrice[ligne][colonne] += 1
                                self.piece_selectionnee.deplacer(ligne, colonne)
                                
                                # Désélectionne la pièce et change de tour
                                self.piece_selectionnee = None
                                self.tour_actuel = "black" if self.tour_actuel == "white" else "white"
                        else:
                            # Si le chemin est bloqué, désélectionner la pièce
                            self.piece_selectionnee = None
                    else:
                        # Si le mouvement  est non valide, désélectionner la pièce
                        self.piece_selectionnee = None
                else:
                    # Sélectionner une pièce si elle appartient au joueur actuel
                    pieces_joueur = self.pieces_J1 if self.tour_actuel == "white" else self.pieces_J2
                    for piece in pieces_joueur:
                        if piece.ligne == ligne and piece.colonne == colonne:
                            self.piece_selectionnee = piece
                            break

    def mettre_a_jour(self):
        """Actualise le plateau."""
        self.plateau.dessiner(self.ecran)
        for piece in self.pieces_J1:
            piece.dessiner(self.ecran)
        for piece in self.pieces_J2:
            piece.dessiner(self.ecran)
        
        pygame.display.flip()

    def lancer(self):
        while True:
            self.gerer_evenements()
            self.mettre_a_jour()

# Démarrer le jeu
if __name__ == "__main__":
    jeu = Jeu()
    jeu.lancer()
    
######################
# Tâches à effectuer #
######################

# Modifier le dessin des pièces

#######################
# Idées pour la suite #
#######################

# Gérer la collision avec une pièces alliées sur la case finale
# Calculer les mouvements possibles à partir des deux rois
# On peut penser à implémenter dans la matrice des +- 1 pour différencier l'appartenance ou mettre à jour la liste des pièces adverses et alliées qui changent avec changement de tour
# Pour la mise en échec, créer une méthode get_mouvements qui renvoie pour une pièce donnée les miuvements possible, attention cette méthode devra faire appel à collision et zone_autorisee
