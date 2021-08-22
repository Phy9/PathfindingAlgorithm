from constants import NodeState
from node import Node, AStarNode
from abc import ABC, abstractmethod

class PathfindingAlgorithm(ABC):
    @abstractmethod
    def init(board):
        pass

    @abstractmethod
    def update(board, target):
        pass

class DijkstrasAlgorithm(PathfindingAlgorithm):
    def init(board):
        """Initialize the board for Djikstra's"""
        board.open_nodes: set[Node] = set()
        board.closed_nodes: set[Node] = set()
    
        start_nodes: set[Node] = set([
            node
            for row in board.grid
            for node in row
            if node.state == NodeState.START
        ])

        for node in start_nodes:
            board.open_nodes.add(node)

    def expand(board, node: Node) -> None:
        """Expands all open nodes"""
        for adj_node in node.get_adjacent_straight(board):
            if adj_node.state == NodeState.GOAL:
                board.completed = True

            elif adj_node not in set.union(board.closed_nodes, board.open_nodes):
                board.open_nodes.add(adj_node)
                adj_node.state = NodeState.HALF

    def update(board) -> None:
        """Main update function"""
        if not board.open_nodes:
            #if there are no open nodes
            board.completed = True

        for node in board.open_nodes.copy():
            DijkstrasAlgorithm.expand(board, node)
            board.open_nodes.remove(node)
            board.closed_nodes.add(node)
            node.state = NodeState.DONE
            if board.completed:
                break

class AStarAlgorithm(PathfindingAlgorithm):
    def init(board):
        """Initialize the board to prepare for the A-Star algorithm"""
        board.explored_nodes: set[Node] = set()
        board.inrange_nodes: set[Node] = set()

        board.grid = [
            [AStarNode(board[y][x]) for x in board.width] 
            for y in board.height 
        ]

        start_nodes: set[Node] = set([
            node
            for row in board.grid
            for node in row
            if node.state == NodeState.START
        ])

        for node in start_nodes:
            board.inrange_nodes.append(node)

    def update(board, target):
        if not board.explored_nodes and not board.inrange_nodes:
            board.init(board)