import random
import os
from os.path import basename
import re
from algorithm import *
from astar import astr
from dfs import dfs
from bfs import bfs
from multiprocessing import Pool
import shutil
import os

SIZE_HEIGHT = 4
SIZE_WIDTH = 4


def clear_folders(base_path, acronyms, parameters):
    """
    Usuwa i ponownie tworzy foldery przed startem programu.
    """
    for acronym in acronyms:
        for param in parameters:
            solved_path = f"{base_path}/{acronym}/{param}/solved"
            addons_path = f"{base_path}/{acronym}/{param}/addons"

            for folder in [solved_path, addons_path]:
                if os.path.exists(folder):
                    shutil.rmtree(folder)  # Usuwa folder i jego zawartość
                os.makedirs(folder)  # Tworzy pusty folder

            print(f"Wyczyszczono foldery dla {acronym} - {param}")


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
    with open(file_name, 'w') as plik:
        plik.write(str(dlugosc_rozw) + '\n')
        if dlugosc_rozw != -1:
            plik.write(' '.join(map(str, solved)))


def save_addons(solved, file_name, visited, processed, max_depth, time):
    dlugosc_rozw = len(solved) if solved else -1
    with open(file_name, 'w') as plik:
        plik.write(f"{dlugosc_rozw}\n")
        if dlugosc_rozw != -1:
            plik.write(f"{visited}\n{processed}\n{max_depth}\n{time}")


def solve(acronym, parametr, file_shuffled, file_solved, file_addons):
    puzzle = read_board(file_shuffled)
    if acronym == "bfs":
        path, visited_states, processed_states, max_depth, timer = bfs(puzzle, parametr)
        if path is None:
            print("Lipa")
    elif acronym == "dfs":
        path, visited_states, processed_states, max_depth, timer = dfs(puzzle, parametr)
        if path is None:
            print("Lipa")
    elif acronym == "astr":
        path, visited_states, processed_states, max_depth, timer = astr(puzzle, parametr)
    save_solved(path, file_solved)
    save_addons(path, file_addons, visited_states, processed_states, max_depth, timer)


def generate_files_for_params(acronym, parametr):
    for i in range(413):
        if i < 2:
            path = generate_path(acronym, 1, i + 1)
            path_solved = generate_path_solved(acronym, parametr, 1, i + 1)
            path_addons = generate_path_addons(acronym, parametr, 1, i + 1)
        elif i < 6:
            path = generate_path(acronym, 2, i + 1 - 2)
            path_solved = generate_path_solved(acronym, parametr, 2, i + 1 - 2)
            path_addons = generate_path_addons(acronym, parametr, 2, i + 1 - 2)
        elif i < 16:
            path = generate_path(acronym, 3, i + 1 - 6)
            path_solved = generate_path_solved(acronym, parametr, 3, i + 1 - 6)
            path_addons = generate_path_addons(acronym, parametr, 3, i + 1 - 6)
        elif i < 40:
            path = generate_path(acronym, 4, i + 1 - 16)
            path_solved = generate_path_solved(acronym, parametr, 4, i + 1 - 16)
            path_addons = generate_path_addons(acronym, parametr, 4, i + 1 - 16)
        elif i < 94:
            path = generate_path(acronym, 5, i + 1 - 40)
            path_solved = generate_path_solved(acronym, parametr, 5, i + 1 - 40)
            path_addons = generate_path_addons(acronym, parametr, 5, i + 1 - 40)
        elif i < 201:
            path = generate_path(acronym, 6, i + 1 - 94)
            path_solved = generate_path_solved(acronym, parametr, 6, i + 1 - 94)
            path_addons = generate_path_addons(acronym, parametr, 6, i + 1 - 94)
        else:
            path = generate_path(acronym, 7, i + 1 - 201)
            path_solved = generate_path_solved(acronym, parametr, 7, i + 1 - 201)
            path_addons = generate_path_addons(acronym, parametr, 7, i + 1 - 201)

        file_shuffled = path + ".txt"
        file_solved = path_solved + "_solved.txt"
        file_addons = path_addons + "_addons.txt"

        solve(acronym, parametr, file_shuffled, file_solved, file_addons)
        print(path_solved)


def generate_path(acronym, y, x):
    path = f"C:/Users/mateu/Downloads/Puzzle/{acronym}/start/4x4_{y:02d}_{x:05d}"
    return path


def generate_path_solved(acronym, parametr, y, x):
    path = f"C:/Users/mateu/Downloads/Puzzle/{acronym}/{parametr}/solved/4x4_{y:02d}_{x:05d}"
    return path


def generate_path_addons(acronym, parametr, y, x):
    path = f"C:/Users/mateu/Downloads/Puzzle/{acronym}/{parametr}/addons/4x4_{y:02d}_{x:05d}"
    return path


def main():
    tab_parameter = ["RDUL", "LUDR", "RDLU", "LURD", "DRUL", "ULDR", "DRLU", "ULRD"]
    acronyms = ["bfs", "dfs"]
    base_path = "C:/Users/mateu/Downloads/Puzzle"

    # Wyczyść foldery przed startem
    clear_folders(base_path, acronyms, tab_parameter)

    with Pool() as pool:
        pool.starmap(generate_files_for_params, [(acronym, parametr) for acronym in acronyms for parametr in tab_parameter])


if __name__ == "__main__":
    main()
