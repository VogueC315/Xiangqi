# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 17:02:13 2025

@author: jlbou
"""

import pygame
import sys
import copy

# Constantes globales
NOMBRE_LIGNES = 10       # Nombre de lignes
NOMBRE_COLONNES = 9      # Nombre de colonnes
TAILLE_CASE = 50         # Taille d'une case en pixels
TAILLE_FENETRE_LARGEUR = NOMBRE_COLONNES * TAILLE_CASE
TAILLE_FENETRE_HAUTEUR = NOMBRE_LIGNES * TAILLE_CASE

# Couleurs
COULEUR_FOND1=(185,156,107)
COULEUR_FOND = (255, 255, 255)   # Blanc pour le fond
COULEUR_LIGNE = (0, 0, 0)        # Noir pour les lignes

class Piece:
    def __init__(self, color, pos):
        self.color = color
        self.position = pos
        self.type = self.__class__.__name__
        self.selection = False

    def possible_moves(self, game):
        return []

    def valid_moves(self, game):
        valid_moves = []
        moves = self.possible_moves(game)
        for pos in moves:
            # On simule le coup sur une copie de l'état du jeu
            game_clone = game.clone_state()
            piece_clone = game_clone.get_piece(self.position)

            # Vérifier que la pièce clonée existe
            if piece_clone is None:
                continue

            # Simuler le coup sur le clone
            captured = game_clone.get_piece(pos)
            game_clone.set_piece(pos, piece_clone)
            game_clone.set_piece(self.position, None)
            piece_clone.position = pos  # Mise à jour de la position dans la copie

            # Vérifier que ce coup ne met pas le général en échec dans la copie
            if not game_clone.is_check():
                valid_moves.append(pos)
        return valid_moves

    def move(self, pos, game):
        captured = game.get_piece(pos)
        game.set_piece(pos, self)
        game.set_piece(self.position, None)
        self.position = pos

    def dessiner(self, ecran):
        """Dessine la pièce sous forme de cercle au centre de la case."""
        x = self.position[1] * TAILLE_CASE + TAILLE_CASE // 2
        y = self.position[0] * TAILLE_CASE + TAILLE_CASE // 2
        rayon = TAILLE_CASE // 3
        if self.color == "white":
            pygame.draw.circle(ecran, "blue", (x, y), rayon)
        else:
            pygame.draw.circle(ecran, "black", (x, y), rayon)

# Subclasses for each piece type with possible_moves implementations

class Soldat(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.type="Soldat"
        
    def possible_moves(self, game):
        moves = []
        row, col = self.position
        direction = 1 if self.color == "white" else -1  # White moves down, black moves up

        # Forward move
        new_row = row + direction
        if 0 <= new_row < NOMBRE_LIGNES:
            if game.get_piece([new_row, col]) is None:
                moves.append([new_row, col])
            elif game.get_piece([new_row, col]).color != self.color:
                moves.append([new_row, col])

        # After crossing the river, can move sideways
        river_row = 5 if self.color == "white" else 4
        if (self.color == "white" and row >= river_row) or (self.color == "black" and row <= river_row):
            for delta_col in [-1, 1]:
                new_col = col + delta_col
                if 0 <= new_col < NOMBRE_COLONNES:
                    if game.get_piece([row, new_col]) is None or game.get_piece([row, new_col]).color != self.color:
                        moves.append([row, new_col])

        return moves

class Char(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.type="Char"
        
    def possible_moves(self, game):
        moves = []
        row, col = self.position

        # Horizontal and vertical moves
        # Up
        for r in range(row - 1, -1, -1):
            piece = game.get_piece([r, col])
            if piece is None:
                moves.append([r, col])
            elif piece.color != self.color:
                moves.append([r, col])
                break
            else:
                break
        # Down
        for r in range(row + 1, NOMBRE_LIGNES):
            piece = game.get_piece([r, col])
            if piece is None:
                moves.append([r, col])
            elif piece.color != self.color:
                moves.append([r, col])
                break
            else:
                break
        # Left
        for c in range(col - 1, -1, -1):
            piece = game.get_piece([row, c])
            if piece is None:
                moves.append([row, c])
            elif piece.color != self.color:
                moves.append([row, c])
                break
            else:
                break
        # Right
        for c in range(col + 1, NOMBRE_COLONNES):
            piece = game.get_piece([row, c])
            if piece is None:
                moves.append([row, c])
            elif piece.color != self.color:
                moves.append([row, c])
                break
            else:
                break

        return moves

class Cavalier(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.type="Cavalier"
    
    def possible_moves(self, game):
        moves = []
        row, col = self.position
        # Possible moves considering blocking pieces
        knight_moves = [
            (-2, -1), (-1, -2),
            (-2, 1), (-1, 2),
            (1, -2), (2, -1),
            (1, 2), (2, 1)
        ]
        for dr, dc in knight_moves:
            mid_row = row + (dr/abs(dr))*(abs(dr) // 2)
            mid_col = col + (dc/abs(dc))*(abs(dc) // 2)
            dest_row = row + dr
            dest_col = col + dc
            if 0 <= dest_row < NOMBRE_LIGNES and 0 <= dest_col < NOMBRE_COLONNES:
                # Check if the path is blocked
                if game.get_piece([int(mid_row), int(mid_col)]) is None:
                    dest_piece = game.get_piece([dest_row, dest_col])
                    if dest_piece is None or dest_piece.color != self.color:
                        moves.append([dest_row, dest_col])
        return moves

class Elephant(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.type="Elephant"
        
    def possible_moves(self, game):
        moves = []
        row, col = self.position
        # Elephant moves diagonally by two points, cannot jump over pieces
        elephant_moves = [
            (-2, -2), (-2, 2),
            (2, -2), (2, 2)
        ]
        # Elephants cannot cross the river
        river_boundary = 4 if self.color == "white" else 5
        for dr, dc in elephant_moves:
            dest_row = row + dr
            dest_col = col + dc
            mid_row = row + (dr // 2)
            mid_col = col + (dc // 2)
            if 0 <= dest_row < NOMBRE_LIGNES and 0 <= dest_col < NOMBRE_COLONNES:
                if ((self.color == "white" and dest_row <= river_boundary) or
                    (self.color == "black" and dest_row >= river_boundary)):
                    # Check if the path is blocked
                    if game.get_piece([mid_row, mid_col]) is None:
                        dest_piece = game.get_piece([dest_row, dest_col])
                        if dest_piece is None or dest_piece.color != self.color:
                            moves.append([dest_row, dest_col])
        return moves

class Conseiller(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.type="Conseiller"
    
    def possible_moves(self, game):
        moves = []
        row, col = self.position
        palace_cols = [3, 4, 5]
        palace_rows_white = [0, 1, 2]
        palace_rows_black = [7, 8, 9]
        advisor_moves = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in advisor_moves:
            dest_row = row + dr
            dest_col = col + dc
            if dest_col in palace_cols:
                if (self.color == "white" and dest_row in palace_rows_white) or \
                   (self.color == "black" and dest_row in palace_rows_black):
                    dest_piece = game.get_piece([dest_row, dest_col])
                    if dest_piece is None or dest_piece.color != self.color:
                        moves.append([dest_row, dest_col])
        return moves

class General(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.type="General"
        
    def possible_moves(self, game):
        moves = []
        row, col = self.position
        palace_cols = [3, 4, 5]
        palace_rows_white = [0, 1, 2]
        palace_rows_black = [7, 8, 9]
        general_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in general_moves:
            dest_row = row + dr
            dest_col = col + dc
            if dest_col in palace_cols:
                if (self.color == "white" and dest_row in palace_rows_white) or \
                   (self.color == "black" and dest_row in palace_rows_black):
                    dest_piece = game.get_piece([dest_row, dest_col])
                    if dest_piece is None or dest_piece.color != self.color:
                        moves.append([dest_row, dest_col])
        return moves

class Canon(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.type="Canon"
        
    def possible_moves(self, game):
        moves = []
        row, col = self.position
        # Can move like a rook but captures differently
        # Movement (like a rook)
        # Up
        for r in range(row - 1, -1, -1):
            piece = game.get_piece([r, col])
            if piece is None:
                moves.append([r, col])
            else:
                break
        # Down
        for r in range(row + 1, NOMBRE_LIGNES):
            piece = game.get_piece([r, col])
            if piece is None:
                moves.append([r, col])
            else:
                break
        # Left
        for c in range(col - 1, -1, -1):
            piece = game.get_piece([row, c])
            if piece is None:
                moves.append([row, c])
            else:
                break
        # Right
        for c in range(col + 1, NOMBRE_COLONNES):
            piece = game.get_piece([row, c])
            if piece is None:
                moves.append([row, c])
            else:
                break
        # Capturing (needs to jump exactly one piece)
        # Up
        for r in range(row - 1, -1, -1):
            piece = game.get_piece([r, col])
            if piece is not None:
                # Found a piece to jump over
                for r2 in range(r - 1, -1, -1):
                    dest_piece = game.get_piece([r2, col])
                    if dest_piece is not None:
                        if dest_piece.color != self.color:
                            moves.append([r2, col])
                        break
                break
        # Down
        for r in range(row + 1, NOMBRE_LIGNES):
            piece = game.get_piece([r, col])
            if piece is not None:
                for r2 in range(r + 1, NOMBRE_LIGNES):
                    dest_piece = game.get_piece([r2, col])
                    if dest_piece is not None:
                        if dest_piece.color != self.color:
                            moves.append([r2, col])
                        break
                break
        # Left
        for c in range(col - 1, -1, -1):
            piece = game.get_piece([row, c])
            if piece is not None:
                for c2 in range(c - 1, -1, -1):
                    dest_piece = game.get_piece([row, c2])
                    if dest_piece is not None:
                        if dest_piece.color != self.color:
                            moves.append([row, c2])
                        break
                break
        # Right
        for c in range(col + 1, NOMBRE_COLONNES):
            piece = game.get_piece([row, c])
            if piece is not None:
                for c2 in range(c + 1, NOMBRE_COLONNES):
                    dest_piece = game.get_piece([row, c2])
                    if dest_piece is not None:
                        if dest_piece.color != self.color:
                            moves.append([row, c2])
                        break
                break
        return moves

class Board:
    """Classe qui représente le plateau de jeu."""
    def __init__(self):
        self.largeur = TAILLE_FENETRE_LARGEUR
        self.hauteur = TAILLE_FENETRE_HAUTEUR

    def dessiner(self, ecran):
        """Dessine la grille du plateau."""
        ecran.fill(COULEUR_FOND1)
        # Tracé des lignes horizontales
        for ligne in range(NOMBRE_LIGNES ):
            pygame.draw.line(ecran, COULEUR_LIGNE, (0, TAILLE_CASE/2 + ligne * TAILLE_CASE), (self.largeur, TAILLE_CASE/2 + ligne * TAILLE_CASE), 2)
        # Tracé des lignes verticales
        for colonne in range(NOMBRE_COLONNES):
            pygame.draw.line(ecran, COULEUR_LIGNE, (TAILLE_CASE/2 + colonne * TAILLE_CASE, 0), (TAILLE_CASE/2 + colonne * TAILLE_CASE, self.hauteur), 2)

class Game:
    """Classe principale qui gère le jeu."""
    def __init__(self, plateau):
        pygame.init()
        self.ecran = pygame.display.set_mode((TAILLE_FENETRE_LARGEUR, TAILLE_FENETRE_HAUTEUR))
        pygame.display.set_caption("Jeu de Xiangqi")

        self.plateau = plateau
        self.m = [[None for _ in range(NOMBRE_COLONNES)] for _ in range(NOMBRE_LIGNES)]

        # Initialiser les pièces des joueurs
        # White pieces
        self.m[0][0] = Char("white", [0, 0])
        self.m[0][1] = Cavalier("white", [0, 1])
        self.m[0][2] = Elephant("white", [0, 2])
        self.m[0][3] = Conseiller("white", [0, 3])
        self.m[0][4] = General("white", [0, 4])
        self.m[0][5] = Conseiller("white", [0, 5])
        self.m[0][6] = Elephant("white", [0, 6])
        self.m[0][7] = Cavalier("white", [0, 7])
        self.m[0][8] = Char("white", [0, 8])

        # Black pieces
        self.m[9][0] = Char("black", [9, 0])
        self.m[9][1] = Cavalier("black", [9, 1])
        self.m[9][2] = Elephant("black", [9, 2])
        self.m[9][3] = Conseiller("black", [9, 3])
        self.m[9][4] = General("black", [9, 4])
        self.m[9][5] = Conseiller("black", [9, 5])
        self.m[9][6] = Elephant("black", [9, 6])
        self.m[9][7] = Cavalier("black", [9, 7])
        self.m[9][8] = Char("black", [9, 8])

        # Soldiers
        for i in range(0, 9, 2):
            self.m[3][i] = Soldat("white", [3, i])
            self.m[6][i] = Soldat("black", [6, i])

        # Cannons
        self.m[2][1] = Canon("white", [2, 1])
        self.m[2][7] = Canon("white", [2, 7])
        self.m[7][1] = Canon("black", [7, 1])
        self.m[7][7] = Canon("black", [7, 7])

        self.current_turn = 'white'
        self.piece_selectionnee = None
        self.historique = []
        self.piece_capturee = None

    def clone_state(self):
        clone = Game(self.plateau)
        clone.current_turn = self.current_turn
        clone.m = copy.deepcopy(self.m)
        clone.piece_selectionnee = None
        return clone

    def get_piece(self, pos):
        if not (0 <= pos[0] < NOMBRE_LIGNES and 0 <= pos[1] < NOMBRE_COLONNES):
            return None
        return self.m[pos[0]][pos[1]]

    def set_piece(self, pos, p):
        self.m[pos[0]][pos[1]] = p

    def line_of_sight(self):
        pos1 = self.find_general('white')
        pos2 = self.find_general('black')
        if pos1[1] == pos2[1]:
            for i in range(pos1[0] + 1, pos2[0]):
                if self.m[i][pos1[1]]:
                    return False
            return True
        return False

    def is_check(self):
        if self.line_of_sight():
            return True
        pos = self.find_general(self.current_turn)
        for row in self.m:
            for piece in row:
                if piece and piece.color != self.current_turn:
                    if pos in piece.possible_moves(self):
                        return True
        return False

    def find_general(self, color):
        for row in self.m:
            for piece in row:
                if piece and piece.type == 'General' and piece.color == color:
                    return piece.position

    def check_mate(self):
        for row in self.m:
            for piece in row:
                if piece and piece.color == self.current_turn:
                    if piece.valid_moves(self):
                        return False
        return True

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
                if self.check_mate():
                    pygame.quit()
                    sys.exit()
                pos_souris = pygame.mouse.get_pos()
                row, col = self.get_mouse_location(pos_souris)
                pos = [row, col]
                # Vérifie si une pièce est sélectionnée
                if self.piece_selectionnee:
                    if pos in self.piece_selectionnee.valid_moves(self):
                        self.piece_selectionnee.move(pos, self)
                        self.piece_selectionnee = None
                        # Changer de tour
                        self.current_turn = "black" if self.current_turn == "white" else "white"
                    else:
                        # Si le clic ne correspond pas à un mouvement valide, désélectionner la pièce
                        self.piece_selectionnee = None
                    self.mettre_a_jour()
                else:
                    # Sélectionner une pièce si elle appartient au joueur actuel
                    piece = self.get_piece(pos)
                    if piece and piece.color == self.current_turn:
                        self.piece_selectionnee = piece
                    self.mettre_a_jour()

    def mettre_a_jour(self):
        """Actualise le plateau."""


        # Optionnel: Mettre en évidence les mouvements possibles
        if self.piece_selectionnee:
            moves = self.piece_selectionnee.valid_moves(self)

            self.plateau.dessiner(self.ecran)
            for move in moves:
                x = move[1] * TAILLE_CASE + TAILLE_CASE // 2
                y = move[0] * TAILLE_CASE + TAILLE_CASE // 2
                rayon = TAILLE_CASE // 6
                pygame.draw.circle(self.ecran, "red", (x, y), rayon)
            for row in self.m:
                for piece in row:
                    if piece:
                        piece.dessiner(self.ecran)
        else: 
            self.plateau.dessiner(self.ecran)
            for row in self.m:
                for piece in row:
                    if piece:
                        piece.dessiner(self.ecran)
        pygame.display.flip()
    
    
    
    def lancer(self):
        clock = pygame.time.Clock()
        self.mettre_a_jour()
        while True:
            self.handle_click()
            #self.mettre_a_jour()
            clock.tick(60)  # Limite à 60 FPS

# Initialisation du jeu
if __name__ == "__main__":
    plateau = Board()
    jeu = Game(plateau)
    jeu.lancer()
