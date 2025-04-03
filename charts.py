from matplotlib import pyplot as plt
from numpy.ma.extras import average as np_average  # Importuj 'average' z numpy z aliasem

from main import *


def addons_opener(acronym, choose):
    tab_parameter = ["RDUL", "LUDR", "RDLU", "LURD", "DRUL", "ULDR", "DRLU", "ULRD"]
    ranges = [0, 2, 6, 16, 40, 94, 201, 413]
    sums, counts, averages = [0] * 7, [0] * 7, [0] * 7  # Zmieniamy 'average' na 'averages'

    for par in tab_parameter:
        for level in range(7):
            for i in range(ranges[level], ranges[level + 1]):
                path = generate_path_addons(acronym, par, level + 1, i - ranges[level] + 1)
                try:
                    with open(path) as file:
                        lines = file.readlines()
                        if len(lines) >= choose and lines[0] != -1:
                            value = float(lines[choose - 1])  # Wybieramy odpowiednią linię
                            sums[level] += value  # Sumujemy wartość
                            counts[level] += 1  # Zliczamy liczbę wierszy
                        else:
                            print(f"Plik {path} ma mniej niż {choose} linii.")
                except FileNotFoundError:
                    print(f"Plik {path} nie istnieje.")
                except IndexError:
                    print(f"Plik {path} nie zawiera wystarczającej liczby wierszy.")

    for level in range(7):
        if counts[level] > 0:
            averages[level] = sums[level] / counts[level]


    return averages




def generate_path_addons(acronym,parametr, y, x):
    # Generowanie pełnej ścieżki
    path = f"C:/Users/mateu/Downloads/Puzzle/{acronym}/{parametr}/addons/4x4_{y:02d}_{x:05d}_addons.txt"
    return path


def rysuj_wykres(averages):
    # Tworzenie wykresu słupkowego
    plt.figure(figsize=(10, 6))
    poziomy = [i + 1 for i in range(7)]  # Poziomy od 1 do 7
    plt.bar(poziomy, averages)
    plt.xlabel('Poziom')
    plt.ylabel('Średnia wartość')
    plt.title('Średnie wartości dla różnych poziomów')
    plt.xticks(poziomy)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Dodawanie wartości nad słupkami
    for i, v in enumerate(averages):
        plt.text(i + 1, v, f"{v:.2f}", ha='center', va='bottom')

    plt.show()

def main():
    for i in range(5):
        averages = addons_opener("bfs", i+1)
        print (f"Średnie wartości dla {i+1} wiersza: {averages}")
        rysuj_wykres(averages)


if __name__ == "__main__":
    main()
