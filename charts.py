from matplotlib import pyplot as plt
import numpy as np
from main import generate_path_addons


def addons_opener(acronym, choose, subcategories=None):
    countError = 0
    """
    Funkcja otwiera pliki z danymi i oblicza średnie wartości dla podanych parametrów.
    """
    tab_parameter = subcategories or ["RDUL", "LUDR", "RDLU", "LURD", "DRUL", "ULDR", "DRLU", "ULRD"]
    ranges = [0, 2, 6, 16, 40, 94, 201, 413]  # Zakresy poziomów
    averages_per_order = {order: [0] * 7 for order in tab_parameter}  # Średnie dla każdego porządku
    counts_per_order = {order: [0] * 7 for order in tab_parameter}  # Liczba danych dla każdego porządku

    for par in tab_parameter:
        for level in range(7):  # Poziomy od 0 do 6
            for i in range(ranges[level], ranges[level + 1]):
                path = generate_path_addons(acronym, par, level + 1, i - ranges[level] + 1)
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


def rysuj_wykres_słupkowy(averages_dict, title, alogorithm):
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

    plt.xlabel('Głębokość rozwiązania')
    plt.ylabel(title)
    plt.title(f'{alogorithm} - {title}')
    plt.xticks(poziomy)

    plt.legend(title="Porządek przeszukiwania")
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.show()


def main():
    # Nazwy kryteriów
    kryteria = [
        "Długość znalezionego rozwiązania",
        "Liczba stanów odwiedzonych",
        "Liczba stanów przetworzonych",
        "Maksymalna osiągnięta głębokość rekursji",
        "Czas trwania procesu obliczeniowego"
    ]

    # Generowanie wykresów dla BFS
    print("Wykresy dla BFS:")
    for i, kryterium in enumerate(kryteria):
        bfs_averages, errorBfs = addons_opener("bfs", choose=i + 1)

        # Wyświetlanie średnich dla każdego porządku na konsoli
        print(f"\nKryterium: {kryterium}")
        for order, averages in bfs_averages.items():
            print(f"BFS ({order}) - średnie wartości: {averages}")

        # Generowanie wykresu słupkowego z podziałem na porządki przeszukiwania
        rysuj_wykres_słupkowy(bfs_averages,  kryterium, "BFS")

    # Generowanie wykresów dla DFS
    print("\nWykresy dla DFS:")
    for i, kryterium in enumerate(kryteria):
        dfs_averages,errorDfs = addons_opener("dfs", choose=i + 1)

        # Wyświetlanie średnich dla każdego porządku na konsoli
        print(f"\nKryterium: {kryterium}")
        for order, averages in dfs_averages.items():
            print(f"DFS ({order}) - średnie wartości: {averages}")

        # Generowanie wykresu słupkowego z podziałem na porządki przeszukiwania
        rysuj_wykres_słupkowy(dfs_averages, kryterium, "DFS")
    print(f"\nLiczba błędów: BFS: {errorBfs} DFS: { errorDfs}")

if __name__ == "__main__":
    main()
