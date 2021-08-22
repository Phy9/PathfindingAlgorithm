from constants import NodeState, Missing
from node import Node, HeuristicNode
from abc import ABC, abstractmethod

from sortedcontainers import SortedList

class PathfindingAlgorithm(ABC):
    @abstractmethod
    def init(board):
        pass

    @abstractmethod
    def update(board):
        pass

class HeuristicAlgorithm(PathfindingAlgorithm):
    reached = False

    def init(board):
        HeuristicAlgorithm.reached = False

        board.grid = [
            [HeuristicNode(board.grid[y][x], 1) for x in range(board.width)] 
            for y in range(board.height)
        ]

        board.open_nodes: SortedList[HeuristicNode] = SortedList()
        board.target_node: Node = board.get_target_node()

        start_nodes: set[HeuristicNode] = set([
            node
            for row in board.grid
            for node in row
            if node.state == NodeState.START
        ])

        for node in start_nodes:
            node.parent = None
            node.gcost = node.get_gcost(parent=None)
            node.hcost = node.get_hcost(board.target_node)
            board.open_nodes.add(node)
    
    @staticmethod
    def add_node(board, node: HeuristicNode, parent: HeuristicNode) -> None:
        """Adds a new node"""
        if node.state == NodeState.GOAL:
            node.parent = parent
            HeuristicAlgorithm.reached = True
            return

        if node.parent is Missing:
            node.hcost = node.get_hcost(board.target_node)

        else:
            #if the cost from given parent node is less than current cost
            if node.get_gcost(parent) < node.gcost:
                #removes the node from the sorted list (will be readded later)
                if node in board.open_nodes:
                    board.open_nodes.remove(node)
            
            else:
                return
        
        node.parent = parent
        node.gcost = node.get_gcost(node.parent)
        board.open_nodes.add(node)
        
        node.state = NodeState.HALF

    def update(board) -> None:
        """Main update function"""
        if not HeuristicAlgorithm.reached:
            parent_node: HeuristicNode = board.open_nodes.pop()
            parent_node.state = NodeState.DONE

            for node in parent_node.get_adjacent(board):
                node: HeuristicNode
                HeuristicAlgorithm.add_node(board, node, parent_node)
        
        else:
            pointer: HeuristicNode = board.target_node.parent

            while pointer.parent is not None:
                pointer.state = NodeState.GOAL
                pointer = pointer.parent
            
            pointer.state = NodeState.GOAL
            board.completed = True

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

    @staticmethod
    def expand(board, node: Node) -> None:
        """Expands all open nodes, up, down, left, right"""
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
            [HeuristicNode(board[y][x]) for x in board.width] 
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