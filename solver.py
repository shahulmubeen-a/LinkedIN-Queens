import numpy as np
from itertools import combinations
from random import choice
from z3 import *


class ReadFile:

    def __init__(self, filemap):
        self.chars = []
        self.zones = {}
        self.filemap = filemap

        self.extract_chars()
        self.extract_zones()

    def extract_chars(self):
        with open(self.filemap, 'r') as f:
            rows = f.readlines()
        for line in rows:
            row = line.strip().split()
            for char in row:
                self.chars.append(char)

    def extract_zones(self):
        for i, char in enumerate(self.chars):
            row, col = divmod(i, int(len(self.chars) ** 0.5))
            if char not in self.zones:
                self.zones[char] = []
            self.zones[char].append((row, col))


def generate_matrices(n):
    zero_matrix = np.zeros((n, n), dtype=int)
    total_elements = n * n

    possible_positions = list(combinations(range(total_elements), n))

    matrices = []
    for pos in possible_positions:
        new_matrix = zero_matrix.copy()
        for p in pos:
            row, col = divmod(p, n)  # Convert 1D index to 2D index
            new_matrix[row, col] = 1

        matrices.append(new_matrix)

    return matrices


def evaluate_solution(n):
    possible_matrices = generate_matrices(n)
    valid_matrices = choice(possible_matrices)

    # solver = Solver()

    # for r in range(n):
    #     for c in range(n):
    #         solver.add(Sum(If(valid_matrices[r][c], 1, 0)) == 1)
    #
    # for c in range(n):
    #     for r in range(n):
    #         solver.add(Sum(If(valid_matrices[r][c], 1, 0)) == 1)
    #
    return valid_matrices
