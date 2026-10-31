"""Extract real game sprites → PNGs for guns/items/enemies.

Resolves each pickup/enemy's AmmonomiconSprite name (encounter_db) to a
tk2dSpriteCollectionData spriteDefinition in the asset bundles, crops the
atlas region, and saves PNGs under assets/images/game/<kind>/.

Adds `game_icon` (relative asset path) to each matched JSON entry.
"""
import json, os, re, io
import UnityPy

TOOLS = r"X:\GungeonMate\tools"
DATA = r"X:\GungeonMate\gungeon_mate\assets\data"
IMG = r"X:\GungeonMate\gungeon_mate\assets\images\game"
ETG = r"X:\Games\Enter the Gungeon"
A = os.path.join(ETG, r"EtG_Data\StreamingAssets\Assets")

_enc = json.load(open(os.path.join(TOOLS, "encounter_db.json"),
                      encoding="utf-8"))

# pickupObjectId -> ammonomicon sprite name
id_sprite = {}
dispkey_sprite = {}
for _e in _enc:
    jd = _e.get("journalData") or {}
    spr = jd.get("AmmonomiconSprite")
    if not spr:
        continue
    pid = _e.get("pickupObjectId")
    if isinstance(pid, int) and pid > 0:
        id_sprite[pid] = spr
    dk = jd.get("PrimaryDisplayName", "")
    if dk:
        dispkey_sprite[dk] = spr

# ── build sprite-name index across bundles ──────────────────────────
index = {}   # sprite name -> (texture_obj, x, y, w, h)
BUNDLES = ["brave_resources_001", "enemies_base_001",
           "shared_auto_001", "shared_auto_002"]
for b in BUNDLES:
    env = UnityPy.load(os.path.join(A, b))
    by_pid = {o.path_id: o for o in env.objects}
    scripts = {}
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
        if scripts.get((t.get("m_Script") or {}).get("m_PathID", 0)) \
                != "tk2dSpriteCollectionData":
            continue
        # texture objects for this collection
        texs = []
        for pptr in t.get("textures") or []:
            to = by_pid.get(pptr.get("m_PathID", 0))
            if to is not None:
                texs.append(to)
        if not texs:
            continue
        for sd in t.get("spriteDefinitions") or []:
            name = sd.get("name")
            if not name or name in index:
                continue
            mid = sd.get("materialId", 0) or 0
            tex = texs[mid] if mid < len(texs) else texs[0]
            uvs = sd.get("uvs") or []
            us = [u.get("x", 0) if isinstance(u, dict) else u[0]
                  for u in uvs]
            vs = [v.get("y", 0) if isinstance(v, dict) else v[1]
                  for v in uvs]
            if us and vs:
                index[name] = (tex, min(us), min(vs),
                               max(us) - min(us), max(vs) - min(vs))
            else:
                index[name] = (tex, sd.get("regionX", 0),
                               sd.get("regionY", 0),
                               sd.get("regionW", 0),
                               sd.get("regionH", 0))
    print(f"{b}: index={len(index)}")

print(f"total sprites indexed: {len(index)}")

# ── crop + save ─────────────────────────────────────────────────────
os.makedirs(IMG, exist_ok=True)
_img_cache = {}

def sprite_png(name):
    ent = index.get(name)
    if ent is None:
        return None
    tex, x, y, w, h = ent
    if not w or not h:
        return None
    tid = tex.path_id
    if tid not in _img_cache:
        try:
            _img_cache[tid] = tex.read().image
        except Exception:
            _img_cache[tid] = None
    img = _img_cache.get(tid)
    if img is None:
        return None
    W, H = img.size
    if x <= 1.0 and w <= 1.0:   # normalized UV coords
        x, y, w, h = x * W, y * H, w * W, h * H
    x, y, w, h = int(round(x)), int(round(y)), int(round(w)), int(round(h))
    if w <= 0 or h <= 0 or x + w > W or y + h > H:
        return None
    crop = img.crop((x, H - y - h, x + w, H - y))
    buf = io.BytesIO()
    crop.save(buf, "PNG")
    return buf.getvalue()


def slug(name):
    s = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    return s + ".png"


def save_for(kind, entries, sprite_for):
    outdir = os.path.join(IMG, kind)
    os.makedirs(outdir, exist_ok=True)
    n = 0
    for e in entries:
        spr = sprite_for(e)
        if not spr:
            continue
        png = sprite_png(spr)
        if png is None:
            continue
        fn = slug(e["name"])
        open(os.path.join(outdir, fn), "wb").write(png)
        e["game_icon"] = f"assets/images/game/{kind}/{fn}"
        n += 1
    return n


report = {}
guns = json.load(open(os.path.join(DATA, "guns.json"), encoding="utf-8"))
items = json.load(open(os.path.join(DATA, "items.json"), encoding="utf-8"))
report["guns"] = save_for("guns", guns,
                          lambda e: id_sprite.get(e.get("id")))
report["items"] = save_for("items", items,
                           lambda e: id_sprite.get(e.get("id")))
json.dump(guns, open(os.path.join(DATA, "guns.json"), "w",
                     encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(items, open(os.path.join(DATA, "items.json"), "w",
                      encoding="utf-8"), ensure_ascii=False, indent=2)

for f, kind in (("enemies.json", "enemies"), ("bosses.json", "bosses")):
    arr = json.load(open(os.path.join(DATA, f), encoding="utf-8"))
    def sp(e):
        k = e.get("game_enc_key")
        if not k:
            return None
        key = k.upper()
        if not key.endswith("_ENCNAME"):
            key += "_ENCNAME"
        return dispkey_sprite.get("#" + key)
    report[kind] = save_for(kind, arr, sp)
    json.dump(arr, open(os.path.join(DATA, f), "w",
                        encoding="utf-8"), ensure_ascii=False, indent=2)

print("extracted:", report)
json.dump(report, open(os.path.join(TOOLS, "sprite_report.json"), "w"))
