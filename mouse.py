from constants import NodeState

import pygame

class Mouse:
    def __init__(self):
        self.active = False
        self.pos = None
        self.state: NodeState = NodeState.EMPTY

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False
    
    def get_pos(self):
        self.pos = pygame.mouse.get_pos()
        return self.pos