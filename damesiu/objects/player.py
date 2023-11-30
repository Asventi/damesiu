from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from damesiu.objects import Pion

from damesiu.ia import IA


class Player:

    def __init__(self, name: str, color: str, playercode: int, is_ia: bool = False):
        self.name = name
        self.color = color
        self.playercode = playercode
        self.is_ia = is_ia
        if self.is_ia:
            self.ia = IA()

        self.score: int = 0
        self.pions: list[Pion] = []
        self.is_playing: bool = False
        self.is_winner: bool = False
