from constants import NodeState, PathCost, Window, Missing

import pygame

class NodeValueError(ValueError):
    pass

class Node:
    def __init__(self, x: int, y: int, state: NodeState=NodeState.EMPTY):
        self.x = x
        self.y = y
        self.state = state

    def draw(self, window) -> None:
        """Draws node onto the window"""
        pygame.draw.rect(
            window,
            self.state.value["color"],
            (
                Window.BORDER_X + self.x*Window.PIXEL_X,
                Window.BORDER_Y + self.y*Window.PIXEL_Y,
                Window.PIXEL_X - Window.GAP_X,
                Window.PIXEL_Y - Window.GAP_Y
            )
        )

    def get_adjacent(self, board) -> set['Node']:
        """Gets the nodes adjacent (both straight and diagonal) to a given node"""
        adjacent_nodes: set[Node] = set()

        directions = [ #eight directions (diag + straight)
            (0, 1),
            (1, 1),
            (1, 0),
            (1, -1),
            (0, -1),
            (-1, -1),
            (-1, 0),
            (-1, 1)
        ]

        for dx, dy in directions:
            x = self.x + dx
            y = self.y + dy
            #if x, y is within the bounds of board
            if 0 <= x < board.width and 0 <= y < board.height: 
                node: Node = board.grid[y][x]
                if node.state != NodeState.FULL:
                    adjacent_nodes.add(node)
        
        return adjacent_nodes

    def get_adjacent_straight(self, board) -> set['Node']:
        """Gets the nodes adjacent (straight) to a given node"""
        adjacent_nodes: set[Node] = set()

        directions = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0)
        ]
        for dx, dy in directions:
            x = self.x + dx
            y = self.y + dy
            if 0 <= x < board.width and 0 <= y < board.height: 
                node: Node = board.grid[y][x]
                if node.state != NodeState.FULL:
                    adjacent_nodes.add(node)
        
        return adjacent_nodes

    
    def __str__(self) -> str:
        return f'Node: x: {self.x}, y: {self.y}, state: {self.state}'

class HeuristicNode(Node):
    def __init__(self, base_node: Node, heuristic_cost: float=1, parent: Node=Missing):
        """Convert a Node to a Heuristic Node"""
        self.parent = parent
        self.hcost = None
        self.gcost = None
        self.heuristic_cost = heuristic_cost
        super().__init__(
            base_node.x,
            base_node.y,
            base_node.state
        )

    def get_hcost(self, target: Node) -> int:
        """H-COST is the cost from a node to the target node."""
        dx = abs(target.x - self.x)
        dy = abs(target.y - self.y)

        return min(dx, dy) * PathCost.DIAGONAL + abs(dx - dy) * PathCost.STRAIGHT

    def get_gcost(self, parent: Node) -> int:
        """G-COST is the cost from a node to the start node"""
        if parent is None:
            return 0

        if self.x != parent.x and self.y != parent.y:
            return PathCost.DIAGONAL*self.heuristic_cost + parent.gcost
        else:
            return PathCost.STRAIGHT*self.heuristic_cost + parent.gcost

    @property
    def cost(self) -> int:
        """Total cost = G-cost + H-cost"""
        if self.hcost is None:
            raise NodeValueError(f"H-COST is not defined for {self}")

        if self.gcost is None:
            raise NodeValueError(f"G-COST is not defined for {self}")

        return self.hcost + self.gcost

    def __gt__(self, other: 'HeuristicNode') -> bool:
        #Note: this __gt__ method is reversed, purely for time complexity.
        #The bisort.insort function inserts a value into a list efficiently. 
        #   This is more efficient if the list is sorted standardly (not in reverse)
        #When a sorted set of nodes is created, the minimum value wil be popped from the set.
        #   For the best time complexity, the pop value should pop at the end.
        if self.cost == other.cost:
            return self.hcost < other.hcost
        return self.cost < other.cost

    def get(self) -> str:
        return f'Node: x: {self.x}, y: {self.y}, state: {self.state}, parent: {self.parent}, gcost: {self.gcost}, hcost: {self.hcost}, cost: {self.cost}'


