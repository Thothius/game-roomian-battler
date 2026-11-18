# User-Reported Bug List

> **Codeword: `bug list`** — say "bug list" and I'll append your notes here.
> Items are not acted on unless explicitly requested. Severity is user-assigned
> or TBD. Status tracks from report → triaged → fixed.

---

## Open

### U-003 — Saved presets invisible after restart (REPORTED, code-verified OK on master)
- **Reported:** 2026-11-19 — "prefs not saving actually???? why the effi cant see the ones i crate later?"
- **Investigation:** `CustomThemeStore` save→persist→load round-trip verified green via `test/_preset_rt_test.dart` (save, wipe notifier, reload — preset survives). All enum deserializers clamped; per-item load resilience in place.
- **Likely cause:** user is on the installed v3.4.0-or-older APK which predates the save/load hardening — the old all-or-nothing `load()` wiped the gallery on any malformed entry. Fix already landed on master; verify on the v3.4.1 build.
- **Severity:** High (data-loss feeling)
- **Status:** Triaged — pending verification on v3.4.1 APK. If still repros there, need device-side SharedPreferences dump.

### U-004 — Special panels missing: Shellegun, Chamber Gun, Polaris, Triple Gun
- **Reported:** 2026-11-19 — "aalso cnt see special panels (ser junkan, gun soul, shellegun!!!!)"
- **Root cause (verified):** commit `3ef238a` deliberately cut these 4 tracker tabs per earlier user review ("they won't need those" — pure mode-switchers); commit `cd6ddcd` then deleted the dashboard widget classes entirely. Ser Junkan + Gun Soul tabs still exist in `buildDashboardTabs` — if those are also invisible, check `showDashboards` pref (Settings → Gameplay → PANELS) and whether items are actually in `player.items`.
- **Severity:** Medium
- **Status:** Reported — user now wants them BACK (restore from git history `3ef238a~1` / `cd6ddcd~1`).

### U-005 — Gungeoneer picker/detail loadout view is wonky
- **Reported:** 2026-11-19 — "gungeoneer picker mode has wonky guns and items view and layout overall when seeing gungeoneers details"
- **Findings:** picker `_GungeoneerPage._loadout` guesses icons via `localGunIcon/localItemIcon` slug (never verifies asset exists, no quality ring, 'Random' → broken-image fallback); detail `_LoadoutPage` mixes guns+items+armor into ONE unlabeled Wrap (indistinguishable), resolves via provider but `showRing:false`/size 22 vs picker's ring/size 30 — the two views disagree visually.
- **Severity:** Low-Medium (UX polish)
- **Status:** Reported — fix plan: unify both to labeled GUNS/ITEMS(/ARMOR) sections, provider-resolved icons + quality rings, 'Random' shuffle glyph.

### U-001 — 08_char_select.png is a white/blank screenshot
- **Reported:** 2026-08-25
- **Source:** Playwright screenshot session
- **Notes:** "08 png seems white page. maybe accident." — likely captured
  the moment the page navigated to `about:blank` during the service-worker
  redirect issue. Not a real app bug; the screenshot should be re-captured
  in a clean session.
- **Severity:** Low (cosmetic — screenshot only)
- **Status:** Reported

---

## Resolved

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
