"""Assessment probe: what ELSE can we pull from the installed EtG bundles?

Runs over every bundle in StreamingAssets/Assets, builds class histograms,
and dumps FULL typetrees for representative objects of interest so we can
see fields the current dump_gungeon.py ignores.

Outputs tools/probe_report.json + console summary.
"""
import json, os, sys
from collections import Counter
import UnityPy

ETG = r"X:\Games\Enter the Gungeon"
ASSETS = os.path.join(ETG, r"EtG_Data\StreamingAssets\Assets")
OUT = r"X:\GungeonMate\tools\probe_report.json"

BUNDLES = [f for f in os.listdir(ASSETS)
           if os.path.isfile(os.path.join(ASSETS, f))]

report = {"bundles": BUNDLES, "histograms": {}, "samples": {}, "notes": []}


def scan_bundle(name):
    """Return (objects_by_pid, script_names, monobehaviours)."""
    try:
        env = UnityPy.load(os.path.join(ASSETS, name))
    except Exception as e:
        report["notes"].append(f"{name}: load failed {e}")
        return {}, {}, []
    by_pid, scripts = {}, {}
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
        if o.type.name != "MonoBehaviour":
            continue
        try:
            t = o.read_typetree()
        except Exception:
            continue
        cls = scripts.get((t.get("m_Script") or {}).get("m_PathID", 0), "?")
        mbs.append((o.path_id, cls, t))
    return by_pid, scripts, mbs


def summarize_fields(t, depth=0):
    """Field name -> type-ish summary, for nested dict/list structures."""
    out = {}
    for k, v in t.items():
        if isinstance(v, dict):
            out[k] = {"dict": summarize_fields(v, depth + 1)} if depth < 2 else "dict"
        elif isinstance(v, list):
            if v and isinstance(v[0], dict):
                out[k] = {"list[dict]": summarize_fields(v[0], depth + 1),
                          "len": len(v)}
            else:
                out[k] = f"list[{type(v[0]).__name__ if v else 'empty'}] len={len(v)}"
        else:
            out[k] = v if not isinstance(v, str) or len(v) < 60 else v[:57] + "..."
    return out


for b in BUNDLES:
    print(f"scanning {b} ...", flush=True)
    by_pid, scripts, mbs = scan_bundle(b)
    hist = Counter(c for _, c, _ in mbs)
    report["histograms"][b] = dict(hist.most_common())
    print(f"  {len(mbs)} monobehaviours, {len(hist)} classes")

# ── brave_resources_001: deep-dive key classes ─────────────────────
by_pid, scripts, mbs = scan_bundle("brave_resources_001")

want = {"Gun", "PassiveItem", "PlayerItem", "BasicStatPickup",
        "ActiveBasicStatItem", "PickupObject"}
seen = set()
for pid, cls, t in mbs:
    if cls in want and cls not in seen:
        seen.add(cls)
        report["samples"][f"{cls}_full"] = summarize_fields(t)

# one full gun with interesting name (skip the very first — often a template)
for pid, cls, t in mbs:
    if cls == "Gun" and (t.get("gunName") or "").lower() in (
            "winchester", "m1rifle", "shadesrevolver", "bow"):
        report["samples"][f"gun_{t['gunName']}"] = summarize_fields(t)

# distinct item-ish classes
item_classes = Counter(c for _, c, _ in mbs
                       if c.endswith("Item") or c.endswith("Pickup"))
report["samples"]["itemish_classes"] = dict(item_classes.most_common())

# ── shared_auto_001: synergy entry + loot/shop classes ─────────────
by_pid, scripts, mbs = scan_bundle("shared_auto_001")
for pid, cls, t in mbs:
    if cls == "AdvancedSynergyDatabase":
        entries = t.get("synergies") or []
        if entries:
            report["samples"]["synergy_entry_full"] = summarize_fields(entries[0])
            report["samples"]["synergy_entry_example"] = entries[0]
        report["samples"]["synergydb_keys"] = list(t.keys())
        break
for pid, cls, t in mbs:
    if cls and ("LootTable" in cls or "Shop" in cls or "Chest" in cls):
        key = f"shared_{cls}"
        if key not in report["samples"]:
            report["samples"][key] = summarize_fields(t)

# ── enemies_base_001: AIActor-adjacent classes of interest ──────────
by_pid, scripts, mbs = scan_bundle("enemies_base_001")
for pid, cls, t in mbs:
    for wantc in ("AIActor", "AIBulletBank", "HealthHaver",
                  "EncounterTrackable", "EnemyPlaceable"):
        if cls == wantc and f"enemy_{wantc}" not in report["samples"]:
            report["samples"][f"enemy_{wantc}"] = summarize_fields(t)

# sprite collection availability (icon extraction feasibility)
for b in BUNDLES:
    try:
        env = UnityPy.load(os.path.join(ASSETS, b))
    except Exception:
        continue
    n_sprites = n_tex = n_coll = 0
    for o in env.objects:
        if o.type.name == "Sprite":
            n_sprites += 1
        elif o.type.name == "Texture2D":
            n_tex += 1
        elif o.type.name == "MonoBehaviour":
            pass
    report["histograms"][b]["__Sprite"] = n_sprites
    report["histograms"][b]["__Texture2D"] = n_tex

json.dump(report, open(OUT, "w", encoding="utf-8"), indent=1, default=str)
print(f"\n-> {OUT}")
print(json.dumps({k: sorted(v) for k, v in
                  report["samples"].items() if isinstance(v, dict)},
                 indent=1)[:3000])
