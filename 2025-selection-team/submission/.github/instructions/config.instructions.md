---
applyTo: '**'
---

## Development Environment Guide

This project is based on Python 3 and uses two external libraries: pandas and matplotlib.

There are three CSV files: `area_map.csv`, `area_struct.csv`, and `area_category.csv`. 

### Data Files Description
- `area_map.csv`: Basic map data containing regional areas and coordinate information.
- `area_struct.csv`: Data representing the location and type (ID) of structures.
- `area_category.csv`: Reference data that maps structure type IDs to names.

The code for each stage should be written in the following files:
- Stage 1: `mas_map.py` (Data Analysis)
- Stage 2: `map_draw.py` (Map Visualization)
- Stage 3: `map_direct_save.py` (Path Finding)

The final outputs will be `map.png`, `map_final.png`, and `home_to_cafe.csv`.

No additional libraries or frameworks should be used; implementation must be done using only Python's standard library.