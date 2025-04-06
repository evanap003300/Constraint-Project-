from constraint import Problem, AllDifferentConstraint

def attack_constraint(k1, k2):
    """Ensures two knights do not attack each other."""
    x1, y1 = k1
    x2, y2 = k2
    
    dx = abs(x1 - x2)  # Difference in rows
    dy = abs(y1 - y2)  # Difference in columns

    attacking_moves = [(2, 1), (1, 2)]  # Relative knight moves

    if (dx, dy) in attacking_moves:
        return False  # Knights are attacking each other
    return True  # Knights are safe

def solve_csp(n, k):
    problem = Problem()

    knights = []

    # Populate knights list
    for i in range(k):
        knight_name = f"K{i}"
        knights.append(knight_name)

    # Populate domain list 
    domain = []
    for x in range(n):
        for y in range(n):
            position = (x, y)
            domain.append(position)

    for knight in knights:
        problem.addVariable(knight, domain)

    # Add constraints: No two knights can attack each other
    for i in range(k):
        for j in range(i + 1, k):
            problem.addConstraint(attack_constraint, (knights[i], knights[j]))

    # Add uniqueness constraint: No two knights can occupy the same position
    problem.addConstraint(AllDifferentConstraint(), knights)

    # Solve and return results
    solution = problem.getSolution() 
    return solution

def find_max_knights(n):
    max_knights = 0
    best_solution = None

    for k in range(1, 64): # n * n + 1
        solution = solve_csp(n, k)
        if solution:
            max_knights = k
            best_solution = solution  # save valid solution
        else:
            break  # stop at first failure

    return max_knights, best_solution

# 8 rows and 8 cols on a chess board
n = 8

print("-------- Solving for possible solutions given k knights --------\n")
k = int(input("How many knights are on the board: "))

if k > n * n: # Check that there are less knights than board positions
    print("Too many Knights for board! (k <= 64)")
else:
    if k > 24:
        print("This may take awhile you may want to try a smaller number like k < 25")
    solutions = solve_csp(n, k)
    if len(solutions) > 0:
        print("Found a Valid Solution")
    else:
        print("No valid solution found")
    if len(solutions) > 0:
        print("Solution:", solutions) 

print("\n\n-------- Solving for maximum knights without any attacks --------\n")
max_knights, solution = find_max_knights(n)
print(f"Maximum knights placed:", max_knights)
print("Knight positions:", solution)
