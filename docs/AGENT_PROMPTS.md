# Agent Kickoff Prompts

> Ready-to-paste instructions for each queued work item. Copy the
> block for the task into a new session. Each prompt assumes the agent
> reads `AGENTS.md` + `AGENT_STATUS.md` first and claims a slot.

---

## 1. AMMONOMICON visual pass — `design ammonomicon`

```
You are the VISUAL agent (Slot 1). Task: full visual pass on the
Ammonomicon wiki. Read docs/AMMONOMICON_DESIGN_BRIEF.md first — it
has the architecture map, data fields, and 6 asks in priority order.

Priority: (1) chapter/mode detail badges surfacing the silent
metadata (floor/secret/music/game_classes), (2) grid + expanded-panel
polish, (3) tab-strip art for all 12 categories, (4) synergy detail
styling, (5) empty states, (6) motion.

Constraints: ThemeFlair/Insets/Radii tokens, GoopText, haptics,
fastRoute, BoxFit.contain, part-of file splits. Do NOT touch
avatar webp deletions in the working tree (Slot 4 WIP).
Commits: ui:/ammonomicon: prefixes, push to origin master.
Verify: flutter analyze clean + widget tests green before done.
```

## 2. CUSTOMIZATION hub rework — `design customization`

```
You are the VISUAL agent (Slot 1). Task: rebuild the theme system as
"Customization" per docs/CUSTOMIZATION_DESIGN_BRIEF.md — read it fully
first, including the LIVE LOOK draggable preview spec (1/3→75% drag
handle), the 5-tab layout (PRESETS/CUSTOM/FONTS/PARTICLES/AMBIANCE),
the sticky BACK/PREVIEW/APPLY top bar, and the save-as-preset flow
with splashSlug icons.

Verified data notes are in the brief (CustomThemeData = palette+font+
aura only — decide whether to extend it for full pick-sets). Unicorn
has 6 sub-palettes via UnicornPalette — the CUSTOM tab must expose
the variant switcher. Picker is already trimmed to 3 presets +
saved customs. PREVIEW button is the hardest part — build it last.

Reuse: existing ColorPicker widget for color popups; studio_* tab
widgets in lib/screens/experience_studio/. Commit: ui:/theme:.
```

## 3. AMMONOMICON data depth — `mine more data`

```
You are the CORE agent (Slot 2). Task: deepen Ammonomicon data via
the tools/ extraction pipeline (tools/dump_gungeon.py,
tools/encounter_db.json, tools/en_*.txt string tables).

Queue: (a) room-category enum + boss/enemy pools per floor from
flows_base_001 into chapters.json, (b) 26 ChallengeModifier name/desc
keys into game_modes.json, (c) curated prose summaries per
mode/chapter entry, (d) NPC names from dialogue/string assets.

Constraints: game data wins on stats, name joins only when
unambiguous, verification fields (game_health pattern) for unsure
joins. After JSON edits: data integrity test + full suite.
Commit: data: prefix.
```

## 4. DETAIL view finishers — `finish detail view`

```
You are a CORE/VISUAL agent. Task: finish the item/gun detail rework
leftovers. Done so far (84072da): _StatGrid uniform stats, element/
ACTIVE-PASSIVE tags top-left, 50/50 charge/duration pills, ornament
divider removed, synergy card aspect fix.

Remaining: (a) chapter-scaling charge table on active items — needs
floor->charge data in items.json (mine from game or wiki, flag which
source), (b) polish the _StatGrid cell spacing/dividers against the
rest of the app, (c) regression test for the new grid presence.
Commit: ui: prefix.
```

## 5. GENERAL QA sweep — `bughunt`

```
You are the SUPPORT agent (Slot 4). Task: full bughunt — run flutter
analyze + the entire test suite, click through the app looking for
overflows/crashes, check the new Ammonomicon (12 tabs, global search,
expandable tiles, MATCHED chip) and the detail rework (_StatGrid,
top-left tags, 50/50 pills). Log confirmed bugs to
docs/USER_BUG_LIST.md with repro steps. Commit: fix:/test:.
```

---

## Coordination (all prompts)
- Read `AGENT_STATUS.md`, claim your slot, set branch if 2+ active.
- Other agent WIP: ~35 deleted `assets/images/avatars/*.webp` are
  Slot 4's in-flight work — never stage them; use explicit git add.
- Two repos: app (`gungeon_mate/` → GungeonMate.git) and root (docs/
  board → game-roomian-battler.git). Push the right one.
- Release slot at end + Session Log row.
