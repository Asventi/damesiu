from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from damesiu.objects import Pion

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
