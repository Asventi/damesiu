from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from damesiu.objects import Player, Cell
    from damesiu.objects import Cell

from damesiu.constants import directions


class Pion:
    """
    Classe representant un pion, il contient sa position, sa couleur, la cellule dans laquelle il est et le joueur
    auquel il appartient. La couleur sert aussi a representé le joueur auquel il appartient.

    :param y: Position y du pion y etant la ligne
    :param x: Position x du pion x etant la colonne
    :param color: Couleur du pion, white ou black
    :param cell: Cellule dans laquelle se trouve le pion
    :param player: Joueur auquel appartient le pion
    """
    def __init__(self, y: int, x: int, color: str, cell: Cell, player: Player):
        self._x = x
        self._y = y
        self._color = color
        self._player = player
        self._cell = cell
        self._player.pions.append(self)

    def get_playable_cells(self, direction: str = None, only_eat: bool = False) -> List[Cell]:
        """
        Fonction qui retourne les cellules jouables pour le pion, si la direction est None, retourne les cellules
        jouables dans toutes les directions, sinon retourne les cellules jouables dans la direction du pion.
        Peut retourner seulement les cellules jouables pour manger un pion adverse. Quand direction est all only_eat est
        a True dans tout les cas.

        :param direction: Direction dans laquelle chercher les cellules jouables, None ou all
        :param only_eat: Retourne ou pas seulement les cellules jouables pour manger un pion adverse
        :return: Liste des cellules jouables
        :rtype: List[Cell]
        """
        if direction is None:
            direction = directions.N if self.color == 'black' else directions.S
        playable_cells = []

        if direction == 'all':
            if self.get_playable_cell(directions.NE, True) is not None:
                playable_cells.append(self.get_playable_cell(directions.NE, True))

            if self.get_playable_cell(directions.SE, True) is not None:
                playable_cells.append(self.get_playable_cell(directions.SE, True))

            if self.get_playable_cell(directions.NW, True) is not None:
                playable_cells.append(self.get_playable_cell(directions.NW, True))

            if self.get_playable_cell(directions.SW, True) is not None:
                playable_cells.append(self.get_playable_cell(directions.SW, True))

        else:
            if self.get_playable_cell(direction - 1, only_eat=only_eat) is not None:
                playable_cells.append(self.get_playable_cell(direction - 1, only_eat=only_eat))

            if self.get_playable_cell(direction + 1, only_eat=only_eat) is not None:
                playable_cells.append(self.get_playable_cell(direction + 1, only_eat=only_eat))

        return playable_cells

    def get_playable_cell(self, direction: int, only_eat: bool = False) -> Optional[Cell]:
        """
        Fonction qui retourne la cellule jouable dans la entrée en parametre, si aucun mouvement n'est possible
        retourne None, on peut aussi retourner seulement les cellules jouables pour manger un pion adverse.

        :param direction: Direction dans laquelle chercher la cellule jouable
        :param only_eat: Retourne ou pas seulement les cellules jouables pour manger un pion adverse
        :return: Cellule jouable ou None
        :rtype: Optional[Cell]
        """
        neighbor = self.cell.neighbors[direction]

        if neighbor is not None:
            if neighbor.pion is not None:
                if neighbor.pion.color != self.color:
                    neighbor_eat = neighbor.pion.cell.neighbors[direction]
                    if neighbor_eat is not None and neighbor_eat.pion is None:
                        return neighbor_eat
            elif not only_eat:
                return neighbor
        return None

    def delete(self) -> None:
        """
        Supprime le pion, retire le pion de la liste des pions du joueur et supprime le pion de la cellule
        """
        self.cell.pion = None
        self.player.pions.remove(self)

    # Getters Setters
    @property
    def player(self):
        return self._player

    @property
    def cell(self):
        return self._cell

    @cell.setter
    def cell(self, cell: Cell):
        self._cell = cell

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x: int):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y: int):
        self._y = y

    @property
    def color(self):
        return self._color

    def __repr__(self):
        return f"Pion(y: {self.y}, x: {self.x}, {self.color})"
