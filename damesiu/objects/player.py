from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from damesiu.objects import Pion


class Player:

    def __init__(self, name: str, color: str, playercode: int):
        self.name = name
        self.color = color
        self.playercode = playercode

        self.score: int = 0
        self.pions: list[Pion] = []
        self.is_playing: bool = False
        self.is_winner: bool = False
