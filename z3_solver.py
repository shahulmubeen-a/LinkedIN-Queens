import numpy as np
from z3 import *




def evaluate_solution(n, zones):
    # Z3 matrix of variables (each element is either 0 or 1)
    X = [[Int(f"x_{r}_{c}") for c in range(n)] for r in range(n)]

    solver = Solver()

    # 1. Ensure each cell contains either 0 or 1
    for r in range(n):
        for c in range(n):
            solver.add(Or(X[r][c] == 0, X[r][c] == 1))

    # 2. Each row should have exactly one `1`
    for r in range(n):
        solver.add(Sum([X[r][c] for c in range(n)]) == 1)

    # 3. Each column should have exactly one `1`
    for c in range(n):
        solver.add(Sum([X[r][c] for r in range(n)]) == 1)

    # 4. Each zone should have exactly one `1`
    for zone, indices in zones.items():
        solver.add(Sum([X[r][c] for r, c in indices]) == 1)

    # 5. No two `1`s should be diagonally adjacent
    for r in range(n):
        for c in range(n):
            # Check diagonals for bounds and prevent diagonal adjacencies
            if r + 1 < n and c + 1 < n:
                solver.add(Implies(X[r][c] == 1, X[r+1][c+1] == 0))  # Main diagonal
            if r + 1 < n and c - 1 >= 0:
                solver.add(Implies(X[r][c] == 1, X[r+1][c-1] == 0))  # Anti-diagonal

    # Check if there's a solution
    if solver.check() == sat:
        model = solver.model()
        # Extract the solution matrix
        solution = np.zeros((n, n), dtype=int)
        for r in range(n):
            for c in range(n):
                solution[r, c] = model[X[r][c]].as_long()
        return solution
    else:
        return None
