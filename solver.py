import numpy as np
from itertools import combinations
from random import choice
from z3 import *


def read_level_map(filemap):
    with open(filemap, 'r') as f:
        rows = f.readlines()

    grid = []
    for line in rows:
        row = line.strip().split()
        for char in row:
            grid.append(char)

    return grid


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
    solver = Solver()
    valid_matrices = choice(possible_matrices)

    # for r in range(n):
    #     for c in range(n):
    #         solver.add(Sum(If(valid_matrices[r][c], 1, 0)) == 1)
    #
    # for c in range(n):
    #     for r in range(n):
    #         solver.add(Sum(If(valid_matrices[r][c], 1, 0)) == 1)
    #
    return valid_matrices
