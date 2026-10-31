"""Probe 2 — deep-dives for the extraction assessment.

1) ProjectileModule field inventory (volleys, charge guns, modules)
2) statToBoost enum inference — dump every item/synergy modifier with names
3) Projectile modifier components (pierce/bounce/explosion/homing) per gun
4) Shop controller -> stock loot tables
5) Chest instances -> tier drop chances
6) Enemy extras: AIBulletBank / EncounterTrackable / journal
7) Gungeoneer-ish classes (player prefabs / starting loadouts)
"""
import json, os
from collections import Counter, defaultdict
import UnityPy

ETG = r"X:\Games\Enter the Gungeon"
A = os.path.join(ETG, r"EtG_Data\StreamingAssets\Assets")
OUT = r"X:\GungeonMate\tools\probe2_report.json"
rep = {}


def scan(name):
    env = UnityPy.load(os.path.join(A, name))
    by_pid = {}
    scripts = {}
    mbs = []
    for o in env.objects:
        by_pid[o.path_id] = o
    for o in env.objects:
        if o.type.name == "MonoScript":
            try:
                scripts[o.path_id] = o.read_typetree().get("m_ClassName")
            except Exception:
                pass
    for o in env.objects:
        if o.type.name == "MonoBehaviour":
            try:
                t = o.read_typetree()
            except Exception:
                continue
            cls = scripts.get((t.get("m_Script") or {}).get("m_PathID", 0), "?")
            mbs.append((o.path_id, cls, t))
    return by_pid, scripts, mbs


by_pid, scripts, mbs = scan("brave_resources_001")

def res(pptr):
    if isinstance(pptr, dict) and pptr.get("m_FileID", 0) == 0 and pptr.get("m_PathID", 0):
        return by_pid.get(pptr["m_PathID"])
    return None

def tree(pptr):
    o = res(pptr)
    if o is None:
        return None
    try:
        return o.read_typetree()
    except Exception:
        return None

def cls_of(t):
    return scripts.get((t.get("m_Script") or {}).get("m_PathID", 0), "?")

# ── 1) ProjectileModule + ProjectileVolleyData inventories ─────────
mod_keys, volley_keys = set(), set()
charge_example = None
for pid, cls, t in mbs:
    if cls == "ProjectileVolleyData":
        volley_keys |= set(t.keys())
    if cls == "Gun":
        sm = t.get("singleModule") or {}
        mod_keys |= set(sm.keys())
        if sm.get("chargeProjectiles") and charge_example is None:
            charge_example = {"gunName": t.get("gunName"),
                              "module": sm}
for pid, cls, t in mbs[:1] + mbs:  # also scan volley module dicts
    if cls == "ProjectileVolleyData":
        for m in t.get("projectiles") or []:
            pass
        for m in (t.get("projectileModules") or []):
            if isinstance(m, dict):
                mod_keys |= set(m.keys())
rep["module_fields"] = sorted(mod_keys)
rep["volley_fields"] = sorted(volley_keys)
rep["charge_example"] = charge_example

# find ProjectileModule objects as separate MBs too
pmod_classes = Counter()
for pid, cls, t in mbs:
    if cls and "Module" in cls:
        pmod_classes[cls] += 1
rep["module_classes"] = dict(pmod_classes)

# ── 2) every *Item modifier for enum inference ─────────────────────
item_mods = []
for pid, cls, t in mbs:
    if not (cls and (cls.endswith("Item") or cls.endswith("Pickup"))):
        continue
    name = t.get("itemName") or t.get("gunName")
    if not name:
        continue
    mods = (t.get("passiveStatModifiers") or []) + (t.get("modifiers") or [])
    extras = {}
    for k, v in t.items():
        if isinstance(v, (int, float)) and not isinstance(v, bool) \
           and k not in ("m_Enabled",) and v not in (0, 1, 0.0, 1.0, -1, -1.0):
            extras[k] = v
    item_mods.append({"name": name, "cls": cls, "id": t.get("PickupObjectId"),
                      "quality": t.get("quality"),
                      "cost": t.get("CustomCost") if t.get("UsesCustomCost") else None,
                      "mods": mods, "nondefault_scalars": extras})
rep["item_mods"] = item_mods

# guns: same scalars + module stats
gun_rows = []
for pid, cls, t in mbs:
    if cls != "Gun":
        continue
    sm = t.get("singleModule") or {}
    mods = (t.get("passiveStatModifiers") or []) + (t.get("currentGunStatModifiers") or [])
    gun_rows.append({
        "name": t.get("gunName"), "id": t.get("PickupObjectId"),
        "quality": t.get("quality"),
        "cost": t.get("CustomCost") if t.get("UsesCustomCost") else None,
        "mods": mods,
        "reloadTime": t.get("reloadTime"),
        "maxAmmo": t.get("maxAmmo"),
        "cooldownTime": sm.get("cooldownTime"),
        "burstShotCount": sm.get("burstShotCount"),
        "burstCooldownTime": sm.get("burstCooldownTime"),
        "numberOfShotsInClip": sm.get("numberOfShotsInClip"),
        "angleVariance": sm.get("angleVariance"),
        "ammoCost": sm.get("ammoCost"),
        "shootStyle": sm.get("shootStyle"),
        "ammoType": sm.get("ammoType"),
        "sequenceStyle": sm.get("sequenceStyle"),
        "chargeCount": len(sm.get("chargeProjectiles") or []),
        "usesOptionalReloadVolley": bool(sm.get("usesOptionalReloadVolley")),
        "has_rawVolley": bool((t.get("rawVolley") or {}).get("m_PathID")),
        "has_alternateVolley": bool((t.get("alternateVolley") or {}).get("m_PathID")),
        "activeReload": bool((t.get("activeReloadData") or {}).get("ActiveReloadStacks")
                             or (t.get("LocalActiveReload"))),
        "contentSource": t.get("contentSource"),
        "curse": t.get("curse"),
        "coolness": t.get("coolness"),
        "magnificence": t.get("magnificence"),
        "ammoPerShot": sm.get("ammoCost"),
    })
rep["guns"] = gun_rows

# ── 3) projectile modifier components per projectile GameObject ─────
# map projectile MB path_id -> its GameObject -> sibling MB classes
proj_mods = Counter()
go_map = {}
for pid, cls, t in mbs:
    go = (t.get("m_GameObject") or {}).get("m_PathID", 0)
    go_map.setdefault(go, []).append(cls)
for pid, cls, t in mbs:
    if cls == "Projectile":
        go = (t.get("m_GameObject") or {}).get("m_PathID", 0)
        for c in go_map.get(go, []):
            if c and "Modifier" in c or c in ("ExplosiveModifier", "HomingModifier"):
                proj_mods[c] += 1
rep["projectile_modifier_classes"] = dict(proj_mods.most_common())

# ── 4+5) shops & chests in shared_auto ──────────────────────────────
shops, chests, loot_tables = [], [], []
for bundle in ("shared_auto_001", "shared_auto_002"):
    by2, s2, m2 = scan(bundle)
    scripts.update(s2)  # for class resolution of refs
    def res2(pptr, _bp=by2):
        if isinstance(pptr, dict) and pptr.get("m_FileID", 0) == 0 and pptr.get("m_PathID", 0):
            return _bp.get(pptr["m_PathID"])
        return None
    def tree2(pptr):
        o = res2(pptr)
        try:
            return o.read_typetree() if o else None
        except Exception:
            return None
    def cls2(t):
        return s2.get((t.get("m_Script") or {}).get("m_PathID", 0), "?")
    for pid, cls, t in m2:
        if cls == "GenericLootTable":
            els = ((t.get("defaultItemDrops") or {}).get("elements")) or []
            loot_tables.append({"bundle": bundle, "name": t.get("m_Name"),
                                "n_drops": len(els),
                                "pickupIds": [e.get("pickupId") for e in els[:60]],
                                "weights": [e.get("weight") for e in els[:60]]})
        if cls == "Chest":
            lt = t.get("lootTable") or {}
            chests.append({"bundle": bundle, "chestId": t.get("ChestIdentifier"),
                           "difficulty": t.get("difficulty"),
                           "chances": {k: lt.get(k) for k in
                                       ("D_Chance","C_Chance","B_Chance","A_Chance","S_Chance","Common_Chance")},
                           "name": t.get("m_Name")})
        if cls == "BaseShopController":
            si = t.get("shopItems") or {}
            shop_tree = tree2(si)
            stock = None
            if shop_tree:
                els = ((shop_tree.get("defaultItemDrops") or {}).get("elements")) or []
                stock = [e.get("pickupId") for e in els[:50]]
            shops.append({"bundle": bundle, "type": t.get("baseShopType"),
                          "n_stock": len(stock or []), "stock": stock})
rep["loot_tables"] = loot_tables
rep["chests"] = chests
rep["shops"] = shops

# ── 6) enemy extras ─────────────────────────────────────────────────
by3, s3, m3 = scan("enemies_base_001")
bulletbank_fields, banks = set(), []
aiactor_fields, track_fields, health_fields = set(), set(), set()
for pid, cls, t in m3:
    if cls == "AIBulletBank":
        bulletbank_fields |= set(t.keys())
        banks.append({"name": t.get("m_Name"),
                      "n_bullets": len((t.get("Bullets") or []))})
    elif cls == "AIActor":
        aiactor_fields |= set(t.keys())
    elif cls == "EncounterTrackable":
        track_fields |= set(t.keys())
    elif cls == "HealthHaver":
        health_fields |= set(t.keys())
rep["enemy"] = {
    "AIBulletBank_fields": sorted(bulletbank_fields),
    "AIActor_fields": sorted(aiactor_fields),
    "EncounterTrackable_fields": sorted(track_fields),
    "HealthHaver_fields": sorted(health_fields),
    "banks_sample": banks[:5],
}

# ── 7) gungeoneer-ish / player classes anywhere ─────────────────────
playerish = Counter()
for bundle in BUNDLES if False else ("brave_resources_001", "shared_auto_001", "shared_auto_002", "foyer_002", "foyer_003"):
    try:
        _, s4, m4 = scan(bundle)
    except Exception:
        continue
    for pid, cls, t in m4:
        if cls and ("Player" in cls or "Character" in cls or "Gungeon" in cls
                    or cls in ("TalkDoer", "TalkDoerLite", "ShopItemController")):
            playerish[f"{bundle}:{cls}"] += 1
rep["playerish_classes"] = dict(playerish.most_common(40))

json.dump(rep, open(OUT, "w", encoding="utf-8"), indent=1, default=str)
print("->", OUT)
print("module_fields:", rep["module_fields"])
print("volley_fields:", rep["volley_fields"])
print("guns rows:", len(gun_rows), "| item mods:", len(item_mods))
print("loot tables:", len(loot_tables), "| chests:", len(chests), "| shops:", len(shops))
