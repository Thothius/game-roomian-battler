# Language Selection & Goopianization Plan

## Status: Research Complete — Ready for Implementation

---

## 1. Current State

### What Already Exists
- **`GoopTalkEngine`** (`lib/services/goop_talk_engine.dart`, 173 lines) — cipher mapping English → alien symbols, plus `GoopText` StatefulWidget
- **`GoopText`** — animated widget that interpolates between English and Goopian character-by-character based on `VisualPrefs.isGoopianLanguage` + `VisualPrefs.spongeActive`
- **`VisualPrefs`** — already has `isGoopianLanguage` (bool, persisted as `vp.goopian_language_v1`) and `spongeActive` (bool, persisted as `vp.sponge_active_v1`) with setters
- **Sponge button** — already implemented in `active_run_screen.dart:1556-1591` inside `GungeoneerHeader` trailing row. Shows 🧽 emoji, only visible when `isGoopianLanguage == true`. Tapping toggles `spongeActive` which triggers GoopText to animate from Goopian → English after 1s delay.
- **GoopText adoption** — already used in: `main_menu_screen.dart` (title, subtitle, buttons, changelog), `synergies_overview_screen.dart`, `shrine_picker_screen.dart`, `theme_picker_screen.dart`, `multiplayer_lobby_screen.dart`, `periodic_tile.dart`, `item_detail_screen.dart` (header)

### What's Missing
- **No language selector on home/main menu screen** — the toggle exists in `VisualPrefs` but there's no UI to set it. Users have no way to switch languages from the home screen.
- **~796 `Text()` widgets** across screens/widgets that are NOT `GoopText` — these won't Goopianize when the language is set to Goopian. Breakdown:
  - `active_run_screen.dart`: 310 Text widgets (many are labels, stats, button text)
  - `item_detail_screen.dart`: 105 Text widgets
  - `settings_screen.dart`: 63 Text widgets
  - `multiplayer_lobby_screen.dart`: 52 Text widgets
  - `stats_detail_screen.dart`: 46 Text widgets
  - `shrine_picker_screen.dart`: 26 Text widgets
  - `browse_screen.dart`: 21 Text widgets
  - `main_menu_screen.dart`: 19 Text widgets (version label, changelog button, some still plain Text)
  - `theme_picker_screen.dart`: 17 Text widgets
  - `effects_summary_screen.dart`: 12 Text widgets
  - `synergies_overview_screen.dart`: 11 Text widgets
  - `favourites_screen.dart`: 10 Text widgets
  - `codex_detail_screen.dart`: 9 Text widgets
  - `character_select_screen.dart`: 7 Text widgets
  - `codex_screen.dart`: 3 Text widgets
  - `home_screen.dart`: 2 Text widgets
  - Widgets: 83 Text widgets across 10 files
- **Animation polish** — current 600ms duration with `Curves.easeInOutCubic` is decent but could be smoother. The 1s sponge delay is a hard timer, no fade-in on the sponge glow.

---

## 2. Goals

1. **Language selector on home screen** — a visible English/Goopian toggle on the main menu
2. **Full Goopianization** — convert all user-facing `Text()` → `GoopText()` so switching to Goopian transforms the entire app
3. **Sponge icon on active run dash** — already exists, verify it's working and polish
4. **Smoother transitions** — polish the GoopText animation curve, sponge activation glow, and language switch transition

---

## 3. Proposed Design

### A. Language Selector on Main Menu

**Location:** Below the version number, above the changelog button — a compact pill toggle.

```
┌─────────────────────────────────────┐
│         GUNGEON MATE                │
│    YOUR COMPANION IN THE GUNGEON    │
│                                     │
│         [Tailor mascot]             │
│                                     │
│    [▶ Local Run]                    │
│    [🔗 Multiplayer]                 │
│                                     │
│         v1.6.7                      │
│                                     │
│    ┌──────────────────┐             │
│    │ 🌐 English │ ⏃⎎⎓⏁ │             │  ← Language toggle pill
│    └──────────────────┘             │
│                                     │
│    [📜 Changelog (v1.6.7)]          │
└─────────────────────────────────────┘
```

**Widget:** A `ScaleButton` wrapping a segmented-control style pill:
- Left segment: "🌐 English" (active when `isGoopianLanguage == false`)
- Right segment: "⏃⎎⎓⏁" (Goopian for "Goopian", active when `isGoopianLanguage == true`)
- Tapping toggles `VisualPrefs.setIsGoopianLanguage(!current)`
- Active segment has a filled background, inactive is outline
- `Haptics.selection()` on tap
- The Goopian label itself is always shown in Goopian symbols (it's the word "Goopian" translated)

**Alternative:** A simple `Switch` with a label — less visual flair but simpler. The pill toggle matches the Gungeon aesthetic better.

### B. GoopText Conversion Strategy

**The scope is large (~796 Text widgets).** A phased approach:

| Phase | Files | Text count | Priority |
|-------|-------|-----------|----------|
| **Phase 1** | `main_menu_screen.dart` | 19 | P0 — home screen is first thing users see |
| **Phase 2** | `character_select_screen.dart`, `home_screen.dart` | 9 | P0 — character select is second screen |
| **Phase 3** | `active_run_screen.dart` | 310 | P1 — most Text widgets, main gameplay screen |
| **Phase 4** | `item_detail_screen.dart`, `browse_screen.dart` | 126 | P1 — browse/detail are core Ammonomicon |
| **Phase 5** | `settings_screen.dart`, `stats_detail_screen.dart` | 109 | P2 — settings/stats |
| **Phase 6** | `multiplayer_lobby_screen.dart`, `shrine_picker_screen.dart` | 78 | P2 — secondary screens |
| **Phase 7** | `theme_picker_screen.dart`, `effects_summary_screen.dart`, `synergies_overview_screen.dart`, `favourites_screen.dart`, `codex_detail_screen.dart`, `codex_screen.dart` | 62 | P3 — tertiary screens |
| **Phase 8** | All widget files (83 Text widgets across 10 files) | 83 | P3 — widgets used across screens |

**Conversion rules:**
- `Text('...')` → `GoopText('...')` — straightforward replacement
- `const Text('...')` → `const GoopText('...')` — preserve const where possible
- Skip `Text` widgets that are:
  - Numeric-only (e.g., `Text('${gun.dps}')`) — numbers don't Goopianize
  - Inside `Tooltip` or `Semantics` labels — accessibility should stay English
  - Debug/diagnostic text that's only visible in dev mode
- For `Text.rich()` with `TextSpan` children — convert to `GoopText` if the entire text is a simple string, leave as-is if it has complex spans (mixed styles, tappable links)

**Script approach:** A regex-based find-and-replace script could handle the bulk conversion, but manual review is needed for:
- `Text.rich()` cases
- `Text()` inside `Tooltip()`
- Numeric-only strings
- Cases where `const` can/can't be preserved

### C. Sponge Button Verification & Polish

**Current state:** The sponge button at `active_run_screen.dart:1556-1591` is already wired correctly:
- Only shows when `isGoopianLanguage == true`
- Tapping toggles `spongeActive`
- When `spongeActive == true`: GoopText shows Goopian for 1s, then animates to English
- When `spongeActive == false`: GoopText stays Goopian
- Visual feedback: amber glow shadow on the 🧽 emoji when active

**Polish opportunities:**
1. **Sponge glow animation** — currently a static shadow. Add a pulsing `AnimationController` that animates the glow intensity when sponge is active (like the S-tier QualityBadge glow).
2. **Sponge activation haptic** — currently `Haptics.heavy()`. Consider `Haptics.success()` for activation and `Haptics.light()` for deactivation for more nuanced feedback.
3. **Tooltip Goopianization** — the tooltip text (`'Sponge: English translation active'`) is a plain `Text`. Convert to `GoopText` for consistency.
4. **Sponge icon size** — currently 18px emoji. Consider 20px for better visibility.

### D. GoopText Animation Polish

**Current animation:** 600ms `Curves.easeInOutCubic`, character-by-character splice.

**Improvements:**
1. **Curve change** — `Curves.easeInOutCubic` → `Curves.easeOutExpo` for a more dramatic deceleration at the end (feels more "alien magic")
2. **Duration** — 600ms → 500ms (snappier, less waiting)
3. **Sponge delay** — 1000ms → 800ms (slightly faster translation kick-in)
4. **Per-character stagger** — instead of a simple threshold splice, animate each character with a tiny stagger (left-to-right wave effect). This would require changing the `AnimatedBuilder` to use a custom `Text` painter or a `Wrap` of per-character `GoopText` widgets. **This is complex and may not be worth the effort** — the current splice is already visually effective.
5. **Language switch transition** — when toggling language on the main menu, all GoopText widgets on screen should animate simultaneously. Currently they do (via `VisualPrefs.notifier` listener), but the main menu itself might need a `ValueListenableBuilder` to rebuild with the new toggle state.

---

## 4. File Changes

| File | Change | Est. Effort |
|------|--------|-------------|
| `lib/screens/main_menu_screen.dart` | Add language toggle pill widget, convert remaining Text → GoopText | 1 hr |
| `lib/services/goop_talk_engine.dart` | Animation polish (curve, duration, sponge delay) | 30 min |
| `lib/screens/active_run_screen.dart` | Sponge button polish (pulsing glow), convert 310 Text → GoopText | 3-4 hr |
| `lib/screens/item_detail_screen.dart` | Convert 105 Text → GoopText | 1.5 hr |
| `lib/screens/settings_screen.dart` | Convert 63 Text → GoopText | 1 hr |
| `lib/screens/multiplayer_lobby_screen.dart` | Convert 52 Text → GoopText | 45 min |
| `lib/screens/stats_detail_screen.dart` | Convert 46 Text → GoopText | 45 min |
| `lib/screens/shrine_picker_screen.dart` | Convert 26 Text → GoopText | 30 min |
| `lib/screens/browse_screen.dart` | Convert 21 Text → GoopText | 30 min |
| `lib/screens/theme_picker_screen.dart` | Convert 17 Text → GoopText | 20 min |
| `lib/screens/effects_summary_screen.dart` | Convert 12 Text → GoopText | 15 min |
| `lib/screens/synergies_overview_screen.dart` | Convert 11 Text → GoopText | 15 min |
| `lib/screens/favourites_screen.dart` | Convert 10 Text → GoopText | 15 min |
| `lib/screens/codex_detail_screen.dart` | Convert 9 Text → GoopText | 15 min |
| `lib/screens/character_select_screen.dart` | Convert 7 Text → GoopText | 10 min |
| `lib/screens/codex_screen.dart` | Convert 3 Text → GoopText | 5 min |
| `lib/screens/home_screen.dart` | Convert 2 Text → GoopText | 5 min |
| `lib/widgets/*.dart` (10 files) | Convert 83 Text → GoopText | 1.5 hr |
| **Total** | | **~12-14 hr** |

### No new files or dependencies needed
- `GoopText` and `GoopTalkEngine` already exist
- `VisualPrefs` already has the language prefs
- Sponge button already wired

---

## 5. Implementation Phases

| Phase | Task | Effort | Priority |
|-------|------|--------|----------|
| **Phase 1** | Add language toggle pill to main menu + convert main_menu Text → GoopText | 1 hr | P0 |
| **Phase 2** | Polish GoopText animation (curve, duration, sponge delay) | 30 min | P0 |
| **Phase 3** | Polish sponge button (pulsing glow, haptic nuance) | 30 min | P1 |
| **Phase 4** | Convert character_select + home_screen Text → GoopText | 15 min | P0 |
| **Phase 5** | Convert active_run_screen Text → GoopText (310 widgets — biggest batch) | 3-4 hr | P1 |
| **Phase 6** | Convert item_detail + browse_screen Text → GoopText | 2 hr | P1 |
| **Phase 7** | Convert settings + stats_detail Text → GoopText | 1.5 hr | P2 |
| **Phase 8** | Convert remaining screens (MP lobby, shrine, theme, effects, synergies, favourites, codex) | 1.5 hr | P2 |
| **Phase 9** | Convert all widget files Text → GoopText | 1.5 hr | P3 |
| **Phase 10** | Final audit: grep for remaining `Text(` that should be `GoopText`, verify no numeric-only or tooltip texts were converted | 30 min | P2 |

### Dependencies
- Phase 1 must come first (language selector UI)
- Phase 2-3 can be done in parallel with Phase 1
- Phases 4-9 are independent file-by-file conversions
- Phase 10 is the final verification

---

## 6. Edge Cases

- **Numeric-only Text:** `Text('${gun.dps}')` — leave as `Text`. Numbers don't have Goopian equivalents.
- **Text.rich with TextSpan:** `Text.rich(TextSpan(children: [...]))` — leave as-is. GoopText doesn't support rich text spans. These are usually complex formatted text (links, mixed styles) where Goopianization would break the formatting.
- **Tooltip text:** `Tooltip(message: '...')` — leave as English. Tooltips are accessibility aids.
- **SnackBar text:** `SnackBar(content: Text('...'))` — convert to `GoopText` for consistency (SnackBars are user-facing).
- **AppBar title:** `AppBar(title: Text('...'))` — convert to `GoopText`.
- **NavigationDestination labels:** `NavigationDestination(label: '...')` — these are plain strings, not Text widgets. Cannot Goopianize without changing the NavigationBar to a custom widget. **Decision: leave as English** — they're short labels that are already hard to read in Goopian.
- **Error messages:** `Text('Error: ${runProvider.error}')` — convert to `GoopText` for full immersion.

---

## 7. Testing Checklist

- [ ] Language toggle appears on main menu below version number
- [ ] Tapping "English" sets language to English (all text instantly English)
- [ ] Tapping "Goopian" sets language to Goopian (all GoopText transforms to alien symbols)
- [ ] Language preference persists across app restarts
- [ ] Sponge button appears on active run dash only when Goopian is active
- [ ] Tapping sponge toggles between Goopian-only and translated-to-English
- [ ] Sponge glow pulses when active
- [ ] GoopText animation is smooth (no jank, no frame drops)
- [ ] All screens show Goopian text when language is set to Goopian
- [ ] No numeric-only or tooltip texts were accidentally Goopianized
- [ ] `flutter analyze` passes with 0 issues
- [ ] No new `dispose()` issues from GoopText (it already manages its own controller)
- [ ] `context.mounted` checks in place for any new interactive elements
