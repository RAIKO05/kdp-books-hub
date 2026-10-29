"""
generate_multigame_cases.py
Builds 35 comprehensive, 4-in-1 multi-stage detective cases.
Each case contains:
1. Incident Dossier & Narrative Story
2. GAME 1: Forensic Evidence Word Search (10x10 letter grid with embedded clues)
3. GAME 2: Encrypted Dispatch (Cryptogram with Caesar or Reverse cipher)
4. GAME 3: Alibi & Motive Matrix (Solver-verified logic grid with 100% unique solution)
5. GAME 4: Official Case Warrant & Resolution
"""

import json
import random
import itertools
import string
import re

def load_assets():
    with open("multi_game_assets.json", "r", encoding="utf-8") as f:
        return json.load(f)

# --- GAME 1: Word Search Generator ---
def generate_word_search(words, grid_size=10):
    grid = [[" " for _ in range(grid_size)] for _ in range(grid_size)]
    placed_words = []

    for word in words:
        w_len = len(word)
        if w_len > grid_size:
            continue
        placed = False
        attempts = 0
        while not placed and attempts < 100:
            attempts += 1
            direction = random.choice(["H", "V"])
            if direction == "H":
                r = random.randint(0, grid_size - 1)
                c = random.randint(0, grid_size - w_len)
                if all(grid[r][c + i] in (" ", word[i]) for i in range(w_len)):
                    for i in range(w_len):
                        grid[r][c + i] = word[i]
                    placed_words.append(word)
                    placed = True
            else:
                r = random.randint(0, grid_size - w_len)
                c = random.randint(0, grid_size - 1)
                if all(grid[r + i][c] in (" ", word[i]) for i in range(w_len)):
                    for i in range(w_len):
                        grid[r + i][c] = word[i]
                    placed_words.append(word)
                    placed = True

    # Fill remaining spaces with random uppercase letters
    for r in range(grid_size):
        for c in range(grid_size):
            if grid[r][c] == " ":
                grid[r][c] = random.choice(string.ascii_uppercase)

    return {"grid": grid, "words_to_find": placed_words}

# --- GAME 2: Cipher Generator ---
def generate_cipher(plain_text):
    shift = 3
    cipher_chars = []
    for ch in plain_text.upper():
        if 'A' <= ch <= 'Z':
            cipher_chars.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
        else:
            cipher_chars.append(ch)
    ciphertext = "".join(cipher_chars)
    hint = "Caesar Shift (Key: +3). Shift each letter back 3 spots in the alphabet (D -> A, E -> B)."
    return {"ciphertext": ciphertext, "plaintext": plain_text.upper(), "hint": hint, "shift": shift}

# --- GAME 3: Constraint Satisfaction Logic Grid ---
def count_valid_solutions(suspects, rooms, weapons, clues):
    room_perms = list(itertools.permutations(rooms))
    weapon_perms = list(itertools.permutations(weapons))
    valid_solutions = []

    for r_perm in room_perms:
        s_to_r = dict(zip(suspects, r_perm))
        for w_perm in weapon_perms:
            s_to_w = dict(zip(suspects, w_perm))
            r_to_w = {s_to_r[s]: s_to_w[s] for s in suspects}

            violation = False
            for clue in clues:
                m1 = re.match(r"(.+?) was confirmed to be in (.+?)\.", clue)
                if m1 and s_to_r.get(m1.group(1)) != m1.group(2):
                    violation = True; break

                m2 = re.match(r"(.+?) was discovered carrying the (.+?)\.", clue)
                if m2 and s_to_w.get(m2.group(1)) != m2.group(2):
                    violation = True; break

                m3 = re.match(r"The investigator found the (.+?) inside (.+?)\.", clue)
                if m3 and r_to_w.get(m3.group(2)) != m3.group(1):
                    violation = True; break

                m4 = re.match(r"(.+?) was never seen near (.+?)\.", clue)
                if m4 and s_to_r.get(m4.group(1)) == m4.group(2):
                    violation = True; break

                m5 = re.match(r"(.+?) had no access to the (.+?)\.", clue)
                if m5 and s_to_w.get(m5.group(1)) == m5.group(2):
                    violation = True; break

                m6 = re.match(r"The weapon recovered from (.+?) was definitely not the (.+?)\.", clue)
                if m6 and r_to_w.get(m6.group(1)) == m6.group(2):
                    violation = True; break

                m7 = re.match(r"Neither (.+?) nor (.+?) had ever visited (.+?)\.", clue)
                if m7 and (s_to_r.get(m7.group(1)) == m7.group(3) or s_to_r.get(m7.group(2)) == m7.group(3)):
                    violation = True; break

                m8 = re.match(r"The lethal strike occurred in (.+?), leaving behind the deadly (.+?)\.", clue)
                if m8 and r_to_w.get(m8.group(1)) != m8.group(2):
                    violation = True; break

                m9 = re.match(r"The suspect in (.+?) did not carry the (.+?)\.", clue)
                if m9 and r_to_w.get(m9.group(1)) == m9.group(2):
                    violation = True; break

                m10 = re.match(r"(.+?) did not enter (.+?)\.", clue)
                if m10 and s_to_r.get(m10.group(1)) == m10.group(2):
                    violation = True; break

            if not violation:
                valid_solutions.append({"s_to_r": s_to_r, "s_to_w": s_to_w})

    return valid_solutions

def generate_logic_puzzle(theme, seed=None):
    if seed: random.seed(seed)
    sus_objs = random.sample(theme["suspects"], 4)
    suspects = [s["name"] for s in sus_objs]
    rooms = random.sample(theme["rooms"], 4)
    weapons = random.sample(theme["weapons"], 4)

    shuffled_rooms = random.sample(rooms, 4)
    shuffled_weapons = random.sample(weapons, 4)

    solution_map = {}
    for i in range(4):
        solution_map[suspects[i]] = {
            "room": shuffled_rooms[i],
            "weapon": shuffled_weapons[i]
        }

    culprit = suspects[0]
    murder_room = solution_map[culprit]["room"]
    murder_weapon = solution_map[culprit]["weapon"]

    clues = [
        f"{suspects[1]} was confirmed to be in {solution_map[suspects[1]]['room']}.",
        f"{suspects[2]} was discovered carrying the {solution_map[suspects[2]]['weapon']}.",
        f"The investigator found the {solution_map[suspects[3]]['weapon']} inside {solution_map[suspects[3]]['room']}.",
        f"{culprit} was never seen near {[r for r in rooms if r != murder_room][0]}.",
        f"{culprit} had no access to the {[w for w in weapons if w != murder_weapon][0]}.",
        f"The weapon recovered from {[r for r in rooms if r != solution_map[suspects[2]]['room']][0]} was definitely not the {solution_map[suspects[2]]['weapon']}.",
        f"Neither {suspects[0]} nor {suspects[3]} had ever visited {solution_map[suspects[1]]['room']}.",
        f"The lethal strike occurred in {murder_room}, leaving behind the deadly {murder_weapon}."
    ]

    sols = count_valid_solutions(suspects, rooms, weapons, clues)
    if len(sols) > 1:
        sol_alt = [s for s in sols if s["s_to_r"] != {s: solution_map[s]["room"] for s in suspects} or s["s_to_w"] != {s: solution_map[s]["weapon"] for s in suspects}][0]
        for s in suspects:
            gt_w = solution_map[s]["weapon"]
            alt_w = sol_alt["s_to_w"][s]
            if gt_w != alt_w:
                clues.append(f"{s} had no access to the {alt_w}.")
                break
            gt_r = solution_map[s]["room"]
            alt_r = sol_alt["s_to_r"][s]
            if gt_r != alt_r:
                clues.append(f"{s} did not enter {alt_r}.")
                break

    final_sols = count_valid_solutions(suspects, rooms, weapons, clues)
    assert len(final_sols) == 1, f"Ambiguous puzzle with {len(final_sols)} solutions!"

    return {
        "suspects": suspects,
        "rooms": rooms,
        "weapons": weapons,
        "clues": clues,
        "solution": {
            "culprit": culprit,
            "murder_room": murder_room,
            "murder_weapon": murder_weapon,
            "full_mapping": solution_map
        }
    }

def build_multigame_cases():
    assets = load_assets()
    all_cases = []

    for case_num in range(1, 36):
        theme = assets["themes"][(case_num - 1) % len(assets["themes"])]
        seed = 7000 + case_num
        random.seed(seed)

        # 1. Logic Grid Generation
        logic = generate_logic_puzzle(theme, seed=seed)

        # 2. Word Search Generation (Select 5 evidence words)
        ev_words = random.sample(theme["forensic_evidence"], 5)
        ws = generate_word_search(ev_words, grid_size=10)

        # 3. Cipher Generation
        cipher_msg = random.choice(theme["cipher_clues"])
        cipher = generate_cipher(cipher_msg)

        case_obj = {
            "case_number": case_num,
            "title": f"Case #{case_num:03d}: The Mystery of {logic['solution']['murder_room']}",
            "theme": theme["name"],
            "briefing": (
                f"A major incident has been declared at {theme['name']}. "
                f"The victim was found deceased in suspicious circumstances. "
                f"Four primary persons of interest are detained on the premises. "
                f"Follow standard detective protocol: conduct a forensic evidence sweep, "
                f"decrypt the intercepted dispatch, analyze alibis on the deduction matrix, "
                f"and sign the official arrest warrant."
            ),
            "game_1_word_search": ws,
            "game_2_cipher": cipher,
            "game_3_logic_grid": {
                "suspects": logic["suspects"],
                "rooms": logic["rooms"],
                "weapons": logic["weapons"],
                "clues": logic["clues"]
            },
            "game_4_solution": logic["solution"]
        }
        all_cases.append(case_obj)

    with open("multigame_cases.json", "w", encoding="utf-8") as f:
        json.dump(all_cases, f, indent=2)

    print(f"Successfully generated {len(all_cases)} 4-in-1 multi-stage cases into multigame_cases.json!")

if __name__ == "__main__":
    build_multigame_cases()
