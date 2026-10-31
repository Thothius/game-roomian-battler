"""Dump Enter the Gungeon item/gun/synergy data from the installed game.

Reads the Unity asset bundle brave_resources_001 (serialized prefabs)
via UnityPy — no mod install or game launch needed.
"""
import json, os, sys
import UnityPy

ETG = r"X:\Games\Enter the Gungeon"
BUNDLE = os.path.join(ETG, r"EtG_Data\StreamingAssets\Assets\brave_resources_001")
OUT = r"X:\GungeonMate\tools\gungeon_dump.json"

env = UnityPy.load(BUNDLE)

# ── indexes ──────────────────────────────────────────────────────────
by_pid = {}
script_names = {}
for o in env.objects:
    by_pid[o.path_id] = o
for o in env.objects:
    if o.type.name == "MonoScript":
        try:
            script_names[o.path_id] = o.read_typetree().get("m_ClassName")
        except Exception:
            pass

def script_of(tree):
    s = tree.get("m_Script") or {}
    return script_names.get(s.get("m_PathID", 0), "")

def resolve(pptr):
    if not isinstance(pptr, dict):
        return None
    if pptr.get("m_FileID", 0) == 0 and pptr.get("m_PathID", 0) != 0:
        return by_pid.get(pptr["m_PathID"])
    return None  # cross-file refs skipped

QUALITY = {0: "D", 1: "C", 2: "B", 3: "A", 4: "S", 5: "COMMON", -1: ""}

def proj_stats(pptr):
    """Resolve a projectile PPtr → its Projectile MonoBehaviour stats."""
    o = resolve(pptr)
    if o is None:
        return None
    try:
        t = o.read_typetree()
    except Exception:
        return None
    if script_of(t) != "Projectile":
        return None
    bd = t.get("baseData") or {}
    return {
        "damage": bd.get("damage"),
        "speed": bd.get("speed"),
        "range": bd.get("range"),
        "force": bd.get("force"),
        "spread": bd.get("spread") or bd.get("spreadDegrees"),
        "accuracy": bd.get("accuracy"),
        "damagesWalls": bd.get("damagesWalls"),
        "dampedFalloff": bd.get("dampedFalloff"),
    }

guns, items, other = [], [], []
synergy_db = None

for o in env.objects:
    if o.type.name != "MonoBehaviour":
        continue
    try:
        t = o.read_typetree()
    except Exception:
        continue
    cls = script_of(t)
    if cls == "Gun":
        g = {
            "gunName": t.get("gunName"),
            "id": t.get("PickupObjectId"),
            "quality": QUALITY.get(t.get("quality"), t.get("quality")),
            "gunClass": t.get("gunClass"),
            "maxAmmo": t.get("maxAmmo"),
            "ammo": t.get("ammo"),
            "reloadTime": t.get("reloadTime"),
            "shootStyle": (t.get("singleModule") or {}).get("shootStyle"),
        }
        projs = []
        for p in (t.get("singleModule") or {}).get("projectiles") or []:
            ps = proj_stats(p)
            if ps:
                projs.append(ps)
        if projs:
            g["projectile"] = projs[0]
            if len(projs) > 1:
                g["projectileCount"] = len(projs)
        guns.append(g)
    elif cls in ("PassiveItem", "PlayerItem", "BasicStatPickup",
                 "ActiveBasicStatItem") or cls.endswith("Item"):
        items.append({
            "class": cls,
            "itemName": t.get("itemName"),
            "id": t.get("PickupObjectId"),
            "quality": QUALITY.get(t.get("quality"), t.get("quality")),
            "type": t.get("consumable") if "consumable" in t else None,
        })
    elif cls in ("AdvancedSynergyDatabase", "PickupObjectDatabase"):
        synergy_db = {"class": cls, "keys": list(t.keys())[:40]}

guns.sort(key=lambda g: g["id"] or 0)
items.sort(key=lambda i: i["id"] or 0)
json.dump({"guns": guns, "items": items,
           "synergyDbHint": synergy_db},
          open(OUT, "w"), indent=1)
print(f"{len(guns)} guns, {len(items)} item-likes, db hint: {bool(synergy_db)}")
print("sample gun:", json.dumps(guns[0], indent=1)[:600])

# ── synergies (shared_auto_001) ─────────────────────────────────────
env2 = UnityPy.load(r"X:\Games\Enter the Gungeon\EtG_Data\StreamingAssets\Assets\shared_auto_001")
scripts2 = {}
for o in env2.objects:
    if o.type.name == "MonoScript":
        try: scripts2[o.path_id] = o.read_typetree().get("m_ClassName")
        except: pass

syns = []
for o in env2.objects:
    if o.type.name != "MonoBehaviour": continue
    try:
        t = o.read_typetree()
        if scripts2.get((t.get("m_Script") or {}).get("m_PathID", 0)) != "AdvancedSynergyDatabase":
            continue
    except: continue
    for e in t.get("synergies") or []:
        syns.append({
            "nameKey": e.get("NameKey"),
            "mandatoryGuns": e.get("MandatoryGunIDs"),
            "mandatoryItems": e.get("MandatoryItemIDs"),
            "optionalGuns": e.get("OptionalGunIDs"),
            "optionalItems": e.get("OptionalItemIDs"),
            "required": e.get("NumberObjectsRequired"),
            "needGunAndItem": bool(e.get("RequiresAtLeastOneGunAndOneItem")),
        })

data = json.load(open(OUT))
data["synergies"] = syns
json.dump(data, open(OUT, "w"), indent=1)
print(f"{len(syns)} synergies added -> {OUT}")

# ── diff vs shipped app data ─────────────────────────────────────
import re, glob
appdir = r"X:\GungeonMate\gungeon_mate\assets\data"
ours = {}
for f in ("guns.json", "items.json", "synergies.json"):
    try:
        ours[f] = len(json.load(open(os.path.join(appdir, f), encoding="utf-8")))
    except Exception as e:
        ours[f] = f"err {e}"
print("game dump:", len(data["guns"]), "guns,", len(data["items"]), "items,", len(syns), "synergies")
print("our json :", ours)

# ── enemies + bosses (enemies_base_001) ────────────────────────────
env3 = UnityPy.load(r"X:\Games\Enter the Gungeon\EtG_Data\StreamingAssets\Assets\enemies_base_001")
by_pid3 = {}
s3 = {}
for o in env3.objects:
    by_pid3[o.path_id] = o
for o in env3.objects:
    if o.type.name == "MonoScript":
        try: s3[o.path_id] = o.read_typetree().get("m_ClassName")
        except: pass

def cls3(tree):
    return s3.get((tree.get("m_Script") or {}).get("m_PathID", 0), "")

# Index GameObject -> child components
go_comps = {}
for o in env3.objects:
    if o.type.name != "MonoBehaviour": continue
    try:
        t = o.read_typetree()
    except: continue
    g = (t.get("m_GameObject") or {}).get("m_PathID", 0)
    go_comps.setdefault(g, []).append((cls3(t), t))

enemies = []
for g, comps in go_comps.items():
    names = [c for c, _ in comps]
    if "AIActor" not in names:
        continue
    go = by_pid3.get(g)
    gname = ""
    if go is not None:
        try: gname = go.read_typetree().get("m_Name", "")
        except: pass
    health = None
    for c, t in comps:
        if c in ("HealthHaver", "DungeonPlaceable"):
            health = t.get("maxHealth") or t.get("health") or t.get("ForceMaximumHealth")
    is_boss = any("boss" in c.lower() for c, _ in comps) or "boss" in gname.lower()
    enemies.append({"prefab": gname, "classes": names[:8],
                    "maxHealth": health, "isBoss": is_boss})

# ── shrines + NPCs (shared_auto bundles) ───────────────────────────
shrines, npcs = [], []
for b in ("shared_auto_001", "shared_auto_002", "foyer_002"):
    try:
        envb = UnityPy.load(rf"X:\Games\Enter the Gungeon\EtG_Data\StreamingAssets\Assets\{b}")
    except Exception:
        continue
    sb = {}
    for o in envb.objects:
        if o.type.name == "MonoScript":
            try: sb[o.path_id] = o.read_typetree().get("m_ClassName")
            except: pass
    for o in envb.objects:
        if o.type.name != "MonoBehaviour": continue
        try:
            t = o.read_typetree()
        except: continue
        cls = sb.get((t.get("m_Script") or {}).get("m_PathID", 0), "")
        if cls and "shrine" in cls.lower() and "controller" in cls.lower():
            shrines.append({"class": cls, "fields": {
                k: v for k, v in t.items()
                if not isinstance(v, dict) and not isinstance(v, list)
                and k not in ("m_GameObject", "m_Enabled", "m_Script", "m_Name")}})
        elif cls in ("TalkDoerLite", "TalkDoer"):
            npcs.append({"class": cls,
                         "fields": {k: v for k, v in t.items()
                                    if not isinstance(v, dict) and not isinstance(v, list)
                                    and k not in ("m_GameObject", "m_Enabled", "m_Script", "m_Name")}})

data = json.load(open(OUT))
data["enemies"] = enemies
data["shrines"] = shrines
data["npcs"] = npcs
json.dump(data, open(OUT, "w"), indent=1)
print(f"+ {len(enemies)} enemies, {len(shrines)} shrine-MBs, {len(npcs)} npcs")
bosses = [e for e in enemies if e["isBoss"]]
print(f"enemies: {len(enemies) - len(bosses)} | boss-like: {len(bosses)}")
print("sample enemy:", json.dumps(enemies[0])[:300] if enemies else "none")
