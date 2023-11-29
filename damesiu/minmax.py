from damesiu.objects import score_position
from damesiu.board_controller import BoardController
from damesiu.game_controller import GameController
from damesiu.objects import Pion
from damesiu.objects import Cell
from damesiu.objects import Player

def minmax(pion, depth, maxim, player, board):
    if depth == 0:
        return score_position.evaluate(board)

    if maxim:
        max_eval = float("-inf")
        the_move = None
        for move in all_moves(pion, board):
            eval = minmax(move, depth - 1, False, player, board)
            max_eval = max(max_eval, eval)
            if max_eval == eval:
                the_move = move
        return max_eval, the_move
    else:
        min_eval = float("inf")
        the_move = None
        for move in all_moves(pion, board):
            eval = minmax(move, depth - 1, True, player, board)
            min_eval = min(min_eval, eval)
            if min_eval == eval:
                the_move = move
        return min_eval, the_move

def simul_move(pion, move, game_controller, skip):
    game_controller.move(pion, move[0], move[1])
    if skip:
        skip(game_controller, move[0], move[1])
    return game_controller

def skip(board, start_position, end_position):
    jumped_position = ((start_position[0] + end_position[0]) // 2, (start_position[1] + end_position[1]) // 2)
    board.remove_piece(jumped_position)

def all_moves(pion, board):
    moves = []
    true_moves = pion.get_playable_cells(board)
    for move, skip in true_moves.items():
        new_board = simul_move(pion, move, board, skip)
        moves.append([new_board, pion])
        if skip:
            moves_after_jump = all_moves(pion, new_board)
            moves.extend(moves_after_jump)

    return moves

def best_coup(player, board, depth):
    the_coup = minmax(None, depth, True, player, board)
    return the_coup