from settings import *
from board import NQueensBoard
import pygame as pg
import sys


def main():
    window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    board = NQueensBoard(window, FILEMAP)

    if board.solution_matrix is None:
        print('No solutions found')
    else:
        print(f'Solution found:\n{board.solution_matrix}')

        # Initialise stuff
        pg.init()
        pg.display.set_caption('LinkedIn Queens Solver')

        clock = pg.time.Clock()

        while True:
            # Check stuff
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_q):
                    pg.quit()
                    sys.exit()

            # Draw stuff
            window.fill('#FFFFFF')
            board.draw_board()

            # Update stuff
            pg.display.update()
            clock.tick(FPS)


if __name__ == '__main__':
    main()
