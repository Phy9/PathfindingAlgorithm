from constants import NodeState, PathCost, Window

import pygame

class NodeNameError(NameError):
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

    def get_adjacent_diag(self, board) -> set['Node']:
        """Gets the nodes adjacent (both straight and diagonal) to a given node"""
        adjacent_nodes: set[Node] = set()

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
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

class AStarNode(Node):
    def __init__(self, base_node: Node, parent_node: Node=None):
        """Convert a Node to an A-Star Node"""
        self.parent = parent_node
        self.hcost = None
        self.gcost = None
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

    def get_gcost(self) -> int:
        """G-COST is the cost from a node to the start node"""
        if self.parent is None:
            return 0

        if (self.x + self.parent.x)%2 == 0:
            return PathCost.DIAGONAL + self.parent.gcost
        else:
            return PathCost.STRAIGHT + self.parent.gcost

    @property
    def cost(self) -> int:
        """Total cost = G-cost + H-cost"""
        if self.hcost is None:
            raise NodeNameError(f"H-COST is not defined for {self}")

        if self.gcost is None:
            self.gcost = self.get_gcost()

        return self.hcost + self.gcost


