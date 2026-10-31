"""Merge game-extracted ground truth into GungeonMate's JSON data.

Game dump wins on stats; our hand-written fields are preserved.
Stamps PickupObjectId (`id`) on every merged entry so future joins
are exact. Emits merge_report.json for review.
"""
import json, os, re, difflib

TOOLS = r"X:\GungeonMate\tools"
DATA = r"X:\GungeonMate\gungeon_mate\assets\data"
REPORT = os.path.join(TOOLS, "merge_report.json")

dump = json.load(open(os.path.join(TOOLS, "gungeon_dump.json"), encoding="utf-8"))
QUALITY = {"D": 0, "C": 1, "B": 2, "A": 3, "S": 4}

# Dev-name → display-name aliases where fuzzy match fails.
ALIASES = {
    "lamp": "Magic Lamp", "awp": "A.W.P.", "baretta": "Beretta",
    "winchestershotgun": "Winchester", "thompsonsubmachinegun": "Thompson Sub-Machinegun",
    "screechgun": "Screecher", "woodbow": "Bow",
    "m79grenadelauncher": "Grenade Launcher", "moonscraperlaser": "Moonscraper",
    "shadesrevolver": "Shades's Revolver", "m1rifle": "M1",
    "vertebraek47": "VertebraeK-47", "smileyrevolver": "Smiley's Revolver",
    "lemonhandcannon": "Pea Cannon", "s.a.a.": "Colt 1851",
    "crescentmooncrossbow": "Crescent Crossbow", "augun": "AU Gun",
    "standardissuelaser": "Laser Rifle", "gunner": "GuNNER",
    "trankgun": "Trank Gun", "arcgun": "Arc Gun", "winchester97": "Winchester Rifle",
    "colt45": "Colt 1851", "machinepistol": "Machine Pistol",
    "kexcalibur": "Excaliber", "zorgun": "Zorgun",
    "morningstar": "Morning Star", "blashmaster": "The Exotic",
    "blackhole": "Black Hole Gun", "combined": "Combined Rifle",
    "betrayerslies": "Betrayer's Shield", "betrayersshield": "Betrayer's Shield",
    "emberbelt": "Ember", "snubnose": "Snubnosed Revolver",
    "flutterby": "Butterfly Gun", "springleader": "Ice Breaker",
    "crescentrevolver": "Crescent Moon", "bluerevolver": "Blue Gun",
    "hegelian": "Hegemony Carbine", "videogame": "Videogame Gun",
}

def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())

def build_lookup(names):
    lut = {}
    for n in names:
        lut.setdefault(norm(n), n)
    return lut

report = {"guns": {}, "items": {}, "synergies": {"total": len(dump["synergies"])}, "unresolved": []}

# ── GUNS ───────────────────────────────────────────────────────────
guns = json.load(open(os.path.join(DATA, "guns.json"), encoding="utf-8"))
gun_names = build_lookup(g["name"] for g in guns)
matched, dupes = 0, set()
for g in dump["guns"]:
    key = norm(g.get("gunName"))
    name = gun_names.get(key) or gun_names.get(ALIASES.get(key, ""))
    if not name:
        c = difflib.get_close_matches(key, gun_names.keys(), 1, 0.8)
        if c: name = gun_names[c[0]]
    if not name:
        report["unresolved"].append(("gun", g.get("gunName")))
        continue
    if g["id"] in dupes:  # variant-form prefab — same id, keep first
        continue
    dupes.add(g["id"])
    ours = next(x for x in guns if x["name"] == name)
    before = dict(ours)
    ours["id"] = g["id"]
    if g.get("quality") and g["quality"] in QUALITY:
        ours["quality"] = g["quality"]
    if g.get("maxAmmo") is not None: ours["ammo_capacity"] = int(g["maxAmmo"])
    if g.get("reloadTime") is not None: ours["reload_time"] = round(g["reloadTime"], 2)
    p = g.get("projectile") or {}
    if p.get("damage") is not None: ours["damage"] = p["damage"]
    if p.get("speed") is not None: ours["shot_speed"] = p["speed"]
    if p.get("range") is not None: ours["range"] = p["range"]
    if p.get("force") is not None: ours["force"] = p["force"]
    if p.get("spread") is not None: ours["spread"] = p["spread"]
    changed = {k: [before.get(k), ours.get(k)] for k in set(before) | set(ours)
               if before.get(k) != ours.get(k)}
    if changed: report["guns"][name] = changed
    matched += 1
print(f"guns: {matched}/{len(dump['guns'])} merged, {len(report['guns'])} with stat changes")

# ── ITEMS ──────────────────────────────────────────────────────────
items = json.load(open(os.path.join(DATA, "items.json"), encoding="utf-8"))
item_names = build_lookup(i["name"] for i in items)
matched_i, dupes_i = 0, set()
for it in dump["items"]:
    if not it.get("itemName"): continue
    key = norm(it["itemName"])
    name = item_names.get(key) or item_names.get(ALIASES.get(key, ""))
    if not name:
        c = difflib.get_close_matches(key, item_names.keys(), 1, 0.8)
        if c: name = item_names[c[0]]
    if not name or it["id"] in dupes_i:
        if not name: report["unresolved"].append(("item", it.get("itemName")))
        continue
    dupes_i.add(it["id"])
    ours = next(x for x in items if x["name"] == name)
    before = dict(ours)
    ours["id"] = it["id"]
    if it.get("quality") and it["quality"] in QUALITY:
        ours["quality"] = it["quality"]
    changed = {k: [before.get(k), ours.get(k)] for k in set(before) | set(ours)
               if before.get(k) != ours.get(k)}
    if changed: report["items"][name] = changed
    matched_i += 1
print(f"items: {matched_i} merged, {len(report['items'])} changed")

json.dump(guns, open(os.path.join(DATA, "guns.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(items, open(os.path.join(DATA, "items.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(report, open(REPORT, "w"), indent=1)
print(f"report -> {REPORT} | unresolved: {len(report['unresolved'])}")
