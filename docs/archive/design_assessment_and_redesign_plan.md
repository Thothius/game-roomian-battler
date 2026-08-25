# GungeonMate — Visual Design Assessment & Redesign Plan

> Based on Playwright screenshot sweep of 28 screens (Aug 2026, v1.9.25)
> Goal: visual unity, decluttered menus, consistent navigation
>
> **UPDATE (user review):** 3 of 8 phases approved for v1.9.26:
> - Phase 3 — Run Options Popup real section headers ✓
> - Phase 2 — Settings App Tab reorganization ✓
> - Phase 5 — Theme Picker section labels ✓ (with taller carousel)
>
> 5 phases rejected — current designs for Active Run header, Shrine Picker
> navigation, Favourites, Codex, and Home Screen stay as-is.

---

## A. Current State Assessment

### What works well
- **Home screen** — Clean, focused. Vortex video bg, title, two buttons, version tag. Good hierarchy.
- **Character Select** — Uniform 3×3 grid, clear. Good.
- **Browse tabs** (All/Guns/Items/Favs) — Consistent layout, search, quality tiers, synergy counts. Good.
- **Item/Gun Detail** — Rich info, well-organized. Good.
- **Shrine Picker** — Clean list with USE buttons. Good.
- **Changelog Dialog** — Simple, readable. Good.

### What needs work — ranked by severity

---

### CRITICAL — Active Run header is overloaded

**Screens affected:** 03 (Active Run), 19 (Effects Panel), 20 (Damage Calculator)

The Active Run header crams **too many controls** into one horizontal strip:
- 4 toggle buttons with labels (Calc, Effects, Shrine, Panels)
- Run options button
- 4 stat capsules (COOL, CURSE, CD↓, AMMO)
- SYN count, DPS readout, Guns/Items counters
- Layout style selectors
- Gun card + Item card
- Bottom tab bar (Inventory / Browse / Settings)

**Problems:**
- The toggle row (Calc/Effects/Shrine/Panels) uses tiny icons + labels that are hard to distinguish at a glance
- "Shrine" is both a toggle AND a navigation button (tap = navigate, long-press = toggle panel) — hidden dual-mode interaction
- "Panels" toggle name is vague — what panels?
- Stats capsules (COOL/CURSE/CD/AMMO) compete with the toggle buttons for visual space
- The header is dense enough that the actual gameplay content (guns/items) gets pushed down

---

### HIGH — Settings App tab mixes unrelated concerns

**Screen affected:** 11 (Settings — App)

The App tab contains:
- Reset character
- Changelog
- Dev Tools
- Add Co-op
- Use Shrine
- Event Log
- INVENTORY & DATA section
- DANGER ZONE (End Run, Reset All Data)

**Problems:**
- "Add Co-op" and "Use Shrine" are **gameplay actions**, not settings — they don't belong in Settings
- "Dev Tools" is a developer feature sitting next to user-facing buttons
- "Reset character" and "End Run" are both destructive but in different sections with different prominence
- "Event Log" is a read-only view that belongs alongside run data, not in settings
- The section labeled "DANGER ZONE" is good, but the non-danger items above it are uncategorized

---

### HIGH — Run Options popup uses disabled buttons as section headers

**Screen affected:** 14 (Run Options Popup)

The popup uses disabled buttons labeled "BROWSE", "ACTIONS", "SESSION", "END", "SETTINGS" as section dividers. This is confusing because:
- Disabled buttons look like broken actions, not headers
- No visual distinction between a header and an actionable item
- "BROWSE" header has only 2 items, "ACTIONS" has 2, "SESSION" has 1, "END" has 1, "SETTINGS" has 1 — some sections have a single item, making the grouping feel forced

---

### MEDIUM — Two redundant Favourites views

**Screens affected:** 22 (Browse Favs tab), 23 (My Favourites from Run Options)

Two different entry points to what appears to be the same favourites concept:
- Browse → Favs tab (inside the Browse screen)
- Run Options → My Favourites (separate screen)

Both show the same empty state. This is redundant navigation.

---

### MEDIUM — Theme Picker is dense with ~24 controls

**Screens affected:** 09 (Theme Picker), 27 (Unicorn variant), 28 (Particle Studio)

The Theme Picker shows on one screen:
- Theme carousel with dot indicators
- Theme name + description
- 5 palette variant buttons (Original/Graphite/Platinum/Charcoal/Obsidian)
- 6 particle preset buttons
- 7 color schema buttons
- 5 speed control buttons
- PARTICLE STUDIO expandable section

That's 24+ interactive elements. While organized into rows, there's no visual grouping or labels explaining what each row does.

---

### MEDIUM — Navigation patterns are inconsistent

**Across all screens:**
- Home screen: full-screen buttons
- Character select: grid of character buttons
- Active run: bottom tab bar + header toggles + popup menu
- Shrine picker: "Back" button + "BACK TO RUN" button (two different back patterns)
- Codex: "Back" button only
- Settings: tab bar inside a dialog
- Theme picker: "Back" button + carousel dots
- Multiplayer: "Back" button + heading

There's no unified navigation language. Some screens use AppBar back, some use custom back buttons, some use Escape, some use named buttons like "BACK TO RUN".

---

### LOW — Codex appears sparse on first load

**Screen affected:** 15/24 (Codex)

The Codex has 11 categories (Paradox, Gunslinger, Bullet Hell, Drake, Challenge, Rat, Objects, Pickups, NPCs, Enemies, Bosses) in a horizontal strip, but the screenshot only shows the "CODEX" header. The category tiles and content are below the fold or still loading. The first impression is an empty screen.

---

### LOW — Home screen title uses Stack text technique

**Screen affected:** 01 (Home)

The "GUNGEON MATE" title is rendered as two stacked text widgets (red stroke outline + gold fill). This is a valid styling technique, but the accessibility tree reports it as duplicate text. Not a visual bug, but worth noting for screen readers.

---

## B. Redesign Plan

### Phase 1: Active Run Header Declutter (CRITICAL)

**Goal:** Reduce header from 10+ elements to 3 clear zones.

**Current layout:**
```
[Back] [Calc] [Effects] [Shrine] [Panels] [Run Options]    ← toggle row
[COOL] [CURSE] [CD↓] [AMMO] [SYN] [DPS] [Guns] [Items]     ← stat row
[Gun card] [Item card] [Add to inventory]                   ← content
[Inventory] [Browse] [Settings]                             ← tab bar
```

**Proposed layout:**
```
[← Back]  [Gungeoneer avatar + name + level]  [⋮ Menu]      ← clean header bar
[COOL] [CURSE] [CD↓] [AMMO]                                 ← stat row (only)
─── Content area (guns, items, panels) ───
[Inventory] [Browse] [Settings]                             ← tab bar
```

**Changes:**
1. **Move Calc/Effects/Shrine/Panels toggles into the Run Options popup** (renamed to "Run Tools"). The popup becomes the control center for optional panels.
2. **Rename "Run options" to a clear "⋮" overflow icon** in the header.
3. **Keep stat capsules as the only header content** below the title bar — they're glanceable and important.
4. **Remove the dual-mode Shrine button** (tap=nav, long-press=toggle). Make Shrine a normal menu item.
5. **Move "Add to inventory" to a FAB or bottom action** — it's currently crammed between cards.

**Run Options popup redesign:**
```
┌─────────────────────────┐
│ RUN TOOLS               │  ← clear title, not disabled button
├─────────────────────────┤
│ □ Damage Calculator     │  ← checkbox-style toggles
│ □ Effects Panel         │
│ □ Shrine Tracker        │
│ □ Special Panels        │
├─────────────────────────┤
│ NAVIGATION              │
│  → Browse Codex         │
│  → My Favourites        │
│  → Shrine Picker        │
├─────────────────────────┤
│ ACTIONS                 │
│  → Gunfortuna Dice      │
│  → Add Co-op Player     │
│  → Save Run             │
├─────────────────────────┤
│ ⚠ END SESSION           │
│  → End Run              │
└─────────────────────────┘
```

### Phase 2: Settings App Tab Reorganization (HIGH)

**Goal:** Separate settings from gameplay actions.

**Current App tab:**
```
Reset The Marine
Changelog
Dev Tools
Add Co-op        ← gameplay action
Use Shrine       ← gameplay action
Event Log        ← run data view
INVENTORY & DATA
DANGER ZONE
  End Run
  Reset All Data
```

**Proposed: Move gameplay actions to Run Tools popup (Phase 1).**
What remains in the App tab:
```
ACCOUNT & DATA
  Reset Character Loadout
  Changelog
  Event Log

DEVELOPER
  Dev Tools (with warning icon)

DANGER ZONE
  End Current Run
  Reset All Data
```

- "Add Co-op" and "Use Shrine" move to Run Tools popup (Phase 1)
- "Event Log" stays but moves under "ACCOUNT & DATA" (it's a data view, not an action)
- "Dev Tools" gets its own section with a warning icon to signal it's advanced

### Phase 3: Run Options Popup — Replace Disabled Buttons with Real Headers (HIGH)

**Goal:** Clear visual hierarchy in the popup.

Replace disabled buttons with styled `Text` widgets that look like section headers:
- Use small uppercase text with a divider line underneath
- Use the accent color for headers, white for actionable items
- Remove sections that have only 1 item — just list the item directly

### Phase 4: Unify Favourites (MEDIUM)

**Goal:** One favourites concept, one entry point.

**Option A (recommended):** Remove "My Favourites" from Run Tools popup. Keep only the Browse → Favs tab. Add a "★ Favourites" quick-access button in the Active Run header that jumps directly to Browse → Favs tab.

**Option B:** Keep both but make "My Favourites" (from Run Tools) show a richer view with both guns and items in a grid, while Browse → Favs stays as the tab version. This adds complexity.

Recommend Option A for simplicity.

### Phase 5: Theme Picker Grouping (MEDIUM)

**Goal:** Add visual section labels to the 24+ controls.

Add small uppercase labels above each row:
```
THEME
[● ● ● ● ●]  Minimalist — Stripped Back...

PALETTE VARIANT
[Original] [Graphite] [Platinum] [Charcoal] [Obsidian]

PARTICLE PRESET
[Gungeon Dust] [Cosmic Stars] [Forge Embers]...

COLOR SCHEMA
[Default] [Theme Match] [Inferno]...

ANIMATION SPEED
[Very Slow] [Slow] [Normal] [Fast] [Very Fast]

[▼ PARTICLE STUDIO]
```

This doesn't reduce controls but makes the screen scannable instead of overwhelming.

### Phase 6: Navigation Consistency (MEDIUM)

**Goal:** One back pattern, one menu pattern.

**Proposed standard:**
- **All sub-screens** use the standard AppBar with back arrow (already used by Codex, Theme Picker, Multiplayer)
- **Active Run** uses a custom header (it's the main hub) with a "⋮" overflow menu
- **Dialogs** (Changelog, Dice, End Run) close with Escape or tap-outside
- **Remove custom "BACK TO RUN" buttons** — use standard AppBar back arrow everywhere
- **Bottom tab bar** stays only on Active Run (Inventory/Browse/Settings)

### Phase 7: Codex First Impression (LOW)

**Goal:** Show content immediately, not an empty header.

- Default to the first special page (Paradox) content visible on load
- Or show a 2-row category grid instead of a horizontal strip — more visible at once
- Add a brief "Codex" subtitle/description below the header on first visit

### Phase 8: Home Screen Title Accessibility (LOW)

**Goal:** Fix duplicate screen-reader text.

- Wrap the Stack text in a `Semantics(label: 'Gungeon Mate')` widget so screen readers announce it once
- No visual change needed

---

## C. Priority Order for Implementation

| Priority | Phase | Effort | Impact |
|----------|-------|--------|--------|
| 1 | Phase 1 — Active Run header declutter | HIGH | CRITICAL |
| 2 | Phase 3 — Run Options popup real headers | LOW | HIGH |
| 3 | Phase 2 — Settings App tab reorganization | MEDIUM | HIGH |
| 4 | Phase 6 — Navigation consistency | MEDIUM | MEDIUM |
| 5 | Phase 4 — Unify favourites | LOW | MEDIUM |
| 6 | Phase 5 — Theme Picker labels | LOW | MEDIUM |
| 7 | Phase 7 — Codex first impression | LOW | LOW |
| 8 | Phase 8 — Home title accessibility | TRIVIAL | LOW |

---

## D. Design Principles to Enforce

1. **One primary action per screen** — don't mix settings, gameplay, and navigation on one screen
2. **Toggles live in menus, not headers** — headers show info, not controls
3. **Section headers are text, not disabled buttons** — visual clarity
4. **One concept = one entry point** — no duplicate favourites/views
5. **Stats are glanceable, controls are tappable** — don't mix the two visually
6. **Standard back navigation everywhere** — AppBar back arrow, not custom buttons
7. **Group by intent, not by feature** — "Run Tools" (actions) vs "Settings" (configuration) vs "Data" (read-only views)
