from __future__ import annotations
from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from damesiu.objects import Pion


class Cell:
    """
    Classe représentant une cellule du plateau, elle contient un pion ou pas, le tableau est composé de cellules.
    Il y a tout les voisins de la cellule, et des attributs pour savoir si la cellule est selectionné, jouable ou
    highlighté.

    :param y: Position y de la cellule y etant la ligne
    :param x: Position x de la cellule x etant la colonne
    """
    def __init__(self, y: int, x: int):
        self.x = x
        self.y = y
        self.highlighted: bool = False
        self.selected: bool = False
        self.playable: bool = False

        self.neighbors: list[Cell | None] = []
        self._pion: Optional[Pion] = None

    def is_border(self) -> bool:
        """
        Fonction qui retourne si la cellule est une bordure ou pas, censé etre utilisé pour l'ia mais finalement pas
        utilisé, toujours presente si besoin.

        :return: True si la cellule est une bordure, False sinon
        :rtype: bool
        """
        if (self.x == 0 or self.y == 0) or (self.x == 9 or self.y == 9):
            return True
        return False

    @property
    def pion(self):
        return self._pion

    @pion.setter
    def pion(self, pion: Optional[Pion]):
        if self._pion is None or pion is None:
            self._pion = pion
            if self._pion is not None:
                self._pion.y = self.y
                self._pion.x = self.x
                self._pion.cell = self
        else:
            raise Exception("La cellule est deja occupé par un pion")
