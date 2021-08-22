import algorithms
from constants import Window, NodeState, Game
from board import Board, DrawBoard, RunBoard
from mouse import Mouse

import pygame
import time

def main():
    pygame.init()

    screen = pygame.display.set_mode((Window.WINSIZE_X, Window.WINSIZE_Y))
    mouse = Mouse()
    board = Board(
        width=Window.BOARD_WIDTH,
        height=Window.BOARD_HEIGHT,
        mouse_processor=mouse
    )
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill((0, 0, 0))
        board.draw(screen)
        pygame.display.update()

        #clock.tick(Game.FPS)

        board.update()
        
        if board.completed:
            Game.FPS = 60
            board.state = DrawBoard

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                
                elif event.key == pygame.K_f:
                    mouse.state = NodeState.FULL
                
                elif event.key == pygame.K_e:
                    mouse.state = NodeState.EMPTY
                
                elif event.key == pygame.K_s:
                    mouse.state = NodeState.START
                
                elif event.key == pygame.K_g:
                    mouse.state = NodeState.GOAL

                elif event.key == pygame.K_SPACE:
                    # Game.FPS = 5
                    board.algorithm = algorithms.DijkstrasAlgorithm
                    board.state = RunBoard
                    board.run_init()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse.activate()
            
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse.deactivate()

if __name__ == "__main__":
    main()
