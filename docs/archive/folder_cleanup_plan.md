# GungeonMate Folder Cleanup Plan

> Created: Aug 2026, v1.9.28
> Target: `X:\apps\GungeonMate` root + `gungeon_mate` subfolder

---

## Current State — What's Messy

### Root folder `X:\apps\GungeonMate\`

**Tracked files that are scattered temp scripts (untracked in git):**
| File | Size | What it is | Verdict |
|------|------|-----------|---------|
| `audit_items.js` | 5.2 KB | One-off data audit script | MOVE to `scripts/` or DELETE |
| `download_synergy_icons.py` | 5.7 KB | Icon download script | MOVE to `scripts/` |
| `fix_synergy_icons.py` | 5.1 KB | Icon fix script | MOVE to `scripts/` |
| `parse_synnergy_sprites.py` | 5.4 KB | Sprite parsing script | MOVE to `scripts/` |
| `vlc-help.txt` | 0.4 KB | Random VLC notes | DELETE (irrelevant) |

**Tracked files that are fine where they are:**
| File | Size | What it is | Verdict |
|------|------|-----------|---------|
| `.gitignore` | 0.2 KB | Git ignore rules | KEEP |
| `.windsurfrules` | 2.5 KB | Dev instructions | KEEP |
| `AGENTS.md` | 25.2 KB | Agent guidelines | KEEP |
| `AGENT_STATUS.md` | 29.2 KB | Agent status board | KEEP |
| `README.md` | 4.4 KB | Project readme | KEEP |
| `gungeon-mate-app-logo.png` | 6 MB | App logo | KEEP (but see note below) |
| `gungeonmate-animation-02.mp4` | 2.4 MB | Home screen animation | KEEP (referenced by app) |
| `BUILD_RELEASE_APK.bat` | 1.3 KB | Build script | KEEP |
| `launch_gungeonmate.bat` | 4.9 KB | Launch script | KEEP |
| `RUN_ON_CHROME.bat` | 0.3 KB | Run script | KEEP |
| `RUN_ON_WINDOWS.bat` | 0.3 KB | Run script | KEEP |

**Directories:**
| Dir | Size | What it is | Verdict |
|-----|------|-----------|---------|
| `.devin/` | — | Devin CLI config | KEEP |
| `.git/` | — | Git repo | KEEP |
| `.idea/` | — | IDE config | KEEP (gitignored) |
| `.playwright-mcp/` | 0.4 MB | Playwright screenshots/snapshots | ADD to .gitignore |
| `.windsurf/` | — | Windsurf config | KEEP |
| `app-releases/` | 1.5 GB | Release APKs/AABs | KEEP (gitignored) |
| `cache_wikigg/` | 24.7 MB | Cached wiki HTML | KEEP (gitignored) |
| `docs/` | — | Documentation | KEEP (needs internal cleanup) |
| `gungeon_mate/` | — | Flutter app (separate git repo) | KEEP |
| `roomian_battler/` | 100 MB | Separate game project (submodule) | KEEP |
| `scripts/` | — | Data pipeline scripts | KEEP (gitignored) |
| `sounds/` | 1.7 MB | Sound files | KEEP (untracked — needs .gitignore decision) |

### `gungeon_mate/` subfolder

**Temp/junk files in the Flutter app root:**
| File | Size | What it is | Verdict |
|------|------|-----------|---------|
| `bar_kitchen_app.iml` | 0.8 KB | Old IntelliJ project file (wrong name!) | DELETE (gitignored, but stale) |
| `build_output.txt` | 0.6 KB | Old build log | DELETE (gitignored, but stale) |
| `check_hardcoded.ps1` | 1.3 KB | One-off check script | MOVE to `tools/` or DELETE |
| `DOCUMENTATION.md` | 10.2 KB | Old documentation | REVIEW — may be stale |
| `README.md` | 3.2 KB | Flutter default readme | KEEP |

**Duplicate/overlapping directories:**
| Dir | What it is | Verdict |
|-----|-----------|---------|
| `tool/` | Flutter tool config | KEEP (standard) |
| `tools/` | Data pipeline Python scripts | KEEP |
| `builds/` | Release build storage | KEEP (gitignored) |
| `build/` | Flutter build output | KEEP (gitignored, ephemeral) |
| `documentation/` | Old docs (2 files) | MERGE into `docs/` or DELETE |

### `docs/` folder — 34 files, many stale plans

**Active/recent docs (KEEP):**
- `bug_tracker.md` — active bug tracker
- `design_view_library.html` — current screenshot gallery
- `redesign_comparison.html` — current redesign gallery
- `design_assessment_and_redesign_plan.md` — current assessment
- `multiplayer_rework_plan.md` — current rework plan
- `SYSTEM_SUMMARY.md` — system overview
- `TECHNICAL_STACK.md` — tech stack reference
- `APP_FEATURES_MAP.md` — feature map

**Stale/completed plan docs (ARCHIVE):**
- `bullet_hell_edition_plan.md` — completed (banner removed)
- `char_select_enhancement_plan.md` — completed (3×3 grid done)
- `codex_plan.md` — completed (codex built)
- `damage_calculator_assessment.md` — completed
- `detail_redesign_curse_plan.md` — completed
- `gungeon_fall_animation_plan.md` — completed (video swap done)
- `language_selection_plan.md` — stale/unimplemented
- `midjourney_reference_guide.md` — art reference, not code
- `mp_auto_reconnect_plan.md` — completed or stale
- `MULTIPLAYER_PLAN.md` — superseded by multiplayer_rework_plan.md
- `npc_view_plan.md` — completed or stale
- `RENDER_GLITCH_NOTES.md` — old debug notes
- `reorg_plan.md` — old reorganization plan (superseded by this doc)
- `robot_enhancements_plan.md` — completed or stale
- `roomian_*` (6 files) — separate game project docs, not GungeonMate
- `SYNERGIES_FIX_PLAN.md` — completed (synergies audited)
- `ui_polish_superplan.md` — completed or stale
- `ux_optimization_plan.md` — superseded by design_assessment
- `wiki_data_mastery_plan.md` — completed (data audited)
- `winchester_huntress_plan.md` — stale/unimplemented
- `GUNGEONMATE_WIRE_OVERVIEW.html` — old wireframe (superseded by design_view_library)

---

## Cleanup Plan

### Phase 1: Move scattered scripts to `scripts/` (5 min)

**Move these root-level scripts into the existing `scripts/` folder:**
- `audit_items.js` → `scripts/audit_items.js`
- `download_synergy_icons.py` → `scripts/download_synergy_icons.py`
- `fix_synergy_icons.py` → `scripts/fix_synergy_icons.py`
- `parse_synnergy_sprites.py` → `scripts/parse_synnergy_sprites.py`

**Delete:**
- `vlc-help.txt` (irrelevant random file)

### Phase 2: Clean `gungeon_mate/` root (2 min)

**Delete temp/junk files (all gitignored, not tracked):**
- `gungeon_mate/bar_kitchen_app.iml` (stale IntelliJ file with wrong project name)
- `gungeon_mate/build_output.txt` (old build log)
- `gungeon_mate/check_hardcoded.ps1` (one-off script — move to `tools/` if still useful, else delete)

**Review:**
- `gungeon_mate/DOCUMENTATION.md` — check if stale, merge into `docs/` or delete
- `gungeon_mate/documentation/` — 2 files (FEATURES_ANALYSIS.md, UI_UX_ISSUES.md) — merge into `docs/` or delete

### Phase 3: Archive stale docs (10 min)

**Create `docs/archive/` folder and move completed/stale plans there:**
- All `roomian_*` files (6 files — they belong to the separate game project)
- All completed plan docs (bullet_hell, char_select, codex, damage_calculator, etc.)
- Superseded docs (MULTIPLAYER_PLAN, reorg_plan, ux_optimization_plan, etc.)
- Old wireframe HTML (GUNGEONMATE_WIRE_OVERVIEW.html)

**Keep in `docs/` root:**
- `bug_tracker.md`
- `design_view_library.html`
- `redesign_comparison.html`
- `design_assessment_and_redesign_plan.md`
- `multiplayer_rework_plan.md`
- `SYSTEM_SUMMARY.md`
- `TECHNICAL_STACK.md`
- `APP_FEATURES_MAP.md`
- `screenshots/` folder

### Phase 4: Update `.gitignore` (2 min)

**Add to root `.gitignore`:**
```
# Playwright MCP artifacts
.playwright-mcp/

# Sound assets (if not tracked)
sounds/
```

### Phase 5: Move large assets (optional, 5 min)

**Consider moving to `gungeon_mate/assets/` since they're app assets:**
- `gungeon-mate-app-logo.png` (6 MB) — if referenced by the app
- `gungeonmate-animation-02.mp4` (2.4 MB) — already copied into `gungeon_mate/assets/images/wallpapers/animated/`

The root-level copies could be deleted if the app only uses the copies inside `gungeon_mate/assets/`. Need to verify no build script references the root copies.

---

## Summary

| Phase | Action | Items | Time |
|-------|--------|-------|------|
| 1 | Move scattered scripts to `scripts/` | 4 files | 5 min |
| 2 | Delete temp files from `gungeon_mate/` | 3-5 files | 2 min |
| 3 | Archive 20+ stale docs to `docs/archive/` | 20+ files | 10 min |
| 4 | Update `.gitignore` | 2 entries | 2 min |
| 5 | Move/delete duplicate large assets | 2 files | 5 min (optional) |

**Result:** Root folder goes from ~12 loose files to ~8 intentional files. `docs/` goes from 34 files to ~10 active + 24 archived. `gungeon_mate/` root loses 3-5 junk files.

**Risk:** LOW — all moves are within gitignored or untracked areas. No tracked source files are deleted. Archived docs are moved, not deleted.
