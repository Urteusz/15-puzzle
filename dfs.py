import timeit
import numpy as np
from algorithm import directions, puzzle_to_tuple, find_zero, matrix, SIZE_HEIGHT, SIZE_WIDTH


def dfs(puzzle, search_order):

    start_time = timeit.default_timer()
    # Odwracamy kolejność przeszukiwania dla operacji na stosie (LIFO)
    search_order = search_order[::-1]

    # Znajdujemy pozycję zera (pustego pola) w początkowym stanie
    zero_pos = find_zero(puzzle)

    # Konwertujemy początkową układankę na krotkę dla możliwości haszowania
    initial_state = puzzle_to_tuple(puzzle)

    # Stan docelowy (ułożona układanka)
    goal_array = matrix(SIZE_WIDTH, SIZE_HEIGHT, list(range(1, SIZE_WIDTH * SIZE_HEIGHT)) + [0])
    target_state = puzzle_to_tuple(goal_array)

    # Śledzimy odwiedzone stany wraz z ich głębokością
    visited = {initial_state: 0}

    # Stos dla DFS przechowujący (stan, ścieżka, głębokość, pozycja_zera)
    stack = [(initial_state, [], 0, zero_pos)]

    # Statystyki algorytmu
    visited_states = 1  # Liczymy stan początkowy
    processed_states = 0
    max_reached_depth = 0

    # Maksymalna głębokość do przeszukania (zapobiega nieskończonym pętlom)
    max_depth = 20

    while stack:
        # Pobieramy stan ze stosu (LIFO - Last In, First Out)
        current_state, path, depth, zero_pos = stack.pop()
        processed_states += 1

        # Aktualizujemy maksymalną osiągniętą głębokość
        max_reached_depth = max(max_reached_depth, depth)

        # Sprawdzamy czy osiągnęliśmy stan docelowy
        if current_state == target_state:
            end_time = timeit.default_timer()
            execution_time = (end_time - start_time) * 1000  # Konwersja na milisekundy
            return path, visited_states, processed_states, max_reached_depth, execution_time

        # Pomijamy stany na maksymalnej głębokości
        if depth >= max_depth:
            continue

        i, j = zero_pos  # Aktualna pozycja zera

        # Sprawdzamy każdy możliwy ruch według ustalonej kolejności
        for direction in search_order:
            di, dj = directions[direction]  # Pobieramy zmianę współrzędnych dla danego kierunku
            ni, nj = i + di, j + dj  # Nowa pozycja zera po wykonaniu ruchu

            # Sprawdzamy czy ruch jest dozwolony (w granicach planszy)
            if 0 <= ni < SIZE_HEIGHT and 0 <= nj < SIZE_WIDTH:
                # Tworzymy nowy stan przez zamianę miejscami zera z sąsiednim elementem
                new_state = [list(row) for row in current_state]
                new_state[i][j], new_state[ni][nj] = new_state[ni][nj], new_state[i][j]
                new_state_tuple = puzzle_to_tuple(new_state)

                # Dodajemy stan do eksploracji, jeśli nie był wcześniej odwiedzony lub był odwiedzony na większej głębokości
                if new_state_tuple not in visited or visited[new_state_tuple] > depth + 1:
                    visited[new_state_tuple] = depth + 1
                    visited_states += 1
                    # Dodajemy nowy stan do stosu wraz z zaktualizowaną ścieżką, głębokością i pozycją zera
                    stack.append((new_state_tuple, path + [direction], depth + 1, (ni, nj)))

    # Jeśli nie znaleziono rozwiązania
    end_time = timeit.default_timer()
    execution_time = (end_time - start_time) * 1000
    return None, visited_states, processed_states, max_reached_depth, execution_time