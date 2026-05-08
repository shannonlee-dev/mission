---
---
Provide project context and coding guidelines that AI should follow when generating code, answering questions, or reviewing changes.

## Stage 1: Data Collection and Analysis

### Tasks
- Load and analyze the contents of `area_map.csv`, `area_struct.csv`, and `area_category.csv` files.
- Convert structure IDs to names based on `area_category.csv`.
- Merge the three datasets into a single DataFrame and sort by area.
- Filter and output only area 1 data, as the confirmed data shows that Bandalkom Coffee is concentrated in area 1, making information from other areas unnecessary.
- Save the result code as `mas_map.py`.

## Stage 2: Map Visualization

### Tasks
- Visualize the regional map based on analyzed data.
- The map should be visualized with the top-left as (1, 1) and the bottom-right as the largest coordinates.
- Draw horizontal and vertical grid lines.
- Represent structures as follows:
  - Apartments and buildings: brown circles
  - Bandalkom Coffee locations: green squares
  - My home location: green triangle
  - Construction sites: gray squares
- Gray squares representing construction sites may slightly overlap with adjacent coordinates.
- If construction sites overlap with other structures (apartments, buildings), consider them as construction sites.
- Save the visualization as `map.png` file.
- Save the visualization code as `map_draw.py`.

## Stage 3: Shortest Path Finding

### Tasks
- Find the shortest path from **my home (starting point)** to **Bandalkom Coffee locations (destination)** using the analyzed map data.
- Implement one of the known shortest path algorithms directly, not randomly (e.g., BFS, Dijkstra, A*).
- Implement so that locations with construction sites cannot be traversed.
- Once the shortest path is found, save the path as a CSV file named `home_to_cafe.csv`.
- Visualize the path on the map with red lines and save as `map_final.png`.
- Save the entire code as `map_direct_save.py`.