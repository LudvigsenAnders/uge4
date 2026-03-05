# uge4 — Project Overview

This repository contains four exercises (delopgave_01 .. delopgave_04). Each exercise has a main script and related data. All data is in ../uge4/data/

- delopgave_01  
  - Entry: [delopgave_01/src/main.py](delopgave_01/src/main.py) — [`delopgave_01.src.main.main`](delopgave_01/src/main.py)  
  - Uses text utilities: [helper_functions/txt_reader.py](helper_functions/txt_reader.py) — [`helper_functions.txt_reader.get_string_from_file`](helper_functions/txt_reader.py)  
  - Data: [data/Navneliste.txt](data/Navneliste.txt)  
  - Run: python delopgave_01/src/main.py

- delopgave_02  
  - Entry: [delopgave_02/src/main.py](delopgave_02/src/main.py) — [`delopgave_02.src.main.main`](delopgave_02/src/main.py)  
  - Run: python delopgave_02/src/main.py

- delopgave_03  
  - Entry: [delopgave_03/src/main.py](delopgave_03/src/main.py) — [`delopgave_03.src.main.main`](delopgave_03/src/main.py)  
  - Uses CSV data: [data/source_data.csv](data/source_data.csv), [data/write_protect_source_data.csv](data/write_protect_source_data.csv)  
  - Output directory: [data/csv_output/](data/csv_output/)  
  - Run: python delopgave_03/src/main.py

- delopgave_04  
  - Entry: [delopgave_04/src/main.py](delopgave_04/src/main.py) — [`delopgave_04.src.main.main`](delopgave_04/src/main.py)  
  - Uses housing dataset: [data/DKHousingPricesSample100k.csv](data/DKHousingPricesSample100k.csv)  
  - Run: python delopgave_04/src/main.py

Common
- Run any main directly with Python from the repository root, e.g.:
  ```sh
  python delopgave_01/src/main.py