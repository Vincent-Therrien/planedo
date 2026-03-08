import json
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt

DATA_FILE = Path(__file__).with_name("exoplanets.json")
OUTPUT_FILE = Path(__file__).with_name("discoveries_by_method_per_year.png")


def load_discovery_counts(data_path: Path):
    with data_path.open("r", encoding="utf-8") as source:
        systems = json.load(source)

    counts = defaultdict(lambda: defaultdict(int))
    methods = set()
    years = set()

    for system in systems.values():
        for planet in system.get("Planets", {}).values():
            year_str = planet.get("Discovery year", "").strip()
            method = planet.get("Discovery method", "").strip() or "Unknown"
            if not year_str.isdigit():
                continue
            year = int(year_str)
            counts[year][method] += 1
            methods.add(method)
            years.add(year)

    return counts, sorted(years), sorted(methods)


def plot_discoveries_by_method_per_year(counts, years, methods, output_file: Path):
    if not years or not methods:
        raise ValueError("No valid discovery data found to plot.")

    x = list(range(len(years)))
    bottoms = [0] * len(years)

    plt.figure(figsize=(16, 8))
    methods.remove("Transit")
    methods.remove("Microlensing")
    methods = ["Transit", "Microlensing"] + list(methods)
    for method in methods:
        values = [counts[year].get(method, 0) for year in years]
        plt.bar(x, values, bottom=bottoms, label=method)
        bottoms = [bottom + value for bottom, value in zip(bottoms, values)]

    plt.xticks(x, years, rotation=45)
    plt.xlabel("Discovery year")
    plt.ylabel("Number of exoplanets discovered")
    plt.title("Exoplanets discovered by method per year")
    plt.legend(title="Discovery method", fontsize=8, title_fontsize=9, ncol=2)
    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    plt.show()


if __name__ == "__main__":
    discovery_counts, discovery_years, discovery_methods = load_discovery_counts(DATA_FILE)
    plot_discoveries_by_method_per_year(
        discovery_counts, discovery_years, discovery_methods, OUTPUT_FILE
    )
    years = sorted(discovery_counts)
    discovery_counts = {k: discovery_counts[k] for k in years}
    with open("discovery_years.json", "w") as output_file:
        json.dump(discovery_counts, output_file, indent=4)
