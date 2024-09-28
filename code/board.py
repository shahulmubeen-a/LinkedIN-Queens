import pygame as pg
from settings import *
from random import randint
from z3_solver import evaluate_solution


def read_file(filemap):
    chars_ = []
    zones = {}
    with open(filemap, 'r') as f:
        rows = f.readlines()
    for line in rows:
        row = line.strip().split()
        for char in row:
            chars_.append(char)

    for i, char in enumerate(chars_):
        row, col = divmod(i, int(len(chars_) ** 0.5))
        if char not in zones:
            zones[char] = []
        zones[char].append((row, col))

    return zones


# Board Class to display different zones with their own colors and place queens based on the solution matrix
class NQueensBoard:
    def __init__(self, window, filemap):
        self.window = window
        self.zones = read_file(filemap)
        self.sides = len(self.zones)
        self.cell_size = BOARD_SIZE // self.sides

        self.solution_matrix = evaluate_solution(self.sides, self.zones)

        # create cells and obtain their positions
        self.cell_rects = {}
        for row in range(self.sides):
            for col in range(self.sides):
                left = col * self.cell_size
                top = row * self.cell_size
                cell_rect = pg.Rect(left, top, self.cell_size, self.cell_size)
                self.cell_rects[(row, col)] = cell_rect

        # obtain zones from file and assign colors
        self.cell_colors = {}
        color_map_from_file = {}
        mapping = self.zones.keys()
        for char in mapping:
            color_map_from_file[char] = (randint(0, 255), randint(0, 255), randint(0, 255))
        for color, zone in self.zones.items():
            for index in zone:
                self.cell_colors[index] = color_map_from_file.get(color, DEFAULT_CELL_COLOR)

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
            if self.solution_matrix[row, col] == 1:
                center_x = col * self.cell_size + self.cell_size // 2 + grid_left
                center_y = row * self.cell_size + self.cell_size // 2 + grid_top
                radius = self.cell_size // 5
                pg.draw.circle(self.window, (0, 0, 0), (center_x, center_y), radius)

        # draw border
        border_rect = pg.Rect(grid_left - PADDING // 2, grid_top - PADDING // 2,
                              grid_width + PADDING, grid_height + PADDING)
        pg.draw.rect(self.window, BORDER_COLOR, border_rect, PADDING * 2)