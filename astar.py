from algorithm import *
import heapq

def manhattan_distance(puzzle):
    height, width = len(puzzle), len(puzzle[0])
    distance = 0

    for i in range(height):
        for j in range(width):
            tile = puzzle[i][j]
            if tile != 0:
                target_i = (tile - 1) // width
                target_j = (tile - 1) % width
                distance += abs(i - target_i) + abs(j - target_j)
    return distance


def hamming_distance(puzzle):
    height, width = len(puzzle), len(puzzle[0])
    distance = 0

    for i in range(height):
        for j in range(width):
            tile = puzzle[i][j]
            if tile != 0:  # Skip the empty tile
                # Calculate correct position for this tile
                target_i = (tile - 1) // width
                target_j = (tile - 1) % width
                # If tile is not in the right position, count it
                if i != target_i or j != target_j:
                    distance += 1

    return distance


def astr(puzzle, heuristic="manh"):
    start_time = timeit.default_timer()
    puzzle = np.array(puzzle)
    height, width = puzzle.shape

    initial_state = puzzle_to_tuple(puzzle)

    target_numbers = list(range(1, width * height)) + [0]
    target = matrix(width, height, target_numbers)
    target_tuple = puzzle_to_tuple(target)

    visited = set({initial_state})

    parent = {initial_state: None}
    move_direction = {initial_state: None}

    if heuristic == "manh":
        open_set = [(manhattan_distance(np.array(initial_state)), 0, initial_state)]
    else:
        open_set = [(hamming_distance(np.array(initial_state)), 0, initial_state)]

    g_scores = {initial_state: 0}

    # Statistics
    visited_states = 1
    processed_states = 0
    max_depth = 0

    while open_set:
        # Get state with lowest f_score
        _, current_g, current_state = heapq.heappop(open_set)
        processed_states += 1

        # Check if goal state
        if current_state == target_tuple:
            # Build solution path
            path = []
            state = current_state
            while move_direction[state] is not None:
                path.append(move_direction[state])
                state = parent[state]
            path.reverse()

            solution_depth = len(path)
            max_depth = max(max_depth, solution_depth)

            end_time = timeit.default_timer()
            execution_time = (end_time - start_time) * 1000
            return path, visited_states, processed_states, max_depth, execution_time

        # Find zero position
        current_puzzle = np.array(current_state)
        i, j = find_zero(current_puzzle)

        # Try all possible moves
        for direction, (di, dj) in directions.items():
            ni, nj = i + di, j + dj

            if 0 <= ni < height and 0 <= nj < width:
                # Create new state by swapping empty tile
                new_puzzle = swap(current_puzzle, i, j, ni, nj)
                new_state = puzzle_to_tuple(new_puzzle)

                # Calculate new g_score
                new_g = current_g + 1

                # If this state is new or we found a better path to it
                if new_state not in visited or new_g < g_scores.get(new_state, float('inf')):
                    # Update path information
                    g_scores[new_state] = new_g
                    parent[new_state] = current_state
                    move_direction[new_state] = direction

                    # Calculate f_score (g + h)
                    if heuristic == "manh":
                        h_score = manhattan_distance(np.array(new_state))
                    else:
                        h_score = hamming_distance(np.array(new_state))
                    f_score = new_g + h_score

                    # Add to open set
                    heapq.heappush(open_set, (f_score, new_g, new_state))

                    # Update statistics
                    if new_state not in visited:
                        visited.add(new_state)
                        visited_states += 1

                    max_depth = max(max_depth, new_g)

    # No solution found
    end_time = timeit.default_timer()
    execution_time = (end_time - start_time) * 1000
    return None, visited_states, processed_states, max_depth, execution_time
