from algorithm import *
from collections import deque

max_depth = 20

def dfs(puzzle, search_order):
    start_time = timeit.default_timer()
    height, width = puzzle.shape

    initial_state = puzzle_to_tuple(puzzle)

    # Stos przechowujący (stan, głębokość)
    stack = [(initial_state, 0)]  # Pierwszy stan z głębokością 0

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
    max_reached_depth = 0

    while stack:
        current_state, depth = stack.pop()  # Pobieramy stan i głębokość
        processed_states += 1

        # Jeśli osiągnięto maksymalną głębokość, wykonujemy nawrót (backtracking)
        if depth >= max_depth:
            continue  # Pomijamy dalsze przetwarzanie tego stanu

        current_puzzle = np.array(current_state)

        if current_state == target:
            path = []
            state = current_state
            while move_direction[state] is not None:
                path.append(move_direction[state])
                state = parent[state]
            path.reverse()

            solution_depth = len(path)
            max_reached_depth = max(max_reached_depth, solution_depth)

            end_time = timeit.default_timer()
            execution_time = (end_time - start_time) * 1000
            return path, visited_states, processed_states, max_reached_depth, execution_time

        i, j = find_zero(current_puzzle)

        for direction in search_order:
            di, dj = directions[direction]
            ni, nj = i + di, j + dj

            if 0 <= ni < height and 0 <= nj < width:
                new_puzzle = swap(current_puzzle, i, j, ni, nj)
                new_state = puzzle_to_tuple(new_puzzle)

                if new_state not in visited:
                    stack.append((new_state, depth + 1))  # Dodajemy stan z nową głębokością
                    visited.add(new_state)
                    visited_states += 1
                    parent[new_state] = current_state
                    move_direction[new_state] = direction

                    max_reached_depth = max(max_reached_depth, depth + 1)

    end_time = timeit.default_timer()
    execution_time = (end_time - start_time) * 1000
    return None, visited_states, processed_states, max_reached_depth, execution_time