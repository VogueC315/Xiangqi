import pygame
import sys
from stable_baselines3 import PPO
from Environnement_IA import XiangqiEnv
from VF import Game, Board  # on réutilise ton jeu local
import numpy as np

# Initialisation
pygame.init()

# Charger le modèle entraîné et l'environnement IA
model = PPO.load("ppo_xiangqi_model")
env = XiangqiEnv()
obs, _ = env.reset()

# Créer le plateau et la version graphique du jeu
plateau = Board()
jeu = Game(plateau)
jeu.mettre_a_jour()

# Fonction utilitaire pour mettre à jour jeu.m à partir de env.state
def update_jeu_from_env():
    game_from_env = env.state_to_game()
    jeu.m = game_from_env.m
    jeu.current_turn = game_from_env.current_turn
    """
    print("Général blanc :", any(piece and piece.__class__.__name__ == "General" and piece.color == "white" for row in jeu.m for piece in row))
    print("Général noir :", any(piece and piece.__class__.__name__ == "General" and piece.color == "black" for row in jeu.m for piece in row))
    for i, row in enumerate(jeu.m):
        for j, p in enumerate(row):
            if p:
                print(f"({i},{j}) → {p.__class__.__name__}, {getattr(p, 'color', '?')}, {getattr(p, 'type', '?')}")
                """

def jeu_to_state(jeu):
    """
    Convertit l’état actuel de jeu.m (Game) en tenseur d’état (14, 10, 9)
    compatible avec l’environnement IA.
    """
    state = np.zeros((14, 10, 9), dtype=np.float32)

    # Mapping des types de pièces vers les canaux
    type_to_channel = {
        'General': 0,
        'Conseiller': 1,
        'Elephant': 2,
        'Cavalier': 3,
        'Char': 4,
        'Canon': 5,
        'Soldat': 6
    }

    for i in range(10):  # lignes
        for j in range(9):  # colonnes
            piece = jeu.m[i][j]
            if piece is not None:
                base_channel = type_to_channel.get(piece.__class__.__name__)
                if base_channel is None:
                    continue  # Ignore les types inconnus
                channel = base_channel if piece.color == 'white' else base_channel + 7
                state[channel, i, j] = 1.0

    return state

def jouer_coup_ia():
    global obs
    action, _ = model.predict(obs)
    obs, reward, done, truncated, info = env.step(action)
    

   
    """ 
    generals = {
        "white": np.sum(env.state[0]),  # canal 0 = white general
        "black": np.sum(env.state[7])   # canal 7 = black general
    }
    print("Présence des généraux dans le tenseur :")
    print(generals)    
    """
    update_jeu_from_env()
    jeu.mettre_a_jour()


# Boucle principale
clock = pygame.time.Clock()
partie_finie = False
while not partie_finie:
    # Tour du joueur humain (blanc)
    if jeu.current_turn == "white":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                partie_finie = True
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if jeu.check_mate():
                    #sound_victory.play()
                    partie_finie = True
                    pygame.quit()
                    sys.exit()
                pos_souris = pygame.mouse.get_pos()
                row, col = jeu.get_mouse_location(pos_souris)
                pos = [row, col]
                # Verify if a piece is selected
                if jeu.piece_selectionnee: 
                    print("moves valides = ",jeu.piece_selectionnee.valid_moves(jeu))
                    if pos in jeu.piece_selectionnee.valid_moves(jeu):
                        print("move impose")
                        jeu.piece_selectionnee.move(pos, jeu)
                        #son_explosion.play()
                        jeu.piece_selectionnee = None
                        #on met à jour le tenseur pour l'IA
                        print("maj tenseur ia impose")
                        env.state = jeu_to_state(jeu)
                        # Changes the turn
                        print("chg turn impose")
                        env.change_current_turn_auto()
                        if jeu.current_turn == "white":
                            jeu.current_turn ="black"
                        else:
                            jeu.current_turn = "white"
                        #if jeu.is_check():
                            #sound_check.play()
                    else:
                        print("move faux demande")
                        # If the movement is not allowed, deselect the piece and print a text asking to make a legal move
                        global mouvement_faux_demande
                        jeu.piece_selectionnee = None
                        mouvement_faux_demande = True
                        # on affiche le texte dans la fonction mettre_a_jour
                    jeu.mettre_a_jour()
                else:
                    # Select a piece if the player possesses it
                    piece = jeu.get_piece(pos)
                    if piece and piece.color == jeu.current_turn:
                        jeu.piece_selectionnee = piece
                    jeu.mettre_a_jour()

            """ elif event.type == pygame.MOUSEBUTTONDOWN:
                print("clic")
                jeu.handle_click()
                previous_state = np.copy(jeu_to_state(jeu))
                new_state = jeu_to_state(jeu)
                # Vérifie si le plateau a changé
                if not np.array_equal(previous_state, new_state):
                    env.state = new_state
                    obs = env.state"""
    else:
        jouer_coup_ia() 
        #pygame.time.wait(300)
        env.change_current_turn_auto()
        """if jeu.current_turn == "white":
            jeu.current_turn ="black"
        else:
            jeu.current_turn = "white"
"""
    clock.tick(60)  # 60 FPS
