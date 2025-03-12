# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 15:00:11 2025

@author: jlbou
"""

import pygame
import sys
import copy

pygame.init()
pygame.mixer.init()

# Constantes globales
NOMBRE_LIGNES = 10       # Nombre de lignes
NOMBRE_COLONNES = 9      # Nombre de colonnes
TAILLE_CASE = 50         # Taille d'une case en pixels
TAILLE_FENETRE_LARGEUR = NOMBRE_COLONNES * TAILLE_CASE
TAILLE_FENETRE_HAUTEUR = NOMBRE_LIGNES * TAILLE_CASE

#son_explosion = pygame.mixer.Sound("awp-shoot-sound-effect-cs_go.mp3")
# sound_victory = 
# sound_capture = 
# sound_check = 


# Couleurs
COULEUR_FOND1=(185,156,107)
COULEUR_FOND = (255, 255, 255)   # Blanc pour le fond
COULEUR_LIGNE = (0, 0, 0)        # Noir pour les lignes

class Piece:
    def __init__(self, color, pos):
        self.color = color   # color of the piece (i.e. indicating its team)
        self.position = pos   # Position of the piece
        self.type = self.__class__.__name__
        self.selection = False   # Boolean True if selected, else False

    def possible_moves(self, game):
        return []

    def valid_moves(self, game):
        valid_moves = []   # List of the valid moves (solve the problem of check and capture)
        moves = self.possible_moves(game)
        for pos in moves:
            # Simulate a move on a copy of the state of the game
            game_clone = game.clone_state()
            piece_clone = game_clone.get_piece(self.position)

            # Verify that the clone piece exists
            if piece_clone is None:
                continue

            # Simulate the move with the clones
            captured = game_clone.get_piece(pos)
            game_clone.set_piece(pos, piece_clone)
            game_clone.set_piece(self.position, None)
            piece_clone.position = pos  # Update the position of the clone

            # Verify that the move does not put our general in check
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
    
    def make_move(self, jeu, movee):
        new_position = jeu.clone_state()  # Crée une copie de la position actuelle
        self.move(movee,new_position)
        '''à modif avec la fonction qui applique un mouvement au jeu'''
        return new_position
##############
# Subclasses #
##############

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
        
        # Squarres where the General can move
        palace_cols = [3, 4, 5]
        palace_rows_white = [0, 1, 2]
        palace_rows_black = [7, 8, 9]
        
        # Allowed movements
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
        # Draw horizontal lines
        for ligne in range(NOMBRE_LIGNES ):
            pygame.draw.line(ecran, COULEUR_LIGNE, (0, TAILLE_CASE/2 + ligne * TAILLE_CASE), (self.largeur, TAILLE_CASE/2 + ligne * TAILLE_CASE), 2)
        # Draw vertical lines
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

        # Initialization of the pieces
        
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
        
        self.pieces_J1=[]
        self.pieces_J2=[]
        
        
        ##evaluation
        self.matrice_char = [[14, 14, 12, 18, 16, 18, 12, 14, 14],[16, 20, 18, 24, 26, 24, 18, 20, 16 ],[12, 12, 12, 18, 18, 18, 12, 12, 12],[12, 18, 16, 22, 22, 22, 16, 18, 12 ],[12, 14, 12, 18, 18, 18, 12, 14, 12],[12, 16, 14, 20, 20, 20, 14, 16, 12],[6, 10, 8 ,14 ,14 ,14 ,8 ,10,6],[4, 8, 6, 14, 12, 14, 6, 8, 4],[8, 4, 8, 16, 8, 16, 8, 4, 8 ],[-2, 10, 6, 14, 12, 14, 6, 10, -2]]

        self.matrice_cavalier = [[4, 8, 16, 12, 4, 12, 16, 8, 4],[4, 10, 28, 16, 8, 16, 28, 10, 4],[12, 14, 16, 20, 18, 20, 16, 14, 12],[8, 24, 18, 24, 20, 24, 18, 24, 8],[6, 16, 14, 18, 16, 18, 14, 16, 6],[4, 12, 16, 14, 12, 14, 16, 12, 4],[2, 6, 8, 6, 10, 6, 8, 6, 2],[4, 2, 8, 8, 4, 8, 8, 2, 4],[0, 2, 4, 4, -2, 4, 4, 2, 0],[0, -4, 0, 0, 0, 0, 0, -4, 0]]

        self.matrice_canon = [[6, 4, 0, -10, -12, -10, 0, 4, 6 ],[2, 2, 0, -4, -14, -4, 0, 2, 2],[2, 2, 0, -10, -8, -10, 0, 2, 2 ],[0, 0, -2, 4, 10, 4, -2, 0, 0 ],[0, 0, 0, 2, 8, 2, 0, 0, 0 ],[-2, 0, 4, 2, 6, 2, 4, 0, -2],[0, 0, 0, 2, 4, 2, 0, 0, 0],[4, 0, 8, 6, 10, 6, 8, 0, 4 ],[0, 2, 4, 6, 6, 6, 4, 2, 0],[0, 0, 2, 6, 6, 6, 2, 0, 0 ]]

        self.matrice_soldat = [[0, 1, 2, 3, 4, 3, 2, 1, 0],[5, 9, 14, 16, 18, 16, 14, 9, 5],[4, 8, 11, 12, 16, 12, 11, 8, 4],[3, 6, 8, 9, 10, 9, 8, 6, 3],[2, 4, 5, 5, 6, 5, 5, 4, 2],[1, 0, 2, 0, 2, 0, 2, 0, 1],[0, 0, -2, 0, 1, 0, -2, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0]]

        self.matrice_elephant = [[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 2, 0, 0, 0, 2, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[2, 0, 0, 0, 4, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 2, 0, 0, 0, 2, 0, 0]]

        self.matrice_conseiller = [[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 1, 0, 1, 0, 0, 0],[0, 0, 0, 0, 2, 0, 0, 0, 0],[0, 0, 0, 1, 0, 1, 0, 0, 0]]

        self.matrice_general = [[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 1, 1, 1, 0, 0, 0],[0, 0, 0, 1, 2, 1, 0, 0, 0],[0, 0, 0, 1, 3, 1, 0, 0, 0]]

        self.valeur_base = {"Conseiller": self.matrice_conseiller, 'Elephant': self.matrice_elephant, 'Cavalier': self.matrice_cavalier, 'Char': self.matrice_char,'Canon': self.matrice_canon, "Soldat": self.matrice_soldat,'General': self.matrice_general}

        self.valeur_capture = {'Conseiller': 2, 'Elephant': 2, 'Cavalier': 4, 'Char': 9,'Canon': 4, 'Soldat': 1,'General':15}


        
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
                if piece and piece.type == "General" and piece.color == color:
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
        x, y = pos_souris           # Collects mouse coords
        colonne = x // TAILLE_CASE  # Converts abscissa in column number
        ligne = y // TAILLE_CASE    # Converts ordiante in row number
        return ligne, colonne

    def handle_click(self):
        """Gère les événements du jeu, comme les clics de souris."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.check_mate():
                    # sound_victory.play()
                    pygame.quit()
                    sys.exit()
            
                pos_souris = pygame.mouse.get_pos()
                row, col = self.get_mouse_location(pos_souris)
                pos = [row, col]
                # Verify if a piece is selected
                if self.piece_selectionnee:
                    if pos in self.piece_selectionnee.valid_moves(self):
                        self.piece_selectionnee.move(pos, self)
                        #son_explosion.play()
                        self.piece_selectionnee = None
                        # Changes the turn
                        self.current_turn = "black" if self.current_turn == "white" else "white"
                    else:
                        # If the movement is not allowed, deselect the piece
                        self.piece_selectionnee = None
                    self.mettre_a_jour()
                else:
                    # Select a piece if the player possesses it
                    piece = self.get_piece(pos)
                    if piece and piece.color == self.current_turn:
                        self.piece_selectionnee = piece
                    self.mettre_a_jour()

    def mettre_a_jour(self):
        """Actualise le plateau."""
        self.pieces_J1=[]
        self.pieces_J2=[]
        
        for row in self.m:
            for piece in row:
                if piece:
                    if piece.color=="white":
                        self.pieces_J1.append(piece)
                    else : 
                        self.pieces_J2.append(piece)
        
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
            if self.current_turn=="black":
                
                _, best_move, best_piece = self.minimax(profondeur=3, joueur_max=True)
                print(best_move)
                print(best_piece)
                print(self.m)
                best_piece.position=best_move
                print(self.m)
                self.current_turn = 'white'
            else:
                self.handle_click()
                #self.mettre_a_jour()
            clock.tick(60)  # Limite à 60 FPS
            
    
            
    def interactions(self,piece): #interactions entre une piece et le plateau (menace, garde, mobilite))
        est_menacé, est_gardé=0,0
        menace,garde=0,0
        pieces_adverses = self.pieces_J2 if self.tour_actuel == "white" else self.pieces_J1
        '''à modif selon qui est blanc/noir'''
        pieces_amies = self.pieces_J1 if self.tour_actuel == "white" else self.pieces_J2
        pos_piece = [piece.ligne,piece.colonne]

        for ami in pieces_amies:
            pos_ami = [ami.ligne,ami.colonne]
            if pos_piece in ami.valid_moves(self):
                '''à modif : mouvements_possibles '''
                est_gardé+=1
            if pos_ami in piece.valid_moves(self):
                garde+=self.valeur_capture[ami.type]

        for adv in pieces_adverses:
            pos_adv = [adv.ligne,adv.colonne]
            if pos_piece in adv.valid_moves(self):
                est_menacé+=1
            if pos_adv in piece.valid_moves(self):
                menace+=self.valeur_capture[adv.type]

        mobilite = len(piece.possible_moves(self))

        return garde,menace,est_gardé,est_menacé,mobilite
    
    def evaluation_piece(self,piece):  #evaluation de l'impact de chaque pièce dans le jeu
        x,y = piece.position[0],piece.position[1]
        evaluate = self.valeur_base[piece.type][x][y]

        bonus=malus=0
        garde,menace,est_gardé,est_menacé,mobilite = self.interactions(piece)
        bonus = bonus + garde + est_gardé + menace + mobilite
        malus = malus + est_menacé*2

        evaluate = evaluate + bonus - malus

        return evaluate
    
    def evaluation_pos(self):  #evaluation globale d'une situation de jeu pour un joueur donné
        pieces_adverses = self.pieces_J1
        pieces_amies = self.pieces_J2
        evaluate=0
        for piece in pieces_adverses:
            evaluate-=self.evaluation_piece(piece)
    
        for piece in pieces_amies:
            evaluate+=self.evaluation_piece(piece)
    
        return evaluate

    def minimax(self, profondeur, joueur_max):
        if profondeur == 0 or self.check_mate():
            return self.evaluation_pos()
    
        best_piece = None
        best_move = None
    
        if joueur_max:  # Tour du joueur
            max_eval = float('-inf')
            for piece in self.pieces_J2:
                for mouv in piece.valid_moves(self):
                    # Clonez l'état actuel avant de simuler le mouvement
                    new_jeu = self.clone_state()
                    new_piece = new_jeu.get_piece(piece.position)
                    new_piece.move(mouv, new_jeu)
                    eval, _, __ = new_jeu.minimax(profondeur - 1, False)
                    if eval > max_eval:  # Mise à jour du meilleur coup
                        max_eval = eval
                        best_move = mouv
                        best_piece = piece
    
            return max_eval, best_move, best_piece
        else:  # Tour de l'adversaire
            min_eval = float('inf')
            for piece in self.pieces_J1:
                for mouv in piece.valid_moves(self):
                    # Clonez l'état actuel avant de simuler le mouvement
                    new_jeu = self.clone_state()
                    new_piece = new_jeu.get_piece(piece.position)
                    new_piece.move(mouv, new_jeu)
                    eval, _, __ = new_jeu.minimax(profondeur - 1, True)
                    if eval < min_eval:  # Mise à jour du pire coup pour MAX
                        min_eval = eval
                        best_move = mouv
                        best_piece = piece
            return min_eval, best_move, best_piece

    # def minimax(self, profondeur, joueur_max):
    #     if profondeur == 0 or self.check_mate():
    #         return self.evaluation_pos()
    #     best_piece=None
    #     best_move = None

    #     if joueur_max:  # Tour du joueur
    #         max_eval = float('-inf')
    #         for piece in self.pieces_J2:
    #             for mouv in piece.valid_moves(self):
    #                 new_jeu = piece.make_move(self, mouv)
    #                 eval,_,__ = new_jeu.minimax(profondeur - 1, False)
    #                 if eval > max_eval:  # Mise à jour du meilleur coup
    #                     max_eval = eval
    #                     best_move = mouv
    #                     best_piece=piece

    #         return max_eval, best_move,best_piece
    #     else:  # Tour de l'adversaire
    #         min_eval = float('inf')
    #         for piece in self.pieces_J1:
    #             for mouv in piece.valid_moves(self):
    #                 new_jeu = piece.make_move(self, mouv)
    #                 eval,_,__ = new_jeu.minimax(profondeur - 1, True)
    #                 if eval < min_eval:  # Mise à jour du pire coup pour MAX
    #                     min_eval = eval
    #                     best_move = mouv
    #                     best_piece=piece
    #         return min_eval, best_move, best_piece
        

# Initialisation du jeu
if __name__ == "__main__":
    
    plateau = Board()
    jeu = Game(plateau)
    jeu.lancer()

