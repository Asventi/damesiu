from __future__ import annotations
from typing import TYPE_CHECKING, List, Tuple

if TYPE_CHECKING:
    from damesiu.objects import Pion
    from damesiu.objects import Cell

from damesiu.graphic_engine import GraphicEngine
from time import sleep
from damesiu.game_state import GameState

class Player:

    def __init__(self, name: str, color: str, playercode: int, is_ia: bool = False):
        self.name = name
        self.color = color
        self.playercode = playercode
        self.is_ia = is_ia

        self._score: int = 0
        self.pions: list[Pion] = []
        self.is_playing: bool = False
        self.is_winner: bool = False

    def get_all_moves(self, only_eat: bool = False) -> List[Tuple[Pion, Cell]]:
        """
        Retourne la liste de tous les mouvements possibles pour le joueur, pour chaque pion

        :param only_eat: Retourne ou pas seulement les cellules jouables pour manger un pion adverse
        :return: Liste des cellules jouables
        :rtype: List[Tuple[Pion, Cell]]
        """
        moves = []
        for pion in self.pions:
            for move in pion.get_playable_cells(only_eat=only_eat):
                moves.append((pion, move))
        return moves

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score: int):
        graphic_engine = GraphicEngine()
        self._score = score
        graphic_engine.set_score(self._score, self.name, self.playercode)
        if self._score >= 20:
            game_state = GameState()
            graphic_engine.add_message(f'Le joueur {self.name} a gagne')
            sleep(5)
            game_state.game_ended = True
            exit()
