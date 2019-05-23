from enum import Enum


class GameStates(Enum):
    PLAYERS_TURN = 1
    ENEMY_TURN = 2
    SHOW_INVENTORY = 3
    INTRO_SCREEN = 4
    CLASS_CHOICE = 5
    EXIT = 6
    TARGETING = 7
