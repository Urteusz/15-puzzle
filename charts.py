from matplotlib import pyplot as plt
import numpy as np
from createFiles import generate_path_addons
import matplotlib.pyplot as plt



def addons_opener(acronym, choose, subcategories=None):
    countError = 0
    tab_parameter = subcategories or ["RDUL", "LUDR", "RDLU", "LURD", "DRUL", "ULDR", "DRLU", "ULRD"]
    ranges = [0, 2, 6, 16, 40, 94, 201, 413]  # Zakresy poziomów
    averages_per_order = {order: [0] * 7 for order in tab_parameter}  # Średnie dla każdego porządku
    counts_per_order = {order: [0] * 7 for order in tab_parameter}  # Liczba danych dla każdego porządku

    for par in tab_parameter:
        for level in range(7):  # Poziomy od 0 do 6
            for i in range(ranges[level], ranges[level + 1]):
                path = generate_path_addons(acronym, par, level + 1, i - ranges[level] + 1) + "_addons.txt"
                try:
                    with open(path) as file:
                        lines = file.readlines()
                        if len(lines) >= choose and lines[0].strip() != "-1":
                            value = float(lines[choose - 1].strip())
                            averages_per_order[par][level] += value
                            counts_per_order[par][level] += 1
                        elif lines[0].strip() == "-1":
                            countError += 1
                except FileNotFoundError:
                    print(f"Plik {path} nie istnieje.")
                except (IndexError, ValueError):
                    print(f"Nieprawidłowe dane w pliku: {path}")

    # Obliczanie średnich
    for par in tab_parameter:
        for level in range(7):
            if counts_per_order[par][level] > 0:
                averages_per_order[par][level] /= counts_per_order[par][level]

    return averages_per_order, countError


def rysuj_wykres_słupkowy(averages_dict, title, algorithm, log_scale=False):
    """
    Tworzy wykres słupkowy z podziałem na poziomy i porządki przeszukiwania.
    """
    poziomy = np.arange(1, 8)  # Poziomy od 1 do 7
    width = 0.1  # Szerokość pojedynczego słupka w grupie

    plt.figure(figsize=(12, 8))

    for idx, (order, averages) in enumerate(averages_dict.items()):
        plt.bar(poziomy + idx * width - (len(averages_dict) / 2) * width,
                averages,
                width=width,
                label=order)

    plt.xlabel('Głębokość rozwiązania', fontsize=20)
    plt.ylabel(title, fontsize=20)
    plt.title(f'{algorithm}', fontsize=20)
    plt.xticks(poziomy)

    if log_scale:
        plt.yscale('log')  # Ustawienie skali logarytmicznej

    plt.legend(title="Porządek przeszukiwania", fontsize=14, ncol=2)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.show()



def rysuj_wykres_słupkowy_astar(averages_dict, title, log_scale=False):
    """
    Tworzy wykres słupkowy dla A* z podziałem na heurystyki.
    """
    poziomy = np.arange(1, 8)  # Poziomy od 1 do 7
    width = 0.35  # Szerokość słupków

    plt.figure(figsize=(12, 8))

    heurystyki = list(averages_dict.keys())
    for idx, heuristic in enumerate(heurystyki):
        plt.bar(poziomy + idx * width - (len(heurystyki) / 2) * width,
                averages_dict[heuristic],
                width=width,
                label=heuristic)

    plt.xlabel('Głębokość rozwiązania', fontsize=20)
    plt.ylabel(title, fontsize=20)
    plt.title(f'A*', fontsize=20)
    plt.xticks(poziomy)

    if log_scale:
        plt.yscale('log')  # Ustawienie skali logarytmicznej

    plt.legend(title="Heurystyka", fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.show()


def rysuj_wykres_zbiorczy(bfs_averages, dfs_averages, astar_averages_combined, title, log_scale=False):
    """
    Tworzy zbiorczy wykres słupkowy dla BFS, DFS i A*.
    """
    poziomy = np.arange(1, 8)  # Głębokości rozwiązania (1 do 7)
    width = 0.25  # Szerokość słupków

    plt.figure(figsize=(12, 8))

    # Obliczanie średnich wartości dla BFS i DFS
    bfs_values = [np.mean([bfs_averages[order][level] for order in bfs_averages]) for level in range(7)]
    dfs_values = [np.mean([dfs_averages[order][level] for order in dfs_averages]) for level in range(7)]

    # Obliczanie średnich wartości dla A* (łącząc heurystyki)
    astar_values = [
        np.mean([astar_averages_combined[heuristic][level] for heuristic in astar_averages_combined])
        for level in range(7)
    ]

    # Rysowanie słupków
    plt.bar(poziomy - width, bfs_values, width=width, label="BFS")
    plt.bar(poziomy, dfs_values, width=width, label="DFS")
    plt.bar(poziomy + width, astar_values, width=width, label="A*")

    plt.xlabel('Głębokość rozwiązania', fontsize=20)
    plt.ylabel(title, fontsize=20)
    plt.title(f'Ogółem', fontsize=20)
    plt.xticks(poziomy)

    if log_scale:
        plt.yscale('log')  # Ustawienie skali logarytmicznej

    plt.legend(title="Strategia", fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.show()




def main():
    # Nazwy kryteriów
    kryteria = [
        "Długość znalezionego rozwiązania",
        "Liczba stanów odwiedzonych",
        "Liczba stanów przetworzonych",
        "Maksymalna osiągnięta głębokość",
        "Czas trwania procesu obliczeniowego"
    ]

    # Kryteria wymagające skali logarytmicznej
    kryteria_log = {
        "Liczba stanów odwiedzonych",
        "Liczba stanów przetworzonych",
        "Czas trwania procesu obliczeniowego"
    }

    print("Generowanie wyników...")

    for i, kryterium in enumerate(kryteria):
        log_scale = kryterium in kryteria_log

        # BFS
        bfs_averages, errorBfs = addons_opener("bfs", choose=i + 1)
        rysuj_wykres_słupkowy(bfs_averages, kryterium, "BFS", log_scale=log_scale)

        # DFS
        dfs_averages, errorDfs = addons_opener("dfs", choose=i + 1)
        rysuj_wykres_słupkowy(dfs_averages, kryterium, "DFS", log_scale=log_scale)

        # A*
        heurystyki = ["manh", "hamm"]
        astar_averages_combined = {}
        for heuristic in heurystyki:
            astar_averages, errorAstar = addons_opener("astr", choose=i + 1, subcategories=[heuristic])
            astar_averages_combined[heuristic] = list(astar_averages[heuristic])

        rysuj_wykres_słupkowy_astar(astar_averages_combined, kryterium, log_scale=log_scale)

        # Zbiorczy wykres
        rysuj_wykres_zbiorczy(bfs_averages, dfs_averages, astar_averages_combined, kryterium, log_scale=log_scale)

    print(f"\nLiczba błędów: BFS: {errorBfs}, DFS: {errorDfs}, A*: {errorAstar}")




if __name__ == "__main__":
    main()


