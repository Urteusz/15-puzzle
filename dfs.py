import timeit
import numpy as np
from algorithm import directions

def dfs(puzzle, search_order):
    start_time = timeit.default_timer()
    # Reverse search order for stack operations
    search_order = search_order[::-1]
    height, width = puzzle.shape

    # Find zero position in initial state
    zero_pos = None
    for i in range(height):
        for j in range(width):
            if puzzle[i, j] == 0:
                zero_pos = (i, j)
                break
        if zero_pos:
            break

    # Convert initial puzzle to tuple for hashing
    initial_state = tuple(map(tuple, puzzle))

    # Target state (goal)
    goal_array = np.reshape(np.array(list(range(1, width * height)) + [0]), (height, width))
    target_state = tuple(map(tuple, goal_array))

    # Track visited states with their depth
    visited = {initial_state: 0}

    # Stack for DFS with (state, path, depth, zero_position)
    stack = [(initial_state, [], 0, zero_pos)]

    # Statistics
    visited_states = 1
    processed_states = 0
    max_reached_depth = 0

    # Maximum depth to explore
    max_depth = 20

    while stack:
        current_state, path, depth, zero_pos = stack.pop()
        processed_states += 1

        # Update max depth reached
        max_reached_depth = max(max_reached_depth, depth)

        # Check if goal is reached
        if current_state == target_state:
            end_time = timeit.default_timer()
            execution_time = (end_time - start_time) * 1000
            return path, visited_states, processed_states, max_reached_depth, execution_time

        # Skip if max depth reached
        if depth >= max_depth:
            continue

        i, j = zero_pos

        # Try each direction according to search order
        for direction in search_order:
            di, dj = directions[direction]
            ni, nj = i + di, j + dj

            # Check if the move is valid
            if 0 <= ni < height and 0 <= nj < width:
                # Create new state by swapping
                new_state = [list(row) for row in current_state]
                new_state[i][j], new_state[ni][nj] = new_state[ni][nj], new_state[i][j]
                new_state_tuple = tuple(map(tuple, new_state))

                # Check if this state hasn't been visited before or has been visited at a deeper level
                if new_state_tuple not in visited or visited[new_state_tuple] > depth + 1:
                    visited[new_state_tuple] = depth + 1
                    visited_states += 1
                    stack.append((new_state_tuple, path + [direction], depth + 1, (ni, nj)))

    # No solution found
    end_time = timeit.default_timer()
    execution_time = (end_time - start_time) * 1000
    return None, visited_states, processed_states, max_reached_depth, execution_time