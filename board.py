import pygame as pg
from settings import *
from random import randint
from string import ascii_lowercase
from solver import ReadFile, evaluate_solution


# Board Class to display different zones with their own colors and place queens based on the solution matrix
class NQueensBoard:
    def __init__(self, window, filemap):
        self.window = window
        self.cells = ReadFile(filemap).chars
        self.zones = ReadFile(filemap).zones
        self.sides = int(len(self.cells) ** 0.5)
        self.cell_size = BOARD_SIZE // self.sides

        self.board_matrix = evaluate_solution(self.sides)

        # create cells and obtain their positions
        self.cell_rects = {}
        for row in range(self.sides):
            for col in range(self.sides):
                left = col * self.cell_size
                top = row * self.cell_size
                cell_rect = pg.Rect(left, top, self.cell_size, self.cell_size)
                self.cell_rects[(row, col)] = cell_rect

        # obtain zones from file and assign colors
        self.color_map_from_file = {}
        mapping = self.zones.keys()
        for char in mapping:
            self.color_map_from_file[char] = (randint(0, 255), randint(0, 255), randint(0, 255))

        # assign each cell a color based on the color map
        self.cell_colors = {}
        for (row, col), color_char in zip(self.cell_rects.keys(), self.cells):
            self.cell_colors[(row, col)] = self.color_map_from_file.get(color_char, DEFAULT_CELL_COLOR)

        print(f'Obtained Matrix:\n{self.board_matrix}')
        print(f'Obtained Zones:\n{self.zones}')
        print(f'Obtained Cells:\n{self.cells}')
        print(f'Assigned Colors:\n{self.color_map_from_file}')

    def draw_board(self):
        grid_width = self.sides * self.cell_size
        grid_height = self.sides * self.cell_size
        grid_left = self.window.get_rect().center[0] - (grid_width // 2)
        grid_top = self.window.get_rect().center[1] - (grid_height // 2)

        # draw board
        for (row, col), rect in self.cell_rects.items():
            cell_rect = rect.move(grid_left, grid_top)
            cell_color = self.cell_colors.get((row, col), DEFAULT_CELL_COLOR)
            pg.draw.rect(self.window, cell_color, cell_rect)
            pg.draw.rect(self.window, BORDER_COLOR, cell_rect, PADDING)

            # draw queens
            if self.board_matrix[row, col] == 1:
                center_x = col * self.cell_size + self.cell_size // 2 + grid_left
                center_y = row * self.cell_size + self.cell_size // 2 + grid_top
                radius = self.cell_size // 5
                pg.draw.circle(self.window, (0, 0, 0), (center_x, center_y), radius)

        # draw border
        border_rect = pg.Rect(grid_left - PADDING // 2, grid_top - PADDING // 2,
                              grid_width + PADDING, grid_height + PADDING)
        pg.draw.rect(self.window, BORDER_COLOR, border_rect, PADDING * 2)
