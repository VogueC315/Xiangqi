def evaluate_position(piece):
    score = 0

    piece_values = {Conseiller: 200, Elephant: 200, Cavalier: 400, Char: 900,Canon: 500, Soldat: 100,General:float('inf')}

    valeur = piece_values.get(type(piece), 0)
    #calcul des bonus de position...
    position_bonus = 0

    if type(piece) == Soldat and riviere(piece):
        position_bonus+=100

    if zone_centrale(piece):
        if type(piece) == Char :
            position_bonus+=10
        if type(piece) == Char :
            position_bonus+=8
        else:
            position_bonus+=5

    #calcul des pénalités...

    #calcul du score de mobilité
    mobilite = len(piece.get_mouvements(position)) * 2


    piece_score = (valeur + position_bonus + mobilite)

    return piece_score

def minmax(board, depth, maximizing_player):
    if depth == 0 or game_over(board):
        return evaluate_position(board, maximizing_player)

    if maximizing_player:
        max_eval = float('-inf')
        for move in get_possible_moves(board):
            evaluation = minmax(make_move(board, move), depth - 1, False)
            max_eval = max(max_eval, evaluation)
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_possible_moves(board):
            evaluation = minmax(make_move(board, move), depth - 1, True)
            min_eval = min(min_eval, evaluation)
        return min_eval

