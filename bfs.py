from collections import deque

from algorithm import *

def bfs(puzzle, search_order):

    start_time = timeit.default_timer()
    height, width = puzzle.shape

    # Konwersja do krotki dla hashowania
    initial_state = puzzle_to_tuple(puzzle)

    # Kolejka dla BFS
    queue = deque([initial_state])

    # Słownik do śledzenia odwiedzonych stanów
    visited = set({initial_state})

    # Słownik do śledzenia ścieżki (poprzedników i wykonanych ruchów)
    parent = {initial_state: None}
    move_direction = {initial_state: None}

    # Stan docelowy
    target = matrix(width, height, list(range(1, width * height)) + [0])
    target = puzzle_to_tuple(target)

    # Liczniki do statystyk
    visited_states = 1
    processed_states = 0
    max_depth = 0

    while queue:
        current_state = queue.popleft()
        processed_states += 1

        current_puzzle = np.array(current_state)

        if current_state == target:
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

        i, j = find_zero(current_puzzle)

        for direction in search_order:
            di, dj = directions[direction]
            ni, nj = i + di, j + dj

            if 0 <= ni < height and 0 <= nj < width:
                new_puzzle = swap(current_puzzle, i, j, ni, nj)
                new_state = puzzle_to_tuple(new_puzzle)

                if new_state not in visited:
                    queue.append(new_state)
                    visited.add(new_state)
                    visited_states += 1
                    parent[new_state] = current_state
                    move_direction[new_state] = direction

                    current_depth = 0
                    state = current_state
                    while state != initial_state:
                        current_depth += 1
                        state = parent[state]
                    max_depth = max(max_depth, current_depth + 1)

    # Jeśli nie znaleziono rozwiązania
    return None, visited_states, processed_states, max_depth