"""
validate_puzzles.py (v2.0)
Independent verification suite:
Tests all 70 cases against the full 576-state combinatorial search space.
"""

import json
import itertools
import re

def solve_case(case):
    suspects = case["categories"]["Suspects"]
    rooms = case["categories"]["Rooms"]
    weapons = case["categories"]["Weapons"]
    clues = case["clues"]

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

def main():
    with open("generated_cases.json", "r", encoding="utf-8") as f:
        cases = json.load(f)

    print("=" * 60)
    print("INDEPENDENT PUZZLE AUDIT & VALIDATION (70 CASES)")
    print("=" * 60)

    total_cases = len(cases)
    passed = 0
    failed_ambiguous = []
    failed_contradiction = []

    for case in cases:
        c_num = case["case_number"]
        solutions = solve_case(case)
        
        if len(solutions) == 1:
            passed += 1
        elif len(solutions) == 0:
            failed_contradiction.append((c_num, 0))
        else:
            failed_ambiguous.append((c_num, len(solutions)))

    print(f"Total Cases Tested: {total_cases}")
    print(f"Unique Solutions (PASSED): {passed}/{total_cases} ({passed/total_cases*100:.1f}%)")
    print(f"Ambiguous Cases (Multiple Solutions): {len(failed_ambiguous)}")
    print(f"Contradictory Cases (Zero Solutions): {len(failed_contradiction)}")

    results = {
        "total": total_cases,
        "passed": passed,
        "failed_ambiguous": failed_ambiguous,
        "failed_contradiction": failed_contradiction
    }
    with open("validation_report.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
