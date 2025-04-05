import timeit
import numpy as np
from algorithm import directions, swap, puzzle_to_tuple, find_zero


def dfs(puzzle, search_order):
    """
    Implementacja algorytmu przeszukiwania w głąb (DFS) dla rozwiązania układanki przesuwnej.

    Parametry:
    puzzle (numpy.ndarray): Początkowy stan układanki jako tablica 2D
    search_order (list): Kolejność przeszukiwania kierunków (np. ['U', 'R', 'D', 'L'])

    Zwraca:
    tuple: (ścieżka rozwiązania, liczba odwiedzonych stanów, liczba przetworzonych stanów,
           maksymalna osiągnięta głębokość, czas wykonania w ms)
    """
    start_time = timeit.default_timer()
    # Odwracamy kolejność przeszukiwania dla operacji na stosie (LIFO)
    search_order = search_order[::-1]
    height, width = puzzle.shape

    # Znajdujemy pozycję zera (pustego pola) w początkowym stanie
    zero_pos = find_zero(puzzle)

    # Konwertujemy początkową układankę na krotkę dla możliwości haszowania
    initial_state = puzzle_to_tuple(puzzle)

    # Stan docelowy (ułożona układanka)
    goal_array = np.reshape(np.array(list(range(1, width * height)) + [0]), (height, width))
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
        # Pobieramy stan ze stosu (LIFO)
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
            if 0 <= ni < height and 0 <= nj < width:
                # Tworzymy nowy stan przez zamianę miejscami zera z sąsiednim elementem (bez uzycia swap bo zbyt obciaza
                new_state = [list(row) for row in current_state]
                new_state[i][j], new_state[ni][nj] = new_state[ni][nj], new_state[i][j]
                new_state_tuple = puzzle_to_tuple(new_state)

                # Dodajemy stan do eksploracji, jeśli nie był wcześniej odwiedzony lub był odwiedzony na większej głębokości
                if new_state_tuple not in visited or visited[new_state_tuple] > depth + 1:
                    visited[new_state_tuple] = depth + 1
                    visited_states += 1
                    stack.append((new_state_tuple, path + [direction], depth + 1, (ni, nj)))

    # Jeśli nie znaleziono rozwiązania
    end_time = timeit.default_timer()
    execution_time = (end_time - start_time) * 1000
    return None, visited_states, processed_states, max_reached_depth, execution_time