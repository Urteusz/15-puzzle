import random
import os
from os.path import basename
import re

from algorithm import *

SIZE_HEIGHT = 4
SIZE_WIDTH = 4


def read_board(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

        SIZE_HEIGHT, SIZE_WIDTH = map(int, lines[0].split())

        puzzle = [list(map(int, line.split())) for line in lines [1:]]

        return puzzle, SIZE_WIDTH, SIZE_HEIGHT
#
# def shuffle_board():
#     tiles = list(range(SIZE_HEIGHT * SIZE_WIDTH))
#     while True:
#         random.shuffle(tiles)
#         if is_solvable(tiles):
#             return tiles





def print_board(tiles):
    for i in range(SIZE_WIDTH):
        for j in range(SIZE_HEIGHT):
            print(tiles[SIZE_HEIGHT * i + j], end=' ')


# def move_tile(tiles, tile):
#     if tile not in tiles or tile == EMPTY_TILE:
#         return tiles
#
#     index = tiles.index(tile)
#     empty_index = tiles.index(EMPTY_TILE)
#     row, col = divmod(index, SIZE_WIDTH)
#     empty_row, empty_col = divmod(empty_index, SIZE_WIDTH)
#
#     if abs(row - empty_row) + abs(col - empty_col) == 1:
#         tiles[index], tiles[empty_index] = tiles[empty_index], tiles[index]
#     return tiles

def solve(acronym, parametr, file_shuffled, file_solved, file_addons):
    if acronym == "bfs":
        print(parametr)
    elif acronym == "dfs":
        print(parametr)
    elif acronym == "astr":
        print(parametr)

def save_solved(solved, file_name):
    dlugosc_rozw = len(solved)
    plik = open('file_name','w')
    if dlugosc_rozw == 1 and solved == -1:
        plik.write(solved + '\n')
    else:
        plik.write(dlugosc_rozw + '\n')
        for i in range(len(solved)):
            if i == dlugosc_rozw-1:
                plik.write(str(solved[i]) + '\n')
            else:
                plik.write(str(solved[i]) + ' ')
    plik.close()

def save_addons(solved, file_addons, file_name):
    dlugosc_rozw = len(solved)
    plik = open('file_name','w')
    if dlugosc_rozw == 1 and solved == -1:
        plik.write(solved + '\n')
    else:
        plik.write(dlugosc_rozw + '\n')

        print("to be continued...")


def main():

    tiles = shuffle_board()
    print_board(tiles)



if __name__ == "__main__":
    main()
