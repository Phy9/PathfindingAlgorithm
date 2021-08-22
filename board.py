from constants import NodeState, Window
from node import Node
from algorithms import *
from mouse import Mouse
from abc import ABC, abstractmethod

class BoardProcess(ABC):
    @abstractmethod
    def update(board):
        """Runs the main function for each process of the board (edit, run)"""

class DrawBoard(BoardProcess):
    def update(board):
        """Allows the player to draw on the board, editing its cells"""
        #defining types, purely to look nicer. This is not necessary
        board.mouse: Mouse
        board.grid: list[list[Node]]

        if board.mouse.active:
            mouse_x, mouse_y = board.mouse.get_pos()
            x = (mouse_x - Window.BORDER_X) // Window.PIXEL_X
            y = (mouse_y - Window.BORDER_Y) // Window.PIXEL_Y

            if 0 <= x < board.width and 0 <= y < board.height: 
                board.grid[y][x].state = board.mouse.state

class RunBoard(BoardProcess):
    def update(board):
        """Runs the selected pathfinding algorithm."""
        #defining types
        board.algorithm: PathfindingAlgorithm

        board.algorithm.update(board)

class Board:
    def __init__(self, width: int, height: int, mouse_processor: Mouse):
        self.width: int = width
        self.height: int = height
        self.grid: list[list[Node]] = [
            [Node(x, y) for x in range(width)] for y in range(height)
        ]

        self.state: BoardProcess = DrawBoard
        self.algorithm: PathfindingAlgorithm = None
        self.mouse: Mouse = mouse_processor
        self.completed: bool = False

    def draw(self, window) -> None:
        """Draw the whole board onto a pygame window"""
        for row in self.grid:
            for node in row:
                node.draw(window)

    def get_target_node(self) -> Node:
        for row in self.grid:
            for node in row:
                if node.state==NodeState.GOAL:
                    return node
        
        raise ValueError("Target Node does not exist")

    def run_init(self) -> None:
        self.algorithm.init(self)

    def update(self) -> None:
        self.state.update(self)
