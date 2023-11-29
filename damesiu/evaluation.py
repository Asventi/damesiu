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

