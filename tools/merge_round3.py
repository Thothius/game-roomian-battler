"""Round-3 merge: enemy extras, chest tables, dungeon flows.

- enemies/bosses.json: game_guid (stable EnemyGuid), collision_damage,
  signature flag, ammonomicon_pos, ammonomicon lore text (journal key).
- chests.json (NEW): per-chest-prefab tier drop chances + loot table.
- floors.json (NEW): dungeon flow names/metadata from flows_base_001.
"""
import json, os, re
import UnityPy

TOOLS = r"X:\GungeonMate\tools"
DATA = r"X:\GungeonMate\gungeon_mate\assets\data"
ETG = r"X:\Games\Enter the Gungeon"
A = os.path.join(ETG, r"EtG_Data\StreamingAssets\Assets")

# string tables (items + enemies)
_strings = {}
for f in ("en_items.txt", "en_enemies.txt"):
    cur, val = None, []
    for ln in open(os.path.join(TOOLS, f), encoding="utf-8",
                   errors="replace").read().replace("\r\n", "\n").split("\n"):
        if ln.startswith("#"):
            if cur:
                _strings[cur] = " ".join(v.strip() for v in val if v.strip())
            cur, val = ln.strip(), []
        else:
            val.append(ln)
    if cur:
        _strings[cur] = " ".join(v.strip() for v in val if v.strip())

_enc = json.load(open(os.path.join(TOOLS, "encounter_db.json"),
                      encoding="utf-8"))
# journal display key -> encounter entry (enemies join via enc key)
enc_by_dispkey = {(_e.get("journalData") or {})
                  .get("PrimaryDisplayName", ""): _e for _e in _enc}
enc_by_base = {os.path.splitext(os.path.basename(
    _e.get("path", "")))[0].lower(): _e for _e in _enc}

report = {"enemies": {}, "chests": 0, "floors": 0}


def scan(bundle):
    env = UnityPy.load(os.path.join(A, bundle))
    by_pid, scripts, mbs = {}, {}, []
    for o in env.objects:
        by_pid[o.path_id] = o
    for o in env.objects:
        if o.type.name == "MonoScript":
            try:
                scripts[o.path_id] = o.read_typetree().get("m_ClassName")
            except Exception:
                pass
    for o in env.objects:
        if o.type.name != "MonoBehaviour":
            continue
        try:
            t = o.read_typetree()
        except Exception:
            continue
        cls = scripts.get((t.get("m_Script") or {}).get("m_PathID", 0), "?")
        mbs.append((o.path_id, cls, t))
    return by_pid, mbs


def go_name(by_pid, tree):
    o = by_pid.get((tree.get("m_GameObject") or {}).get("m_PathID", 0))
    if o is None:
        return ""
    try:
        return o.read_typetree().get("m_Name", "")
    except Exception:
        return ""


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


# ── 1) enemy extras ─────────────────────────────────────────────────
by_pid, mbs = scan("enemies_base_001")
actors = []   # (prefab_name, tree)
for pid, cls, t in mbs:
    if cls == "AIActor":
        actors.append((go_name(by_pid, t), t))

our_f = [os.path.join(DATA, f) for f in ("enemies.json", "bosses.json")]
ours = []
for f in our_f:
    for e in json.load(open(f, encoding="utf-8")):
        e["_file"] = f
        ours.append(e)

def enc_for(prefab, enc_key):
    e = enc_by_base.get(prefab.lower())
    if e:
        return e
    if enc_key:
        return enc_by_dispkey.get("#" + enc_key.upper())
    return None

n_join = 0
for prefab, t in actors:
    enc = enc_for(prefab, None)
    if enc is None:
        continue
    disp_key = (enc.get("journalData") or {}).get("PrimaryDisplayName", "")
    disp = _strings.get(disp_key, "")
    if not disp:
        continue
    hits = [e for e in ours if norm(e["name"]) == norm(disp)]
    if not hits:
        continue
    e = hits[0]
    ch = {}
    def sf(k, v):
        if v not in (None, "", 0, 0.0, False) and e.get(k) != v:
            ch[k] = [e.get(k), v]; e[k] = v
    sf("game_guid", t.get("EnemyGuid"))
    cd = t.get("CollisionDamage")
    if isinstance(cd, (int, float)) and cd > 0:
        sf("collision_damage", cd)
    if t.get("IsSignatureEnemy"):
        sf("signature_enemy", True)
    if t.get("ForcedPositionInAmmonomicon") is not None:
        sf("ammonomicon_pos", t["ForcedPositionInAmmonomicon"])
    lore = _strings.get((enc.get("journalData") or {})
                        .get("AmmonomiconFullEntry", ""), "").strip()
    if lore and not e.get("ammonomicon"):
        sf("ammonomicon", lore)
    if t.get("EffectResistances"):
        res = t["EffectResistances"]
        if isinstance(res, list) and res:
            sf("effect_resistances", res)
    if ch:
        report["enemies"][e["name"]] = ch
        n_join += 1
print(f"enemies: {n_join} entries enriched")

for e in ours:
    e.pop("_file", None)
# rebuild each file, preserving original order
for f in our_f:
    orig = json.load(open(f, encoding="utf-8"))
    idx = {e["name"]: e for e in ours}
    for o in orig:
        if o["name"] in idx:
            o.update(idx[o["name"]])
    json.dump(orig, open(f, "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

# ── 2) chests ───────────────────────────────────────────────────────
chests = []
for b in ("shared_auto_001", "shared_auto_002"):
    by2, m2 = scan(b)
    for pid, cls, t in m2:
        if cls != "Chest":
            continue
        lt = t.get("lootTable") or {}
        chests.append({
            "prefab": go_name(by2, t) or "chest",
            "bundle": b,
            "identifier": t.get("ChestIdentifier"),
            "difficulty": t.get("difficulty"),
            "chances": {k: lt.get(k) for k in
                        ("D_Chance", "C_Chance", "B_Chance",
                         "A_Chance", "S_Chance", "Common_Chance")
                        if lt.get(k)},
            "completesSynergy": bool(lt.get("CompletesSynergy")),
            "onlyOneGunCanDrop": bool(lt.get("onlyOneGunCanDrop")),
        })
report["chests"] = len(chests)
json.dump(chests, open(os.path.join(DATA, "chests.json"), "w",
                       encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"chests: {len(chests)} prefabs -> chests.json")

# ── 3) dungeon flows ────────────────────────────────────────────────
by3, m3 = scan("flows_base_001")
flows = []
for pid, cls, t in m3:
    if cls in ("DungeonFlow", "GenericRoomTable"):
        flows.append({
            "class": cls,
            "name": t.get("m_Name") or "",
            "keys": [k for k in t.keys()
                     if not k.startswith("m_")][:30],
        })
report["floors"] = len(flows)
json.dump(flows, open(os.path.join(DATA, "floors.json"), "w",
                      encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"floors: {len(flows)} flow/table objects -> floors.json")

json.dump(report, open(os.path.join(TOOLS, "round3_report.json"),
                       "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("-> round3_report.json")
