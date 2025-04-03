import timeit
import numpy as np

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
    new_puzzle = np.copy(puzzle)
    new_puzzle[i1, j1], new_puzzle[i2, j2] = new_puzzle[i2, j2], new_puzzle[i1, j1]
    return new_puzzle


def puzzle_to_tuple(puzzle):
    return tuple(tuple(row) for row in puzzle)







