import importlib

from pipeline.common import OUTPUT, write

STEPS = ["02_buildings", "03_damage", "04_validate", "05_triage"]


def main():
    buildings = None
    for name in STEPS:
        module = importlib.import_module(f"pipeline.{name}")
        buildings = module.run(buildings)
        print(f"{name}: {len(buildings)} buildings")
    write(buildings)
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    main()
