"""Merge deep game stats into app JSONs — join key: PickupObjectId.

- guns.json      : quality (FIXES systematic off-by-one from the old
                   QUALITY map), fire_rate, magazine_size, spread, type,
                   damage/speed/range/force, burst/charge/active_reload,
                   curse/coolness from stat modifiers, ammo/content meta.
- items.json     : quality fix, stat_modifiers, curse/coolness,
                   shop_price, damage immunities, ammonomicon order.
- synergies.json : stat_modifiers, activation state.

Enum maps verified against Assembly-CSharp.dll via dnfile.
Writes merge_stats_report.json with every change for review.
"""
import json, os, re

TOOLS = r"X:\GungeonMate\tools"
DATA = r"X:\GungeonMate\gungeon_mate\assets\data"

dump = json.load(open(os.path.join(TOOLS, "gungeon_dump.json"), encoding="utf-8"))

TYPE_MAP = {"SemiAutomatic": "Semiautomatic", "Automatic": "Automatic",
            "Beam": "Beam", "Charged": "Charged", "Burst": "Burst"}
GAME_QUALITIES = {"D", "C", "B", "A", "S"}

# id → display name backbone: EncounterDatabase journal keys resolved
# through the EN string table (dev prefab names like "Armored Gun"
# differ from display names like "AC-15").
_strings = {}
_cur_key, _cur_val = None, []
for _ln in open(os.path.join(TOOLS, "en_items.txt"),
                encoding="utf-8", errors="replace").read() \
        .replace("\r\n", "\n").split("\n"):
    if _ln.startswith("#"):
        if _cur_key:
            _strings[_cur_key] = " ".join(
                v.strip() for v in _cur_val if v.strip())
        _cur_key, _cur_val = _ln.strip(), []
    else:
        _cur_val.append(_ln)
if _cur_key:
    _strings[_cur_key] = " ".join(
        v.strip() for v in _cur_val if v.strip())
_enc = json.load(open(os.path.join(TOOLS, "encounter_db.json"),
                      encoding="utf-8"))
id_to_name = {}
for _e in _enc:
    pid = _e.get("pickupObjectId")
    if isinstance(pid, int) and pid > 0:
        key = (_e.get("journalData") or {}).get("PrimaryDisplayName", "")
        disp = _strings.get(key, "")
        if disp:
            id_to_name.setdefault(pid, disp)


def display_name(ent):
    """Display name for a dump entry via its PickupObjectId."""
    return id_to_name.get(ent.get("id"), ent.get("gunName")
                          or ent.get("itemName") or "")


# Master drop pools — used to pick the canonical prefab among same-named
# dev variants (e.g. three "Regular Shotgun" prefabs: only one is in
# All_Guns_Loot_Table).
_gun_pool = {pid for lt in dump.get("lootTables", [])
             if "Gun" in (lt.get("name") or "")
             for pid in lt.get("pickupIds", [])}
_item_pool = {pid for lt in dump.get("lootTables", [])
              if "Gun" not in (lt.get("name") or "")
              for pid in lt.get("pickupIds", [])}


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


# Dev-prefab-name → our display name (normalized keys).
ALIASES = {
    "lamp": "Magic Lamp", "awp": "A.W.P.", "baretta": "Beretta",
    "winchestershotgun": "Winchester", "thompsonsubmachinegun":
        "Thompson Sub-Machinegun", "screechgun": "Screecher",
    "woodbow": "Bow", "m79grenadelauncher": "Grenade Launcher",
    "moonscraperlaser": "Moonscraper", "shadesrevolver":
        "Shades's Revolver", "m1rifle": "M1",
    "vertebraek47": "VertebraeK-47", "smileyrevolver":
        "Smiley's Revolver", "lemonhandcannon": "Pea Cannon",
    "saa": "Colt 1851", "crescentmooncrossbow": "Crescent Crossbow",
    "augun": "AU Gun", "standardissuelaser": "Laser Rifle",
    "gunner": "GuNNER", "trankgun": "Trank Gun", "arcgun": "Arc Gun",
    "winchester97": "Winchester Rifle", "colt45": "Colt 1851",
    "machinepistol": "Machine Pistol", "kexcalibur": "Excaliber",
    "zorgun": "Zorgun", "morningstar": "Morning Star",
    "blashmaster": "The Exotic", "blackhole": "Black Hole Gun",
    "combined": "Combined Rifle", "betrayerslies": "Betrayer's Shield",
    "betrayersshield": "Betrayer's Shield", "emberbelt": "Ember",
    "snubnose": "Snubnosed Revolver", "flutterby": "Butterfly Gun",
    "springleader": "Ice Breaker", "crescentrevolver":
        "Crescent Moon", "bluerevolver": "Blue Gun",
    "hegelian": "Hegemony Carbine", "videogame": "Videogame Gun",
    "machinegunhand": "Machine Fist",
    "rubeadynemkvi": "RUBE-ADYNE MK.II",
}


def canonical(entries, pool):
    """Pick canonical prefab: in master loot table > lowest id."""
    in_pool = [e for e in entries if e.get("id") in pool]
    cands = in_pool or [e for e in entries
                        if e.get("id") is not None]
    return min(cands, key=lambda e: e["id"]) if cands else None


def name_match(our_name, dev_name):
    """Is this dump prefab a name-plausible join for our entry?"""
    if norm(dev_name) == norm(our_name):
        return True
    return ALIASES.get(norm(dev_name)) == our_name

report = {"guns": {}, "items": {}, "synergies": {}, "notes": []}


def fmt_num(v, nd=2):
    if v is None:
        return None
    r = round(float(v), nd)
    return str(int(r)) if r == int(r) else str(r)


def _num(s):
    """Parse a possibly-unit-suffixed stat string; None if non-numeric."""
    if not isinstance(s, str):
        return None
    s = s.strip().rstrip("s").rstrip("\u00b0").strip()
    try:
        return float(s)
    except ValueError:
        return None


def set_field(entry, field, newval, rep):
    old = entry.get(field)
    if old == newval:
        return False
    rep[field] = [old, newval]
    entry[field] = newval
    return True


def set_stat_grow(entry, field, newval, rep):
    """Like set_stat but never shrinks a numeric value and never
    writes 0 — protects curated values for semantic fields like
    damage where the primary projectile understates the weapon
    (melee, orbital strikes, sub-projectiles)."""
    old, nn = entry.get(field), _num(str(newval))
    if nn is None or nn <= 0:
        return False
    on = _num(str(old)) if old is not None else None
    if on is not None:
        if nn <= on:
            return False
        rep[field] = [old, newval]
        entry[field] = newval
        return True
    return set_stat(entry, field, newval, rep)


def set_stat(entry, field, newval, rep):
    """Set a display stat field. Never clobbers curated non-numeric
    strings ('∞', 'N/A', ...) — those go to game_<field> instead.
    Skips numeric-equal rewrites ('1.20' vs '1.2')."""
    old = entry.get(field)
    if newval is None:
        return False
    on, nn = _num(str(old)) if old is not None else None, _num(str(newval))
    if on is not None and nn is not None:
        if abs(on - nn) < 1e-6:
            return False
        rep[field] = [old, newval]
        entry[field] = newval
        return True
    if old is not None:
        # curated non-numeric value — record ground truth alongside
        if entry.get(f"game_{field}") != newval:
            rep[f"game_{field}"] = [entry.get(f"game_{field}"), newval]
            entry[f"game_{field}"] = newval
        return False
    rep[field] = [None, newval]
    entry[field] = newval
    return True


def gun_module(g):
    """Primary module stats: inline module else first volley module."""
    if g.get("module"):
        return g["module"]
    vol = g.get("volley")
    if vol and vol.get("modules"):
        return vol["modules"][0]
    return {}


def gun_projectile(g, module):
    """Best-representative projectile: full charge for charge guns."""
    if module.get("chargeLevels"):
        lvls = [c.get("projectile") for c in module["chargeLevels"]
                if c.get("projectile")]
        if lvls:
            return lvls[-1]
    projs = module.get("projectiles") or []
    if projs:
        return projs[0]
    return g.get("projectile") or {}


def additive(mods, stat):
    """Additive amount for a stat, else None."""
    amt = 0.0
    found = False
    for m in mods or []:
        if m.get("stat") == stat and m.get("op") == "ADDITIVE":
            amt += m.get("amount") or 0
            found = True
    return amt if found else None


# ── GUNS ────────────────────────────────────────────────────────────
guns = json.load(open(os.path.join(DATA, "guns.json"), encoding="utf-8"))
dump_guns = [g for g in dump["guns"] if g.get("id") is not None]
by_id = {g["id"]: g for g in dump_guns}

n_id = nq = n_swap = 0
for g in guns:
    # name-driven canonical join — stamped ids alone proved unreliable
    # (dev variants + outright collisions), so names win, pools break ties
    cands = [e for e in dump_guns
             if name_match(g["name"], display_name(e))]
    ent = canonical(cands, _gun_pool) if cands else None
    rep = {}
    if ent is not None:
        if ent["id"] != g.get("id"):
            rep["id"] = [g.get("id"), ent["id"]]
            g["id"] = ent["id"]
            n_swap += 1
    else:
        # no name candidate — stamped id must name-verify to merge
        ent = by_id.get(g.get("id"))
        if ent is not None:
            disp = display_name(ent)
            if id_to_name.get(ent["id"]) \
                    and not name_match(g["name"], disp):
                # proven wrong stamp — display name says otherwise
                report.setdefault("unjoinable", []).append(
                    ["gun", g["name"], g.get("id"), disp])
                del g["id"]
                continue
            if ent["id"] not in id_to_name:
                report.setdefault("unverified", []).append(
                    ["gun", g["name"], g.get("id"),
                     ent.get("gunName")])
                continue
        else:
            report.setdefault("unjoinable", []).append(
                ["gun", g["name"], g.get("id"), None])
            continue
    n_id += 1
    # quality — only real game tiers (COMMON/SPECIAL/EXCLUDED left alone)
    q = ent.get("quality")
    if q in GAME_QUALITIES:
        if set_field(g, "quality", q, rep):
            nq += 1
    mod = gun_module(ent)
    proj = gun_projectile(ent, mod)
    set_stat(g, "fire_rate", fmt_num(mod.get("cooldownTime"), 3), rep)
    # -1 = no reload clip (beam/infinite) — keep curated display value
    if (mod.get("numberOfShotsInClip") or -1) >= 0:
        set_stat(g, "magazine_size",
                 fmt_num(mod.get("numberOfShotsInClip")), rep)
    av = mod.get("angleVariance")
    if av is not None:
        set_stat(g, "spread", f"{fmt_num(av, 1)}\u00b0", rep)
    if proj.get("damage") is not None:
        set_stat_grow(g, "damage", fmt_num(proj["damage"]), rep)
    if proj.get("speed") is not None:
        set_stat(g, "shot_speed", fmt_num(proj["speed"]), rep)
    if proj.get("range") is not None:
        set_stat(g, "range", fmt_num(proj["range"]), rep)
    if proj.get("force") is not None:
        set_stat(g, "force", fmt_num(proj["force"]), rep)
    if ent.get("reloadTime") is not None:
        set_stat(g, "reload_time", fmt_num(ent["reloadTime"]), rep)
    if ent.get("maxAmmo") is not None:
        set_stat(g, "ammo_capacity", fmt_num(ent["maxAmmo"]), rep)
    # type — game shootStyle wins, with two mechanism quirks:
    #  - alternate/multi-module volleys are genuinely Variable
    #  - "Beam" shootStyle is used internally by some hitscan
    #    guns (e.g. Regular Shotgun) — never relabel a non-Beam
    #    display type as Beam; record it as game_type instead
    vol = ent.get("volley") or {}
    vmods = vol.get("modules") or []
    styles = {m.get("shootStyle") for m in vmods}
    if ent.get("alternateVolley") or vol.get("modulesAreTiers") \
            or len(styles) > 1:
        gt = "Variable"
    else:
        gt = TYPE_MAP.get(mod.get("shootStyle"))
    if g.get("type") == "Variable":
        # curated judgment wins (e.g. Gunderfury is separate
        # per-level prefabs — game side just says Automatic)
        if gt and gt != "Variable":
            set_stat(g, "game_type", gt, rep)
    elif gt == "Beam":
        # hitscan weapons report Beam internally — never relabel
        set_stat(g, "game_type", "Beam", rep)
    elif gt:
        set_field(g, "type", gt, rep)
    if mod.get("shootStyle") == "Burst" and mod.get("burstShotCount"):
        set_field(g, "burst_count", int(mod["burstShotCount"]), rep)
    if mod.get("chargeLevels"):
        set_field(g, "charge_stages", len(mod["chargeLevels"]), rep)
    if ent.get("activeReload"):
        set_field(g, "active_reload", True, rep)
    if ent.get("infiniteAmmo"):
        set_field(g, "infinite_ammo", True, rep)
    c = additive(ent.get("statModifiers"), "Curse")
    if c is not None:
        set_field(g, "curse", float(c), rep)
    c = additive(ent.get("statModifiers"), "Coolness")
    if c is not None:
        set_field(g, "coolness", float(c), rep)
    if ent.get("contentSource") and ent["contentSource"] != "BASE":
        set_field(g, "content_source", ent["contentSource"], rep)
    if ent.get("ammonomiconPos") is not None:
        set_field(g, "ammonomicon_pos", ent["ammonomiconPos"], rep)
    if rep:
        report["guns"][g["name"]] = rep

json.dump(guns, open(os.path.join(DATA, "guns.json"), "w",
                     encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"guns: {n_id} id-joined ({n_swap} rejoined to canonical prefab), "
      f"{len(report['guns'])} changed, {nq} quality fixes")

# ── ITEMS ───────────────────────────────────────────────────────────
items = json.load(open(os.path.join(DATA, "items.json"), encoding="utf-8"))
dump_items = [i for i in dump["items"] if i.get("id") is not None]
by_id = {i["id"]: i for i in dump_items}

n_id = nq = n_swap = 0
for it in items:
    cands = [e for e in dump_items
             if name_match(it["name"], display_name(e))]
    ent = canonical(cands, _item_pool) if cands else None
    rep = {}
    if ent is not None:
        if ent["id"] != it.get("id"):
            rep["id"] = [it.get("id"), ent["id"]]
            it["id"] = ent["id"]
            n_swap += 1
        n_id += 1
    else:
        ent = by_id.get(it.get("id"))
        if ent is not None:
            disp = display_name(ent)
            if id_to_name.get(ent["id"]) \
                    and not name_match(it["name"], disp):
                report.setdefault("unjoinable", []).append(
                    ["item", it["name"], it.get("id"), disp])
                del it["id"]
                continue
            if ent["id"] in id_to_name:
                n_id += 1
            else:
                report.setdefault("unverified", []).append(
                    ["item", it["name"], it.get("id"),
                     ent.get("itemName")])
                continue
        else:
            report.setdefault("unjoinable", []).append(
                ["item", it["name"], it.get("id"), None])
            continue
    q = ent.get("quality")
    if q in GAME_QUALITIES:
        if set_field(it, "quality", q, rep):
            nq += 1
    if ent.get("statModifiers"):
        set_field(it, "stat_modifiers", ent["statModifiers"], rep)
        c = additive(ent["statModifiers"], "Curse")
        if c is not None:
            set_field(it, "curse", float(c), rep)
        c = additive(ent["statModifiers"], "Coolness")
        if c is not None:
            set_field(it, "coolness", float(c), rep)
    if ent.get("damageTypeModifiers"):
        imm = [t for m in ent["damageTypeModifiers"]
               if m.get("multiplier") == 0
               for t in m.get("types", [])]
        if imm:
            set_field(it, "damage_immunities", imm, rep)
    if ent.get("customCost") is not None:
        set_field(it, "shop_price", int(ent["customCost"]), rep)
    if ent.get("ammonomiconPos") is not None:
        set_field(it, "ammonomicon_pos", ent["ammonomiconPos"], rep)
    if rep:
        report["items"][it["name"]] = rep

json.dump(items, open(os.path.join(DATA, "items.json"), "w",
                      encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"items: {n_id} id-joined ({n_swap} rejoined to canonical prefab), "
      f"{len(report['items'])} changed, {nq} quality fixes")

# ── SYNERGIES ───────────────────────────────────────────────────────
syns = json.load(open(os.path.join(DATA, "synergies.json"),
                      encoding="utf-8"))
by_key = {s["nameKey"]: s for s in dump["synergies"] if s.get("nameKey")}
n_key = 0
for s in syns:
    key = s.get("game_name_key")
    if not key:
        continue
    ent = by_key.get(key)
    if ent is None:
        continue
    n_key += 1
    rep = {}
    if ent.get("statModifiers"):
        set_field(s, "stat_modifiers", ent["statModifiers"], rep)
    if ent.get("activation") and ent["activation"] != "ACTIVE":
        set_field(s, "activation", ent["activation"], rep)
    if ent.get("activeWhenGunUnequipped"):
        set_field(s, "active_when_gun_unequipped", True, rep)
    if rep:
        report["synergies"][s["name"]] = rep

json.dump(syns, open(os.path.join(DATA, "synergies.json"), "w",
                     encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(report, open(os.path.join(TOOLS, "merge_stats_report.json"),
                      "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"synergies: {n_key} key-joined, {len(report['synergies'])} changed")
print("report -> merge_stats_report.json")
