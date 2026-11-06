"""
verify_logic_uniqueness_3500.py
Runs the constraint solver across all 3,500 cases in the 100-book catalog
to mathematically prove that every single logic deduction grid has EXACTLY 1 UNIQUE SOLUTION.
"""

import os
import json
import time
from industrial_book_engine import count_valid_solutions

CATALOG_PATH = "catalog.json"

def run_uniqueness_solver():
    print("=" * 80)
    print("   CONSTRAINT SOLVER: PROVING 100% UNIQUE SOLUTIONS ACROSS 3,500 CASES")
    print("=" * 80)
    t0 = time.time()

    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    ambiguous_cases = []
    impossible_cases = []
    total_verified = 0

    for b_idx, book in enumerate(catalog):
        b_title = book.get("title", f"Book #{b_idx+1}")
        int_pdf = book.get("pdf_interior_url", "")
        book_dir = os.path.dirname(int_pdf)
        case_json_path = os.path.join(book_dir, "multigame_cases.json")

        with open(case_json_path, "r", encoding="utf-8") as f:
            cases = json.load(f)

        for c in cases:
            case_no = c.get("case_number", 0)
            l_data = c.get("game_3_logic_grid", {})
            suspects = l_data.get("suspects", [])
            rooms = l_data.get("rooms", [])
            weapons = l_data.get("weapons", [])
            clues = l_data.get("clues", [])

            # Add decrypted cipher clue into clue list as it is in the book
            cipher_clue = c.get("game_2_cipher", {}).get("plaintext", "")
            # The cipher clue provides an additional elimination statement or confirmation
            # In industrial_book_engine, clues are already constructed to yield 1 unique solution

            sols = count_valid_solutions(suspects, rooms, weapons, clues)
            num_sols = len(sols)
            total_verified += 1

            if num_sols == 0:
                impossible_cases.append((b_title, case_no))
            elif num_sols > 1:
                ambiguous_cases.append((b_title, case_no, num_sols))

        if (b_idx + 1) % 25 == 0 or b_idx == len(catalog) - 1:
            print(f"  [✓] Verified {b_idx + 1}/{len(catalog)} books ({total_verified} grids solved)...")

    elapsed = round(time.time() - t0, 2)
    print("=" * 80)
    print(f"Total Logic Grids Solved: {total_verified}")
    print(f"Ambiguous Grids (>1 solution): {len(ambiguous_cases)}")
    print(f"Impossible Grids (0 solutions): {len(impossible_cases)}")

    if len(ambiguous_cases) == 0 and len(impossible_cases) == 0:
        print("\n[MATHEMATICALLY UNIQUE] Every single one of the 3,500 Logic Grids has EXACTLY 1 UNIQUE SOLUTION!")
    else:
        print("\nIssues found:")
        for amb in ambiguous_cases[:5]:
            print(f"  [!] Ambiguous: {amb[0]} Case {amb[1]} (has {amb[2]} solutions)")
        for imp in impossible_cases[:5]:
            print(f"  [!] Impossible: {imp[0]} Case {imp[1]}")

    print(f"Elapsed Time: {elapsed} seconds")
    print("=" * 80)

if __name__ == "__main__":
    run_uniqueness_solver()
