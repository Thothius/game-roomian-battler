# GungeonMate — Full App UX/UI Assessment
**Date:** 2026-08-25
**Assessor:** Slot 2 — Coder-Maintainer-Reworker-Genius
**Method:** Playwright web build + accessibility tree inspection + source code review
**Build:** v2.0.3, web release

---

## Executive Summary

GungeonMate is a feature-rich companion app for *Enter the Gungeon* with a strong dark-neon visual identity, 27 themes, particle engines, shader effects, multiplayer, and a comprehensive codex. The app has matured significantly but still has UX gaps in navigation clarity, empty/loading states, accessibility, and several interaction patterns that feel "ported" rather than native.

**Test coverage:** 186 tests (137 existing + 49 new widget tests). All pass.

---

## Screen-by-Screen Assessment

### 1. Main Menu (`main_menu_screen.dart`)
**Verdict: Good, with minor polish needed**

✅ **Strengths:**
- Strong hero title "GUNGEON MATE" with subtitle
- 4 clear primary actions: Local Run, Multiplayer, Customization, Codex
- New "How to Use" modal (6 steps) with Semantics labels — good onboarding
- Version label visible
- Atmospheric background (particles/shader)

⚠️ **Issues:**
- **M1 — No visual feedback on button press.** The ScaleButton provides haptic but the visual scale-down is barely perceptible. Consider a brighter glow or ripple on press.
- **M2 — "How to Use" button is low-contrast.** `Colors.white.withValues(alpha: 0.4)` on a dark background is below WCAG AA (4.5:1). The button is nearly invisible.
- **M3 — No first-run detection.** The How to Use modal is always accessible but never auto-shown. New users may miss it. Consider auto-opening on first launch.
- **M4 — No changelog/what's-new surface.** The changelog exists in `assets/data/changelog.json` but there's no "What's New" button or badge on the main menu.
- **M5 — Character preview absent.** The main menu doesn't show which character was last played. A small avatar or "Continue as The Marine" hint would help returning users.

💡 **Ideas:**
- Add a "Continue Run" button when a saved run exists (jump straight back in)
- Add a subtle pulse animation on the primary CTA (Local Run) to draw the eye
- Show a small "What's New" badge dot on the version label when there are unread changelog entries

---

### 2. Character Select (`character_select_screen.dart`)
**Verdict: Solid, one significant UX issue**

✅ **Strengths:**
- Clean 3×3 grid of square character cards
- In-game sprite fills each tile (not card art — consistent)
- Character name overlay at bottom
- "?" info button in top-right opens detail screen
- Animated entrance (fadeIn + slide)

⚠️ **Issues:**
- **C1 — CRITICAL: Tap target collision.** The "?" info button overlaps the card's tap area. Playwright clicks kept hitting the "?" button instead of starting a run. On a real device, users near the top-right corner will accidentally open the detail screen instead of starting a run. The "?" button needs a larger margin or the card tap area needs to exclude it.
- **C2 — No "Start Run" confirmation.** Tapping a card instantly starts a run. There's no "Are you sure?" or preview. For a new user, this is surprising. Consider a brief card-flip animation or a small "Starting..." state.
- **C3 — No scroll indicator.** The grid uses `NeverScrollableScrollPhysics` — if the viewport is too short, characters are clipped with no indication there are more.
- **C4 — No character lock/unlock progression.** All 9 characters are always visible. EtG has unlock progression — showing locked characters (silhouettes) would add authenticity.

💡 **Ideas:**
- Add a long-press gesture on the card to open the detail screen (instead of the "?" button)
- Show a brief "Starting run as The Marine..." toast before navigating
- Add character stats preview on card hover/long-press (DPS, armor, etc.)

---

### 3. Gungeoneer Detail (`gungeoneer_detail_screen.dart`)
**Verdict: Good information architecture, needs visual polish**

✅ **Strengths:**
- 5 content tabs: LOADOUT, TIPS, PLAYSTYLE, LORE, SPOILERS
- "View on Wiki" opens external wiki in new tab — works correctly
- Character description and stats visible
- Spoiler tab is separate (good content gating)

⚠️ **Issues:**
- **G1 — No "Start Run" button on detail screen.** Users who open the detail screen to learn about a character can't start a run from there — they have to go back and tap the card. This is a dead-end.
- **G2 — Tab content is sparse.** The LOADOUT tab shows weapons/items as text buttons. No icons, no stats, no visual hierarchy. Feels like a list, not a dashboard.
- **G3 — No "Back to Character Select" affordance.** The back button works but there's no breadcrumb or contextual title.
- **G4 — SPOILERS tab has no warning.** Tapping it immediately shows spoiler content. Consider a blur overlay or "Show spoilers" tap-to-reveal.

💡 **Ideas:**
- Add a "PLAY AS THE MARINE" button at the bottom of the detail screen
- Show weapon/item icons in the LOADOUT tab with quality badges
- Add a spoiler blur overlay that requires a tap to dismiss

---

### 4. Active Run Screen (`active_run_screen.dart`)
**Verdict: Feature-dense, needs information hierarchy work**

✅ **Strengths:**
- P1/P2 player switcher tabs
- Toolbar with labeled icons (Effects, Shrine, Panels, More)
- Stat pills (COOL, CURSE, SYN, DPS) — quick-glance metrics
- Guns and Items sections with count badges
- Layout style picker
- Bottom navigation (Inventory, Browse, Codex, Settings)

⚠️ **Issues:**
- **A1 — Toolbar labels are tiny.** "Effects", "Shrine", "Panels", "More" are very small text under icons. On mobile these may be hard to read.
- **A2 — "Add to inventory" floating button overlaps content.** The floating "Add to inventory" text appeared as a stray element in the accessibility tree during Browse tab testing.
- **A3 — No empty state for guns/items.** When a player has 0 items, the section shows "0" with no helpful message. Consider "No items yet — tap Browse to add some".
- **A4 — Browse tab opens as a modal dialog, not a tab.** Tapping Browse opens a "QUICK ADD TO RUN" search dialog instead of switching the tab content. This is confusing — the tab looks like it should switch content, not open a dialog.
- **A5 — Escape key doesn't close the Browse dialog.** The dialog persisted through Escape key presses. No visible close button was found either.
- **A6 — END RUN button behavior unclear.** Tapping END RUN in Settings seemed to switch to the Codex tab instead of showing a confirmation dialog. This needs investigation — may be a focus/event issue.
- **A7 — No run timer or floor tracker.** The active run has no visible elapsed time or current-floor indicator. EtG players track progress by floor.

💡 **Ideas:**
- Add a floor tracker (1-5) and run timer to the player header
- Make Browse a proper tab content view, not a modal dialog
- Add empty state illustrations for 0 guns / 0 items
- Add a "Run Summary" preview accessible from the toolbar

---

### 5. Browse / Quick Add Dialog (`browse_screen.dart`)
**Verdict: Functional but confusing as a tab**

✅ **Strengths:**
- Search field with "509 results" count
- Alphabetical list with quality badges
- ADD buttons for each item
- "ADVANCED LIBRARY" link for full browse mode

⚠️ **Issues:**
- **B1 — Modal dialog is the wrong pattern for a bottom-nav tab.** Users expect tab content to replace the current view, not open a dialog on top. This breaks the mental model of bottom navigation.
- **B2 — No close button on the dialog.** Escape doesn't work. Users may feel trapped.
- **B3 — No filter/sort options in quick-add mode.** Only search is available. No quality filter, type filter, or "show only guns/items" toggle.
- **B4 — No visual feedback when ADD is tapped.** No haptic, no animation, no toast. Users don't know if the item was added.

💡 **Ideas:**
- Replace the modal with a proper tab content view
- Add filter chips (Guns, Items, Active, Passive, by Quality)
- Show a brief "Added: Marine Sidearm" toast with undo option
- Add recently-added items at the top

---

### 6. Codex (`codex_screen.dart`)
**Verdict: Excellent structure, needs loading polish**

✅ **Strengths:**
- 10 category tabs: Gungeoneers, NPCs, Enemies, Bosses, Pickups, Objects, Rat, Dragun, Bullet Hell, Challenge
- Standalone mode (from main menu) with back button + "CODEX Encyclopedia of the Gungeon" title
- Embedded mode (bottom nav tab) without back button
- Grid of entries with names
- Detail screen with tabs (LOADOUT, TIPS, etc.)

⚠️ **Issues:**
- **X1 — Skeleton loaders during initial load.** The codex shows skeleton shimmer widgets while loading data. This is good but the shimmer is a perpetual animation that prevents `pumpAndSettle()` in tests.
- **X2 — No search in standalone Codex mode.** The Objects tab had a search field but the Gungeoneers tab didn't. Search should be universal.
- **X3 — No entry count per tab.** Each tab doesn't show how many entries it contains. "Bosses (12)" would help.
- **X4 — No favorites/bookmarks in Codex.** Can't mark entries for quick return.
- **X5 — Special codex screens (Rat, Dragun, Bullet Hell, Challenge) are separate files.** These may have inconsistent layouts compared to the main codex.

💡 **Ideas:**
- Add a universal search bar at the top of the Codex
- Add entry counts per category tab
- Add a "Recently Viewed" section
- Add cross-links between related entries (e.g., Boss → its drops)

---

### 7. Settings (`settings_screen.dart` / `settings_tab.dart`)
**Verdict: Well-organized, good information architecture**

✅ **Strengths:**
- 6 collapsible sections: RUN TOOLS, DICE STYLE, MULTIPLAYER, DATA & STORAGE, DEBUG, DANGER ZONE
- RUN TOOLS expanded by default (most-used)
- DANGER ZONE visually distinct with warning styling
- Grid layout for action tiles (2 columns)
- Confirmation dialogs for destructive actions
- Multiplayer status bar shows "SOLO" when no MP

⚠️ **Issues:**
- **S1 — No theme/customization access from Settings.** The user explicitly wanted themes to be separate from settings, but there's no link or "Customize themes" button in Settings. Users in a run may not know how to get to the Customization screen.
- **S2 — No haptic toggle.** Haptics are used throughout but there's no setting to disable them. Accessibility concern.
- **S3 — No reduced-motion toggle.** The app has extensive animations but no way to disable them for motion-sensitive users.
- **S4 — No text-scale slider.** No way to adjust font size beyond system settings.
- **S5 — DEBUG section is visible in production.** Should be hidden behind a dev-mode flag or long-press gesture.
- **S6 — No "About" section.** No app info, licenses, credits, or links to support/wiki.

💡 **Ideas:**
- Add a "Customize Themes" link at the top of Settings
- Add Accessibility section: haptic toggle, reduced motion, text scale
- Hide DEBUG behind 5-tap on version number (Easter egg style)
- Add About section with licenses, credits, support link

---

### 8. Customization / Experience Studio (`experience_studio_screen.dart`)
**Verdict: Impressive feature set, needs flow polish**

✅ **Strengths:**
- 4 tabs: THEME, PARTICLES, TYPOGRAPHY, AMBIANCE
- 9 theme presets visible (CUSTOM, UNICORN, FORGE MASTER, etc.)
- Theme names with descriptors ("CLEAN · METAL")
- RESET, PREVIEW, APPLY buttons
- Live preview mode

⚠️ **Issues:**
- **E1 — No live whole-app preview.** The PREVIEW button shows a sample scene, not the actual app with the theme applied. Users can't see how their inventory/run will look.
- **E2 — APPLY vs PREVIEW confusion.** Two buttons that seem to do similar things. The distinction isn't clear.
- **E3 — No theme description.** Each theme has a name and tagline but no description of what inspired it or what colors it uses.
- **E4 — No undo/revert after APPLY.** Once a theme is applied, there's no quick way to go back to the previous theme.

💡 **Ideas:**
- Make PREVIEW show the actual app screens with the theme applied (not a sample scene)
- Merge APPLY into PREVIEW (preview → "Apply this theme?" confirmation)
- Add a "Recently used themes" strip at the top
- Add a side-by-side comparison mode (current vs new)

---

### 9. MP Lobby (`mp_lobby_screen.dart`)
**Verdict: Significantly improved in latest redesign**

✅ **Strengths:**
- Character preview card at top (tap to change) — strong identity
- Nickname field with persistence
- PIN field labeled "HOST PIN (JOIN ONLY)" — clear
- Helper text: "HOST: a PIN is auto-generated. JOIN: enter the host's PIN."
- HOST GAME and JOIN GAME buttons with distinct colors
- How to Play modal with 4 numbered steps + Semantics
- Permission rationale dialog before connecting

⚠️ **Issues:**
- **L1 — PIN field is always visible, even for HOST.** The label says "JOIN ONLY" but the field is still editable when hosting. Consider disabling/hiding it when the user taps HOST.
- **L2 — No paired-devices list visible.** The `PairedPartnersStore` exists but the paired devices list isn't shown in the lobby. Previously paired partners should appear for quick reconnect.
- **L3 — No connection status indicator.** No visual feedback while permissions are being requested or while the transport initializes.
- **L4 — Web platform shows no warning.** `nearby_connections` has no web implementation. Tapping HOST on web silently fails. Should show "Multiplayer requires Android" message.

💡 **Ideas:**
- Show paired partners as quick-connect chips above the nickname field
- Disable PIN field when HOST is tapped (or hide it with a smooth animation)
- Add a platform check: if web, show "Multiplayer is available on Android only"
- Add a "Test Connection" button for paired devices

---

### 10. MP Connect (`mp_connect_screen.dart`)
**Verdict: Functional, limited web testing**

✅ **Strengths:**
- Pulsing animation for waiting state
- Player portraits
- Host PIN display
- Auto-navigation when connected (600ms delay for success state)
- Error/permission-denied states

⚠️ **Issues:**
- **N1 — Cannot fully test on web.** `nearby_connections` has no web implementation. The connect screen's core flow can't be verified via Playwright.
- **N2 — No elapsed time indicator.** No timer showing how long the connection attempt has been running.
- **N3 — No cancel button visible during connection.** If the user wants to abort, there's no obvious way back.

💡 **Ideas:**
- Add an elapsed-time counter ("Connecting... 0:15")
- Add a prominent "Cancel" button during connection
- Add a "Troubleshooting" link if connection takes >30s

---

### 11. MP Reconnect Banner (`mp_reconnect_banner.dart`)
**Verdict: Fixed in latest commit**

✅ **Strengths:**
- "tap for options" (fixed from misleading "tap to cancel")
- Amber color (softened from orangeAccent)
- Dismissable dialog + persistent banner
- Connection-restored snackbar with haptic

⚠️ **Issues:**
- **R1 — No maximum reconnect duration.** The banner can persist indefinitely. Consider an escalation prompt after 2 minutes: "Having trouble reconnecting? End run?"
- **R2 — No reconnect attempt counter.** Users don't know how many attempts have been made.

---

### 12. Home Screen / Bottom Navigation (`home_screen.dart`)
**Verdict: Good structure, needs state handling polish**

✅ **Strengths:**
- 4-tab bottom navigation: Inventory, Browse, Codex, Settings
- Loading state with skeleton loaders
- Main menu state when no run is active
- Active run state with full UI

⚠️ **Issues:**
- **H1 — Browse tab opens a modal, not tab content.** (Same as A4/B1 above)
- **H2 — No tab persistence.** Switching tabs and coming back doesn't preserve scroll position.
- **H3 — No swipe-to-switch tabs.** Bottom nav requires tap; no gesture swipe between tabs.

---

## Cross-Cutting Issues

### Accessibility
- **AC1 — No semantic labels on icon-only buttons in several screens.** (BUG-052 was marked done but new screens may have regressed.)
- **AC2 — Low contrast on secondary text.** `Colors.white.withValues(alpha: 0.4)` appears frequently and fails WCAG AA.
- **AC3 — No screen reader navigation order verification.** Semantics are added but the tab/focus order hasn't been verified.
- **AC4 — No haptic preference toggle.** Haptics fire throughout but can't be disabled.

### Performance
- **P1 — Perpetual animations prevent `pumpAndSettle()`.** AvatarAura, particle engines, skeleton loaders, and dialog animations all run infinitely. This is fine for production but makes testing harder.
- **P2 — No RepaintBoundary audit.** Particle engines and animations may cause unnecessary repaints of static content.

### Responsive Design
- **RD1 — BrowseScreen AppBar overflow on 800×600.** The test subagent caught a RenderFlex overflow error. This is a pre-existing lib issue.
- **RD2 — No tablet/desktop layout.** The app is phone-first. On larger screens, content stretches full-width with no adaptive layout.

### State Management
- **SM1 — No undo/redo for inventory changes.** Adding/removing items is immediate with no undo.
- **SM2 — No run autosave indicator.** The run is saved manually via Settings. No autosave or "last saved" indicator.

---

## 12 Questions for the User

These are areas I found important during the assessment that we haven't discussed yet:

1. **Should the Browse tab be a proper content view instead of a modal dialog?** It currently opens a "QUICK ADD TO RUN" dialog when tapped, which breaks the bottom-nav mental model. Making it a real tab with filter/sort would be more intuitive.

2. **Do you want a "Continue Run" button on the main menu?** When a saved run exists, jumping straight back in would save 3 taps (Local Run → pick character → start). The run data is already persisted.

3. **Should the character select "?" info button be replaced with long-press?** The current "?" button in the top-right corner causes tap target collision — Playwright kept hitting it instead of starting a run. Long-press for detail, tap for start would fix this.

4. **Do you want a "Start Run from Detail" button on the gungeoneer detail screen?** Users who browse character info can't start a run from there — they have to go back to the grid. A "PLAY AS THE MARINE" button would close the loop.

5. **Should we add an Accessibility section in Settings?** Haptic toggle, reduced-motion toggle, and text-scale slider are all missing. These are important for inclusivity and App Store/Play Store compliance.

6. **Should the DEBUG section be hidden in production?** It's currently visible to all users. A 5-tap-on-version-number Easter egg would hide it from regular users while keeping it accessible for devs.

7. **Do you want a floor tracker and run timer in the active run header?** EtG players track progress by floor (1-5). A timer + floor indicator would make the active run feel more game-connected.

8. **Should we add empty states for 0 guns / 0 items?** Currently shows "0" with no guidance. A friendly "No items yet — tap Browse to add some" would help new users.

9. **Should the SPOILERS tab in character detail have a blur overlay?** Currently shows spoiler content immediately on tap. A tap-to-reveal blur would prevent accidental spoilers.

10. **Should we show paired partners in the MP lobby?** The `PairedPartnersStore` exists but isn't shown in the redesigned lobby. Quick-connect chips for previously paired devices would streamline reconnect.

11. **Should we add a "What's New" / changelog surface on the main menu?** The changelog exists in `changelog.json` but there's no way for users to see what changed. A badge on the version label or a "What's New" button would surface this.

12. **Should the Customization PREVIEW show the actual app screens instead of a sample scene?** Currently PREVIEW shows a mockup with sample items/buttons. Showing the user's actual inventory or the main menu with the theme applied would be more useful.

---

## Test Coverage Summary

| Test File | Tests | Coverage |
|-----------|-------|----------|
| `mp_integration_test.dart` | 12 | MP protocol (handshake, gifts, dice, emotes, disconnect) |
| `mp_reliability_test.dart` | 20 | MP reliability (reconnect, teardown, permissions) |
| `mp_lobby_screen_test.dart` | 7 | Lobby UI, validation, How to Play modal |
| `mp_connect_screen_test.dart` | 6 | Connect screen states |
| `main_menu_test.dart` | 10 | **NEW** — title, buttons, navigation, How to Use |
| `character_select_screen_test.dart` | 8 | **NEW** — solo/coop/MP modes, empty state |
| `codex_screen_test.dart` | 9 | **NEW** — loading, back button, tabs |
| `settings_screen_test.dart` | 14 | **NEW** — all 6 sections, dialogs, danger zone |
| `home_screen_test.dart` | 10 | **NEW** — loading, main menu, bottom nav |
| Other tests | 90 | Various models, services, utilities |
| **Total** | **186** | **All pass** |

---

## Priority Recommendations

### High Priority (UX-breaking)
1. Fix Browse tab — make it a proper tab, not a modal dialog (A4, B1, B2, H1)
2. Fix character select tap target collision (C1)
3. Add "Start Run from Detail" button (G1)
4. Add empty states for 0 guns/items (A3)
5. Add Accessibility section in Settings (S3, S4, AC4)

### Medium Priority (Polish)
6. Add floor tracker + run timer (A7)
7. Add "Continue Run" on main menu (M5)
8. Hide DEBUG in production (S5)
9. Improve low-contrast text (M2, AC2)
10. Add "What's New" surface (M4)

### Low Priority (Nice-to-have)
11. Add spoiler blur on SPOILERS tab (G4)
12. Add paired partners in MP lobby (L2)
13. Add entry counts in Codex tabs (X3)
14. Add undo for inventory changes (SM1)
15. Add tablet/desktop adaptive layout (RD2)
