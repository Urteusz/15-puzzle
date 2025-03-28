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
    puzzle = np.array([list(map(int, line.split())) for line in lines[1:]])

    return puzzle


def print_board(tiles):
    for i in range(SIZE_WIDTH):
        for j in range(SIZE_HEIGHT):
            print(tiles[SIZE_HEIGHT * i + j], end=' ')


def save_solved(solved, file_name):
    if solved is not None:
        dlugosc_rozw = len(solved)
    else:
        dlugosc_rozw = -1
    plik = open(file_name,'w')
    if dlugosc_rozw == -1:
        plik.write(str(dlugosc_rozw) + '\n')
    else:
        plik.write(str(dlugosc_rozw) + '\n')
        for i in range(len(solved)):
            if i == dlugosc_rozw-1:
                plik.write(str(solved[i]) + '\n')
            else:
                plik.write(str(solved[i]) + ' ')
    plik.close()

def save_addons(solved, file_name, visited, processed, max_depth, time):
    if solved is not None:
        dlugosc_rozw = len(solved)
    else:
        dlugosc_rozw = -1
    plik = open(file_name,'w')
    if dlugosc_rozw == -1:
        plik.write(str(dlugosc_rozw) + '\n')
    else:
        plik.write(str(dlugosc_rozw) + '\n')
        plik.write(str(visited) + '\n')
        plik.write(str(processed) + '\n')
        plik.write(str(max_depth) + '\n')
        plik.write(str(time))
    plik.close()

def solve(acronym, parametr, file_shuffled, file_solved, file_addons):
    puzzle = read_board(file_shuffled)
    if acronym == "bfs":
        path, visited_states, processed_states, max_depth, timer = bfs(puzzle, parametr)
        if path is None:
            print("Lipa")
        save_solved(path,file_solved)
        save_addons(path, file_addons, visited_states, processed_states, max_depth, timer)
    elif acronym == "dfs":
        path, visited_states, processed_states, max_depth, timer = dfs(puzzle, parametr)
        if path is None:
            print("Lipa")
        save_solved(path, file_solved)
        save_addons(path, file_addons, visited_states, processed_states, max_depth, timer)
    elif acronym == "astr":
        print(parametr)


def main():
    # acronym = input()
    # parametr = input()
    # file_shuffled = input()
    # file_solved = input()
    # file_addons = input()
    # solve(acronym, parametr, file_shuffled, file_solved, file_addons)
    acronym = "dfs"
    parametr = "LRUD"
    for i in range(413):
        if i<2:
            path = generate_path(acronym,1,i+1)
            path_solved = generate_path_solved(acronym,1,i+1)
            path_addons = generate_path_addons(acronym,1,i+1)
        elif i<6:
            path = generate_path(acronym,2,i+1-2)
            path_solved = generate_path_solved(acronym,2,i+1-2)
            path_addons = generate_path_addons(acronym,2,i+1-2)
        elif i<16:
            path = generate_path(acronym,3,i+1-6)
            path_solved = generate_path_solved(acronym,3,i+1-6)
            path_addons = generate_path_addons(acronym,3,i+1-6)
        elif i<40:
            path = generate_path(acronym,4,i+1-16)
            path_solved = generate_path_solved(acronym,4,i+1-16)
            path_addons = generate_path_addons(acronym,4,i+1-16)
        elif i<94:
            path = generate_path(acronym,5,i+1-40)
            path_solved = generate_path_solved(acronym,5,i+1-40)
            path_addons = generate_path_addons(acronym,5,i+1-40)
        elif i<201:
            path = generate_path(acronym,6,i+1-94)
            path_solved = generate_path_solved(acronym,6,i+1-94)
            path_addons = generate_path_addons(acronym,6,i+1-94)
        else:
            path = generate_path(acronym,7,i+1-201)
            path_solved = generate_path_solved(acronym,7,i+1-201)
            path_addons = generate_path_addons(acronym,7,i+1-201)

        file_shuffled = path + ".txt"
        file_solved = path_solved + "_solved.txt"
        file_addons = path_addons + "_addons.txt"

        solve(acronym, parametr, file_shuffled, file_solved, file_addons)
        print(path)

def generate_path(acronym,y, x):
    path = "C:/Users/mateu/Downloads/Puzzle/{}/start/4x4_{:02d}_{:05d}".format(acronym,y, x)
    return path
def generate_path_solved(acronym,y, x):
    path = "C:/Users/mateu/Downloads/Puzzle/{}/solved/4x4_{:02d}_{:05d}".format(acronym,y, x)
    return path
def generate_path_addons(acronym,y, x):
    path = "C:/Users/mateu/Downloads/Puzzle/{}/addons/4x4_{:02d}_{:05d}".format(acronym,y, x)
    return path

if __name__ == "__main__":
    main()
