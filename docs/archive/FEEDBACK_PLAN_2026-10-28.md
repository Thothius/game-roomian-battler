# User Feedback Triage & Plan — 2026-10-28

> Scouting session (SUPPORT/CORE-planning, read-only recon). No code changes made.
> PARALLEL (Slot 3) is actively working on **Paradox Mode v3.0.0** — their
> files-in-progress (`run_provider.dart`, `mp_session.dart`, `lib/services/mp/*`,
> `multiplayer_messages.dart`) are off-limits per AC4 and directly overlap item #3.

---

## 1. Gunderfury DPS lapses — CONFIRMED BUG (wrong values + inconsistent thresholds)

**Findings:**
- `guns.json` has the real per-form DPS: `"dps": "25.45 29.57 33.157 34.09 107.14 181.82"` (6 space-separated values, one per form). Same multi-value pattern for magazine_size, ammo_capacity, damage, fire_rate, range, spread.
- `Gun.dpsValue` (gun.dart:59-63) regex-grabs only the **first** number → 25.45 everywhere static.
- `Gun.getDynamicDps(gunderLevel:)` (gun.dart:76-80) is **hardcoded and wrong**: `lvl<30 → 22.5`, `lvl<60 → 45.5`, `else → 75.0`. Only 3 tiers vs 6 real forms, and none of the values match real data.
- `GunderfuryDashboardSliver` (special_gun_dashboards.dart:32-56) uses **different** thresholds (forms at lvl 20/30/40/50/60) and made-up stat text (Damage 4.5/6.5/10.0, Reload 1.5s/1.1s/0.6s, Capacity 450/550/650) — none of it matches guns.json.
- So: dashboard says "Automatic Form" at lvl 20-29 while getDynamicDps still returns base 22.5; at lvl 60 the HUD shows "Awakened" but DPS reads 75.0 instead of 181.82. That's the "lapse".
- Callers of dynamic DPS: `player_page.dart:183`, `gun_stats.dart:1179`, `run_provider` avg DPS (1589/1617/1695/1709). Static `dpsValue` used in: browse_pills.dart:212, periodic_tile.dart:191, sort_picker.dart:116, inventory_list_row.dart:99 → all permanently show 25.45.

**Plan:**
1. Define one source of truth: a `static const _gunderfuryForms` table in `gun.dart` (or parse guns.json's space-separated fields by form index) — form name, level threshold, DPS, and per-form stats. **Verify milestone levels against the wiki** (dashboard's 20/30/40/50/60 needs a fact-check — wiki lists form unlock milestones, possibly every 10 levels).
2. `getDynamicDps` returns the table value for the current level's form.
3. Rebuild `GunderfuryDashboardSliver` to render from the same table — real damage/mag/ammo/range per form instead of the fabricated stats.
4. Decide static display: periodic tile + browse pill keep base DPS (or show "25–182" range string). Low priority.

**Files:** `lib/models/gun.dart`, `lib/widgets/dashboards/special_gun_dashboards.dart`, optionally `lib/widgets/periodic_tile.dart`, `lib/widgets/browse/browse_pills.dart`. ⚠️ Check PARALLEL's board entry before touching `run_provider.dart`.

---

## 2. Sir Junkan junk adding — partially implemented, name-mismatch bug

**Findings:**
- `JunkanDashboardSliver` (junkan_dashboard.dart) **already has working +/- junk buttons** calling `p.addItem/removeItem('Junk')`, plus a Gold Junk "ACTIVATE MECH" toggle. 'Junk' and 'Gold Junk' both exist in items.json.
- Dashboard tab is gated by `dashboard_swiper.dart:41` — appears when the player owns any item containing 'ser junkan'.
- **BUG:** `item_body.dart:1043` gates the detail-screen tracker with `item.name.toLowerCase() == 'ser junkan'` — the actual item name in items.json is **"Ser Junkan 1"**, so `_buildJunkanInfo` is dead code and never renders. This is likely why the user thinks junk can't be added — the item detail page shows no tracker.
- The rank table (Peasant→Angelic Knight) is copy-pasted in both files — duplication.

**Plan:**
1. Fix the name check: `startsWith('ser junkan')` (covers "Ser Junkan 1" and any future variants).
2. Extract the shared rank-data table to one place (e.g. a small `junkan_ranks.dart` data class or into the Item/RunProvider layer) — both widgets render from it.
3. UX polish (optional): surface the Junkan dashboard more discoverably — e.g. the dashboard exists but only inside the panels swiper; consider whether user found it.

**Files:** `lib/widgets/item_detail/item_body.dart`, `lib/widgets/dashboards/junkan_dashboard.dart`.

---

## 3. Paradox → sidekick starts with no items — clarify + COORDINATE WITH PARALLEL

**Findings:**
- `gungeoneers.json`: The Paradox `starting_guns: ['Random']`, `starting_items: ['Random']`.
- `run_provider._buildPlayerFor` (837-849) name-matches starters → 'Random' resolves to nothing → **Paradox currently gets an EMPTY loadout** (starter_hint.dart already tells the user "Paradox starts with a random loadout").
- `startCoopPlayer` (859-863) uses the same path — a Cultist sidekick gets its real starters (Dart Gun, Friendship Cookie, Number 2).
- ⚠️ **PARALLEL (Slot 3) owns this area right now** — Paradox Mode v3.0.0 is their active task in run_provider + MP files. This feedback item should be delegated to them via the Inter-Slot Task Queue or sequenced after their merge.

**Ambiguity — needs user clarification:**
- (a) Desired: "when main = Paradox, sidekick also gets no items" → rule in `startCoopPlayer`: if `main.character == Paradox`, build empty coop player.
- (b) Or: Paradox should actually ROLL a random gun+item (the real game behavior: a random starter from another character's pool) — and the sidekick inherits the same "random" rule.
- (c) Or: sidekick should mirror Paradox (also paradox-random).

**Plan (pending clarification + PARALLEL handoff):**
- Likely small change in `_buildPlayerFor`/`startCoopPlayer`. If random-rolling: pick a random other gungeoneer's starter set (excluding co-op-locked entries).

---

## 4. Drill / Clown / Lootbag combo companions choosable — HUD exists, read-only

**Findings:**
- `_buildPaydayInfo` (item_body.dart:621-765) already renders a "PAYDAY CREW ASSEMBLY HUD" with three heister slots — Dallas (Clown Mask), Wolf (Drill), Chains (Loot Bag) — but they're **display-only badges** (SUMMONED/LOCKED). Shows inside the item detail of any of the 3 items only.
- No "Payday" synergy exists in synergies.json (verified — the 3-item combo isn't a formal synergy entry).
- `hasDrill` also checks `player.guns` for 'drill' — Drill is an item, not a gun (harmless dead check).
- `itemByName('Clown Mask'/'Drill'/'Loot Bag')` all exist → toggling is trivially implementable via the Junkan pattern.

**Plan:**
1. Make `_buildHeisterSlot` tappable: tap a heister → `p.addItem`/`p.removeItem` the backing item (haptic + SUMMONED state flips). Wrap in InkWell with ripple.
2. Optional: register a Payday tab in `DashboardSwiper` when any Payday item is owned (mirrors Junkan discoverability fix).
3. Optional: add proper icons/splash for the three heisters instead of Material icons.

**Files:** `lib/widgets/item_detail/item_body.dart`, `lib/widgets/dashboards/dashboard_swiper.dart` (optional).

---

## 5. Item descriptions missing — CONFIRMED: two fields never surface in UI

**Findings:**
- All 270 items have `effect` (one-line gameplay description) — parsed into `Item.effect` but **never rendered** in the item detail screen (used only for heuristics: duration extraction, elemental tagging, isActive detection).
- All 270 items have `ammonomicon_entry` (flavor Ammonomicon text) — **the Item model doesn't even parse it** (no field, no `json['ammonomicon_entry']` in fromJson/toJson).
- Detail screen shows: quote, quality/type pills, special HUDs, stat pills, wiki sections — but no plain description block.

**Plan:**
1. Add `ammonomiconEntry` field to `Item` (model + fromJson/toJson).
2. Render in `ItemBody.build`: the `effect` line (primary description, below special HUDs / above stat pills) and optionally the ammonomicon entry as italic flavor text block.
3. Optional: surface `effect` as a subtitle/expanded line in browse rows or quick-add sheet.

**Files:** `lib/models/item.dart`, `lib/widgets/item_detail/item_body.dart`.

---

## 6. Remove "Exit the Gungeon" info — small, contained

**Findings:** 4 entities contain XtG text inside wiki token lists:
- Items: **Meatbun** (effects.sub), **Pig** (effects.sub), **Wolf** (effects bullet with `ref`/lore token "Exit the Gungeon")
- Guns: **Brick Breaker** (same pattern)

**Plan (two options):**
- **(a) Render-side filter (recommended):** where `WikiContent`/rich_text tokens are flattened to display text (`lib/models/rich_text.dart` or `wiki_sections.dart`), drop any paragraph/bullet whose concatenated text mentions "Exit the Gungeon". Survives future data regen; zero data churn.
- **(b) Data-side strip:** delete those token blocks from items.json/guns.json. Cleaner data, but a regeneration script could re-add them.

**Files:** `lib/models/rich_text.dart` / `lib/widgets/wiki_sections.dart` (or the two JSON files).

---

## 7. Remove screen timeout — missing wakelock

**Findings:** No wakelock anywhere — not in main.dart, pubspec, or AndroidManifest. Screen sleeps during runs.

**Plan:**
1. Add `wakelock_plus` to pubspec (check for a version >7 days old — e.g. `^1.2.x`; verify current latest).
2. `WakelockPlus.enable()` in `main()` after `WidgetsFlutterBinding.ensureInitialized()`.
3. Optional: Settings toggle "Keep screen awake" under RUN TOOLS if users want control. Simplest shippable version = always-on.
- Note: Android uses FLAG_KEEP_SCREEN_ON under the hood; Windows build is unaffected (desktop sleep is OS-managed).

**Files:** `pubspec.yaml`, `lib/main.dart`, optionally `lib/widgets/settings/settings_tab.dart`.

---

## Suggested execution order

| # | Item | Effort | Risk | Notes |
|---|------|--------|------|-------|
| 6 | XtG filter | XS | low | single filter point |
| 7 | Wakelock | XS | low | new dep — verify version age |
| 5 | Item descriptions | S | low | model + render |
| 2 | Junkan name fix | XS→S | low | plus optional dedupe |
| 4 | Payday toggles | S | low | tappable heisters |
| 1 | Gunderfury DPS | M | med | needs wiki fact-check on form milestones; unify thresholds |
| 3 | Paradox sidekick | S | **blocked** | clarify intent + hand to PARALLEL (AC4 collision) |

All changes → version bump → release checklist: `pubspec.yaml`, `asset_paths.dart`, `changelog.json`, `VERSION_HISTORY.md` (5 files in lockstep — see docs/TECHNICAL_REFERENCE.md §4).
