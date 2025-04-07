from constraint import Problem, AllDifferentConstraint

def knight_attack(pos1, pos2):
    """
    Return True if knights at pos1 and pos2 do NOT attack each other.
    """
    x1, y1 = pos1
    x2, y2 = pos2
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return not ((dx == 2 and dy == 1) or (dx == 1 and dy == 2))

def solve_k_knights(n, k):
    """
    Try to place k non-attacking knights on an n x n chessboard.
    Returns a dict of knight positions or None if not possible.
    """
    if k > 32:
        return None  

    board = [(x, y) for x in range(n) for y in range(n)]

    white_squares = [pos for pos in board if (pos[0] + pos[1]) % 2 == 0]
    if k <= len(white_squares):
        return { f"K{i}": white_squares[i] for i in range(k) }

    problem = Problem()
    knights = [f"K{i}" for i in range(k)]
    problem.addVariables(knights, board)
    problem.addConstraint(AllDifferentConstraint(), knights)

    for i in range(k - 1):
        problem.addConstraint(lambda a, b: a < b, (knights[i], knights[i + 1]))

    for i in range(k):
        for j in range(i + 1, k):
            problem.addConstraint(knight_attack, (knights[i], knights[j]))

    return problem.getSolution()

def find_max_knights(n):
    max_knights = 0
    best_solution = None

    for k in range(1, 64): # n * n + 1
        solution = solve_k_knights(n, k)
        if solution:
            max_knights = k
            best_solution = solution  # save valid solution
        else:
            break  # stop at first failure

    return max_knights, best_solution

n = 8  # board size
mode = input("Choose mode (solve/max): ").strip().lower()

if mode == "solve":
    k = int(input("Enter number of knights (k): "))
    solution = solve_k_knights(n, k)
    if solution:
        print("\nSolution found:")
        for knight, pos in sorted(solution.items()):
            print(f"{knight}: {pos}")
    else:
        print("No solution found.")
elif mode == "max":
    max_k, solution = find_max_knights(n)
    print(f"\nMaximum number of non-attacking knights on an {n}x{n} board is: {max_k}, Solution is: ", solution)
else:
    print("Invalid mode. Use 'solve' or 'max'.")
