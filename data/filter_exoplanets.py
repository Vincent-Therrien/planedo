import csv
import json
from pathlib import Path

ALL_FILE = Path(__file__).with_name("all_exoplanets.csv")
OUTPUT = Path(__file__).with_name("exoplanets.json")

star_systems = {}
unknown_distance = []
star_system_entry = {
    "RA": float,
    "Dec": float,
    "Distance": float,
    "Planets": list,
}
planet_entry = {
    "Confirmed": bool,
    "Mass (Earth)": float,
    "Discovery year": int,
}


def _iter_data_lines(csv_path: Path):
    with csv_path.open("r", newline="", encoding="utf-8") as source:
        for line in source:
            if line.startswith("#") or not line.strip():
                continue
            yield line


def process_file(filename: Path) -> None:
    reader = csv.DictReader(_iter_data_lines(filename))
    for row in reader:
        system_name = row.get("hostname")
        if system_name not in star_systems:
            try:
                distance = float(row.get("sy_dist").strip())
            except:
                distance = "Unknown"
                unknown_distance.append(system_name)
            star_systems[system_name] = {
                "RA (deg)": float(row.get("ra").strip()),
                "Dec (deg)": float(row.get("dec").strip()),
                "Distance (pc)": distance,
                "Planets": {}
            }
        mass = row.get("pl_masse").strip()
        mass = mass if mass else "Unknown"
        radius = row.get("pl_rade").strip()
        radius = radius if radius else "Unknown"
        link_name = row.get("pl_name").strip().lower().replace(" ", "-")
        star_systems[system_name]["Planets"][row.get("pl_name").strip()] = {
            "Mass (Earth mass)": mass,
            "Radius (Earth radius)": radius,
            "Discovery year": row.get("disc_year").strip(),
            "Discovery method": row.get("discoverymethod").strip(),
            "Catalog link": f"https://science.nasa.gov/exoplanet-catalog/{link_name}",
        }


process_file(ALL_FILE)

with open(OUTPUT, "w") as file:
    json.dump(star_systems, file, indent=4)

print(f"Number of star systems: {len(star_systems)}")
print(f"Number of planets: {sum([len(s['Planets']) for s in star_systems.values()])}")
print(unknown_distance)
print(len(unknown_distance))
