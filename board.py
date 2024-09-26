import pygame as pg
from settings import *
from random import randint
from string import ascii_lowercase
from solver import read_level_map, evaluate_solution


class NQueensBoard:
    def __init__(self, window, filemap):
        self.cell_rects = {}
        self.window = window
        self.colors = read_level_map(filemap)
        self.sides = int(len(self.colors) ** 0.5)
        self.cell_size = BOARD_SIZE // self.sides

        self.color_map_from_file = {}
        mapping = list(ascii_lowercase)
        for char in mapping:
            self.color_map_from_file[char] = (randint(0, 255), randint(0, 255), randint(0, 255))

        self.create_cells()
        self.cell_colors = self.assign_colors_to_cells()

        self.board_matrix = evaluate_solution(self.sides)
        print(f'Obtained Matrix:\n{self.board_matrix}')
        print(self.cell_rects)

    def create_cells(self):
        for row in range(self.sides):
            for col in range(self.sides):
                left = col * self.cell_size
                top = row * self.cell_size
                cell_rect = pg.Rect(left, top, self.cell_size, self.cell_size)
                self.cell_rects[(row, col)] = cell_rect

    def assign_colors_to_cells(self):
        _cell_colors = {}
        for (row, col), color_char in zip(self.cell_rects.keys(), self.colors):
            _cell_colors[(row, col)] = self.color_map_from_file.get(color_char, DEFAULT_CELL_COLOR)
        return _cell_colors

    def draw_board(self):
        grid_width = self.sides * self.cell_size
        grid_height = self.sides * self.cell_size
        grid_left = self.window.get_rect().center[0] - (grid_width // 2)
        grid_top = self.window.get_rect().center[1] - (grid_height // 2)

        for (row, col), rect in self.cell_rects.items():
            cell_rect = rect.move(grid_left, grid_top)
            cell_color = self.cell_colors.get((row, col), DEFAULT_CELL_COLOR)
            pg.draw.rect(self.window, cell_color, cell_rect)
            pg.draw.rect(self.window, BORDER_COLOR, cell_rect, PADDING)

            if self.board_matrix[row, col] == 1:
                center_x = col * self.cell_size + self.cell_size // 2 + grid_left
                center_y = row * self.cell_size + self.cell_size // 2 + grid_top
                radius = self.cell_size // 5
                pg.draw.circle(self.window, (0, 0, 0), (center_x, center_y), radius)

        border_rect = pg.Rect(grid_left - PADDING // 2, grid_top - PADDING // 2,
                              grid_width + PADDING, grid_height + PADDING)
        pg.draw.rect(self.window, BORDER_COLOR, border_rect, PADDING * 2)

    def draw_elements(self):
        self.draw_board()
        pg.display.update()
