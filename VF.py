
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 17:02:13 2025

@author: jlbou
"""

import pygame
import sys
import copy
import pygame.surfarray
import numpy as np

pygame.init()
pygame.mixer.init()

# Constantes globales
NOMBRE_LIGNES = 10       # Nombre de lignes
NOMBRE_COLONNES = 9      # Nombre de colonnes
TAILLE_CASE = 50         # Taille d'une case en pixels
TAILLE_FENETRE_LARGEUR = NOMBRE_COLONNES * TAILLE_CASE
TAILLE_FENETRE_HAUTEUR = NOMBRE_LIGNES * TAILLE_CASE

#son_explosion = pygame.mixer.Sound("awp-shoot-sound-effect-cs_go.mp3")
sound_victory = pygame.mixer.Sound("sons/victory.mp3") 
sound_capture = pygame.mixer.Sound("sons/capture.mp3")
sound_check = pygame.mixer.Sound("sons/check.wav")
sound_loss = pygame.mixer.Sound("sons/loss.mp3")
sound_move =  pygame.mixer.Sound("sons/move.wav")

# Couleurs
COULEUR_FOND1=(185,156,107)
COULEUR_FOND = (255, 255, 255)   # Blanc pour le fond
COULEUR_LIGNE = (0, 0, 0)        # Noir pour les lignes
mouvement_faux_demande = False
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
        print("mouvement possibles =", moves)
        for pos in moves:
            # Simulate a move on a copy of the state of the game
            game_clone = game.clone_state()
            piece_clone = game_clone.get_piece(self.position)

            # Verify that the clone piece exists
            if piece_clone is None:
                print("piece_clone is None")
                continue
            else:
                print("piece clone not none")

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
        if captured:
            sound_capture.play()
        else : 
            sound_move.play()
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
                if piece and piece.__class__.__name__ == 'General' and piece.color == color:
                    return piece.position

    def check_mate(self):
        for row in self.m:
            for piece in row:
                if piece and piece.color == self.current_turn:
                    if piece.valid_moves(self):
                        return False
        sound_loss.play()
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
                    sound_victory.play()
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
                        if self.is_check():
                            sound_check.play()
                    else:
                        # If the movement is not allowed, deselect the piece and print a text asking to make a legal move
                        global mouvement_faux_demande
                        self.piece_selectionnee = None
                        mouvement_faux_demande = True
                        # on affiche le texte dans la fonction mettre_a_jour
                    self.mettre_a_jour()
                else:
                    # Select a piece if the player possesses it
                    piece = self.get_piece(pos)
                    if piece and piece.color == self.current_turn:
                        self.piece_selectionnee = piece
                    self.mettre_a_jour()

    def mettre_a_jour(self):
        global mouvement_faux_demande
        """Actualise le plateau."""
        if self.piece_selectionnee:
            moves = self.piece_selectionnee.valid_moves(self)

            self.plateau.dessiner(self.ecran)
            for move in moves:
                x = move[1] * TAILLE_CASE + TAILLE_CASE // 2
                y = move[0] * TAILLE_CASE + TAILLE_CASE // 2
                rayon = TAILLE_CASE // 6
                if self.m[move[0]][move[1]]!=None:
                    print("self.m ")
                    print(self.m)
                    print("l'element dans la case")
                    print(self.m[move[0]][move[1]])
                    pygame.draw.circle(self.ecran, "red", (x, y), int(2.3 * rayon))
                else:
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
        "si le joeur demande un mouvement interdit, affichez un meessage d'erreur"
        if mouvement_faux_demande: 
            font = pygame.font.SysFont(None, 30)
            text_surface = font.render("Selectionnez un mouvement autorisé", True, (255, 255, 255))
            clock = pygame.time.Clock()
            self.ecran.blit(text_surface, (50, 50))
            pygame.display.flip()
            mouvement_faux_demande = False
                        
            
    
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

