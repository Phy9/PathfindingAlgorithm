"""CONSTANTS TO BE USED. All constants can be changed here"""
from enum import Enum, auto

class Game:
    FPS = 60

class Window:
    WINSIZE_X: int = 820
    WINSIZE_Y: int = 820

    BOARD_WIDTH: int = 120
    BOARD_HEIGHT: int = 120

    BORDER_X: int = 10
    BORDER_Y: int = 10

    PIXEL_X: int = (WINSIZE_X - 2*BORDER_X) // BOARD_WIDTH
    PIXEL_Y: int = (WINSIZE_Y - 2*BORDER_Y) // BOARD_HEIGHT

    GAP_X: int = 1
    GAP_Y: int = 1

class NodeState(Enum):
    EMPTY: dict = {"color": (240, 240, 240)}
    HALF: dict = {"color": (120, 120, 240)}
    DONE: dict = {"color": (120, 120, 0)}
    FULL: dict = {"color": (60, 60, 60)}
    START: dict = {"color": (0, 240, 0)}
    GOAL: dict = {"color": (240, 0, 0)}

class PathCost:
    DIAGONAL: int = 14
    STRAIGHT: int = 10

Missing = object()