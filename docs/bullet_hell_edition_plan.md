# 🔥 Bullet Hell Edition — Release Plan

> **Persistent reference for the next major release.** All agents working on
> bugs/features tagged for this edition should read this doc first and keep
> it in sync as items land. The edition is a branded milestone, not a single
> patch — fixes accumulate under one banner until we ship the APK.

---

## Identity

| Field | Value |
|-------|-------|
| **Edition name** | Bullet Hell Edition |
| **Version** | `v2.0.0` (build `+79`) |
| **Title (changelog/main menu)** | `🔥 BULLET HELL EDITION` |
| **Status** | IN PROGRESS — accumulating fixes |
| **Started** | 2026-08-12 |
| **Folds in** | The v1.8.39 hotfix batch (BUG-017/019/020) — no separate v1.8.39 ship |

---

## Scope — Bug Lineup

### Landed (done, committed)
| Bug | Sev | Summary | Commit |
|-----|-----|---------|--------|
| BUG-017 | HIGH | Max Pane synergy: added `Glass Guon Stone` to items array so it flags active when both are owned | `e0f928b` |
| BUG-019 | HIGH | MP reconnect: floating "Connection restored — sync resumed" snackbar + `Haptics.success()` on real reconnect (not teardown) | `e0f928b` |
| BUG-020 | MED | Quality `1S` → `S` across 36 data entries (guns 19 + items 17); browse sort simplified | `e0f928b` |

### Pending (in the Task Queue, ready for Coder pickup)
| Bug | Sev | Summary | Notes |
|-----|-----|---------|-------|
| BUG-035 | UX | PeriodicTile gun panel: gun type below title (centered addon-panel) + RANGE on the periodic grid alongside DPS | Touches `periodic_tile.dart` — coordinate with pre-existing uncommitted UI tweaks in that file (see AGENT_STATUS handoff) |
| BUG-036 | UX | Active run HeaderMenu: quick "Reset Player Items" action + move Settings to bottom section | Lift `_confirmClearInventory` from `run_tab.dart` to share |
| BUG-037 | UX | Remove MP Summary panel/tab (SummaryTab + MpSummaryPage) | Leave `summary_tab.dart` on disk (Safety S4) — just unwire it |
| BUG-038 | HIGH | Unicorn theme: particles don't show + palette selector scrolls + no per-palette particle previews | Largest scope — theme+particle system. Prefer overlay-side preset override over clobbering global pref |
| BUG-039 | MED | S-tier chest/quality colors unreadable — revert to documented black pill + white text + gold glow across `QualityBadge` + `_ChestChip` + `PeriodicTile` | Touches `item_detail/header.dart` — coordinate with pre-existing uncommitted UI tweaks (see AGENT_STATUS handoff) |

### Optional / consider folding in (open bugs, lower priority)
| Bug | Sev | Summary |
|-----|-----|---------|
| BUG-018 | MED | Browse screen has no empty-search state |
| BUG-021 | MED | 46 active items missing `recharge_time` |
| BUG-022 | MED | 289 synergies missing local icon assets |
| BUG-023 | LOW | 3 guns missing wiki notes content |
| BUG-024 | LOW | 2 items missing wiki content |
| BUG-026 | MED | Browse grid add-button tap target too small |
| BUG-027 | LOW | Item detail buttons lack haptic feedback |
| BUG-028 | LOW | Collapsible sections pop instead of animate height |
| BUG-029 | LOW | Quick Add sheet search results limited to 6 |
| BUG-032 | LOW | `catch (_) {}` silently swallows SharedPreferences errors |
| BUG-033 | LOW | Browse filter chips use emoji instead of Material icons |
| BUG-034 | LOW | Favourites heart toggle clears all snackbars |

> The optional list is the "and things" of the edition — fold in as many as
> time allows before the APK build. The UX polish group (BUG-018/026/027/028/
> 029/033/034) is the natural second batch after BUG-035–039.

---

## Styling & Branding Direction

- **Changelog entry** (`assets/data/changelog.json`): single entry, version
  `v2.0.0`, title `🔥 BULLET HELL EDITION`, date `August 2026`. Each fix is a
  punchy headline item with a leading emoji (💥/🔗/✨/🎯…). As pending bugs
  land, append their headline items to the same `items` array — do NOT create
  a second v2.0.0 entry.
- **Main menu** (`main_menu_screen.dart`): version string `v2.0.0`, changelog
  button `Changelog (v2.0.0)`, subtitle line `v2.0.0 — BULLET HELL EDITION`.
- **VERSION_HISTORY.md**: one `## v2.0.0 — 🔥 BULLET HELL EDITION` section with
  "Landed so far" + "Coming in the edition" subsections; move pending items to
  "Landed" as they commit.
- **APK filename** (when shipped): `gungeon-mate-v2.0.0-bullet-hell-edition.apk`
  — include the edition slug for discoverability.
- **Aesthetic**: keep the dark neon Gungeon look. The edition is a branding
  moment, not a reskin — no new color system. Particle/haptic polish from
  BUG-038/039 should feel like the "bullet hell" energy: snappy, bright, alive.

---

## Ship Checklist (when ready to release)

1. All targeted bugs fixed + bughunted + committed.
2. `flutter analyze` clean on all modified files.
3. Changelog `items` array finalized — no "coming soon" placeholders left.
4. VERSION_HISTORY "Coming in the edition" section emptied into "Landed".
5. `pubspec.yaml` version confirmed `2.0.0+79`.
6. Build release APK → `app-releases/gungeon-mate-v2.0.0-bullet-hell-edition.apk`.
7. Tag `v2.0.0` + GitHub Release with APK asset.
8. Update AGENT_STATUS Session Log with the edition ship row.

---

## Coordination Notes

- **Maintainer** logged BUG-035–039 with implementation-ready detail (commit
  `73569c9`, outer repo). Coder picks them up from the Task Queue.
- **Pre-existing uncommitted UI tweaks** in `lib/widgets/item_detail/header.dart`
  and `lib/widgets/periodic_tile.dart` (from the prior Coder session) overlap
  with BUG-035 and BUG-039. The Coder must coordinate/stash before starting
  those two to avoid clobbering (see AGENT_STATUS Session Log note).
- `gungeon_mate/` is a nested git repo — code commits land there; the outer
  repo holds docs + AGENT_STATUS. Keep both in sync on edition progress.
