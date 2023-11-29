from damesiu.objects import BoardController, Pion

def score_position(board: BoardController, joueur_code):
    score = 0

    for pion in board.pions():
        if pion.player.playercode == joueur_code:
            score += evaluer_position_pion(pion)
            if pion.dame:
                score += 2
            if sauts_dispo(pion, board):
                score += 3
        else:
            score -= evaluer_position_pion(pion)
            if pion.dame:
                score -= 2
            if sauts_dispo(pion, board):
                score -= 3
    return score

def evaluer_position_pion(pion: Pion):
    playable_cells = pion.get_playable_cells()
    position_score = len(playable_cells)
    return position_score

def sauts_dispo(pion: Pion, board: BoardController):
    playable_cells = pion.get_playable_cells()
    sauts_disponibles = any(playable_cells)
    return sauts_disponibles
