from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from damesiu.controllers import BoardController
    from damesiu.controllers import GameController

from damesiu.game_state import GameState
from damesiu.board_selector import BoardSelector
import random
from time import sleep


def turn(board: BoardController, game_controller: GameController):
    sleep(0.2)
    board_selector = BoardSelector(board)
    game_state = GameState()
    eat_moves = []
    moves = []
    if game_state.pion_lock:
        for eat_move_lock in game_state.pion_lock.get_playable_cells(direction='all'):
            eat_moves.append((game_state.pion_lock, eat_move_lock))

    else:
        eat_moves = game_state.current_player.get_all_moves(only_eat=True)
        moves = game_state.current_player.get_all_moves()
    if len(eat_moves) > 0:
        move = random.choice(eat_moves)
        board_selector.selected_cell = move[0].cell
        game_controller.move(source=move[0].cell, target=move[1])
    else:
        if len(moves) == 0:
            game_controller.move(source=None, target=None)
            return
        move = random.choice(moves)
        board_selector.selected_cell = move[0].cell
        game_controller.move(source=move[0].cell, target=move[1])

# def minmax(self, pion, depth, maxim, board):
#     if depth == 0:
#         return self.score_position(board)
#
#     if maxim:
#         max_eval = float("-inf")
#         the_move = None
#         for move in self.all_moves(pion, board):
#             eval = self.minmax(move, depth - 1, False, board)
#             max_eval = max(max_eval, eval)
#             if max_eval == eval:
#                 the_move = move
#         return max_eval, the_move
#     else:
#         min_eval = float("inf")
#         the_move = None
#         for move in self.all_moves(pion, board):
#             eval = self.minmax(move, depth - 1, True, board)
#             min_eval = min(min_eval, eval)
#             if min_eval == eval:
#                 the_move = move
#         return min_eval, the_move
#
# def simul_move(self, pion, move, game_controller, skip):
#     game_controller.move(pion, move[0], move[1])
#     if skip:
#         skip(game_controller, move[0], move[1])
#     return game_controller
#
# def skip(self, board, start_position, end_position):
#     jumped_position = ((start_position[0] + end_position[0]) // 2, (start_position[1] + end_position[1]) // 2)
#     board.remove_piece(jumped_position)
#
# def all_moves(self, pion, board):
#     moves = []
#     true_moves = pion.get_playable_cells(board)
#     for move, skip in true_moves.items():
#         new_board = self.simul_move(pion, move, board, skip)
#         moves.append([new_board, pion])
#         if skip:
#             moves_after_jump = self.all_moves(pion, new_board)
#             moves.extend(moves_after_jump)
#
#     return moves
#
# def best_coup(self, board, depth):
#     the_coup = self.minmax(None, depth, True, board)
#     return the_coup
#
# def score_position(self, board: BoardController, joueur_code):
#     score = 0
#
#     for pion in board.pions():
#         if pion.player.playercode == joueur_code:
#             score += self.evaluer_position_pion(pion)
#             if pion.dame:
#                 score += 2
#             if self.sauts_dispo(pion, board):
#                 score += 3
#         else:
#             score -= self.evaluer_position_pion(pion)
#             if pion.dame:
#                 score -= 2
#             if self.sauts_dispo(pion, board):
#                 score -= 3
#     return score
#
# def evaluer_position_pion(pion: Pion):
#     playable_cells = pion.get_playable_cells()
#     position_score = len(playable_cells)
#     return position_score
#
# def sauts_dispo(pion: Pion, board: BoardController):
#     playable_cells = pion.get_playable_cells()
#     sauts_disponibles = any(playable_cells)
#     return sauts_disponibles
