import time

import numpy as np
from collections import deque

from scipy.optimize import newton

EMPTY_TILE = 0

directions = {
            'L': (0, -1),  # Lewo
            'R': (0, 1),   # Prawo
            'U': (-1, 0),  # Góra
            'D': (1, 0)    # Dół
        }

def is_solvable(tiles):
    inv_count = 0
    for i in range(len(tiles)):
        if tiles[i] == EMPTY_TILE:
            continue
        for j in range(i + 1, len(tiles)):
            if tiles[j] != EMPTY_TILE and tiles[i] > tiles[j]:
                inv_count += 1
    return inv_count % 2 == 0

def matrix(width, height, numer_list):
    tiles = np.zeros((width, height), dtype=int)
    for i in range(width):
        for j in range(height):
            tiles[i][j] = numer_list[height * i + j]
    return tiles


def find_zero(puzzle):
    for i, row in enumerate(puzzle):
        for j, val in enumerate(row):
            if val == 0:
                return i, j
    return None

def get_neighbours(i, j, width, height):
  moves = []
  if i > 0: moves.append((i - 1, j))
  if i < height - 1: moves.append((i + 1, j))
  if j > 0: moves.append((i, j - 1))
  if j < width - 1: moves.append((i, j + 1))
  return moves


def swap(puzzle, i1, j1, i2, j2):
    new_puzzle = []
    for row in puzzle:
        new_row = []
        for val in row:
            new_row.append(val)
        new_puzzle.append(new_row)

    new_puzzle[i1][j1], new_puzzle[i2][j2] = new_puzzle[i2][j2], new_puzzle[i1][j1]

    return new_puzzle

def puzzle_to_tuple(puzzle):
    return tuple(tuple(row) for row in puzzle)


def bfs(puzzle, search_order):
    start_time = time.time()
    height, width = puzzle.shape

    # Konwersja do krotki dla hashowania
    initial_state = puzzle_to_tuple(puzzle)

    # Kolejka dla BFS
    queue = deque([initial_state])

    # Słownik do śledzenia odwiedzonych stanów
    visited = {initial_state: True}

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

        # Konwersja z krotki z powrotem na tablicę
        current_puzzle = np.array(current_state)

        # Sprawdź, czy osiągnięto stan docelowy
        if current_state == target:
            # Odtwarzanie ścieżki
            path = []
            state = current_state
            while move_direction[state] is not None:
                path.append(move_direction[state])
                state = parent[state]
            path.reverse()

            # Określenie głębokości rozwiązania
            solution_depth = len(path)
            max_depth = max(max_depth, solution_depth)

            end_time = time.time()
            execution_time = (end_time - start_time) * 1000
            return path, visited_states, processed_states, max_depth, execution_time

        # Znajdź pozycję pustego pola
        i, j = find_zero(current_puzzle)

        # Sprawdź wszystkie możliwe ruchy zgodnie z podanym porządkiem
        for direction in search_order:
            di, dj = directions[direction]
            ni, nj = i + di, j + dj

            # Sprawdź, czy ruch jest możliwy
            if 0 <= ni < height and 0 <= nj < width:
                # Wykonaj ruch
                new_puzzle = swap(current_puzzle, i, j, ni, nj)
                new_state = puzzle_to_tuple(new_puzzle)

                # Jeśli ten stan nie był jeszcze odwiedzony
                if new_state not in visited:
                    queue.append(new_state)
                    visited[new_state] = True
                    visited_states += 1
                    parent[new_state] = current_state
                    move_direction[new_state] = direction

                    # Aktualizacja maksymalnej głębokości
                    current_depth = 0
                    state = current_state
                    while state != initial_state:
                        current_depth += 1
                        state = parent[state]
                    max_depth = max(max_depth, current_depth + 1)

    # Jeśli nie znaleziono rozwiązania
    return None, visited_states, processed_states, max_depth