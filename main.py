import concurrent.futures
import multiprocessing
import random
import os
from os.path import basename
import re
import shutil
import numpy as np
import time
from algorithm import *
from astar import astr
from dfs import dfs
from bfs import bfs

SIZE_HEIGHT = 4
SIZE_WIDTH = 4


def create_folder_structure(base_path, acronyms, parameters):
    """
    Tworzy strukturę folderów dla wszystkich algorytmów i parametrów.
    Jeśli foldery już istnieją, usuwa je i tworzy nowe.
    """
    # Najpierw upewnij się, że istnieje folder bazowy
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    for acronym in acronyms:
        # Upewnij się, że istnieje folder dla danego algorytmu
        algorithm_path = f"{base_path}/{acronym}"
        if not os.path.exists(algorithm_path):
            os.makedirs(algorithm_path)

        # Upewnij się, że istnieje folder start dla danego algorytmu
        start_path = f"{algorithm_path}/start"
        if not os.path.exists(start_path):
            os.makedirs(start_path)

        for param in parameters:
            # Ścieżka do folderu parametru
            param_path = f"{algorithm_path}/{param}"
            if not os.path.exists(param_path):
                os.makedirs(param_path)

            # Ścieżki do podfolderów
            solved_path = f"{param_path}/solved"
            addons_path = f"{param_path}/addons"

            # Usuń i utwórz podfoldery
            for folder in [solved_path, addons_path]:
                if os.path.exists(folder):
                    shutil.rmtree(folder)  # Usuwa folder i jego zawartość
                os.makedirs(folder)  # Tworzy pusty folder

            print(f"Utworzono strukturę folderów dla {acronym} - {param}")


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
    # Upewnij się, że folder docelowy istnieje
    os.makedirs(os.path.dirname(file_solved), exist_ok=True)
    os.makedirs(os.path.dirname(file_addons), exist_ok=True)

    try:
        puzzle = read_board(file_shuffled)
        if acronym == "bfs":
            path, visited_states, processed_states, max_depth, timer = bfs(puzzle, parametr)
        elif acronym == "dfs":
            path, visited_states, processed_states, max_depth, timer = dfs(puzzle, parametr)
            if path is None:
                print(f"Nie znaleziono rozwiązania dla {file_shuffled}")
        elif acronym == "astr":
            path, visited_states, processed_states, max_depth, timer = astr(puzzle, parametr)
        save_solved(path, file_solved)
        save_addons(path, file_addons, visited_states, processed_states, max_depth, timer)
        return True, file_shuffled
    except Exception as e:
        print(f"Błąd podczas rozwiązywania {file_shuffled}: {e}")
        return False, file_shuffled


def process_single_file(args):
    """
    Funkcja do przetwarzania pojedynczego pliku w puli wątków.
    """
    acronym, parametr, level_folder, index, task_id, total_tasks = args

    path = generate_path(level_folder, index)
    path_solved = generate_path_solved(acronym, parametr, level_folder, index)
    path_addons = generate_path_addons(acronym, parametr, level_folder, index)

    file_shuffled = path + ".txt"
    file_solved = path_solved + "_solved.txt"
    file_addons = path_addons + "_addons.txt"

    if os.path.exists(file_shuffled):
        result = solve(acronym, parametr, file_shuffled, file_solved, file_addons)
        return result, task_id, total_tasks
    else:
        return (False, f"Brak pliku: {file_shuffled}"), task_id, total_tasks


def generate_path(y, x):
    path = f"puzzles/start/4x4_{y:02d}_{x:05d}"
    return path


def generate_path_solved(acronym, parametr, y, x):
    path = f"puzzles/{acronym}/{parametr}/solved/4x4_{y:02d}_{x:05d}"
    return path


def generate_path_addons(acronym, parametr, y, x):
    path = f"puzzles/{acronym}/{parametr}/addons/4x4_{y:02d}_{x:05d}"
    return path


# Funkcja do wyświetlania paska postępu
def print_progress_bar(completed, total, length=50):
    progress = completed / total
    bar = '█' * int(length * progress) + '-' * (length - int(length * progress))
    percent = int(progress * 100)
    print(f'\r[{bar}] {percent}% ({completed}/{total}) ukończono', end='')
    if completed == total:
        print()


def main():
    tab_parameter = ["RDUL", "LUDR", "RDLU", "LURD", "DRUL", "ULDR", "DRLU", "ULRD"]
    acronyms = ["bfs", "dfs"]
    base_path = "puzzles"
    ranges = [0, 2, 6, 16, 40, 94, 201, 413]

    # Tworzy strukturę folderów przed rozpoczęciem
    create_folder_structure(base_path, acronyms, tab_parameter)

    # Przygotowanie listy wszystkich zadań do wykonania
    all_tasks = []
    task_id = 0
    total_tasks = 0

    # Obliczenie całkowitej liczby zadań
    for acronym in acronyms:
        for parametr in tab_parameter:
            for level in range(7):  # Poziomy od 0 do 6
                total_tasks += ranges[level + 1] - ranges[level]

    for acronym in acronyms:
        for parametr in tab_parameter:
            for level in range(7):  # Poziomy od 0 do 6
                for i in range(ranges[level], ranges[level + 1]):
                    if i < 2:
                        level_folder = 1
                        index = i + 1
                    elif i < 6:
                        level_folder = 2
                        index = i + 1 - 2
                    elif i < 16:
                        level_folder = 3
                        index = i + 1 - 6
                    elif i < 40:
                        level_folder = 4
                        index = i + 1 - 16
                    elif i < 94:
                        level_folder = 5
                        index = i + 1 - 40
                    elif i < 201:
                        level_folder = 6
                        index = i + 1 - 94
                    else:
                        level_folder = 7
                        index = i + 1 - 201

                    all_tasks.append((acronym, parametr, level_folder, index, task_id, total_tasks))
                    task_id += 1

    # Ustawienie ilości wątków
    num_workers = multiprocessing.cpu_count()
    print(f"Używanie {num_workers} wątków do przetwarzania {len(all_tasks)} zadań")

    # Inicjalizacja licznika ukończonych zadań
    completed_tasks = 0
    progress_update_interval = max(1, total_tasks // 100)  # Aktualizacja co 1% zadań
    success_count = 0
    failure_count = 0

    # Wyświetl początkowy pasek postępu
    print_progress_bar(completed_tasks, total_tasks)

    # Ostatnia aktualizacja czasu
    last_update_time = time.time()
    update_interval = 1.0  # Aktualizacja co sekundę

    # Przetwarzanie wszystkich zadań równolegle z monitorowaniem postępu
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(process_single_file, task) for task in all_tasks]

        for future in concurrent.futures.as_completed(futures):
            result, task_id, total = future.result()
            completed_tasks += 1

            if result[0]:
                success_count += 1
            else:
                failure_count += 1

            # Aktualizuj pasek postępu co określony interwał czasowy
            current_time = time.time()
            if current_time - last_update_time >= update_interval:
                print_progress_bar(completed_tasks, total_tasks)
                last_update_time = current_time

    # Końcowe wyświetlenie paska postępu
    print_progress_bar(completed_tasks, total_tasks)

    # Podsumowanie wyników
    print(f"Zakończono przetwarzanie. Sukcesy: {success_count}, Niepowodzenia: {failure_count}")


if __name__ == "__main__":
    main()