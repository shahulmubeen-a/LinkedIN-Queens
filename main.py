from settings import *
from board import NQueensBoard
import pygame as pg
import sys


def main():
    pg.init()

    # Initialise stuff
    window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pg.time.Clock()
    board = NQueensBoard(window, FILEMAP)

    pg.display.set_caption('LinkedIn Queens Solver')

    while True:
        # Check stuff
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        # Draw stuff
        window.fill('#FFFFFF')
        board.draw_elements()

        # Update stuff
        clock.tick(FPS)


if __name__ == '__main__':
    main()
