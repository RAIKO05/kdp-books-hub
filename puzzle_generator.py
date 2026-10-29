"""
puzzle_generator.py (v2.0)
Generates 100% original murder mystery logic grid puzzles with an integrated
solver-in-the-loop: Every single puzzle is mathematically solved on the fly
and guaranteed to have EXACTLY ONE unique solution before being accepted.
"""

import json
import random
import itertools
import re

def load_assets():
    with open("case_assets.json", "r", encoding="utf-8") as f:
        return json.load(f)

def count_valid_solutions(suspects, rooms, weapons, clues):
    room_perms = list(itertools.permutations(rooms))
    weapon_perms = list(itertools.permutations(weapons))

    valid_solutions = []

    for r_perm in room_perms:
        s_to_r = dict(zip(suspects, r_perm))
        for w_perm in weapon_perms:
            s_to_w = dict(zip(suspects, w_perm))
            r_to_w = {s_to_r[s]: s_to_w[s] for s in suspects}

            # Clue evaluations
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

def generate_case(case_num, theme_data, seed=None):
    if seed is not None:
        random.seed(seed)
        
    theme = theme_data
    suspects = random.sample(theme["suspects"], 4)
    rooms = random.sample(theme["rooms"], 4)
    weapons = random.sample(theme["weapons"], 4)
    
    shuffled_rooms = random.sample(rooms, len(rooms))
    shuffled_weapons = random.sample(weapons, len(weapons))
    
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

    # Solver-in-the-loop: Test current clue set
    sols = count_valid_solutions(suspects, rooms, weapons, clues)
    
    # If ambiguous (> 1 solution), iteratively add targeted constraint until exactly 1 solution
    if len(sols) > 1:
        # Identify differences between alternative solution and ground truth
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
                
    # Final check
    final_sols = count_valid_solutions(suspects, rooms, weapons, clues)
    assert len(final_sols) == 1, f"Case #{case_num} did not resolve to 1 solution! Has {len(final_sols)}"

    briefing = (
        f"A ghastly crime has disturbed {theme['name']}. "
        f"The victim was discovered lifeless, and four key persons of interest were found across the grounds. "
        f"Examine the physical evidence, analyze witness statements, and complete the deduction matrix "
        f"to unmask the true culprit and recover the murder weapon."
    )

    return {
        "case_number": case_num,
        "title": f"Case #{case_num:03d}: The Mystery of {murder_room}",
        "theme": theme["name"],
        "briefing": briefing,
        "categories": {
            "Suspects": suspects,
            "Rooms": rooms,
            "Weapons": weapons
        },
        "clues": clues,
        "solution": {
            "culprit": culprit,
            "murder_room": murder_room,
            "murder_weapon": murder_weapon,
            "full_mapping": solution_map
        }
    }

def main():
    assets = load_assets()
    all_cases = []
    themes = assets["themes"]
    
    print("Generating and mathematically verifying 70 cases...")
    for case_id in range(1, 71):
        theme = themes[(case_id - 1) % len(themes)]
        case = generate_case(case_id, theme, seed=2000 + case_id)
        all_cases.append(case)
        
    with open("generated_cases.json", "w", encoding="utf-8") as f:
        json.dump(all_cases, f, indent=2)
        
    print(f"Verified all {len(all_cases)} cases successfully saved to generated_cases.json.")

if __name__ == "__main__":
    main()
