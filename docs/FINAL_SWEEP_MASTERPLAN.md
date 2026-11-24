# Final Sweep Masterplan — bughunt, fixes & polish

> Status: PROPOSED — awaiting GO.
> Context: v3.8.0 shipped (app `f9d202c`, tag `v3.8.0-stable` local,
> APK on Desktop). Post-release bughunt already landed U-057–U-062
> (studio preset flow, tools-sheet declutter, studio landing rebuild,
> backpack restore, Mimic Storage rename). USER_BUG_LIST is fully
> resolved — every U-0xx is Fixed/Closed/Won't-fix. This plan is the
> **last planned session**: verify the new build is honest, excise
> the remaining dead weight, and give Settings the polish pass the
> user flagged ("aint changed what-so-oever").

## Workstream A — Final bughunt (verify, don't assume)

| # | Check | Method |
|---|-------|--------|
| A1 | Literal `'Backpack'` sweep post-rename | grep lib/+test — expect only migration guard + comments |
| A2 | Migration edge: case-sensitivity | `i.name == 'Backpack'` is exact-case; saves always wrote 'Backpack' but harden to case-insensitive anyway (1-line) |
| A3 | Co-op migration coverage | `_refreshAgainstData` runs `refreshPlayer` on main AND coop — verified this session; pin with a P2 legacy-save test |
| A4 | MP cross-version edges | New peer sends 'Mimic Storage' → old build can't resolve name → cosmetic drop (partner's own bag unaffected). Old peer sends 'Backpack' → new build resolves REAL Backpack → partner view shows an unearned D-tier item + re-grant adds Mimic Storage. Decide: accept+document, or gate snapshot item resolution to known-safe names |
| A5 | `backpackKeys` collision | `'i:Backpack'` keys can't exist (bag can't stash itself; real Backpack was unreachable pre-rename) — verified, no action |
| A6 | Mimic Storage detail view | Synthetic item has no wiki/ammonomicon — verify ItemDetailScreen renders gracefully (empty NOTES tab?) |
| A7 | GIF actually animates in tiles | `GameIcon` uses `Image.asset` + `cacheWidth` — gungeoneer GIFs animate through the same path, but verify Mimic Storage tile on-device/emulator |
| A8 | Deferred-item re-check | AGENTS.md open deferreds: TIERS test regression, synergy-scan recompute-per-build perf, browse row overflow ≤500px, MP first-endpoint mis-pair race, host-gone hint — verify each is fixed or still live |
| A9 | Full mechanical re-sweep | dead screens, missing assets, stale strings, deprecated widgets — rerun the scripts from this session's audit |

## Workstream B — Fixes (small, mechanical)

| # | Item | Effort |
|---|------|--------|
| B1 | **U-053**: excise `lib/widgets/synergies_section.dart` — 415 lines of dead code (zero refs, pinned by earlier audit) | S |
| B2 | Rename `lib/widgets/settings/debug_tab.dart` → `special_items_grid.dart` (file contains `SpecialItemsGridScreen`, not a debug tab) + fix import in `settings_tab.dart` | XS |
| B3 | `bug_report.dart` doc example `GM-BUG v3.7.0` → current version | XS |
| B4 | A2 migration case-hardening if confirmed | XS |

## Workstream C — Polish (user-flagged)

| # | Item | Scope |
|---|------|-------|
| C1 | **Settings visual pass** — the screen is functionally complete (status strip, 3 collapsible panels, studio card, danger zone) but visually flat vs the reworked surfaces. Pass: hero header treatment (theme splash thumb + version), subtle motion on panel expand (exists — verify), section spacing rhythm, danger-zone framing. NO IA changes, NO new features — visual refresh only | M |
| C2 | **Item detail tabs UX verify** — SYNERGIES/NOTES collapsible tabs shipped in v3.8.0 (U-051 card chrome, U-054 tappable synergy rows). Verify on-device: tap targets, count badges, empty-NOTES state for synthetic items (A6). Polish only if something reads broken | S |
| C3 | Optional: stash discoverability — STASH is long-press-only; consider a one-time hint or caption on first inventory view | S — user call |

## Workstream D — Verify, document, ship

1. `flutter analyze` — 0 issues; full suite green; coverage baseline honest
2. VERSION_HISTORY — Unreleased entries for everything above
3. USER_BUG_LIST — log anything A/B turns up; close B1–B4
4. AGENT_STATUS — session log + slot release
5. **APK rebuild → Desktop** — version question: v3.8.1 patch (recommended — v3.8.0 tag exists locally) or roll everything into v3.9.0. User decides at ship time
6. Commit app repo + root repo, push both

## Explicitly OUT of scope

- No new features, no IA redesigns, no MP protocol changes
- No re-audit of already-verified-clean areas beyond A9 spot-check
- Settings gets visual polish ONLY — no new settings rows
- Tag push (`v3.8.0-stable` stays local unless user asks)

## Open questions for user

1. Settings polish depth — light touch-up (spacing/motion/header) or fuller restyle matching studio chrome?
2. A4 cross-version MP edge — accept as cosmetic or harden?
3. C3 stash hint — want it or is long-press fine?
4. Ship as v3.8.1 or v3.9.0?
