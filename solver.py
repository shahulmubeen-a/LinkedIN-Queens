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


def evaluate_solution(n, zones):
    solver_matrix = [[Int(f"x_{r}_{c}") for c in range(n)] for r in range(n)]

    solver = Solver()

    # Each row should have exactly one `1`
    for r in range(n):
        solver.add(Sum([solver_matrix[r][c] for c in range(n)]) == 1)

    # Each column should have exactly one `1`
    for c in range(n):
        solver.add(Sum([solver_matrix[r][c] for r in range(n)]) == 1)

    # Each zone should have exactly one `1`
    for zone, indices in zones.items():
        solver.add(Sum([solver_matrix[r][c] for r, c in indices]) == 1)

    # No two `1`s should be diagonally adjacent
    for r in range(n):
        for c in range(n):
            # Check diagonals for bounds and diagonal conditions
            if r + 1 < n and c + 1 < n:
                solver.add(Implies(solver_matrix[r][c] == 1, solver_matrix[r + 1][c + 1] == 0))  # Primary diagonal
            if r + 1 < n and c - 1 >= 0:
                solver.add(Implies(solver_matrix[r][c] == 1, solver_matrix[r + 1][c - 1] == 0))  # Secondary diagonal

    # Check if there's a solution
    if solver.check() == sat:
        model = solver.model()

        # Extract the solution matrix
        solution = np.zeros((n, n), dtype=int)
        for r in range(n):
            for c in range(n):
                solution[r, c] = model[solver_matrix[r][c]].as_long()
        return solution
    else:
        return None
