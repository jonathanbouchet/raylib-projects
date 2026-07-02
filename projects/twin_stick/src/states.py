from enum import Enum


class GameStates(Enum):
    INIT = 0  # start of the app
    RUN = 1  # game is running
    PAUSE = 2  # game is paused
    OVER = 3  # game is over


class WaveStates(Enum):
    INIT = 0  # start of the app
    ONGOING = 1  # game is running
    SUCCESS = 2  # game is paused
    FAIL = 3  # game is over
