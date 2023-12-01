from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from damesiu.objects import Player
    from damesiu.objects import Pion

from threading import Lock


class GameStateSingleton(type):
    """
    Thread safe singleton pour le game state, ce qui le rendra accessible partout dans le code en retournant
    la meme instance a chaque appel.
    """
    _instances = {}
    # Pour lock les thread pour eviter que deux thread instancie la classe en meme temps ce qui casserai le singleton
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        """
        Fonction de creation d'instance
        """
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class GameState(metaclass=GameStateSingleton):
    """
    Classe qui contient l'etat du jeu, le joueur courant, le pion selectionné, et si le jeu est terminé ou pas.
    Aucune fonctionnalite en soit, juste un moyen d'avoir des informations sur l'etat du jeu, partout, sans avoir a
    les passer en argument partout.
    """

    def __init__(self):
        self._current_player: Player | None = None
        self._pion_lock: Pion | None = None
        self._game_ended: bool = False

    # Getters Setters
    @property
    def current_player(self):
        return self._current_player

    @current_player.setter
    def current_player(self, player: Player):
        if self._current_player == player:
            raise Exception("Le joueur est deja le joueur actuel")
        self._current_player = player

    @property
    def pion_lock(self):
        return self._pion_lock

    @pion_lock.setter
    def pion_lock(self, pion: Pion):
        self._pion_lock = pion

    @property
    def game_ended(self):
        return self._game_ended

    @game_ended.setter
    def game_ended(self, game_ended: bool):
        self._game_ended = game_ended
