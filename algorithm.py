import numpy as np
from collections import deque

from scipy.optimize import newton

EMPTY_TILE = 0

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
  if j < width - 1: moves.append(i, j + 1)
  return moves

def swap(puzzle, x1, y1, x2, y2):
    puzzle[x1][y1], puzzle[x2][y2] = puzzle[x2][y2], puzzle[x1][y1]
    return puzzle