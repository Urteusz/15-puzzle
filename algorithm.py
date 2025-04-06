import numpy as np

SIZE_HEIGHT = 4
SIZE_WIDTH = 4

directions = {
            'L': (0, -1),  # Lewo
            'R': (0, 1),   # Prawo
            'U': (-1, 0),  # Góra
            'D': (1, 0)    # Dół
        }


def read_board(filename):
    global SIZE_HEIGHT, SIZE_WIDTH
    with open(filename, 'r') as file:
        lines = file.readlines()

    SIZE_HEIGHT, SIZE_WIDTH = map(int, lines[0].split())

    puzzle = np.array([list(map(int, line.split())) for line in lines[1:]])

    return puzzle

def puzzle_to_tuple(puzzle):
    return tuple(map(tuple, puzzle))

def is_solvable(tiles):
    inv_count = 0
    for i in range(len(tiles)):
        if tiles[i] == 0:
            continue
        for j in range(i + 1, len(tiles)):
            if tiles[j] != 0 and tiles[i] > tiles[j]:
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


def swap(puzzle, i1, j1, i2, j2):
    new_puzzle = np.copy(puzzle)
    new_puzzle[i1, j1], new_puzzle[i2, j2] = new_puzzle[i2, j2], new_puzzle[i1, j1]
    return new_puzzle