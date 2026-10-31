"""Round-2 merge: drop/shop sources, ammonomicon lore, gungeoneer loadouts.

- guns/items.json + `sources`: which pools/shops can yield it
  (GenericLootTable + BaseShopController stock lists, id-joined).
- guns/items.json + `ammonomicon`: full lore entry text
  (AmmonomiconFullEntry string key -> EN table), same as enemies.json.
- gungeoneers.json: PlayerController starting loadout verification
  (startingGunIds/Active/Passive item ids -> display names).
"""
import json, os, re
import UnityPy

TOOLS = r"X:\GungeonMate\tools"
DATA = r"X:\GungeonMate\gungeon_mate\assets\data"
ETG = r"X:\Games\Enter the Gungeon"

dump = json.load(open(os.path.join(TOOLS, "gungeon_dump.json"), encoding="utf-8"))

# ── shared join backbone (same as merge_stats) ─────────────────────
_strings = {}
_cur, _val = None, []
for _ln in open(os.path.join(TOOLS, "en_items.txt"),
                encoding="utf-8", errors="replace").read() \
        .replace("\r\n", "\n").split("\n"):
    if _ln.startswith("#"):
        if _cur:
            _strings[_cur] = " ".join(v.strip() for v in _val if v.strip())
        _cur, _val = _ln.strip(), []
    else:
        _val.append(_ln)
if _cur:
    _strings[_cur] = " ".join(v.strip() for v in _val if v.strip())

_enc = json.load(open(os.path.join(TOOLS, "encounter_db.json"),
                      encoding="utf-8"))
id_to_name, id_to_lorekey = {}, {}
for _e in _enc:
    pid = _e.get("pickupObjectId")
    if isinstance(pid, int) and pid > 0:
        jd = _e.get("journalData") or {}
        nm = _strings.get(jd.get("PrimaryDisplayName", ""), "")
        if nm:
            id_to_name.setdefault(pid, nm)
        if jd.get("AmmonomiconFullEntry"):
            id_to_lorekey.setdefault(pid, jd["AmmonomiconFullEntry"])


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


ALIASES = {
    "lamp": "Magic Lamp", "awp": "A.W.P.", "baretta": "Beretta",
    "winchestershotgun": "Winchester", "thompsonsubmachinegun":
        "Thompson Sub-Machinegun", "screechgun": "Screecher",
    "woodbow": "Bow", "m79grenadelauncher": "Grenade Launcher",
    "moonscraperlaser": "Moonscraper", "shadesrevolver":
        "Shades's Revolver", "m1rifle": "M1", "vertebraek47":
        "VertebraeK-47", "smileyrevolver": "Smiley's Revolver",
    "lemonhandcannon": "Pea Cannon", "saa": "Colt 1851",
    "crescentmooncrossbow": "Crescent Crossbow", "augun": "AU Gun",
    "standardissuelaser": "Laser Rifle", "gunner": "GuNNER",
    "trankgun": "Trank Gun", "arcgun": "Arc Gun", "winchester97":
        "Winchester Rifle", "colt45": "Colt 1851", "machinepistol":
        "Machine Pistol", "kexcalibur": "Excaliber", "zorgun": "Zorgun",
    "morningstar": "Morning Star", "blashmaster": "The Exotic",
    "blackhole": "Black Hole Gun", "combined": "Combined Rifle",
    "betrayerslies": "Betrayer's Shield", "betrayersshield":
        "Betrayer's Shield", "emberbelt": "Ember", "snubnose":
        "Snubnosed Revolver", "flutterby": "Butterfly Gun",
    "springleader": "Ice Breaker", "crescentrevolver": "Crescent Moon",
    "bluerevolver": "Blue Gun", "hegelian": "Hegemony Carbine",
    "videogame": "Videogame Gun", "machinegunhand": "Machine Fist",
    "rubeadynemkvi": "RUBE-ADYNE MK.II",
}

report = {"sources": {"guns": 0, "items": 0},
          "ammonomicon": {"guns": 0, "items": 0},
          "gungeoneers": {}}

# ── 1) loot/shop sources ───────────────────────────────────────────
TABLE_LABELS = {
    "Chest_Wood_Loot_Table": "Wooden chests",
    "Chest_Gungeon_Items_01": "Chests",
    "TruthChestLootTable": "Truth chest",
    "BossDropLootTable": "Boss drops",
    "Broken_Chest_Items_01": "Broken chests",
    "CommonItemRoomClearDropTable": "Room-clear rewards",
    "CommonItemRoomClearDropTable_laterfloors": "Room-clear rewards",
    "Shop_Gungeon_Items_01": "Shop",
    "Shop_Gungeon_Cheap_Items_01": "Shop",
    "Shop_Gungeon_SpecialCase_Items": "Shop",
    "Shop_Gungeon_Table_Items_01": "Shop",
    "Shop_Gungeon_GunsAndItems": "Shop",
    "Shop_Curse_Items_01": "Curse shop",
    "Shop_Key_Items_01": "Key shop",
    "Shop_Blank_Items_01": "Blank shop",
    "Shop_Goop_Items_01": "Goop shop",
    "Shop_Truck_Items_01": "Truck shop",
    "Shop_Beetle_Meta": "Beetle shop",
    "Shop_Truck_Meta": "Meta shop",
    "Shop_Goop_Meta": "Meta shop",
    "All_Guns_Loot_Table": "Gungeon loot pool",
    "All_Item_Loot_Table": "Gungeon loot pool",
    "PickupLootTable": "Pickups",
}
SKIP_TABLES = {"DEMO_AllItems", "DEMO_AllGuns", "GungeonTableTable",
               "GungeonCrateAndBarrelTableTable", "PlatterContentsTable",
               "StoneTableTableTable", "CastleSetDressingTableTable",
               "LibrarySetDressingTableTable", "MineCrateTableTable",
               "CurrencyLootTable", "GunslingKingShittyGunTable"}

pool_of = {}   # id -> set(labels)
for lt in dump.get("lootTables", []):
    name = lt.get("name") or ""
    if name in SKIP_TABLES:
        continue
    label = TABLE_LABELS.get(name, name)
    for pid in lt.get("pickupIds") or []:
        if isinstance(pid, int) and pid > 0:
            pool_of.setdefault(pid, set()).add(label)

# shop controller stock (probe2 captured live shops too)
try:
    p2 = json.load(open(os.path.join(TOOLS, "probe2_report.json"),
                        encoding="utf-8"))
    for sh in p2.get("shops", []):
        for pid in sh.get("stock") or []:
            if isinstance(pid, int) and pid > 0:
                pool_of.setdefault(pid, set()).add("Shop")
except FileNotFoundError:
    pass


def our_entry_id(e):
    return e.get("id")


def apply_sources(entries):
    n = 0
    for e in entries:
        pid = e.get("id")
        if pid is None:
            continue
        src = sorted(pool_of.get(pid, ()))
        if src:
            e["sources"] = src
            n += 1
    return n


def apply_lore(entries):
    n = 0
    for e in entries:
        pid = e.get("id")
        if pid is None or pid not in id_to_lorekey:
            continue
        text = _strings.get(id_to_lorekey[pid], "").strip()
        if text and text != e.get("ammonomicon"):
            e["ammonomicon"] = text
            n += 1
    return n


guns = json.load(open(os.path.join(DATA, "guns.json"), encoding="utf-8"))
items = json.load(open(os.path.join(DATA, "items.json"), encoding="utf-8"))
report["sources"]["guns"] = apply_sources(guns)
report["sources"]["items"] = apply_sources(items)
report["ammonomicon"]["guns"] = apply_lore(guns)
report["ammonomicon"]["items"] = apply_lore(items)
json.dump(guns, open(os.path.join(DATA, "guns.json"), "w",
                     encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(items, open(os.path.join(DATA, "items.json"), "w",
                      encoding="utf-8"), ensure_ascii=False, indent=2)
print(report["sources"], report["ammonomicon"])

# ── 2) gungeoneer starting loadouts ────────────────────────────────
env = UnityPy.load(os.path.join(
    ETG, r"EtG_Data\StreamingAssets\Assets\brave_resources_001"))
scripts = {}
for o in env.objects:
    if o.type.name == "MonoScript":
        try:
            scripts[o.path_id] = o.read_typetree().get("m_ClassName")
        except Exception:
            pass
IDENTITY = {0: "The Pilot", 1: "The Convict", 2: "The Robot",
            5: "The Marine", 6: "The Hunter", 7: "The Cultist",
            8: "The Bullet", 10: "The Gunslinger"}
geers = json.load(open(os.path.join(DATA, "gungeoneers.json"),
                       encoding="utf-8"))
by_name = {g["name"]: g for g in geers}
for o in env.objects:
    if o.type.name != "MonoBehaviour":
        continue
    try:
        t = o.read_typetree()
    except Exception:
        continue
    if scripts.get((t.get("m_Script") or {}).get("m_PathID", 0)) \
            != "PlayerController":
        continue
    who = IDENTITY.get(t.get("characterIdentity"))
    if who is None:
        continue
    g = by_name.get(who)
    if g is None:
        continue
    gun_ids = [i for i in t.get("startingGunIds") or [] if i > 0]
    act_ids = [i for i in t.get("startingActiveItemIds") or [] if i > 0]
    pas_ids = [i for i in t.get("startingPassiveItemIds") or [] if i > 0]
    names = lambda ids: [id_to_name.get(i, f"#{i}") for i in ids]
    rep = {
        "guns": names(gun_ids), "actives": names(act_ids),
        "passives": names(pas_ids),
        "max_guns": t.get("MAX_GUNS_HELD"),
        "max_items": t.get("MAX_ITEMS_HELD"),
        "ours_guns": g.get("starting_guns"),
        "ours_items": g.get("starting_items"),
    }
    # apply ground truth
    if rep["guns"]:
        g["starting_guns"] = rep["guns"]
        g["starting_gun_ids"] = gun_ids
    items_all = rep["passives"] + rep["actives"]
    if items_all:
        g["starting_items"] = items_all
        g["starting_item_ids"] = pas_ids + act_ids
    if rep["max_guns"]:
        g["max_guns"] = rep["max_guns"]
    if rep["max_items"]:
        g["max_items"] = rep["max_items"]
    report["gungeoneers"][who] = rep

json.dump(geers, open(os.path.join(DATA, "gungeoneers.json"), "w",
                      encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(report, open(os.path.join(TOOLS, "round2_report.json"),
                       "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for who, rep in report["gungeoneers"].items():
    print(f"{who}: guns={rep['guns']} items={rep['passives']+rep['actives']} "
          f"(ours: {rep['ours_guns']}/{rep['ours_items']})")
print("-> round2_report.json")
