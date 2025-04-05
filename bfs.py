import timeit
from collections import deque
import numpy as np

from algorithm import directions, matrix, swap, find_zero, puzzle_to_tuple


def bfs(puzzle, search_order):
    """
    Implementacja algorytmu przeszukiwania wszerz (BFS) dla rozwiązania układanki przesuwnej.

    Parametry:
    puzzle (numpy.ndarray): Początkowy stan układanki jako tablica 2D
    search_order (list): Kolejność przeszukiwania kierunków (np. ['U', 'R', 'D', 'L'])

    Zwraca:
    tuple: (ścieżka rozwiązania, liczba odwiedzonych stanów, liczba przetworzonych stanów,
           maksymalna osiągnięta głębokość, czas wykonania w ms)
    """
    start_time = timeit.default_timer()
    height, width = puzzle.shape

    # Konwersja do krotki dla hashowania (umożliwia przechowywanie stanu w zbiorach i słownikach)
    initial_state = puzzle_to_tuple(puzzle)

    # Kolejka dla BFS - zapewnia przeszukiwanie poziomami (najpierw stany na mniejszej głębokości)
    queue = deque([initial_state])

    # Zbiór do szybkiego sprawdzania odwiedzonych stanów
    visited = {initial_state}

    # Słowniki do śledzenia ścieżki powrotnej - dla każdego stanu pamiętamy jego poprzednika
    parent = {initial_state: None}  # Stan poprzedni
    move_direction = {initial_state: None}  # Kierunek ruchu prowadzący do aktualnego stanu

    # Stan docelowy - uporządkowane liczby od 1 do n-1 z zerem na końcu
    target = matrix(width, height, list(range(1, width * height)) + [0])
    target = puzzle_to_tuple(target)

    # Liczniki do statystyk
    visited_states = 1  # Liczymy stan początkowy
    processed_states = 0
    max_depth = 0

    while queue:
        # Pobieramy stan z początku kolejki (FIFO - First In, First Out)
        current_state = queue.popleft()
        processed_states += 1

        # Konwersja krotki z powrotem do tablicy numpy dla łatwiejszej manipulacji
        current_puzzle = np.array(current_state)

        # Sprawdzamy czy osiągnęliśmy stan docelowy
        if current_state == target:
            # Odtwarzamy ścieżkę od stanu końcowego do początkowego
            path = []
            state = current_state
            while move_direction[state] is not None:
                path.append(move_direction[state])
                state = parent[state]
            path.reverse()  # Odwracamy ścieżkę, aby była od początku do końca

            solution_depth = len(path)
            max_depth = max(max_depth, solution_depth)

            end_time = timeit.default_timer()
            execution_time = (end_time - start_time) * 1000  # Konwersja na milisekundy
            return path, visited_states, processed_states, max_depth, execution_time

        # Znajdujemy pozycję pustego pola (zera)
        i, j = find_zero(current_puzzle)

        # Sprawdzamy każdy możliwy ruch według ustalonej kolejności
        for direction in search_order:
            di, dj = directions[direction]  # Pobieramy zmianę współrzędnych dla danego kierunku
            ni, nj = i + di, j + dj  # Nowa pozycja zera po wykonaniu ruchu

            # Sprawdzamy czy ruch jest dozwolony (w granicach planszy)
            if 0 <= ni < height and 0 <= nj < width:
                # Wykonujemy ruch - zamieniamy zero z sąsiednim elementem
                new_puzzle = swap(current_puzzle, i, j, ni, nj)
                new_state = puzzle_to_tuple(new_puzzle)

                # Jeśli stan nie był wcześniej odwiedzony, dodajemy go do kolejki
                if new_state not in visited:
                    queue.append(new_state)
                    visited.add(new_state)
                    visited_states += 1
                    parent[new_state] = current_state
                    move_direction[new_state] = direction

                    # Obliczamy głębokość aktualnego stanu (długość ścieżki od stanu początkowego)
                    current_depth = 0
                    state = current_state
                    while state != initial_state:
                        current_depth += 1
                        state = parent[state]
                    max_depth = max(max_depth, current_depth + 1)

    # Jeśli nie znaleziono rozwiązania
    end_time = timeit.default_timer()
    execution_time = (end_time - start_time) * 1000
    return None, visited_states, processed_states, max_depth, execution_time