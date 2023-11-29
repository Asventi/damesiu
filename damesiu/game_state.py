from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from damesiu.objects import Player
    from damesiu.objects import Pion

from threading import Lock


class GameStateSingleton(type):
    """
    Thread safe singleton for Graphic Engine
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
    def __init__(self):
        self.current_player: Player | None = None
        self.pion_lock: Pion | None = None
        self.game_ended: bool = False
