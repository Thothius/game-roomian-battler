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

def load_bundle(path):
    """Rebind indexes to another bundle (update-era pickups live in
    shared_auto_*)."""
    global env, by_pid, script_names
    env = UnityPy.load(path)
    by_pid = {o.path_id: o for o in env.objects}
    script_names = {}
    for o in env.objects:
        if o.type.name == "MonoScript":
            try:
                script_names[o.path_id] = o.read_typetree().get(
                    "m_ClassName")
            except Exception:
                pass
    return env.objects

def script_of(tree):
    s = tree.get("m_Script") or {}
    return script_names.get(s.get("m_PathID", 0), "")

def resolve(pptr):
    if not isinstance(pptr, dict):
        return None
    if pptr.get("m_FileID", 0) == 0 and pptr.get("m_PathID", 0) != 0:
        return by_pid.get(pptr["m_PathID"])
    return None  # cross-file refs skipped

# Verified against ItemQuality enum in Assembly-CSharp.dll (dnfile):
#   COMMON=0, D=1, C=2, B=3, A=4, S=5, SPECIAL=-50, EXCLUDED=-100
QUALITY = {0: "COMMON", 1: "D", 2: "C", 3: "B", 4: "A", 5: "S",
           -50: "SPECIAL", -100: "EXCLUDED"}

# PlayerStats.StatType / StatModifier.ModifyMethod / ShootStyle /
# ProjectileSequenceStyle / SynergyActivation — all verified via dnfile.
STAT_TYPE = {
    0: "MovementSpeed", 1: "RateOfFire", 2: "Accuracy", 3: "Health",
    4: "Coolness", 5: "Damage", 6: "ProjectileSpeed",
    7: "AdditionalGunCapacity", 8: "AdditionalItemCapacity",
    9: "AmmoCapacityMultiplier", 10: "ReloadSpeed",
    11: "AdditionalShotPiercing", 12: "KnockbackMultiplier",
    13: "GlobalPriceMultiplier", 14: "Curse", 15: "PlayerBulletScale",
    16: "AdditionalClipCapacityMultiplier", 17: "AdditionalShotBounces",
    18: "AdditionalBlanksPerFloor", 19: "ShadowBulletChance",
    20: "ThrownGunDamage", 21: "DodgeRollDamage", 22: "DamageToBosses",
    23: "EnemyProjectileSpeedMultiplier", 24: "ExtremeShadowBulletChance",
    25: "ChargeAmountMultiplier", 26: "RangeMultiplier",
    27: "DodgeRollDistanceMultiplier", 28: "DodgeRollSpeedMultiplier",
    29: "TarnisherClipCapacityMultiplier", 30: "MoneyMultiplierFromEnemies",
}
MODIFY_METHOD = {0: "ADDITIVE", 1: "MULTIPLICATIVE"}
SHOOT_STYLE = {0: "SemiAutomatic", 1: "Automatic", 2: "Beam",
               3: "Charged", 4: "Burst"}
SEQ_STYLE = {0: "Random", 1: "Ordered", 2: "OrderedGroups"}
AMMO_TYPE = {0: "SMALL_BULLET", 1: "MEDIUM_BULLET", 2: "BEAM",
             3: "GRENADE", 4: "SHOTGUN", 5: "SMALL_BLASTER",
             6: "MEDIUM_BLASTER", 7: "NAIL", 8: "MUSKETBALL",
             9: "ARROW", 10: "MAGIC", 11: "BLUE_SHOTGUN",
             12: "SKULL", 13: "FISH", 14: "CUSTOM"}
SYNERGY_ACTIVATION = {0: "ACTIVE", 1: "DEMO", 2: "INACTIVE",
                      3: "ACTIVE_UNBOOSTED"}
CONTENT_SOURCE = {0: "BASE", 1: "CONTENT_UPDATE_01",
                  2: "CONTENT_UPDATE_01_FINAL", 3: "CONTENT_UPDATE_02",
                  4: "CONTENT_UPDATE_03", 999: "EXCLUDED"}
CORE_DAMAGE_TYPES = {1: "Void", 2: "Magic", 4: "Fire", 8: "Ice",
                     16: "Poison", 32: "Water", 64: "Electric",
                     128: "SpecialBossDamage"}

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
        "knockback": bd.get("knockback") or bd.get("KnockbackStrength"),
        "stunChance": bd.get("stunChance") or bd.get("StunApplyChance"),
        "damagesWalls": bd.get("damagesWalls"),
        "dampedFalloff": bd.get("dampedFalloff"),
    }

def module_stats(m):
    """Flatten a ProjectileModule dict into mergeable stats."""
    if not isinstance(m, dict):
        return None
    out = {
        "cooldownTime": m.get("cooldownTime"),
        "burstShotCount": m.get("burstShotCount"),
        "burstCooldownTime": m.get("burstCooldownTime"),
        "numberOfShotsInClip": m.get("numberOfShotsInClip"),
        "angleVariance": m.get("angleVariance"),
        "ammoCost": m.get("ammoCost"),
        "shootStyle": SHOOT_STYLE.get(m.get("shootStyle"),
                                     m.get("shootStyle")),
        "ammoType": AMMO_TYPE.get(m.get("ammoType"), m.get("ammoType")),
        "sequenceStyle": SEQ_STYLE.get(m.get("sequenceStyle"),
                                       m.get("sequenceStyle")),
        "maxChargeTime": m.get("maxChargeTime"),
    }
    projs = []
    for p in m.get("projectiles") or []:
        ps = proj_stats(p)
        if ps:
            projs.append(ps)
    if projs:
        out["projectiles"] = projs
    charges = []
    for c in m.get("chargeProjectiles") or []:
        if not isinstance(c, dict):
            continue
        ps = proj_stats(c.get("projectile") or c)
        charges.append({"chargeTime": c.get("ChargeTime"),
                        "projectile": ps})
    if charges:
        out["chargeLevels"] = charges
    return out

def volley_modules(pptr):
    """Resolve a ProjectileVolleyData PPtr → volley metadata."""
    o = resolve(pptr)
    if o is None:
        return None
    try:
        t = o.read_typetree()
    except Exception:
        return None
    if script_of(t) != "ProjectileVolleyData":
        return None
    mods = []
    for m in t.get("projectiles") or []:
        ms = module_stats(m)
        if ms:
            mods.append(ms)
    if not mods:
        return None
    return {"modules": mods,
            "modulesAreTiers": bool(t.get("ModulesAreTiers")),
            "shotgunVelocity": bool(
                t.get("UsesShotgunStyleVelocityRandomizer"))}

def stat_mods(raw):
    """Decode StatModifier list → readable stat modifiers."""
    out = []
    for m in raw or []:
        if not isinstance(m, dict):
            continue
        if "damageType" in m:
            continue  # damage-type modifiers handled separately
        st = m.get("statToBoost")
        if st is None:
            continue
        out.append({
            "stat": STAT_TYPE.get(st, f"UNKNOWN_{st}"),
            "op": MODIFY_METHOD.get(m.get("modifyType"),
                                    m.get("modifyType")),
            "amount": m.get("amount"),
        })
    return out

def damage_mods(t):
    """Collect damageType modifiers (immunities / multipliers)."""
    out = []
    for key in ("passiveStatModifiers", "modifiers",
                "currentGunDamageTypeModifiers"):
        for m in t.get(key) or []:
            if isinstance(m, dict) and "damageType" in m:
                names = [n for b, n in CORE_DAMAGE_TYPES.items()
                         if m["damageType"] & b]
                out.append({"types": names or [m["damageType"]],
                            "multiplier": m.get("damageMultiplier")})
    return out

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
        sm = module_stats(t.get("singleModule"))
        g = {
            "gunName": t.get("gunName"),
            "id": t.get("PickupObjectId"),
            "quality": QUALITY.get(t.get("quality"), t.get("quality")),
            "gunClass": t.get("gunClass"),
            "maxAmmo": t.get("maxAmmo"),
            "ammo": t.get("ammo"),
            "reloadTime": t.get("reloadTime"),
            "shootStyle": (t.get("singleModule") or {}).get("shootStyle"),
            "module": sm,
            "statModifiers": stat_mods(
                (t.get("passiveStatModifiers") or []) +
                (t.get("currentGunStatModifiers") or [])),
            "contentSource": CONTENT_SOURCE.get(t.get("contentSource"),
                                                t.get("contentSource")),
            "ammonomiconPos": t.get("ForcedPositionInAmmonomicon"),
            "activeReload": bool(t.get("LocalActiveReload") or
                                 (t.get("activeReloadData") or {})
                                 .get("ActiveReloadStacks")),
            "infiniteAmmo": bool(t.get("LocalInfiniteAmmo")),
        }
        if t.get("UsesCustomCost"):
            g["customCost"] = t.get("CustomCost")
        vol = volley_modules(t.get("rawVolley"))
        if vol:
            g["volley"] = vol
        alt = volley_modules(t.get("alternateVolley"))
        if alt:
            g["alternateVolley"] = alt
        # backward-compat primary projectile (first module, first proj)
        projs = (sm or {}).get("projectiles") or \
            ((vol["modules"][0].get("projectiles")) if vol else None) or []
        if projs:
            g["projectile"] = projs[0]
            if len(projs) > 1:
                g["projectileCount"] = len(projs)
        guns.append(g)
    elif cls in ("PassiveItem", "PlayerItem", "BasicStatPickup",
                 "ActiveBasicStatItem") or cls.endswith("Item"):
        it = {
            "class": cls,
            "itemName": t.get("itemName"),
            "id": t.get("PickupObjectId"),
            "quality": QUALITY.get(t.get("quality"), t.get("quality")),
            "type": t.get("consumable") if "consumable" in t else None,
            "statModifiers": stat_mods(
                (t.get("passiveStatModifiers") or []) +
                (t.get("modifiers") or [])),
            "damageTypeModifiers": damage_mods(t),
            "ammonomiconPos": t.get("ForcedPositionInAmmonomicon"),
            "canBeDropped": bool(t.get("CanBeDropped")),
            "canBeSold": bool(t.get("CanBeSold")),
            "excludedFromShops": bool(t.get("ShouldBeExcludedFromShops")),
        }
        if t.get("UsesCustomCost"):
            it["customCost"] = t.get("CustomCost")
        for f in ("ArmorToGive", "CurrencyToGive", "healAmount",
                  "damageToEnemies", "duration", "consumable",
                  "numberOfUses", "cooldownTime", "requiredDamageType"):
            if t.get(f) not in (None, 0, 0.0, False):
                it[f] = t.get(f)
        items.append(it)
    elif cls in ("AdvancedSynergyDatabase", "PickupObjectDatabase"):
        synergy_db = {"class": cls, "keys": list(t.keys())[:40]}

# ── update-era pickups in shared_auto_* bundles ─────────────────────
_base = os.path.join(ETG, r"EtG_Data\StreamingAssets\Assets")
_gun_ids = {g["id"] for g in guns}
_item_ids = {i["id"] for i in items}
for extra in ("shared_auto_001", "shared_auto_002",
              "enemies_base_001", "foyer_001", "foyer_002",
              "foyer_003", "dungeon_scene_001", "shared_base_001"):
    objs = load_bundle(os.path.join(_base, extra))
    for o in objs:
        if o.type.name != "MonoBehaviour":
            continue
        try:
            t = o.read_typetree()
        except Exception:
            continue
        cls = script_of(t)
        if cls == "Gun":
            if t.get("PickupObjectId") in _gun_ids:
                continue
            sm = module_stats(t.get("singleModule"))
            g = {
                "gunName": t.get("gunName"),
                "id": t.get("PickupObjectId"),
                "quality": QUALITY.get(t.get("quality"), t.get("quality")),
                "gunClass": t.get("gunClass"),
                "maxAmmo": t.get("maxAmmo"),
                "ammo": t.get("ammo"),
                "reloadTime": t.get("reloadTime"),
                "module": sm,
                "statModifiers": stat_mods(
                    (t.get("passiveStatModifiers") or []) +
                    (t.get("currentGunStatModifiers") or [])),
                "contentSource": CONTENT_SOURCE.get(
                    t.get("contentSource"), t.get("contentSource")),
                "ammonomiconPos": t.get("ForcedPositionInAmmonomicon"),
                "activeReload": bool(t.get("LocalActiveReload") or
                                     (t.get("activeReloadData") or {})
                                     .get("ActiveReloadStacks")),
                "infiniteAmmo": bool(t.get("LocalInfiniteAmmo")),
            }
            if t.get("UsesCustomCost"):
                g["customCost"] = t.get("CustomCost")
            vol = volley_modules(t.get("rawVolley"))
            if vol:
                g["volley"] = vol
            alt = volley_modules(t.get("alternateVolley"))
            if alt:
                g["alternateVolley"] = alt
            projs = (sm or {}).get("projectiles") or \
                ((vol["modules"][0].get("projectiles")) if vol
                 else None) or []
            if projs:
                g["projectile"] = projs[0]
                if len(projs) > 1:
                    g["projectileCount"] = len(projs)
            guns.append(g)
            _gun_ids.add(g["id"])
        elif cls and cls.endswith("Item"):
            if t.get("PickupObjectId") in _item_ids:
                continue
            it = {
                "class": cls,
                "itemName": t.get("itemName"),
                "id": t.get("PickupObjectId"),
                "quality": QUALITY.get(t.get("quality"),
                                       t.get("quality")),
                "statModifiers": stat_mods(
                    (t.get("passiveStatModifiers") or []) +
                    (t.get("modifiers") or [])),
                "damageTypeModifiers": damage_mods(t),
                "ammonomiconPos": t.get("ForcedPositionInAmmonomicon"),
            }
            if t.get("UsesCustomCost"):
                it["customCost"] = t.get("CustomCost")
            items.append(it)
            _item_ids.add(it["id"])

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
loot_tables = []
for o in env2.objects:
    if o.type.name != "MonoBehaviour": continue
    try:
        t = o.read_typetree()
        cls2 = scripts2.get((t.get("m_Script") or {}).get("m_PathID", 0))
        if cls2 == "GenericLootTable":
            els = ((t.get("defaultItemDrops") or {}).get("elements")) or []
            loot_tables.append({
                "name": t.get("m_Name"),
                "pickupIds": [e.get("pickupId") for e in els],
                "weights": [e.get("weight") for e in els],
            })
        if cls2 != "AdvancedSynergyDatabase":
            continue
    except: continue
    for e in t.get("synergies") or []:
        bonus = []
        for b in e.get("bonusSynergies") or []:
            if isinstance(b, dict):
                bonus.append({
                    "nameKey": b.get("NameKey"),
                    "mandatoryGuns": b.get("MandatoryGunIDs"),
                    "mandatoryItems": b.get("MandatoryItemIDs"),
                    "optionalGuns": b.get("OptionalGunIDs"),
                    "optionalItems": b.get("OptionalItemIDs"),
                    "required": b.get("NumberObjectsRequired"),
                    "statModifiers": stat_mods(b.get("statModifiers")),
                })
        syns.append({
            "nameKey": e.get("NameKey"),
            "mandatoryGuns": e.get("MandatoryGunIDs"),
            "mandatoryItems": e.get("MandatoryItemIDs"),
            "optionalGuns": e.get("OptionalGunIDs"),
            "optionalItems": e.get("OptionalItemIDs"),
            "required": e.get("NumberObjectsRequired"),
            "needGunAndItem": bool(e.get("RequiresAtLeastOneGunAndOneItem")),
            "statModifiers": stat_mods(e.get("statModifiers")),
            "bonusSynergies": bonus,
            "activation": SYNERGY_ACTIVATION.get(
                e.get("ActivationStatus"), e.get("ActivationStatus")),
            "activeWhenGunUnequipped": bool(e.get("ActiveWhenGunUnequipped")),
            "suppressVfx": bool(e.get("SuppressVFX")),
        })

data = json.load(open(OUT))
data["synergies"] = syns
data["lootTables"] = loot_tables
json.dump(data, open(OUT, "w"), indent=1)
print(f"{len(syns)} synergies + {len(loot_tables)} loot tables -> {OUT}")

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
