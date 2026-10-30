"""Regenerate synergies.json from the game's AdvancedSynergyDatabase.

Join key: item PickupObjectId sets — our synergy entries' item names
map to ids via the merged guns/items.json, then compare ID sets.
"""
import json, os, re, difflib

TOOLS = r"X:\MEDIA SILO\APPS\GungeonMate\tools"
DATA = r"X:\GungeonMate\gungeon_mate\assets\data"

dump = json.load(open(os.path.join(TOOLS, "gungeon_dump.json"), encoding="utf-8"))
guns = json.load(open(os.path.join(DATA, "guns.json"), encoding="utf-8"))
items = json.load(open(os.path.join(DATA, "items.json"), encoding="utf-8"))
our_syn = json.load(open(os.path.join(DATA, "synergies.json"), encoding="utf-8"))

id2name = {}
for g in guns:
    if "id" in g: id2name[g["id"]] = g["name"]
for i in items:
    if "id" in i: id2name[i["id"]] = i["name"]

def norm(s): return re.sub(r"[^a-z0-9]", "", (s or "").lower())
name2id = {norm(v): k for k, v in id2name.items()}

def ids_for(e):
    return sorted(set((e.get("mandatoryGuns") or []) + (e.get("mandatoryItems") or []) +
                      (e.get("optionalGuns") or []) + (e.get("optionalItems") or [])))

# Our synergy -> id set via item names
def our_ids(s):
    out = set()
    for n in (s.get("items") or []) + (s.get("any_of") or []):
        k = norm(n if isinstance(n, str) else n.get("name", ""))
        if k in name2id: out.add(name2id[k])
    return sorted(out)

report = {"merged": 0, "newFromGame": 0, "oursUnmatched": [], "gameUnmatched": []}
used = set()
for s in our_syn:
    oid = our_ids(s)
    if not oid: continue
    for gi, g in enumerate(dump["synergies"]):
        gid = ids_for(g)
        if oid == gid or (oid and gid and set(oid) == set(gid)):
            s.setdefault("game_name_key", g["nameKey"])
            used.add(gi)
            report["merged"] += 1
            break
    else:
        report["oursUnmatched"].append(s["name"])

new_syns = []
for gi, g in enumerate(dump["synergies"]):
    if gi in used: continue
    req = [id2name.get(i) for i in (g["mandatoryGuns"] or []) + (g["mandatoryItems"] or [])]
    opt = [id2name.get(i) for i in (g["optionalGuns"] or []) + (g["optionalItems"] or [])]
    if all(req) and all(opt) and (req or opt):
        new_syns.append({"name": g["nameKey"], "items": [n for n in req if n],
                         "any_of": [n for n in opt if n], "effect": "",
                         "icon": "", "_from_game": True})
        report["newFromGame"] += 1
    else:
        report["gameUnmatched"].append(g["nameKey"])

print(f"matched: {report['merged']} | new from game: {report['newFromGame']} | ours unmatched: {len(report['oursUnmatched'])} | game unmatched: {len(report['gameUnmatched'])}")
print("ours unmatched sample:", report["oursUnmatched"][:15])
print("game unmatched sample:", report["gameUnmatched"][:15])
json.dump(report, open(os.path.join(TOOLS, "synergy_merge_report.json"), "w"), indent=1)
json.dump(new_syns, open(os.path.join(TOOLS, "new_synergies.json"), "w"), indent=1)
