# Next Round Masterplan — bughunt, avatar variants, palette expansion, studio UX

> Status: PROPOSED — awaiting GO per workstream.
> Supersedes nothing; FINAL_SWEEP items fold into Slot 3's share.
> User directive (2026-11-24): "we got 3 agents each can take one when
> we done planning including u" — work divided 3 ways below.

## Workstream division (3 agents)

### Slot 3 — PARALLEL (Devin): crash bughunt + carry-over fixes
**Priority: the particle memory leak — a crash beats everything.**

| # | Task | Notes |
|---|------|-------|
| P1 | **Particle preset memory leak** — user report: pick `Skull` particles, later switch to `Neon` → leak/crash. Repro: Experience Studio → particles → Skull → Neon, watch memory across switches. Suspects: undisposed AnimationControllers/tickers per preset, particle systems not torn down on schema/preset change, timers in `studio_particles.dart`/`theme_overlay.dart`. Fix + regression test (pump preset A→B→A, assert controller/ticker counts stable) | HIGH |
| P2 | **Main menu touch-up** (user request, in-flight): menu buttons −15% (height 62→~53×sf, icon/font scaled), align GUNGEON MATE title + subtitle pill to the same side inset as the button column, hide the top corner chips (Settings/Asset Viewer/Bug) "for now" | S |
| P3 | FINAL_SWEEP leftovers: U-053 dead-code excision (`synergies_section.dart` 415 lines), `debug_tab.dart`→`special_items_grid.dart` rename, `bug_report.dart` doc version, migration case-hardening, Mimic Storage run-start tooltip ("Mimic Storage now available" on new run) | S |
| P4 | Full gate + ship: analyze, suite, VERSION_HISTORY, bug list, APK → Desktop (version: recommend v3.8.1) | S |

### Slot 1 — VISUAL (Devin): customization UX consolidation
**The studio's in-progress view has 3 rows of tabs up top — reclaim the space.**

| # | Task | Notes |
|---|------|-------|
| V1 | **In-progress view tab consolidation** — user: "3 ROWS of tabs lol. need back, apply changes to save. middle is toggleable options as we group the tabs there!! save shitton of space". Rework the customize/preset-edit view: single header row (BACK + APPLY/SAVE), remaining controls grouped under ONE tab strip instead of stacked rows. Apply REWORK_LESSONS_LEARNED.md standards; keep every existing control reachable | M |
| V2 | **Settings light touch-up** (carried from audit): hero header strip (theme splash thumb + version), spacing rhythm, verify panel-expand motion — NO IA changes, NO new rows | S |
| V3 | Bug-hunt own work per S6; coordinate file locks via board (studio files may overlap Slot 3's tooltip work — different files, OK) | — |

### Slot 2 — CORE (Devin): color system expansion
**"More colorpicker palette variety from darks to lights… specials group of 64 amazing special colors that glow/pulse."**

| # | Task | Notes |
|---|------|-------|
| C1 | **Research + design doc first** (`docs/COLOR_SYSTEM_PLAN.md`): audit current palette data flow (where color lists live — studio color wells, favorites, presets), then spec: per-hue-group 32-shade ramps (dark→light incl. lighter neons), PLUS a SPECIALS group of 64 interactive colors with behavioral hooks (glow/pulse/etc.). Decide data format (JSON vs code), how "special" colors carry behavior, perf cost of animated swatches | M |
| C2 | Implement palette data + picker UI per approved spec | M–L |
| C3 | Tests: palette integrity (count/uniqueness), picker renders all groups, special-color selection round-trips through prefs/presets | S |

### Avatar variants — RESEARCH SPIKE (unassigned, blocked on user)

User directive: "female versions / more feminine energy… iconic M and F versions for all… one by one… i will tell u the index of all the avatars we make alt versions of first… genous lvl prompting and PW… can login if u open up GemGem."

- **BLOCKED:** needs (a) research into the generation pipeline ("GemGem" tool — what is it, auth, API?), (b) user's avatar index/list.
- **Research task** (whoever frees first, or Slot 4 SUPPORT): document how avatar assets are produced today (`avatar-base` folder → `tools/` scripts? manual?), what "GemGem" is, prompting template for masculine/feminine pairs (hair, silhouette, demeanor), output specs (320×320 webp, `custom_NN` id scheme, avatar picker registration).
- Output: `docs/AVATAR_VARIANTS_PLAN.md` — generation is asset production, likely batched per user index, NOT a code task until assets exist.

## Dependencies & ordering

1. **Now:** Slot 3 starts P1 (leak) immediately — crash > everything. Slot 1 starts V1. Slot 2 starts C1 research.
2. Avatar research can start any time (read-only, no conflicts).
3. Ship gate (P4) waits for all three slots' merges — single v3.8.1 release.
4. AC4 watch: Slot 1 touches `experience_studio/` + `settings/`; Slot 3 touches `main_menu_screen.dart`, `run_provider.dart`, widgets/settings — minimal overlap. Slot 2 touches palette/picker code — check overlap with studio color wells (coordinate via board before C2).

## Open questions

1. Avatar index — user provides list of which avatars get variants first.
2. "GemGem" — what tool/service is this? (Research spike answers.)
3. Special colors' behaviors — glow/pulse/shimmer options; scope to picker-time selection or per-swatch animation?
4. v3.8.1 vs v3.9.0 at ship time (recommend v3.8.1 — fixes+polish on v3.8.0).
