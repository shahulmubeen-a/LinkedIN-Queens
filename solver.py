import numpy as np
from itertools import combinations
from random import choice
from z3 import *


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

    print(f'Found {len(matrices)} possible combinations')

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
