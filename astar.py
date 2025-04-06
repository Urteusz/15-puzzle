import timeit
import heapq
import numpy as np

from algorithm import directions, matrix, swap, find_zero, puzzle_to_tuple, SIZE_HEIGHT, SIZE_WIDTH

# Funkcja obliczająca odległość Manhattan dla układu puzzli
def manhattan_distance(puzzle):
    distance = 0
    for i in range(SIZE_HEIGHT):  # Iteracja po wierszach
        for j in range(SIZE_WIDTH):  # Iteracja po kolumnach
            tile = puzzle[i][j]
            if tile != 0:  # Pomijamy puste pole (0)
                # Obliczenie docelowej pozycji kafelka
                target_i = (tile - 1) // SIZE_WIDTH
                target_j = (tile - 1) % SIZE_WIDTH
                # Dodanie odległości Manhattan do sumy
                distance += abs(i - target_i) + abs(j - target_j)
    return distance

# Funkcja obliczająca odległość Hamminga dla układu puzzli
def hamming_distance(puzzle):
    distance = 0
    for i in range(SIZE_HEIGHT):  # Iteracja po wierszach
        for j in range(SIZE_WIDTH):  # Iteracja po kolumnach
            tile = puzzle[i][j]
            if tile != 0:  # Pomijamy puste pole (0)
                # Obliczenie docelowej pozycji kafelka
                target_i = (tile - 1) // SIZE_WIDTH
                target_j = (tile - 1) % SIZE_WIDTH
                # Sprawdzenie, czy kafelek jest na właściwej pozycji
                if i != target_i or j != target_j:
                    distance += 1  # Zwiększenie odległości Hamminga
    return distance

# Algorytm A* do rozwiązywania układanki przesuwanej
def astr(puzzle, heuristic="manh"):
    start_time = timeit.default_timer()  # Start pomiaru czasu wykonania algorytmu

    puzzle = np.array(puzzle)  # Konwersja układanki na macierz NumPy
    initial_state = puzzle_to_tuple(puzzle)  # Konwersja początkowego stanu na krotkę

    # Tworzenie stanu docelowego (posortowana układanka)
    target_numbers = list(range(1, SIZE_WIDTH * SIZE_HEIGHT)) + [0]
    target = matrix(SIZE_WIDTH, SIZE_HEIGHT, target_numbers)
    target_tuple = puzzle_to_tuple(target)

    visited = {initial_state}  # Zbiór odwiedzonych stanów
    parent = {initial_state: None}  # Słownik przechowujący rodzica dla każdego stanu
    move_direction = {initial_state: None}  # Słownik przechowujący kierunek ruchu dla każdego stanu

    # Inicjalizacja zbioru otwartego w zależności od wybranej heurystyki
    if heuristic == "manh":
        open_set = [(manhattan_distance(np.array(initial_state)), 0, initial_state)]
    else:
        open_set = [(hamming_distance(np.array(initial_state)), 0, initial_state)]

    g_scores = {initial_state: 0}  # Koszt dojścia do każdego stanu

    # Statystyki algorytmu
    visited_states = 1  # Liczba odwiedzonych stanów
    processed_states = 0  # Liczba przetworzonych stanów
    max_depth = 0  # Maksymalna głębokość rekursji

    while open_set:
        _, current_g, current_state = heapq.heappop(open_set)  # Pobranie stanu o najniższym f_score
        processed_states += 1

        if current_state == target_tuple:  # Sprawdzenie, czy osiągnięto stan docelowy
            path = []  # Odtworzenie ścieżki rozwiązania
            state = current_state
            while move_direction[state] is not None:
                path.append(move_direction[state])
                state = parent[state]
            path.reverse()  # Odwrócenie ścieżki na właściwą kolejność

            solution_depth = len(path)  # Głębokość rozwiązania (liczba ruchów)
            max_depth = max(max_depth, solution_depth)

            end_time = timeit.default_timer()  # Koniec pomiaru czasu wykonania algorytmu
            execution_time = (end_time - start_time) * 1000  # Czas w milisekundach

            return path, visited_states, processed_states, max_depth, execution_time

        current_puzzle = np.array(current_state)  # Konwersja bieżącego stanu na macierz NumPy
        i, j = find_zero(current_puzzle)  # Znalezienie pozycji pustego pola (0)

        for direction, (di, dj) in directions.items():  # Przetwarzanie wszystkich możliwych ruchów
            ni, nj = i + di, j + dj

            if 0 <= ni < SIZE_HEIGHT and 0 <= nj < SIZE_WIDTH:  # Sprawdzenie poprawności ruchu
                new_puzzle = swap(current_puzzle, i, j, ni, nj)  # Wykonanie ruchu (zamiana pól)
                new_state = puzzle_to_tuple(new_puzzle)  # Konwersja nowego stanu na krotkę

                new_g = current_g + 1  # Obliczenie nowego kosztu dojścia do tego stanu

                if new_state not in visited or new_g < g_scores.get(new_state, float('inf')):
                    g_scores[new_state] = new_g
                    parent[new_state] = current_state
                    move_direction[new_state] = direction

                    if heuristic == "manh":
                        h_score = manhattan_distance(np.array(new_state))
                    else:
                        h_score = hamming_distance(np.array(new_state))
                    f_score = new_g + h_score

                    heapq.heappush(open_set, (f_score, new_g, new_state))

                    if new_state not in visited:
                        visited.add(new_state)
                        visited_states += 1

                    max_depth = max(max_depth, new_g)

    end_time = timeit.default_timer()
    execution_time = (end_time - start_time) * 1000
    return None, visited_states, processed_states, max_depth, execution_time
