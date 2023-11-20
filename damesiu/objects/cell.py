from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from damesiu.objects import Pion


class Cell:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.highlighted: bool = False
        self.selected: bool = False

        self.neighbors: list[Cell | None] = []
        self._pion: Pion | None = None

    def is_border(self) -> bool:
        if (self.x == 0 or self.y == 0) or (self.x == 9 or self.y == 9):
            return True
        return False

    @property
    def pion(self):
        return self._pion

    @pion.setter
    def pion(self, pion: Pion):
        if self._pion is None:
            self._pion = pion
        else:
            raise Exception("La cellule est déjà occupée")
