from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from damesiu.objects import Player


class Pion:
    def __init__(self, x, y, couleur, player: Player):
        self.ligne = x
        self.colonne = y
        self.couleur = couleur
        self.player = player
