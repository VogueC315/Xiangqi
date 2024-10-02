# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 11:06:53 2024

@author: jlbou
"""


##################
# Echecs chinois #
##################

class Piece:
    def __init__(self, color):
        self.color = color
    
    # Vérification de la validité d'un mouvement
    def is_valid_move(self, start_pos, end_pos, board):
        raise NotImplementedError("This method should be overridden by subclasses")
    
    # Vérifie si une position est dans une zone donnée
    def is_in_allowed_zone(self, pos, allowed_columns=None, allowed_rows=None):
        # Vérifie si une position est dans une zone donnée (colonnes ou lignes spécifiques)
        if allowed_columns is not None and pos[0] not in allowed_columns:
            return False
        if allowed_rows is not None and pos[1] not in allowed_rows:
            return False
        return True

    # Vérifie si une pièce se trouve sur la trajectoire du coups
    def is_path_clear(self, start_pos, end_pos, board):
        start_col, start_row = start_pos
        end_col, end_row = end_pos

        # Cas où le mouvement est vertical (colonne inchangée)
        if start_col == end_col:
            step = 1 if start_row < end_row else -1
            for row in range(start_row + step, end_row, step):
                if board[start_col][row] is not None:
                    return False

        # Cas où le mouvement est horizontal (ligne inchangée)
        elif start_row == end_row:
            step = 1 if start_col < end_col else -1
            for col in range(start_col + step, end_col, step):
                if board[col][start_row] is not None:
                    return False

        # Cas où le mouvement est diagonal
        elif abs(end_col - start_col) == abs(end_row - start_row):
            step_col = 1 if end_col > start_col else -1
            step_row = 1 if end_row > start_row else -1
            for col, row in zip(range(start_col + step_col, end_col, step_col), range(start_row + step_row, end_row, step_row)):
                if board[col][row] is not None:
                    return False

        # Si aucune pièce n'est sur le chemin, le chemin est dégagé
        return True

    def __str__(self):
        return self.symbol


class General(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '帅' if color == 'white' else '将'
        
    # Définition des mouvements du Général
    def is_valid_move(self, start_pos, end_pos, board):
        if self.color == 'white':
            # Roi blanc restreint aux colonnes 2, 3 et lignes 5, 6
            if not self.is_in_allowed_zone(end_pos, allowed_columns=range(3, 6), allowed_rows=range(0, 3)):
                return False
        else:
            # Roi noir restreint aux colonnes 0, 1 et lignes 0, 1
            if not self.is_in_allowed_zone(end_pos, allowed_columns=range(3, 6), allowed_rows=range(7, 10)):
                return False
        
        dx = abs(start_pos[0] - end_pos[0])
        dy = abs(start_pos[1] - end_pos[1])
        return (dx == 1 and dy == 0) or (dx == 0 and dy == 1) 
    
    
class Conseiller(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '仕' if color == 'white' else '士'
            
    # Définition des mouvement du Conseiller
    def is_valid_move(self, start_pos, end_pos, board):
        if self.color == 'white':
            # Roi blanc restreint aux colonnes 2, 3 et lignes 5, 6
            if not self.is_in_allowed_zone(end_pos, allowed_columns=range(3, 6), allowed_rows=range(0, 3)):
                return False
        else:
            # Roi noir restreint aux colonnes 0, 1 et lignes 0, 1
            if not self.is_in_allowed_zone(end_pos, allowed_columns=range(3, 6), allowed_rows=range(7, 10)):
                return False
        
        dx = abs(start_pos[0] - end_pos[0])
        dy = abs(start_pos[1] - end_pos[1])  
        return dx == 1 and dy == 1
   
     
class Elephant(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '相' if color == 'white' else '象'
            
    # Définition des mouvement du Elephant
    def is_valid_move(self, start_pos, end_pos, board):
        if self.color == 'white':
            # Roi blanc restreint aux colonnes 2, 3 et lignes 5, 6
            if not self.is_in_allowed_zone(end_pos, allowed_rows=range(0, 5)):
                return False
        else:
            # Roi noir restreint aux colonnes 0, 1 et lignes 0, 1
            if not self.is_in_allowed_zone(end_pos, allowed_rows=range(6, 10)):
                return False
        
        dx = abs(start_pos[0] - end_pos[0])
        dy = abs(start_pos[1] - end_pos[1])  
        return dx == 2 and dy == 2
 
        
class Cavalier(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '傌' if color == 'white' else '马'

    # Définition des mouvement du Cavalier
    def is_valid_move(self, start_pos, end_pos, board):
        dx = abs(start_pos[0] - end_pos[0])
        dy = abs(start_pos[1] - end_pos[1]) 
        return (dx == 2 and dy == 1) or (dx == 1 and dy == 2) 


class Char(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '俥' if color == 'white' else '車'
      
    # Définition des mouvement du Char
    def is_valid_move(self, start_pos, end_pos, board):
        return start_pos[0] == end_pos[0] or start_pos[1] == end_pos[1] 


class Canon(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '炮' if color == 'white' else '砲'
    
    # Définition des mouvement du Canon
    def is_valid_move(self, start_pos, end_pos, board):
        return start_pos[0] == end_pos[0] or start_pos[1] == end_pos[1]  

class Soldat(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '兵' if color == 'white' else '卒'
    
    # Définition des mouvement du Soldat
    def is_valid_move(self, start_pos, end_pos, board):
        if self.color == 'white':
            if start_pos[1] <= 4:
                if end_pos[1] == start_pos[1] + 1:
                    return True
            else :
                dx = abs(end_pos[0] - start_pos[0])
                dy = abs(end_pos[1] - start_pos[1])
                return dx <= 1 and dy <= 1
        elif self.color == 'black' :
            if start_pos[1] >= 5:
                if end_pos[1] == start_pos[1] - 1:
                    return True
            else :
                dx = abs(end_pos[0] - start_pos[0])
                dy = abs(end_pos[1] - start_pos[1])
                return dx <= 1 and dy <= 1
        else :
            return False
        

class Board:
    def __init__(self):
        self.board = [[None for _ in range(9)] for _ in range(9)]
        self.setup_board()

    def setup_board(self):
        for i in range(0,9,2):
            self.board[i][3] = Soldat('white')
            self.board[i][6] = Soldat('black')

        pieces = [Char, Cavalier, Elephant, Conseiller, General, Conseiller, Elephant, Cavalier, Char]

        for i, piece in enumerate(pieces):
            self.board[i][0] = piece('white')
            self.board[i][8] = piece('black')

        self.board[1][2] = Canon('white')
        self.board[-2][2] = Canon('white')
        self.board[1][7] = Canon('black')
        self.board[-2][7] = Canon('black')

    def print_board(self):
        for row in range(9):
            print(' '.join([str(self.board[col][row]) if self.board[col][row] else '.' for col in range(9)]))
        print()

    def move_piece(self, start_pos, end_pos):
        piece = self.board[start_pos[0]][start_pos[1]]
        if piece and piece.is_valid_move(start_pos, end_pos, self.board):
            self.board[end_pos[0]][end_pos[1]] = piece
            self.board[start_pos[0]][start_pos[1]] = None
        else:
            print("Invalid move!")


class Game:
    def __init__(self):
        self.board = Board()
        self.turn = 'white'

    def play(self):
        while True:
            self.board.print_board()
            print(f"{self.turn}'s turn")
            start_pos = self.get_position("Enter the start position (e.g. 'a2'): ")
            end_pos = self.get_position("Enter the end position (e.g. 'a3'): ")

            self.board.move_piece(start_pos, end_pos)
            self.switch_turn()

    def switch_turn(self):
        self.turn = 'black' if self.turn == 'white' else 'white'

    def get_position(self, prompt):
        pos = input(prompt)
        col = ord(pos[0]) - ord('a')
        row = int(pos[1]) - 1
        return (col, row)


if __name__ == '__main__':
    game = Game()
    game.play()
