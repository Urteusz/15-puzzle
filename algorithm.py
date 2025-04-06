import numpy as np

# Domyślne wymiary planszy
SIZE_HEIGHT = 4
SIZE_WIDTH = 4

# Kierunki ruchu na planszy
directions = {
    'L': (0, -1),  # Lewo
    'R': (0, 1),   # Prawo
    'U': (-1, 0),  # Góra
    'D': (1, 0)    # Dół
}

def read_board(filename):
    # Odczyt planszy z pliku
    global SIZE_HEIGHT, SIZE_WIDTH
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Ustawienie wymiarów planszy
    SIZE_HEIGHT, SIZE_WIDTH = map(int, lines[0].split())

    # Tworzenie macierzy NumPy na podstawie danych z pliku
    puzzle = np.array([list(map(int, line.split())) for line in lines[1:]])
    return puzzle

def puzzle_to_tuple(puzzle):
    # Konwersja macierzy NumPy na krotkę krotek
    return tuple(map(tuple, puzzle))

def matrix(width, height, numer_list):
    # Tworzenie macierzy o podanych wymiarach z listy liczb
    tiles = np.zeros((width, height), dtype=int)  # Pusta macierz wypełniona zerami
    for i in range(width):
        for j in range(height):
            tiles[i][j] = numer_list[height * i + j]  # Wypełnianie wartościami z listy
    return tiles

def find_zero(puzzle):
    # Znajdowanie pozycji elementu o wartości 0
    for i, row in enumerate(puzzle):  # Iteracja po wierszach
        for j, val in enumerate(row):  # Iteracja po kolumnach w wierszu
            if val == 0:  # Sprawdzenie, czy wartość to zero
                return i, j
    return None

def swap(puzzle, i1, j1, i2, j2):
    # Zamiana miejscami dwóch elementów na planszy
    new_puzzle = np.copy(puzzle)  # Kopia oryginalnej planszy
    new_puzzle[i1, j1], new_puzzle[i2, j2] = new_puzzle[i2, j2], new_puzzle[i1, j1]  # Zamiana elementów
    return new_puzzle
