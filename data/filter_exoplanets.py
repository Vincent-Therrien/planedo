from __future__ import annotations

import csv
from pathlib import Path

INPUT_FILE = Path(__file__).with_name("exoplanets.csv")
OUTPUT_FILE = Path(__file__).with_name("filtered_exoplanets.csv")


def _iter_data_lines(csv_path: Path):
    with csv_path.open("r", newline="", encoding="utf-8") as source:
        for line in source:
            if line.startswith("#") or not line.strip():
                continue
            yield line


def main() -> None:
    reader = csv.DictReader(_iter_data_lines(INPUT_FILE))
    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as target:
        writer = csv.writer(target)
        writer.writerow(["system_name", "planet_name", "ra", "dec", "distance"])
        for row in reader:
            print(row.get("soltype"))
            system_name = (row.get("hostname") or "").strip()
            planet_name = (row.get("pl_name") or "").strip()
            ra = row.get("ra").strip()
            dec = row.get("dec").strip()
            distance = row.get("sy_dist").strip()
            writer.writerow([system_name, planet_name, ra, dec, distance])


if __name__ == "__main__":
    main()
