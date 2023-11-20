from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from damesiu.objects import Player
    from damesiu.objects import Cell

from damesiu.constants import directions


class Pion:
    def __init__(self, x: int, y: int, color: str, cell: Cell, player: Player):
        self.ligne = x
        self.colonne = y
        self.color = color
        self.player = player

        self.cell = cell
        self.queen: bool = False

    def get_playable_cells(self) -> list[Cell]:
        neighbors = self.cell.neighbors
        neighbor_nw = neighbors[directions.NW]
        neighbor_ne = neighbors[directions.NE]
        playable_cells = []

        if neighbor_nw is not None:
            if neighbor_nw.pion is not None:
                # TODO: Logique si il y a un pion pour verifier derriere si on peut bouffer sa grand mere la pute
                pass
            else:
                playable_cells.append(neighbor_nw)

        if neighbor_ne is not None:
            if neighbor_ne.pion is not None:
                # TODO: Logique si il y a un pion pour verifier derriere si on peut bouffer sa grand mere la pute
                pass
            else:
                playable_cells.append(neighbor_ne)


        return playable_cells
