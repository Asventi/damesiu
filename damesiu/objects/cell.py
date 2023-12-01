from __future__ import annotations
from typing import TYPE_CHECKING, Optional

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
        self._x = x
        self._y = y
        self._highlighted: bool = False
        self._selected: bool = False
        self._playable: bool = False

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

    # Getters Setters
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

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def highlighted(self):
        return self._highlighted

    @highlighted.setter
    def highlighted(self, highlighted: bool):
        self._highlighted = highlighted

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, selected: bool):
        self._selected = selected

    @property
    def playable(self):
        return self._playable

    @playable.setter
    def playable(self, playable: bool):
        self._playable = playable

    def __repr__(self):
        return f"Cell(y: {self.y}, x: {self.x})"