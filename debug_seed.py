import build_volume_2, random, re

theme = build_volume_2.load_assets()['themes'][0]
random.seed(9003)
sus_objs = random.sample(theme['suspects'], 4)
suspects = [s['name'] for s in sus_objs]
rooms = random.sample(theme['rooms'], 4)
weapons = random.sample(theme['weapons'], 4)
shuffled_rooms = random.sample(rooms, 4)
shuffled_weapons = random.sample(weapons, 4)
solution_map = {suspects[i]: {'room': shuffled_rooms[i], 'weapon': shuffled_weapons[i]} for i in range(4)}
culprit = suspects[0]
murder_room = solution_map[culprit]['room']
murder_weapon = solution_map[culprit]['weapon']
wrong_rooms = [r for r in rooms if r != murder_room]
wrong_weapons = [w for w in weapons if w != murder_weapon]

clues = [
    f"{suspects[1]} was confirmed to be in {solution_map[suspects[1]]['room']}.",
    f"{suspects[2]} was discovered carrying the {solution_map[suspects[2]]['weapon']}.",
    f"The investigator found the {solution_map[suspects[3]]['weapon']} inside {solution_map[suspects[3]]['room']}.",
    f"{culprit} was never seen near {wrong_rooms[0]}.",
    f"{culprit} had no access to the {wrong_weapons[0]}.",
    f"The weapon recovered from {[r for r in rooms if r != solution_map[suspects[2]]['room']][0]} was definitely not the {solution_map[suspects[2]]['weapon']}.",
    f"Neither {suspects[0]} nor {suspects[3]} had ever visited {solution_map[suspects[1]]['room']}.",
    f"The lethal strike occurred in {murder_room}, leaving behind the deadly {murder_weapon}."
]

s_to_r = {s: solution_map[s]['room'] for s in suspects}
s_to_w = {s: solution_map[s]['weapon'] for s in suspects}
r_to_w = {s_to_r[s]: s_to_w[s] for s in suspects}

print("s_to_r:", s_to_r)
print("s_to_w:", s_to_w)
print("r_to_w:", r_to_w)

for idx, clue in enumerate(clues):
    m = re.match(r"(.+?) was confirmed to be in (.+?)\.", clue)
    if m and s_to_r.get(m.group(1)) != m.group(2): print(f"Clue {idx+1} violated!")
    m = re.match(r"(.+?) was discovered carrying the (.+?)\.", clue)
    if m and s_to_w.get(m.group(1)) != m.group(2): print(f"Clue {idx+1} violated!")
    m = re.match(r"The investigator found the (.+?) inside (.+?)\.", clue)
    if m and r_to_w.get(m.group(2)) != m.group(1): print(f"Clue {idx+1} violated!")
    m = re.match(r"(.+?) was never seen near (.+?)\.", clue)
    if m and s_to_r.get(m.group(1)) == m.group(2): print(f"Clue {idx+1} violated!")
    m = re.match(r"(.+?) had no access to the (.+?)\.", clue)
    if m and s_to_w.get(m.group(1)) == m.group(2): print(f"Clue {idx+1} violated!")
    m = re.match(r"The weapon recovered from (.+?) was definitely not the (.+?)\.", clue)
    if m and r_to_w.get(m.group(1)) == m.group(2): print(f"Clue {idx+1} violated!")
    m = re.match(r"Neither (.+?) nor (.+?) had ever visited (.+?)\.", clue)
    if m and (s_to_r.get(m.group(1)) == m.group(3) or s_to_r.get(m.group(2)) == m.group(3)): print(f"Clue {idx+1} violated!")
    m = re.match(r"The lethal strike occurred in (.+?), leaving behind the deadly (.+?)\.", clue)
    if m and r_to_w.get(m.group(1)) != m.group(2): print(f"Clue {idx+1} violated!")
