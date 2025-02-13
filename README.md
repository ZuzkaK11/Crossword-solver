# CSP - Crossword-solver
The "Crossword Solver" project, implemented in Python, solves crossword puzzles using CSP techniques, backtracking, and the MRV heuristic. It efficiently fills a 2D grid with words from a dictionary, ensuring valid placements. Key features include word preprocessing, heuristic optimization, and saving solved puzzles with performance metrics.

Projekt z predmetu úvod do umelej inteligencie.

Tento program je implementovaný v jazyku **Python** a rieši problém **CSP (Constraint Satisfaction Problem)**, konkrétne problém riešenia krížoviek. Používa algoritmus **backtracking** a heuristiku **MRV (Minimum Remaining Values)** na vyplnenie prázdnych pozícií v krížovke slovami zo zadaného zoznamu. 

Krížovka je reprezentovaná ako **2D zoznam**, kde každý prvok môže byť:
- `#` (blokované miesto),
- `" "` (prázdne miesto, kde môže byť umiestnené písmeno).

Krížovka sa považuje za vyriešenú, ak:
- nie sú prítomné žiadne prázdne miesta,
- všetky slová v smere nadol a doprava sú platné slová zo zadaného slovníka.

## Mnou implementované metódy
- **`can_write_word(self, position, word)`**: Skontroluje, či je možné umiestniť slovo na danú pozíciu.
- **`grid_to_string(self)`**: Formátovanie aktuálnej mriežky na reťazec na účely uloženia do súboru.
- **`preprocess_words(words)`**: Predspracuje zoznam slov - zgrupuje ich podľa dĺžky a vráti slovník, kde kľúčom je dĺžka slova a hodnotou zoznam slov tejto dĺžky. Tento krok zefektívňuje vyhľadávanie vhodných slov.
- **`mrv(crossword, preprocessed_words)`**: Heuristika MRV - výber pozície s najmenším počtom možných slov.
- **`solve(crossword, words)`**: Hlavná funkcia na riešenie krížovky. Používa **backtracking** na vyplnenie krížovky zo zoznamu slov.
- **`save_solved_grids(grids, times, points_tracker, path)`**: Zapisuje vyriešené krížovky do súboru vrátane času riešenia a počtu bodov.

## Algoritmus Riešenia Krížovky – Metóda `solve`
1. **Predspracovanie slov**:
   - Vytvorí sa slovník `preprocessed_words`, ktorý zoskupuje slová podľa dĺžky, čo zefektívňuje vyhľadávanie.
   
2. **Backtracking**:
   - **Kontrola dokončenia**: Ak neexistujú voľné pozície, krížovka je dokončená.
   - **Výber pozície pomocou MRV**: Zvolí sa pozícia s najmenším počtom možných slov.
   - **Získanie platných slov**: Získajú sa slová správnej dĺžky, ktoré môžu byť umiestnené.
   - **Rekurzívne volanie**: Slovo sa umiestni, pozícia sa odstráni zo zoznamu voľných pozícií, a algoritmus pokračuje.
   - **Backtracking**: Ak sa zistí, že slovo vedie k neplatnému riešeniu, pozícia sa obnoví do voľných miest.

3. **Ukončenie procesu**:
   - Ak sú všetky pozície úspešne vyplnené, algoritmus vráti `True`. Inak vráti `False`.

## Poznámky k optimalizácii
- Implementované metódy umožnili vyriešiť prvých 8 úloh.
- Skúšali sa aj iné prístupy, napríklad **LCV (Least Constraining Value)** a optimalizácie MRV. Tieto metódy však boli pomalšie a neposkytli lepšie výsledky.
