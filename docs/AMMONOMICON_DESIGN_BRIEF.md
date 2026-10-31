# Ammonomicon Design Brief

> Handoff for the **VISUAL/DESIGN agent** (claim Slot 1 on the board).
> Written post-rename — everything is `Ammonomicon*` now, nothing
> `Codex*` remains. This doc describes what exists, what data you can
> surface, and the design asks. Commit prefix: `ui:` / `ammonomicon:`.

## A — Architecture (where things live)

| File | Role |
|---|---|
| `lib/screens/ammonomicon_screen.dart` (~1,080 ln) | Category grid, global search, expandable tiles, quality/sort/MATCHED chips, `_openEntry` routing, `ammonomiconSectionForIndex` |
| `lib/screens/ammonomicon_widgets.dart` (part) | `_AmmonomiconList`, `_AmmonomiconCard`, `_GungeoneersAmmonomiconPage`, `_SearchGroup` |
| `lib/screens/ammonomicon_detail_screen.dart` | Generic entry detail — name/desc/ammonomicon/tips/health/location/wiki button |
| `lib/widgets/ammonomicon/ammonomicon_tabs.dart` | `AmmonomiconTab` model + `AmmonomiconTabStrip` (bookmark-style strip, collapsed toggle) |
| `lib/screens/synergy_detail_screen.dart` | Synergy graph — tappable owned-state chips |
| `lib/screens/item_detail_screen.dart` | Gun/item detail — flat stats + `_GunDeepStats` chips |

**Category order** (12 tabs):
`Gungeoneers(sp) · NPCs · Enemies · Bosses · Pickups · Objects · Guns · Items · Synergies · Shrines · Chapters(exp) · GameModes(exp)`.
`expandable` tabs open a themed member-picker panel in place of the grid
(`_buildExpandedPanel`). `isSpecial` = bespoke page (Gungeoneers only).

**UX state machine:** `_selected` (drill-down index), `_expanded`
(member-panel index), `_query` (search → grouped global results),
`_qualityFilter`/`_sortMode`/`_matchedOnly` (chips row on 6/7/8).

## B — Data available per entry (`AmmonomiconEntry.fromJson` fields)

`name, category, description, icon, wikiUrl, location, game, health, ammonomicon, tips[]` — all rendered by the generic detail screen today.

**Silent metadata (stored, NOT rendered — the design opportunity):**
- `chapters.json` (12): `floor` (1–6, null=secret/hub), `secret`, `bundle` (`base_castle`…), `music` (`Play_MUS_Forge_theme_01`)
- `game_modes.json` (6): `game_classes` (26 ChallengeModifier class names, Bossrush flow names)
- `enemies/bosses.json`: `game_enc_key`, `game_health` (game-truth HP vs wiki `health`)
- `guns/items`: verified stats — `quality`, `damage`, `shot_speed`, `range`, `force`, `spread`, `ammo_capacity`, `reload_time`, `type`
- `synergies.json`: `items`, `any_of`, `game_ids`, `game_name_key`, `effect`

Icons: `assets/images/{section}/` folders per category; tabs use
`assets/images/ammonomicon/tabs/Ammonomicon_Tab_*.png|webp` — only
Guns/Items have `assetIcon` today.

## C — Design asks (full pass, priority order)

1. **Chapter/mode detail treatment** — surface the silent metadata:
   `FLOOR 5` / `SECRET` / `HUB` badges, theme-name row, bundle tag,
   modifier list on Challenge Mode. Either extend the generic detail
   with a badge row or build a dedicated chapter card — your call.
   Bonus: floor-chain mini-map (F1→F6 + secret side-branches).
2. **Grid + expanded-panel polish** — tile art direction beyond
   tinted borders; member cards could carry floor badges
   (`F1`/`SECRET`) as leading chips.
3. **Tab strip art** — `Ammonomicon_Tab_*` assets exist only for a
   few tabs; either generate consistent icons for all 12 or settle on
   a coherent Material-icon set.
4. **Synergy detail polish** — chip graph styling, owned-glow tuning,
   ACTIVE badge treatment.
5. **Empty states + skeletons** — search-empty already has
   `search_off` icon; per-category empty needs the same level.
6. **Motion** — `flutter_animate` is in use; keep reduced-motion
   respected (existing patterns in ammonomicon_widgets).

## D — Conventions (non-negotiable)

- `flair.*`/`Insets`/`Radii` tokens — not raw `EdgeInsets`/`BorderRadius`
  values where tokens exist (category accent `Color(0x…)` are
  intentional identity accents, not violations)
- `GoopText` not `Text`; `maxLines`/`TextOverflow` on fixed-height text
- `Haptics.selection()` on taps; `BoxFit.contain` in fixed-height image
  slots; `fastRoute` for nav pushes; `Responsive.factor` scaling
- `dispose()` every controller; `context.mounted` before overlays
- No `GridView`/`ListView` inside `PageView` (landmine)
- `part`/`part of` for file splits (see `ammonomicon_widgets.dart`)

## E — Coordination

- Claim **Slot 1 VISUAL** in `AGENT_STATUS.md`; commit prefixes
  `ui:`/`ammonomicon:` (data edits → `data:`)
- Other agent's dirty files: ~35 deleted `assets/images/avatars/*.webp`
  in the working tree are Slot 4 WIP — **do not stage/commit them**;
  use explicit `git add` paths
- After JSON edits: run `python tools/data_integrity.py` if present +
  `flutter test test/data_integrity_test.dart`
- Push app repo to `origin master`; board updates in root repo
- Known deferred: `ammonomicon_screen.dart` still ~1,080 lines (fine),
  room-category enum mining for per-floor pools, curated prose per
  entry

## F — Quick wins already done (don't redo)

Global grouped search, expandable tiles, quality/sort/MATCHED chips,
`_openEntry` shared routing, `cacheWidth` icons, Fallen Angel icon
special-case, `ammonomiconSectionForIndex` + regression test,
'Codex'→'Ammonomicon' full rename (e15e070/35e5879).
