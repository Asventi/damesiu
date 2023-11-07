from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from damesiu.objects import Pion


class Cell:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.selected: bool = False

        self._pion: Pion | None = None

    # TODO: Fonction isBorder pour checker si la cellule est en bordure de plateuea
    def is_border(self) -> bool:
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
