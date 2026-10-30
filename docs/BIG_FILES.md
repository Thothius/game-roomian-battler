# BIG FILES — ALL ≥1k-line files SPLIT (Phases 3–5, 2026-10-30)

# Big Files — Split Candidates (tracked 2026-10-29)

> Inventory of oversized source files in `gungeon_mate/lib/`, for staged
> breakup work in future sessions. Sorted by priority, not just size —
> files that change often and have clear seams go first.
> Rule for all splits: smallest correct diff per step, `flutter analyze`
> must stay clean, `flutter test` must stay green after every extraction.

---

## Tier 1 — extract first (biggest win per risk)

### `lib/services/app_theme.dart ✅` — 4,702 lines
The monolith. Holds theme palettes, fonts, particle configs, glows,
`ThemeFlair`, `displayedMode` preview plumbing, Palette Maker.
Suggested seams:
- `theme/palettes.dart` — the 9 built-in palette definitions + data tables
- `theme/theme_flair.dart` — ThemeFlair model + extensions
- `theme/palette_maker.dart` — Palette Maker state + persistence
- `theme/particle_presets.dart` — particle/glow default maps
  (`kThemeParticleDefaults`)
- Keep `app_theme.dart ✅` as the AppTheme notifier + `displayedMode` plumbing
  that re-exports the parts.
Risk: HIGH touch count — ThemeFlair is referenced everywhere. Do it in
per-domain extractions, not one big move. Add a smoke test that iterates
all themes and builds a themed widget per palette first.

### `lib/screens/experience_studio_screen.dart ✅` — 3,188 lines
Studio is already tab-shaped: PALETTES / FONTS / PARTICLES / GLOWS /
PREVIEW sections. Each tab body → `screens/studio/*_tab.dart` widgets.
Board history notes this file was "structurally broken → reverted" once
already — write/extend a widget test that opens each tab BEFORE touching it.

### `lib/providers/run_provider.dart ✅` — 2,002 lines
The only provider; classic god object. 18+ special-item trackers live
inline (Robot, Gunderfury, Evolver, Ser Junkan, Triple Gun…).
Suggested seams:
- `providers/special_trackers.dart` — per-item tracker state objects
  (each owns its keys, load/save, reset-on-endRun contract)
- `providers/run_lifecycle.dart` — endRun/startNewRun/reset flows
  (partially extracted already — verify what's left inline)
- Keep RunProvider as the facade that composes trackers + inventory.
Risk: persistence keys must not change — add a save-load round-trip test
snapshotting all `special.*` keys before/after refactor.

### `lib/widgets/particle_engine.dart ✅` — 2,071 lines
Custom particle engine. Likely separable into emitter/painter/preset
layers. Lower priority only because it changes less often.

## Tier 2 — medium splits

| File | Lines | Note |
|---|---|---|
| `widgets/dashboards/compact_dashboards.dart ✅` | 1,647 | ~15 dashboards in one file — one file per dashboard family |
| `widgets/item_detail/gun_stats.dart ✅` | 1,486 | Gunderfury per-form table should move to `models/` |
| `screens/shrine_picker_screen.dart ✅` | 1,243 | |
| `widgets/active_run/dice_roll.dart ✅` | 1,221 | physics + widgets + presets likely separable |
| `services/mp_session.dart ✅` | 1,214 | session facade — keep cohesive, extract event-log plumbing |
| `screens/paradox/paradox_flow_screen.dart ✅` | 1,214 | |
| `screens/stats_detail_screen.dart ✅` | 1,212 | fontSize-52 responsiveness bug noted in UI_HEALTH |
| `widgets/item_detail/item_body.dart ✅` | 1,168 | 13 name-gated special panels — table-driven registry |
| `widgets/periodic_tile.dart ✅` | 1,107 | |
| `screens/active_run_screen.dart ✅` | 1,079 | |
| `widgets/active_run/player_page.dart ✅` | 1,010 | AC4 split-file history — coordinate before touching |

## Tier 3 — watch list (700–1,000 lines)

`rich_link_text.dart` (965) · `mp/mp_sync.dart` (947) ·
`quiz_session_screen.dart` (922) · `browse_screen.dart` (922) ·
`settings/settings_tab.dart` (902) · `gungeoneer_header.dart` (888) ·
`avatar_aura.dart` (851) · `codex_screen.dart` (847) ·
`gungeoneer_detail_screen.dart` (812) · `mp_lobby_screen.dart` (798) ·
`active_run/stat_sheets.dart` (794) · `effect_tagger.dart` (768) ·
`paradox/chat_sheet.dart` (755) · `quiz_engine.dart` (727)

## Duplication to hunt during splits
- Ser Junkan rank table copy-pasted in `item_body.dart ✅` + `junkan_dashboard.dart`
- Surprise preset fx map duplicated between `surprise_overlay.dart` and `chat_sheet.dart`
- Gun/Item meta pill logic (`browse_pills.dart`) vs `periodic_tile.dart ✅`

## House rules for split sessions
1. One file → one PR-sized commit per extraction. No behavior changes.
2. `flutter analyze` clean + `flutter test` green at every step.
3. Check `AGENT_STATUS.md` — claim a slot, respect AC4 file locks.
4. Update this doc when a file drops under ~700 lines or gains a split.


## Status 2026-10-30

All monoliths ≥1,000 lines have been split via same-library part files
(zero import churn) + mixin extraction for class internals. Pattern:
`mixin _X on <Base>` in part files + abstract member requirements
(prune unused get/set halves). Every split: analyze clean + tests green
+ own commit. Remaining large-but-manageable files are in the 600–900
range (browse_screen, mp_sync, run_provider main).
