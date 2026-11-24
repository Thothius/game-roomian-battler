# User-Reported Bug List

> **Codeword: `bug list`** — say "bug list" and I'll append your notes here.
> Items are not acted on unless explicitly requested. Severity is user-assigned
> or TBD. Status tracks from report → triaged → fixed.

---

## Open




### U-038 — MP reconnect banner X button silently kills the whole session
- **Reported:** 2026-11-25 — UI/MP bughunt (Slot 3 PARALLEL)
- **Root cause:** `lib/widgets/mp_reconnect_banner.dart` `_PersistentBanner` — the small ✕ at the row's right edge calls `session.cancel()` (full MP teardown), while the banner body tap only re-opens the dialog. Doc comment even says "tap to cancel" but the affordance reads as "dismiss banner". User tapping ✕ expecting to hide the banner loses the entire co-op session.
- **Severity:** Medium (destructive action behind ambiguous affordance)
- **Status:** Fixed in app `4705729` — ✕ replaced with explicit END label; banner tap reopens dialog.

### U-039 — MP players lost the path to the full Cool & Curse explainer
- **Reported:** 2026-11-25 — UI/MP bughunt (Slot 3 PARALLEL); regression from `654fbed`
- **Root cause:** `paradox_player_panel.dart` `_PanelStat` has no `onLongPress` — solo header capsules long-press → `CoolCurseScreen` (full mechanics explainer), but MP tap now opens only the quick sheet. No MP surface reaches the explainer anymore.
- **Severity:** Low-Medium (feature access regression)
- **Status:** Fixed in app `4705729` — `_PanelStat.onLongPress` → `CoolCurseScreen` on COOL/CURSE (solo parity).

### U-040 — Quick-add sheet: unguarded async toast can fire after dispose
- **Reported:** 2026-11-25 — UI/MP bughunt (Slot 3 PARALLEL); file is foreign WIP (`active_run_screen.dart` `_QuickAddSheet`)
- **Root cause:** `_addIt` MP-peer path: `mpSession.sendAddToPeer(...).then((_) => _showToast(...))` — no `mounted`/disposed guard. If the sheet closes before the Nearby send completes, `_showToast` writes `_addedToast.value` on an already-disposed `ValueNotifier` → async FlutterError.
- **Severity:** Low (narrow race, self-inflicted crash only)
- **Status:** Fixed in app `4705729` — mounted guards on sendAddToPeer then/catchError.

### U-041 — MP request dialog can be dismissed by system back without answering
- **Reported:** 2026-11-25 — UI/MP bughunt (Slot 3 PARALLEL)
- **Root cause:** `mp_request_listener.dart` `_maybeShowIncomingRequest` — `showDialog(barrierDismissible: false)` still lets Android system-back pop the route (no `PopScope`). The peer's request is never answered → sender waits the full 30s timeout before seeing a denial.
- **Severity:** Low (edge case; denial arrives anyway, just slow)
- **Status:** Fixed in app `4705729` — PopScope treats system-back pop as DENY.

### U-042 — `dice_roll.dart` triple `@override` + orphaned field comments
- **Reported:** 2026-11-25 — UI/MP bughunt (Slot 3 PARALLEL)
- **Root cause:** `lib/widgets/active_run/dice_roll.dart:51-53` — three stacked `@override` annotations on `build()` plus three orphaned comments where fields moved into `_DiceRollLogic`. Committed merge/refactor artifact; legal but sloppy.
- **Severity:** Trivial (cosmetic)
- **Status:** Fixed in dice-system rework — file rewritten for single-die flow; artifact gone.

### U-043 — Emote menu + 'End MP Session' unreachable while `kMpSocialEnabled=false`
- **Reported:** 2026-11-25 — UI/MP bughunt (Slot 3 PARALLEL)
- **Root cause:** `mp_handlers.dart` `_showEmoteMenu` is only invoked from `mpTabTap` behind `kMpSocialEnabled` — with the flag off the whole sheet (kiss/slap buttons AND its 'End MP Session' row) is dead code. Run-tools 'Leave MP' covers teardown, so no functional loss — just ~100 lines of unreachable UI.
- **Severity:** Trivial (dead code)
- **Status:** Won't fix (by design, 2026-11-25) — the dead code IS the disable mechanism: `kMpSocialEnabled` is a const kill-switch documented as 'flip to re-enable'; excising would break that contract. Reachability is gated at `mpTabTap` + dispatch, so nothing user-facing is broken.





### U-047 — Item detail shows sell price twice
- **Reported:** 2026-11-25 — detail-view UI audit (Slot 3 PARALLEL)
- **Root cause:** `lib/widgets/item_detail/header.dart` — item variant renders `_SellBadge` in the top-left badge row AND a `Sell` `MetadataChip` in the tag Wrap. Gun variant shows it once (badge only).
- **Severity:** Low (cosmetic redundancy)
- **Status:** Fixed in app `9fb8759`

### U-048 — `gun.type` (fire mode) rendered nowhere; dead branch chain in GunStats
- **Reported:** 2026-11-25 — detail-view UI audit (Slot 3 PARALLEL)
- **Root cause:** `item_detail_screen.dart` passes `gun.type` as `subtitle`, but the gun branch of `ItemDetailHeader` never renders it. `gun_stats.dart:330-335` has an if/else chain on `typeLower` with all-empty branches (leftover from removed feature). BUG-048/050 type normalization feeds a field no UI displays.
- **Severity:** Low-Medium (invisible game data)
- **Status:** Fixed in app `3f2e607`

### U-049 — Gun header dropped metadata items still show
- **Reported:** 2026-11-25 — detail-view UI audit (Slot 3 PARALLEL)
- **Root cause:** Gun variant of `ItemDetailHeader` renders no tag Wrap — no chest color, curse/coolness chips, or synergy count. Item variant shows all. Stat grid covers CHEST/CURSE/COOL as rows but synergy count only appears inside the collapsed SYNERGIES tab.
- **Severity:** Low (consistency)
- **Status:** Fixed in app `3f2e607`

### U-050 — Elemental properties rendered in 4 different visual languages
- **Reported:** 2026-11-25 — detail-view UI audit (Slot 3 PARALLEL)
- **Root cause:** header `_ElementDot` (28px icon circles, guns top-left), `_ElementTagRow` (9.5px uppercase pills below card, guns), `ElementDot`/`elementDots` (8px plain dots, browse rows), `_ElementDot` (8px dots, inventory_list_row). Gun detail shows elements twice in two styles.
- **Severity:** Low (design consistency)
- **Status:** Fixed in app `3f2e607`

### U-051 — Gun detail body lacks card chrome (item body is card-contained)
- **Reported:** 2026-11-25 — detail-view UI audit (Slot 3 PARALLEL)
- **Root cause:** `GunStats` returns bare `Padding` — stat grid + special panels float on scaffold background. Item path renders `ItemBody` INSIDE the header card container. Different page rhythm for the two entity types.
- **Severity:** Low (design consistency)
- **Status:** Fixed in app `3f2e607`

### U-052 — Three tappable surfaces missed the ScaleButton press-feedback sweep
- **Reported:** 2026-11-25 — detail-view UI audit (Slot 3 PARALLEL)
- **Root cause:** `_DetailTabHeader` (`item_detail_screen.dart:651`) raw `GestureDetector` accordion headers; `_chip` filter chips + `_LebTogglePill` (`gun_synergies_tab.dart:254,1023`) raw `GestureDetector` — haptics present, no press scale.
- **Severity:** Low (dead-feeling taps, same class fixed in `f15eaa2`)
- **Status:** Fixed in app `9fb8759`

### U-053 — `synergies_section.dart` is 415 lines of dead code
- **Reported:** 2026-11-25 — detail-view UI audit (Slot 3 PARALLEL)
- **Root cause:** `SynergiesSection`/`SynergyCard`/`SynergyChip` have zero references in lib/ or test/ — superseded by `EntitySynergiesView`. Only consumer of its `Navigator.push` drill-in was itself.
- **Severity:** Trivial (dead code)
- **Status:** Fixed in app `9fb8759`

### U-054 — Synergy rows in detail view are dead-ends (not tappable)
- **Reported:** 2026-11-25 — detail-view UI audit (Slot 3 PARALLEL)
- **Root cause:** `entity_synergies_view.dart` `_SynergyRow` has no onTap — users can't drill into a missing piece or synergy member from the SYNERGIES tab, unlike browse rows which navigate to detail. The only row-level `Navigator.push` lived in the dead `synergies_section.dart`.
- **Severity:** Low-Medium (UX dead-end)
- **Status:** Fixed in app `dfe70d8`

### U-055 — Special item/gun panels ignore theme tokens (~180 raw Colors.* literals)
- **Reported:** 2026-11-25 — detail-view UI audit (Slot 3 PARALLEL)
- **Root cause:** `item_body_sections.dart` (103 hardcoded `Colors.*`, e.g. `Colors.amber` panels) and `gun_stats_sections.dart` (74) use raw Material colors — panels stay amber/white regardless of selected palette/flair, unlike the rest of the themed UI.
- **Severity:** Low (theming gap)
- **Status:** Fixed in app `dfe70d8` (neutral sweep) + `a7b8c09` (accent tail) — `_panelAccent()` derives each panel's signature hue from `AppTheme.flair.primary` lightness/saturation; only neutral white/black/transparent literals remain.

### U-056 — Dead header params + mojibake comment
- **Reported:** 2026-11-25 — detail-view UI audit (Slot 3 PARALLEL)
- **Root cause:** `ItemDetailHeader.quote` unused by both variants; `subtitle`/`isActive` dead for guns; `â€"` mojibake in comment at `header.dart:446`.
- **Severity:** Trivial (cosmetic)
- **Status:** Fixed in app `9fb8759`

### U-057 — "Neo-Skeuo" still visible after excision
- **Reported:** 2026-11-25 — v3.8.0 APK user test
- **Root cause:** RESOLVED — not a code bug. Code excision verified complete (`6d4f1d8`, zero `skeuo` refs in lib/). `neoSkeuo` was the LAST `AppThemeMode` member, so persisted mode indexes don't shift — a user persisted ON it falls out of bounds at `init()` and lands on `kVisibleThemes.first` (paperInk, dark — cannot look like neo-skeuo). What survives is **user data**: a preset the user saved while Neo-Skeuo was active lives in `CustomThemeStore` (`custom.themes.v1` SharedPreferences JSON). `SavedCustomTheme.name` is free-text and `baseMode` only clamps its index — so a gallery card literally named "Neo-Skeuo" persists forever by design. Fix on device: Customization → gallery → delete the preset (or overwrite it).
- **Severity:** Low (stale user data, expected persistence)
- **Status:** Closed — explained to user; no code change warranted. If it still shows as the ACTIVE theme label in Settings, that means a saved preset with `customData` carrying the neo-skeuo palette is applied — same fix: pick another preset/theme.

### U-058 — Settings/prefs menu is packed full
- **Reported:** 2026-11-25 — v3.8.0 APK user test
- **Root cause:** The in-run tools sheet (`_RunToolsSheet`) accreted to 14 rows / 5 groups (RUN/RESET/APP/DANGER + MP conditionals). The Settings screen itself was already tidy (status strip + collapsible RUN DISPLAY panels).
- **Severity:** Low-Medium (UX clutter)
- **Status:** Fixed — user supplied the keep-list (END RUN, PAUSE RUN, SHRINES, RESET P1/P2, DICE, QUIZ). Sheet now shows RUN (Shrines/Dice/Quiz + MP-gated Pause-Resume) → RESET → DANGER only; cut rows remain reachable elsewhere (Ammonomicon on main menu, MP actions in Paradox panel ⋮, app rows in Settings). Tests updated: `active_run_widgets_test` keep-list pin + `settings_screen_test` group labels.

### U-059 — Customization new-preset flow: APPLY doesn't save, name discarded on saved-source copy
- **Reported:** 2026-11-25 — v3.8.0 APK user test
- **Root cause:** Two compounding bugs in `experience_studio_screen.dart`: (1) the dashboard hero APPLY commits the look but never saves the preset — the only save path was the buried SAVE AS NEW card, which re-prompted for the name the user already typed at NEW PRESET, reading as "can't apply/save". (2) `_seedFromEntry`'s saved-preset branch overwrote `_presetName`/`_editingPresetId` with the SOURCE preset's identity — NEW PRESET "My Copy" → COPY EXISTING "Base Look" discarded "My Copy" and armed SAVE as an in-place overwrite of "Base Look".
- **Severity:** Medium-High (silent data-loss path on user presets)
- **Status:** Fixed — SAVE "<staged name>" card saves directly (name consumed after save, card reverts); `_seedFromEntry` no longer claims source identity (edit-pencil path unaffected — `_onEditPreset` pre-sets id/name); regression test pins typed-name survival + source untouched. 57 studio tests green.

### U-060 — Customization landing IA: no active-preset visibility, redundant stages, cryptic source choice
- **Reported:** 2026-11-25 — v3.8.0 APK user test ("first view sucks, another similar view, can't tell clone vs new")
- **Root cause:** The CHOOSE stage led with bare quick slots and two unlabeled doors; nothing showed which preset was actually live; the source stage offered "COPY EXISTING / START FROM SCRATCH" without saying which was "clone" vs "new".
- **Severity:** Medium (orientation, not data loss — U-059 covered the save bug)
- **Status:** Fixed — landing reordered per user spec: ACTIVE PRESET card (live `AppTheme.mode`, saved presets resolve by gallery name) → PRESETS → YOUR SLOTS (3 quick slots) → NEW PRESET. Source cards renamed CLONE EXISTING PRESET / START BLANK with explicit subtitles; quick-slot pill labels scale-to-fit instead of ellipsizing. Regression test pins the order.

## Resolved

### U-035 — Studio pills/tabs: type sizes below readable floor + touch targets under minimum
- **Reported:** 2026-11-25 — customization pills/tabs assessment (Slot 2 CORE)
- **Status:** Fixed in app `eb1ea7c` — tab pills 9→10.5px, glow-style labels 8→9px inside FittedBox, look-tile name/blurb 7.5/6.5→9/8px, font role tag 8→9px; glow color dots gained 30×40 hit areas (visual stays 26px). Regression tests in `experience_studio_test.dart`.

### U-036 — Studio pickers: zero semantics/screen-reader labels on non-text controls
- **Reported:** 2026-11-25 — same assessment
- **Status:** Fixed in app `eb1ea7c` — glow dots carry Tooltip + Semantics(button/selected/label), atmosphere meter dots labeled per-layer active/inactive, THIN STACK chip gets button semantics.

### U-037 — Studio chip recipe duplicated 7x with drifted params, mixed animation, uneven haptics/press feedback
- **Reported:** 2026-11-25 — same assessment
- **Status:** Fixed in app `eb1ea7c` — `_GlowFxChip`, `_ShaderChip`, `_PhysicsToggle`, `_HapticsChips` cells, `_GlowStyleRow` cells, `_SchemaChip` all delegate to one `_SelectChip` (shared 0.16/0.04 fill, 1.5/1.0 border, radius 10, 140ms AnimatedContainer, Semantics). Haptics verified at every call site; border-mode chip gap patched. Intentional variants (tiles, THIN STACK amber warning, tab strip) left as-is.

### U-044 — Huntress dashboard reads P1 inventory in co-op (slot ignored)
- **Reported:** 2026-11-25 — special-panels subsystem assessment (Slot 2 CORE)
- **Status:** Fixed in app `eb1ea7c` — `HuntressDashboardSliver` takes `PlayerSlot` and resolves `runState.coop` for P2. Robot trackers confirmed RunProvider-global by design. Regression test pins slot propagation.

### U-045 — `hasSpecialDashboards` hand-mirrors `buildDashboardTabs` + fragile name matching
- **Reported:** 2026-11-25 — same assessment
- **Status:** Fixed in app `eb1ea7c` — probe deleted entirely; `buildDashboardTabs` is the single source and the Settings SPECIAL PANELS toggle is unconditional. Character names verified against data ('The Hunter'/'The Robot').

### U-046 — Dashboard swiper state duplicated; nested double-collapse UX
- **Reported:** 2026-11-25 — same assessment
- **Status:** Fixed in app `eb1ea7c` — selection/collapse consolidated into stateful `DashboardSwiperCardBody` shared by sliver + embedded paths; `DashboardSwiper`/`DashboardSwiperCard` are thin stateless wrappers; Robot HUD's inner collapse removed (pill chevron is the single affordance). Widget test covers select/collapse.


### U-001 — 08_char_select.png is a white/blank screenshot
- **Reported:** 2026-08-25
- **Source:** Playwright screenshot session
- **Notes:** "08 png seems white page. maybe accident." — likely captured
  the moment the page navigated to `about:blank` during the service-worker
  redirect issue. Not a real app bug; the screenshot should be re-captured
  in a clean session.
- **Severity:** Low (cosmetic — screenshot only)
- **Status:** Closed (S3, 2026-11-23) — the named artifact no longer exists
  anywhere in either repo (it was an uncommitted Playwright session output).
  Its successor already landed: `gungeon_mate/design-lab/reference/
  ref-02-character-select.png` — captured 2026-10-31 in a clean
  `flutter build web` session at 390×844 per that folder's README. Verified
  non-blank: 42 KB PNG, mean luminance 18.2 (dark neon UI, not a white
  page). No re-capture needed — the underlying need (valid char-select
  reference shot) is already met.

### U-002 — White button labels hard to read on light-colored buttons
- **Reported:** 2026-08-25
- **Source:** User visual review of screenshots
- **Notes:** "btn's maybe a bit bright to see labels on when btn is lighter
  colored and font inside is white you know." — when a button uses a light
  fill color (e.g. light theme flair, yellow PLAY AS gradient, light accent
  cards), white text inside loses contrast. Affects: PLAY AS button
  (yellow gradient + dark text is OK, but other light buttons may not be),
  role cards in light themes, and any flair-driven button where the fill
  gets bright but the text stays white.
- **Severity:** TBD (needs audit across all themes/flairs)
- **Status:** Fixed in `0ab0f10` — `onSurface` text color is now derived from
  the surface luminance via `Contrast.luminance()` in `app_theme.dart:4167-4170`.
  Dark surfaces get off-white text; light surfaces get near-black text,
  preventing the white-on-light contrast bug across all themes/flairs.

### U-003 — Saved presets invisible after restart (REPORTED, code-verified OK on master)
- **Reported:** 2026-11-19 — "prefs not saving actually???? why the effi cant see the ones i crate later?"
- **Investigation:** `CustomThemeStore` save→persist→load round-trip verified green via `test/_preset_rt_test.dart` (save, wipe notifier, reload — preset survives). All enum deserializers clamped; per-item load resilience in place.
- **Likely cause:** user is on the installed v3.4.0-or-older APK which predates the save/load hardening — the old all-or-nothing `load()` wiped the gallery on any malformed entry. Fix already landed on master; verify on the v3.4.1 build.
- **Severity:** High (data-loss feeling)
- **Status:** Fixed on master — round-trip proven + pinned by `test/preset_store_test.dart` (app `e8a5c6e`). Was the pre-hardening APK wiping the gallery; verify on v3.4.1.

### U-004 — Special panels missing: Shellegun, Chamber Gun, Polaris, Triple Gun
- **Reported:** 2026-11-19 — "aalso cnt see special panels (ser junkan, gun soul, shellegun!!!!)"
- **Root cause (verified):** commit `3ef238a` deliberately cut these 4 tracker tabs per earlier user review ("they won't need those" — pure mode-switchers); commit `cd6ddcd` then deleted the dashboard widget classes entirely. Ser Junkan + Gun Soul tabs still exist in `buildDashboardTabs` — if those are also invisible, check `showDashboards` pref (Settings → Gameplay → PANELS) and whether items are actually in `player.items`.
- **Severity:** Medium
- **Status:** Fixed in app `a6f4336` — widgets resurrected from `cd6ddcd~1`, tabs + hasSpecialDashboards restored, `test/dashboard_tabs_test.dart` pins all 16 panels.

### U-005 — Gungeoneer picker/detail loadout view is wonky
- **Reported:** 2026-11-19 — "gungeoneer picker mode has wonky guns and items view and layout overall when seeing gungeoneers details"
- **Findings:** picker `_GungeoneerPage._loadout` guesses icons via `localGunIcon/localItemIcon` slug (never verifies asset exists, no quality ring, 'Random' → broken-image fallback); detail `_LoadoutPage` mixes guns+items+armor into ONE unlabeled Wrap (indistinguishable), resolves via provider but `showRing:false`/size 22 vs picker's ring/size 30 — the two views disagree visually.
- **Severity:** Low-Medium (UX polish)
- **Status:** Fixed in app `a6f4336` — detail LOADOUT split into labeled GUNS/ITEMS + armor; picker resolves via provider (quality rings, Random shuffle, dim+strikethrough on misses); both views now identical.

### U-006 — Applying a saved preset silently toggles IMMERSIVE wallpaper mode
- **Reported:** 2026-11-25 — found in Slot 4 QA/code-review pass over the customization + MP batch (`246ddfb..HEAD`)
- **Root cause:** `wallpaperImmersive` lives in `VisualPrefs` (app-level pref) but was serialized into every saved preset's `prefs.toJson()`. All three preset-restore sites (`_previewGalleryEntry`, `_applyEntry`, `_seedFromEntry` in `experience_studio_screen.dart`) swapped the whole snapshot, so applying/seeding/previewing a preset flipped the user's immersive toggle to whatever it was when the preset was saved.
- **Severity:** Medium (silent app-wide setting change; contradicts the in-code "app-level pref, not part of the theme draft" contract)
- **Status:** Fixed (uncommitted, QA pass) — new `VisualPrefs.preserveAppLevel()` wraps all three restore sites; `wallpaperImmersive` removed from preset `toJson`; `custom_wallpaper_test.dart` updated to pin the new contract.

### U-007 — Avatar idle animation burns vsync under reduced-motion
- **Reported:** 2026-11-25 — found in Slot 4 QA/code-review pass
- **Root cause:** `_AvatarIdle` (avatar_frame.dart) started its 4s `AnimationController.repeat()` unconditionally; `build` returned the static child under `MediaQuery.disableAnimationsOf`, but the controller kept ticking every frame for every idle avatar (lobby, player panel, MP portraits).
- **Severity:** Low (battery/perf; no visual defect)
- **Status:** Fixed (uncommitted, QA pass) — controller now starts/stops via `didChangeDependencies` on the reduced-motion flag.

### U-008 — Multi-word Google Fonts silently fall back to default typeface
- **Reported:** 2026-11-25 — found during google_fonts 6→9 upgrade assessment
- **Root cause:** `app_theme.dart` built the bundled family as `'GoogleFonts.${selectedFont.label}'` where `label` keeps spaces ('DM Sans', 'Press Start 2P', 'JetBrains Mono'…). Pubspec declares the space-stripped names ('GoogleFonts.DMSans', 'GoogleFonts.PressStart2P'…). ~14 of 29 pickable fonts never matched a declared family → silent fallback to system font. Same class of bug in `AppFont.textStyle`/`textTheme` (used `GoogleFonts.getFont`/`getTextTheme`, which return runtime-fetch family names that also don't match bundled assets — the v6 code comment already documented this failure mode).
- **Severity:** Medium (wrong typeface for roughly half the font picker, offline AND online)
- **Status:** Fixed (uncommitted) — new `AppFont.bundledFontFamily` getter is the single source of truth (`label.replaceAll(' ', '')` for Google fonts); `app_theme.dart`, `textStyle`, `textTheme`, studio TYPE header, and the Neo-Skeuo clean theme all route through it. google_fonts v9 `TextTheme` type incompatibility resolved by dropping the package calls entirely.

### U-009 — Co-op "active synergy" counted pieces split across both players
- **Reported:** 2026-11-20 — synergy/LEB correctness audit (Slot 4, Gemini-verified game mechanics)
- **Root cause:** `RunProvider.getActiveSynergiesCombined()`, the gun-detail ALL pager page, and `ItemDetailScreen` all computed `active` against `runState.allItemNames` — the UNION of P1+P2 inventories. Enter the Gungeon evaluates synergies strictly per `PlayerController` (no cross-player union), so a synergy whose pieces were split across the two players displayed COMPLETE / counted in run stats while never actually triggering in-game.
- **Severity:** High (actively misleading co-op status + synergy-count stats)
- **Status:** Fixed (uncommitted) — combined query now counts a synergy only when ONE player's own inventory satisfies it; ALL page and item detail pass per-player `active` while keeping combined inventory for missing-piece display. `test/coop_synergy_per_player_test.dart` pins the semantics (4 tests).

### U-010 — LEB simulated view listed game-excluded synergies
- **Reported:** 2026-11-20 — same audit
- **Root cause:** the LEB ghost page rendered every synergy containing the viewed gun, including entries the game flags `IgnoreLichEyeBullets` (verified: Rubenstein's Monster — prevents instant floor-1 RUBE-ADY fusion).
- **Severity:** Low-Medium (simulated view over-promised)
- **Status:** Fixed (uncommitted) — `kLebExcludedSynergies` filter + `_LebBlockedNote` footnote naming excluded synergies.

### U-011 — `any_of` synergy data can't express multi-pick optional pools
- **Reported:** 2026-11-20 — same audit
- **Root cause:** game requirements are mandatory lists + optional pools gated by `NumberObjectsRequired`; our JSON only models "all items + ≥1 anyOf". Known-wrong entries: `360 Yes Scope` (anchor/pool inverted — misses the scope/accuracy pool), `Smart Bombs`, `Unbelievably Charming`, `Tea for Two` (incomplete pools). Also `Resourceful Indeed,` trailing-comma name typo.
- **Severity:** High (data correctness — wrong active/missing states)
- **Status:** Fixed — new `groups` field (AND-of-OR pools) on `Synergy`; `Smart Bombs` = (Bomb|Ice Bomb)+(Crutch|Homing Bullets), `Unbelievably Charming` = (Charmed Bow|Shotgun Full of Love)+(Charming Rounds|Pink Guon Stone), `Super Serum` = (Plague Pistol|Plunger)+(Gas Mask|Hazmat Suit); `Tea for Two` pool expanded to all 12 valid companions (Dog/Turtle Problem excluded per wiki); `Resourceful Indeed,` renamed (fixes broken item cross-links). `360 Yes Scope` verified CORRECT as-is (Scope + A.W.P./Sniper Rifle — audit's "inverted" claim was wrong). Name-based hardcodes in `matchesOwnedSet` removed. Tests: `synergy_logic_test.dart` groups coverage.

### U-015 — `items.json` id collision: `Junk` claims id 580 (dump: SackKnightBoon companion)
- **Reported:** 2026-11-25 — dump cross-validation pass (Slot 4)
- **Root cause:** our `Junk` passive ("often spawned by destroying chests") carries `id: 580`, but the game dump resolves 580 to `SackKnightBoon` (CompanionItem). Either Junk's id is wrong or two objects share the slot. `Ser Junkan 1` has `id: null` — the real Ser Junkan id is unset.
- **Severity:** Low — no synergy references Junk by id; only affects game_ids joins/provenance.
- **Status:** Verified closed (S3, 2026-11-23) — fixed in `7f629dd` (Junk→127, Ser Junkan 1→580). App-wide id-uniqueness invariant now enforced by `test/entity_id_integrity_test.dart` covering BOTH `guns.json` and `items.json` (the only files carrying `id`); guns-only guard was `gun_id_integrity_test` before S3.1 generalized it. Both files currently have zero duplicate non-null ids.

### U-012 — `assets/images/game/` is ~97% bundled dead weight
- **Reported:** 2026-11-25 — full asset inventory pass (Slot 4)
- **Root cause:** 614 raw game PNGs (237 guns, 262 items, 103 enemies, 12 bosses) ship in the APK, but code references only 13 gun sprites — 12 in `home_backdrop.dart` `driftGuns` (menu flock) + 1 in `neo_skeuo_lab_screen.dart`. The rest are never loaded.
- **Severity:** Low (≈900 KB APK weight; no user-facing defect)
- **Status:** Fixed — `edf7b77` removed all 602 unreferenced `images/game/` PNGs (bosses/enemies/items dirs deleted entirely, 225 dead guns culled); the 12 live icons kept; pubspec asset dirs trimmed to `guns/` only.

### U-013 — 12 theme splash slugs point at missing artwork
- **Reported:** 2026-11-25 — asset inventory pass
- **Root cause:** `AppThemeMode.splashSlug` maps 26 themes but `assets/images/themes/splash/` only has 14 JPGs. Missing: `the_cultist`, `the_gunslinger`, `the_convict`, `the_hunter`, `the_pilot`, `the_rat`, `the_breach`, `lead_lord_keep`, `the_oubliette`, `black_powder_mine`, `bullet_hell`, `rg_department`. `themeSplashPath()` still returns a path → studio theme panel silently shows gradient fallback.
- **Severity:** Low (cosmetic inconsistency in studio/gallery previews)
- **Status:** Fixed — all 12 missing slugs now have dedicated 1200×1200 sigil splash JPGs generated procedurally (palette-matched emblem + motif per theme, name set in its curated font; real painted art can replace the files later without code changes). Generator script kept at `tools/gen_sigil_splashes.py`. Splash-integrity tests assert every advertised `splashSlug` resolves to a file on disk and vice versa (no orphans). Ambience-mud guard shipped alongside: `VisualPrefs.ambienceLoad` counts heavy backdrop layers, studio shows an ATMOSPHERE LOAD meter with a THIN STACK escape hatch at BUSY+, and the overlay drops the disposable foreground dust field at max load.

### U-014 — Wallpaper set is 40% of image payload (12 MB / 46 files)
- **Reported:** 2026-11-25 — asset inventory pass
- **Root cause:** `assets/images/wallpapers/custom/wp_01–46.webp` average ~270 KB each — full-res sources kept as-is. Already on the deferred list as "wallpaper re-encode pipeline" (normalize ≥1200px, consistent crop).
- **Severity:** Low (APK/download size only)
- **Status:** Fixed — app `8e30e5b` (on top of Slot 4's `968fe55`): all 46 webp normalized to ≤1600px side + q75 re-encode; set went 12.1→10.1→**7.0 MB** (-42% total). Wallpapers sit under a ~62% scrim so q75 is visually safe. Reproducible via `tools/reencode_wallpapers.py`.

### U-016 — Run-tools sheet could overflow short viewports
- **Reported:** 2026-11-25 — CORE self-bughunt (Slot 2) after Settings IA ship
- **Root cause:** `_RunToolsSheet` body was a fixed `Column(mainAxisSize: min)`; the WP-1 additions (Add/Remove Co-op, Save Run, Leave MP) pushed row count to ~14 — overflow risk on short screens / large text scale.
- **Severity:** Medium (layout crash on small devices)
- **Status:** Fixed — app `c8aadb8`, sheet body wrapped in `SingleChildScrollView`.

### U-017 — Neo-Skeuo chrome whites invisible on paper (quiz/stats/Cool & Curse)
- **Reported:** 2026-11-25 — CORE self-bughunt (Slot 2), WP-5 follow-up
- **Root cause:** WP-5 wrapped semantic accents in `Skeuo.inkIf` but left raw `Colors.white*` chrome (card borders, fills, dim states, slider track/thumb) in `quiz_session_screen`, `quiz_home_screen`, `stats_detail_screen`, `cool_curse_screen`. On cream paper these render invisible; the inactive quiz streak also lost its dim-vs-active distinction (GoopText collapsed both states to full ink).
- **Severity:** Low-Medium (cosmetic — Neo-Skeuo only)
- **Status:** Fixed — app `c8aadb8`, all white chrome routed through `Skeuo.collapse` (alpha-preserving pencil washes / dim ink; no-op outside the skin).

### U-018 — Stats slider value bubble black-on-ink under Neo-Skeuo
- **Reported:** 2026-11-25 — CORE self-bughunt (Slot 2)
- **Root cause:** `valueIndicatorColor` follows the ink-collapsed stat color (ink under Neo-Skeuo) while `valueIndicatorTextStyle` stayed `Colors.black` — unreadable label.
- **Severity:** Low (Neo-Skeuo only, transient drag label)
- **Status:** Fixed — app `c8aadb8`, label flips to `Skeuo.paper` when `AppTheme.isSkeuo`.


### U-019 — Artless synergies showed generic hub icon despite piece-icon fallback
- **Reported:** 2026-11-25 — synergy verification pass
- **Root cause:** `localSynergyIcon()` returned an asset path unconditionally, so `iconPath.isEmpty` was never true and the first-component-icon fallback in `gun_synergies_tab`/`entity_synergies_view` was dead code. ~290 of 395 synergies (only 108 have dedicated webp art) rendered `Icons.hub_outlined`.
- **Severity:** Low (cosmetic)
- **Status:** Fixed — app `236778c`, `localSynergyIcon` now gated by `kSynergyIconSlugs`; integrity test pins the set to the directory.

### U-020 — LEB view ignored real LEB ownership; ghost list over-promised
- **Reported:** 2026-11-25 — synergy/LEB re-audit
- **Root cause (a):** `ItemDetailScreen` forced `lebView = false` whenever `ownerSlot != null`, so in-run detail never showed the simulation even when the player actually held Lich's Eye Bullets; nothing auto-enabled the pref on acquisition either.
- **Root cause (b):** the LEB ghost list only excluded 3 named synergies — all 11 other pure dual-wield synergies (Blammo!, Assault and Battery, etc.) were shown as simulable though the game can't dual-wield under LEB, and the five 3+-component synergies (Behold!, Cormorant, In The Mood!, Mmmmmmmmm MMMMmm!, Resourceful Indeed) were shown as LEB-only though LEB counts as just one component there.
- **Severity:** Medium (incorrect game-mechanics display)
- **Status:** Fixed — run-context detail now resolves `playerHasLeb(slot) && pref`; `_autoEnableLebViewsIfHeld` flips both LEB prefs on once per acquisition (starter/pickup/coop/snapshot/reset) with a latch that respects manual toggle-off; `isLebExcludedSynergy` covers all dual-wield except Trigger Twins; `lebNeedsRealPieces` routes 3+-piece synergies to a needs-real-items note. Tests: `leb_auto_enable_test.dart` (11).

### U-021 — Synergy data holes vs game dump (15 entries) + dead `activation` field
- **Reported:** 2026-11-25 — third synergy audit pass (dump + wiki + JP loc strings)
- **Root causes:**
  - Smart Bombs lost its `groups`/Ice Bomb arm in the `9e48e86` pool pass (regression).
  - Deadly/Frosty Distraction used `Explosive Decoy` — that's Deadlier/Frostier; Deadly/Frosty pair with plain `Decoy` (dump items 71 vs 438).
  - `Blade Runner` was an exact duplicate of `Running Blades`; the real `#BLADERUNNER` (Deck4rd + Origuni) was missing.
  - `In The Mood!`, `Chief Master`, `Synthetic Shield`, `The Void Corps` encode "pick N of M" requirements the schema couldn't express — all were effectively all-of or wrong-pair.
  - `The Elephant in the Room` pool truncated (missing Chicken Flute, Super Space Turtle, Compressed Air Tank, Bait Launcher).
  - `Grouch`, `Klobbering Time`, `Brave New World` lacked `game_name_key`; `Fairy Bow` was marked INACTIVE though dump `#ZELDA` has a live `ACTIVE_UNBOOSTED` entry; `activation` was never parsed anyway.
  - `Junk`/`Ser Junkan 1` item ids collided with dump ids 127/580 (U-015 resolved).
- **Severity:** High (wrong activation results + wrong displayed requirements)
- **Status:** Fixed — `any_of_min` + `activation` schema fields added; 15 synergies corrected; query layer filters `INACTIVE`; LEB slot math counts K-of-N picks. Tests: `synergy_logic_test` +8, `leb_auto_enable_test` updated.

### U-022 — Dice roll dialog header overflows 76px on the right
- **Reported:** 2026-11-23 — found by new S2.5 widget test (`DiceRollDialog renders as dialog`)
- **Root cause:** header `Row` (dice_roll.dart) had no `Flexible` — the "GUNFORTUNA'S DUEL" title + action icons could exceed the 440px dialog on wide fonts/narrow screens.
- **Severity:** Low-Medium (visual overflow in a user-facing dialog)
- **Status:** Fixed in app `46230c4` — title wrapped in `Flexible` + `maxLines:1`/`ellipsis`.

### U-023 — FramedAvatar crashes when avatar asset fails to load
- **Reported:** 2026-11-23 — found by new S2.6 widget test (`ParadoxPlayerPanel renders`)
- **Root cause:** `avatar_frame.dart` errorBuilder used `size * 0.6` — callers pass `size: double.infinity`, producing an infinite Icon fontSize (`fontSize.isFinite` assertion) whenever the avatar asset 404s.
- **Severity:** Medium (crash on missing/corrupt avatar asset)
- **Status:** Fixed in app `451cf80` — errorBuilder falls back to `(w ?? 40) * 0.6`.

### U-024 — Active saved preset couldn't be edited; SAVE created duplicates
- **Reported:** 2026-11-23 — user: "still cant edit current preset in use"
- **Root cause:** `_detectSavedPreset()` only matched session-flow state (`_presetName`/`_editingPresetId`), which is empty when the studio opens fresh on an already-applied preset — no EDIT PRESET card, and SAVE minted a same-name duplicate instead of updating.
- **Severity:** High (core customization loop broken — couldn't tweak the live preset)
- **Status:** Fixed in app `fa25ef8` (+merge `f39dcc9`) — detection falls back to the live `CustomThemeData.name` (saved presets persist their name app-wide); theme panel shows preset name + SAVED PRESET badge; SAVE tab offers UPDATE PRESET; `_onSavePreset` resolves the same target so edits overwrite the existing preset id. Tests: `experience_studio_test.dart` "Active preset editing" group (3).

### U-026 — RESET DATA never restarts, leaves stale in-memory state, strands user on char select
- **Reported:** 2026-11-25 — settings/prefs audit (Slot 3)
- **Root cause:** `_confirmResetAppData` did `prefs.clear()` then `pushAndRemoveUntil(CharacterSelectScreen)` — no restart, stale `VisualPrefs`/`RunProvider`/`MpSession` in-memory state, and char select became the only route so the run couldn't be entered.
- **Severity:** Critical
- **Status:** Fixed in app `1748b80` — new `AppDataReset` service: MP teardown → in-memory defaults across RunProvider/VisualPrefs/AppTheme/CustomThemeStore/CodexPrefs/ColorFavorites/Haptics/HomeCustomization → `prefs.clear()` → rehydrate; lands on the existing Home route. Regression test in `settings_screen_test.dart`.

### U-027 — Settings "Dev Tools" tile is a dead end without an active run
- **Reported:** 2026-11-25 — settings/prefs audit (Slot 3)
- **Root cause:** DEV TOOLS card offered `SpecialItemsGridScreen` with no run — a snackbar dead end.
- **Severity:** Low
- **Status:** Fixed in app `1748b80` — DEV TOOLS section only renders while `hasRun`; the grid is retitled "Special Items & Guns" and is responsive. Widget tests pin both states.

### U-031 — Run-tools sheet bottom is an unlabeled grab-bag between RESET and End Run
- **Reported:** 2026-11-25 — multi-view composition audit (Slot 3)
- **Root cause:** Customization/Quiz/Report a Bug/Settings sat unlabeled after RESET; End Run had no DANGER label.
- **Severity:** Low
- **Status:** Fixed in app `1748b80` — every action row gained a subtitle; groups are now RUN → RESET → APP → DANGER. Widget test pins labels + order.

### U-025 — ItemDetailHeader top row overflows ~47px at ≤~390px width
- **Reported:** 2026-11-25 — found by new char-select widget test tapping a starting item at 400px viewport
- **Root cause:** `item_detail/header.dart` spaceBetween Row packed QualityBadge + SellBadge + ACTIVE/PASSIVE chip against CodexFavButton + BugReportButton + favourite IconButton.
- **Severity:** Medium
- **Status:** Fixed in app `921399d` — badge cluster wrapped in `Flexible` + `FittedBox(scaleDown)` on both gun and item variants; 360px regression test added (`item_detail_sections_test`).

### U-028 — Duplicate switch arm in `AppFontLabel.migrate` (dead code + analyzer warning)
- **Reported:** 2026-11-23 — S5.1′ post-excision audit (Slot 2 CORE)
- **Root cause:** `app_theme_modes.dart` ~line 2139 — `shantellSans || architectsDaughter || patrickHand => fjallaOne` appeared twice; second arm unreachable.
- **Severity:** Trivial
- **Status:** Fixed in app `921399d` — duplicate arm deleted; `flutter analyze` now reports 0 issues project-wide.

### U-029 — LEB ghost-row "marching ants" ticker ignores reduced-motion
- **Reported:** 2026-11-23 — S5.2 ticker/reduced-motion audit (Slot 2 CORE)
- **Root cause:** `_LebPageState._march` `AnimationController.repeat()` unconditional.
- **Severity:** Low
- **Status:** Fixed in app `921399d` — `didChangeDependencies` gates on `ReduceMotion.of(context)`; stops under disableAnimations, restarts when cleared.

### U-030 — Ammonomicon carries 12 flat categories; world-object cats blur into inventory cats
- **Reported:** 2026-11-25 — multi-view composition audit (Slot 3)
- **Root cause:** 12 categories in one flat strip; Pickups/Objects (world) vs Guns/Items (inventory) visually indistinguishable.
- **Severity:** Low
- **Status:** Fixed in app `921399d` — `AmmonomiconTab.group` field + eyebrows LIVING WORLD / ARMORY / CODEX / STRUCTURE in overview grid and jump strip. Indices/section mapping unchanged (display-only).

### U-032 — Browse Robot-tier badges classify items by fragile name substrings
- **Reported:** 2026-11-25 — multi-view composition audit (Slot 3)
- **Root cause:** `BrowseRow` hardcoded `contains` lists for GOD TIER / CONVERTS TO ARMOR / DEAD WEIGHT.
- **Severity:** Low
- **Status:** Fixed in app `921399d` — lists centralized into `_RobotTier` const map (single source). Explicit `robot_tier` data field remains a possible future data-pass improvement.

### U-033 — ItemDetailHeader shows two competing "favorite" systems + crowded action cluster
- **Reported:** 2026-11-25 — item/gun detail top-panel review (Slot 3)
- **Root cause:** `item_detail/header.dart` top-right cluster rendered `CodexFavButton` (Ammonomicon bookmark, `CodexPrefs`) AND a heart `IconButton` (`RunProvider.isFavourite`) AND `BugReportButton.iconButton` — three icons where two are both "favorites" doing different things.
- **Severity:** Low-Medium (UX confusion + overflow contributor)
- **Status:** Fixed in app `11b78e7` — cluster collapsed into a single `_DetailActionsMenu` overflow menu with explicit labels (Save to Codex Favorites / Add to Favourites / Report a Bug); state shown via filled icons. Both fav systems preserved, now self-describing.

### U-034 — Gun vs item detail header hierarchy is inverted
- **Reported:** 2026-11-25 — item/gun detail top-panel review (Slot 3)
- **Root cause:** item path rendered badge row → ICON → name → tags; gun path badge row → NAME → icon → effect.
- **Severity:** Low (visual consistency)
- **Status:** Fixed in app `11b78e7` — item variant reordered to name-first (badge row → name → icon → tags), matching the gun variant; corrected the copy-pasted `_TagChip` doc comment. (The reported `â€"` mojibake was a console-encoding artifact — file comments are clean UTF-8 em-dashes.)

