import gymnasium as gym
from gymnasium import spaces
from gymnasium.utils import seeding
import numpy as np
import pygame
from Game import Game
from General import General
from Conseiller import Conseiller
from Char import Char
from Canon import Canon
from Cavalier import Cavalier
from Soldat import Soldat
from Board import Board
from Elephant import Elephant

class XiangqiEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    # Fixe un nombre maximum de coups valides (pour l'action space)
    MAX_VALID_ACTIONS = 100

    def __init__(self):
        super(XiangqiEnv, self).__init__()
        # Observation : tenseur multi-canal de forme (14, 10, 9) avec des float (normalisés entre 0 et 1)
        self.observation_space = spaces.Box(low=0, high=1, shape=(14, 10, 9), dtype=np.float32)
        # Action : indice dans un espace discret [0, MAX_VALID_ACTIONS)
        self.action_space = spaces.Discrete(self.MAX_VALID_ACTIONS)
        # Initialisation de l'état (ici, un tenseur de 14x10x9 rempli de 0)
        self.state = np.zeros((14, 10, 9), dtype=np.float32)
        self.seed()
        self.reset()
        self.current_turn = "white"
        self.move_count = 0  # Compteur de coups
        self.max_moves = 300  # Limite de coups avant troncature
        # Stockera la liste des coups valides pour le joueur courant
        self.valid_actions = []

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def change_current_turn_auto(self):
        if self.current_turn == 'white':
            self.current_turn = 'black'
        else:
            self.current_turn = 'white'

    def change_current_turn(self, couleur):
        self.current_turn = couleur

    def reset(self, seed=None, options=None):
        if seed is not None:
            self.seed(seed)
        # Réinitialiser l'état à zéro
        self.state = np.zeros((14, 10, 9), dtype=np.float32)
        self.change_current_turn('white')
        # -------------------------
        # Initialiser les pièces blanches (channels 0 à 6)
        # -------------------------
        self.state[4, 0, 0] = 1    # Char (exemple) sur la position (0,0) → canal 4
        self.state[4, 0, 8] = 1    # Char sur (0,8)
        self.state[3, 0, 1] = 1    # Cavalier sur (0,1) → canal 3
        self.state[3, 0, 7] = 1    # Cavalier sur (0,7)
        self.state[2, 0, 2] = 1    # Elephant sur (0,2) → canal 2
        self.state[2, 0, 6] = 1    # Elephant sur (0,6)
        self.state[1, 0, 3] = 1    # Conseiller sur (0,3) → canal 1
        self.state[1, 0, 5] = 1    # Conseiller sur (0,5)
        self.state[0, 0, 4] = 1    # Général sur (0,4) → canal 0
        for col in range(0, 9, 2):
            self.state[6, 3, col] = 1   # Soldats sur la rangée 3 → canal 6
        self.state[5, 2, 1] = 1    # Canon sur (2,1) → canal 5
        self.state[5, 2, 7] = 1    # Canon sur (2,7)
        # -------------------------
        # Initialiser les pièces noires (channels 7 à 13)
        # -------------------------
        self.state[11, 9, 0] = 1   # Char noir sur (9,0) → canal 11
        self.state[11, 9, 8] = 1   # Char noir sur (9,8)
        self.state[10, 9, 1] = 1   # Cavalier noir sur (9,1) → canal 10
        self.state[10, 9, 7] = 1   # Cavalier noir sur (9,7)
        self.state[9, 9, 2] = 1    # Elephant noir sur (9,2) → canal 9
        self.state[9, 9, 6] = 1    # Elephant noir sur (9,6)
        self.state[8, 9, 3] = 1    # Conseiller noir sur (9,3) → canal 8
        self.state[8, 9, 5] = 1    # Conseiller noir sur (9,5)
        self.state[7, 9, 4] = 1    # Général noir sur (9,4) → canal 7
        for col in range(0, 9, 2):
            self.state[13, 6, col] = 1  # Soldats noirs sur la rangée 6 → canal 13
        self.state[12, 7, 1] = 1   # Canon noir sur (7,1) → canal 12
        self.state[12, 7, 7] = 1   # Canon noir sur (7,7)
        self.move_count = 0
        # Calcul initial des coups valides
        self.valid_actions = self.compute_valid_actions()
        return self.state, {}

    def compute_valid_actions(self):
        """
        Parcourt le plateau via une instance Game et compile la liste
        de tous les coups valides pour le joueur courant.
        Chaque coup est un tuple: (from_row, from_col, to_row, to_col)
        """
        game_instance = self.state_to_game()
        valid_actions = []
        for i in range(10):
            for j in range(9):
                piece = game_instance.get_piece([i, j])
                if piece and piece.color == self.current_turn:
                    for move in piece.possible_moves(game_instance):
                        valid_actions.append((i, j, move[0], move[1]))
        return valid_actions


    def state_to_game(self):
        board_matrix = [[None for _ in range(9)] for _ in range(10)]
        white_mapping = {
            0: General,
            1: Conseiller,
            2: Elephant,
            3: Cavalier,
            4: Char,
            5: Canon,
            6: Soldat
        }
        black_mapping = {
            7: General,
            8: Conseiller,
            9: Elephant,
            10: Cavalier,
            11: Char,
            12: Canon,
            13: Soldat
        }
        # Debug : vérifier où sont les généraux dans self.state
        """
        white_gen_coords = np.argwhere(self.state[0] > 0.01)
        black_gen_coords = np.argwhere(self.state[7] > 0.01)
        print("Coordonnées général blanc dans self.state:", white_gen_coords)
        print("Coordonnées général noir dans self.state:", black_gen_coords)
        """
        # Reconstruction des pièces
        for i in range(10):
            for j in range(9):
                for channel in range(14):
                    if self.state[channel, i, j] > 0.01:
                        if channel < 7:
                            piece_class = white_mapping[channel]
                            color = "white"
                        else:
                            piece_class = black_mapping[channel]
                            color = "black"
                        piece = piece_class(color, [i, j])
                        board_matrix[i][j] = piece
        
                        """if piece.__class__.__name__ == "General":
                            print(f"Créé : Général {color} à {i, j}")
                        """
                        break

    
        # Création du Game proprement avec le plateau
        board = Board()
        game = Game(board)
    
        # On injecte manuellement la matrice, mais on garde les autres attributs du constructeur
        game.m = board_matrix
        print(game.m)
        
        # Vérification directe dans jeu.m
        """
        found_white = any(p for row in board_matrix for p in row if p and p.__class__.__name__ == "General" and p.color == "white")
        found_black = any(p for row in board_matrix for p in row if p and p.__class__.__name__ == "General" and p.color == "black")
        print("Général blanc dans board_matrix :", found_white)
        print("Général noir dans board_matrix :", found_black)
        """
        game.current_turn = self.current_turn
        game.piece_selectionnee = None
    
        return game




    def echec_et_mat(self):
        game_instance = self.state_to_game()
        # On suppose que check_mate() retourne True si c'est checkmate
        result = game_instance.check_mate()
        # Si le résultat est None, on considère que c'est une fin de partie
        if result is None:
            return True
        return result

    def step(self, action_index):
        # Recalculer la liste des coups valides à chaque étape
        self.valid_actions = self.compute_valid_actions()
        num_valid = len(self.valid_actions)
        if num_valid == 0:
            return self.state, -100, True, True, {"error": "Aucune action valide possible"}

        # Si l'indice d'action est hors des bornes, on le force à choisir le dernier coup valide et on applique une pénalité
        if action_index >= num_valid:
            action = self.valid_actions[-1]
            penalty = -10
        else:
            action = self.valid_actions[action_index]
            penalty = 0

        from_row, from_col, to_row, to_col = action
        game_instance = self.state_to_game()
        piece = game_instance.get_piece([from_row, from_col])
        if piece is None:
            print(f"Aucune pièce trouvée à la position {from_row}, {from_col}")
            return self.state, -100, True, False, {"error": "Mouvement invalide, aucune pièce à déplacer"}

        legal_moves = piece.possible_moves(game_instance)
        # Vérification de sécurité : normalement, action doit être dans legal_moves
        if (to_row, to_col) not in legal_moves:
            return self.state, -100, True, False, {"error": "Mouvement non valide"}
        
        # Recherche du canal de la pièce
        piece_channel = None
        for channel in range(self.state.shape[0]):
            if self.state[channel, from_row, from_col] == 1:
                piece_channel = channel
                break
        if piece_channel is None:
            return self.state, -5, True, False, {"error": "Aucune pièce à la position de départ"}

        # Retirer la pièce de la position de départ
        self.state[piece_channel, from_row, from_col] = 0

        # Gestion d'une capture (si une pièce est présente à la destination)
        capture = False
        captured_channel = None
        for channel in range(self.state.shape[0]):
            if self.state[channel, to_row, to_col] == 1:
                capture = True
                captured_channel = channel
                self.state[channel, to_row, to_col] = 0  # Retirer la pièce adverse
                break
        # Placer la pièce à la destination
        self.state[piece_channel, to_row, to_col] = 1
        self.move_count += 1

        # Calcul du reward de base
        reward = 1 + penalty
        if capture:
            piece_values = {
                0: 100, 1: 2, 2: 2, 3: 4, 4: 8, 5: 5, 6: 1,
                7: 100, 8: 2, 9: 2, 10: 4, 11: 8, 12: 5, 13: 1
            }
            reward = piece_values.get(captured_channel, 5) + penalty

        # Vérifier si c'est échec et mat
        if self.echec_et_mat():
            reward += 100
            done = True
        else:
            done = False

        # Si trop de coups ont été joués, tronquer l'épisode
        if self.move_count >= self.max_moves:
            reward += -10
            done = True
            truncated = True
        else:
            truncated = False

        info = {}
        self.change_current_turn_auto()
        return self.state, reward, done, truncated, info

    def render(self, mode='human'):
        print("État actuel (représentation multi-canal) :")
        print(self.state)

    def close(self):
        pygame.quit()

# Exemple d'utilisation
if __name__ == "__main__":
    env = XiangqiEnv()
    obs, _ = env.reset()
    env.render()
    
    # Exemple : tester avec une action aléatoire basée sur les coups valides
    # Note : ici, on utilise l'index d'une action à partir de la liste valid_actions
    valid_actions = env.compute_valid_actions()
    if len(valid_actions) > 0:
        action_index = 0  # Prendre le premier coup valide
    else:
        action_index = 0  # Pas d'action valide disponible
    obs, reward, done, truncated, info = env.step(action_index)
    env.render()
    env.close()
