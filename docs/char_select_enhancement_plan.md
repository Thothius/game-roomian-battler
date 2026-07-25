# Character Select Enhancement Plan

## Status: Research Complete — Ready for Implementation

---

## 1. Current State

`character_select_screen.dart` (309 lines) is a simple StatelessWidget:
- 2-column GridView of `_CharacterCard` widgets
- Each card shows animated card GIF, name, gun count badge, starting gun names
- Tapping a card **immediately** starts the run / selects character — no confirmation, no equipment inspection
- No expandable panels, no tooltips, no flip animation

### Existing Reusable Components
- `GameIcon` — pixel-art sprite in quality-colored ring, with fallback
- `QualityBadge` — tier circle (S/A/B/C/D/N) with animated glow for S-tier
- `gungeoneerAnimatedCardPath(name)` — card GIF path (already used in cards)
- `gungeoneerGifPath(name)` — in-game animated model GIF path (used in MP summary `_GungeoneerPortrait`)
- `RunProvider.gunByName(name)` / `RunProvider.itemByName(name)` — case-insensitive lookup returning full `Gun`/`Item` objects
- `Gun` model: dps, magazineSize, ammoCapacity, damage, fireRate, reloadTime, shotSpeed, range, force, spread, gunClass, sellPrice, curse, coolness, quality
- `Item` model: effect, quote, quality, sellPrice, rechargeTime, duration, curse, coolness, type, isActive

### Character Data (gungeoneers.json — 9 entries)
| Character | Guns | Items |
|-----------|------|-------|
| The Marine | Marine Sidearm | Supply Drop |
| The Pilot | Rogue Special | Trusty Lockpicks, Disarming Personality, Hidden Compartment |
| The Convict | Sawed-Off, Budget Revolver | Molotov, Enraging Photo |
| The Hunter | Rusty Sidearm, Crossbow | Dog |
| The Bullet | Blasphemy | Live Ammo |
| The Robot | Robot's Right Hand | Battery Bullets, Coolant Leak |
| The Cultist | Dart Gun | Friendship Cookie, Number 2 |
| The Paradox | — | — |
| The Gunslinger | Slinger | — |

---

## 2. Redesign Goals

1. **Expandable equipment panel** below each character card
2. **Gun/Item icons with tooltips** — tap an icon to see a compact stat popup
3. **Auto-collapse** — expanding one card collapses any other open card
4. **Confirmation step** — selecting a character requires a confirm action (not immediate)
5. **Card flip** — tapping the character graphic flips between card GIF and animated in-game model GIF

---

## 3. Proposed Layout

```
┌─────────────────────────────────────┐
│  Choose your Gungeoneer             │
│  ─────────────────────────────────  │
│                                     │
│  ┌──────────┐  ┌──────────┐         │
│  │ [Card    │  │ [Card    │         │
│  │  GIF or  │  │  GIF or  │         │  ← Tap graphic to flip
│  │  Model   │  │  Model   │         │     between card GIF & model GIF
│  │  GIF]    │  │  GIF]    │         │
│  │          │  │          │         │
│  │ THE      │  │ THE      │         │
│  │ MARINE   │  │ PILOT    │         │
│  │ ▼ Expand │  │ ▼ Expand │         │  ← Tap chevron to expand
│  └──────────┘  └──────────┘         │
│                                     │
│  When expanded:                     │
│  ┌─────────────────────────────┐    │
│  │ THE MARINE          [✕]     │    │
│  │ ─── GUNS ───                │    │
│  │ [icon] Marine Sidearm  ⓘ   │    │  ← Tap ⓘ or icon for tooltip
│  │ ─── ITEMS ───               │    │
│  │ [icon] Supply Drop     ⓘ   │    │
│  │                             │    │
│  │    [ Select Gungeoneer ]    │    │  ← Confirmation button
│  └─────────────────────────────┘    │
│                                     │
│  Tooltip popup (gun example):       │
│  ┌─────────────────────────────┐    │
│  │ Marine Sidearm       [D]    │    │
│  │ DPS: 5.0   Mag: 10         │    │
│  │ Damage: 6  Fire Rate: 1.5  │    │
│  │ Reload: 1.2s  Spread: 5°   │    │
│  │ Range: 20  Shot Speed: 4   │    │
│  └─────────────────────────────┘    │
│                                     │
│  Tooltip popup (item example):      │
│  ┌─────────────────────────────┐    │
│  │ Supply Drop          [C]    │    │
│  │ Active · 6s recharge        │    │
│  │ Calls in a supply drop      │    │
│  │ that refills ammo.          │    │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘
```

---

## 4. Implementation Details

### A. Screen Conversion: StatelessWidget → StatefulWidget

`CharacterSelectScreen` must become StatefulWidget to track:
- `_expandedIndex` (int? — null = all collapsed, index = which card is expanded)
- `_flippedSet` (Set<int> — which cards are showing model GIF vs card GIF)
- `_selectedCharacter` (Gungeoneer? — for confirmation step)
- `_tooltipGun` / `_tooltipItem` (Gun?/Item? — for tooltip overlay)

### B. Card Flip Animation

- Tap the character graphic area → flip between `gungeoneerAnimatedCardPath` (card GIF) and `gungeoneerGifPath` (model GIF)
- Use `AnimatedSwitcher` with `FlipTransition` or a simple `RotationTransition` on Y-axis
- Lightweight: no extra dependencies, use `AnimationController` + `Tween<double>(0, 1)` for half-rotation
- At 0.0 → show card GIF, at 1.0 → show model GIF, swap at 0.5
- `_flippedSet` tracks which cards are in model-GIF mode

### C. Expandable Equipment Panel

- Each card has a chevron button (▼ when collapsed, ▲ when expanded)
- Tapping chevron toggles `_expandedIndex`:
  - If tapping the already-expanded card → collapse (set to null)
  - If tapping a different card → set `_expandedIndex` to that index (auto-collapses the previous)
- Expanded panel slides in below the card within the GridView cell
- **GridView → ListView** consideration: GridView with variable heights is tricky. Two options:
  - **Option A (recommended):** Switch to a `ListView` with 2-column manual pairing (Row of two cards). Each card can then expand to full-width below its row, pushing content down.
  - **Option B:** Keep GridView but make expanded panel an overlay/tooltip that appears below the grid item. More complex, less natural.
- **Chosen: Option A** — Convert to ListView with paired rows. When a card expands, it expands inline within its row, pushing the next row down. This is the most natural scroll behavior.

### D. Equipment Panel Content

For each character, the expanded panel shows:
- **GUNS section:** For each `startingGuns` name → look up `RunProvider.gunByName(name)` → show `GameIcon` + name + quality badge
- **ITEMS section:** For each `startingItems` name → look up `RunProvider.itemByName(name)` → show `GameIcon` + name + quality badge
- Empty state: "No starting equipment" (for The Paradox)
- Each equipment row is tappable → shows tooltip popup

### E. Tooltip Popup

- **Not a full screen navigation** — use a themed `AlertDialog` or a positioned overlay
- **Gun tooltip:** Name, quality badge, DPS, damage, mag size, ammo, fire rate, reload time, shot speed, range, spread, force — compact 2-column grid
- **Item tooltip:** Name, quality badge, type (Active/Passive), recharge time, duration, effect text (truncated to ~3 lines), curse/coolness if > 0
- Dismiss: tap outside or tap a close button
- Styled as a dark neon card with quality-colored border (matching `AppTheme.flair`)

### F. Confirmation Step

- The card's main tap no longer immediately starts the run
- Instead, expanding the panel shows a **"Select [Character Name]"** button at the bottom
- Tapping this button triggers the actual selection (`startNewRun` / `startCoopPlayer` / `Navigator.pop` for MP)
- For multiplayer pick mode: same flow — expand → confirm → pop with result
- Visual: the confirm button is a prominent `FilledButton` with the character's accent color
- Optional: show a brief "Ready?" confirmation dialog before starting. But the plan says "confirmation on this screen" — so the expand → confirm button flow IS the confirmation. No extra dialog needed.

### G. Visual Polish

- Expanded panel has a subtle slide+fade animation (`flutter_animate` already imported)
- Chevron rotates 180° when expanding (animated)
- Equipment icons use `GameIcon` with quality ring — consistent with browse/inventory
- Tooltip has a scale-in animation
- Haptics: `Haptics.selection()` on expand/collapse, `Haptics.light()` on tooltip open
- Card flip: `Haptics.selection()` on flip

---

## 5. File Changes

| File | Change | Est. Lines |
|------|--------|-----------|
| `lib/screens/character_select_screen.dart` | Full rewrite of screen + card logic | ~450 (from 309) |
| No new files needed | All widgets inline — _CharacterCard, _EquipmentPanel, _EquipmentTooltip, _FlipCard | — |

### No new dependencies required
- `flutter_animate` — already imported
- `GameIcon`, `QualityBadge` — already exist
- `Haptics` — already imported
- `gungeoneerGifPath` — already exists in `asset_paths.dart`

---

## 6. Implementation Phases

| Phase | Task | Effort | Priority |
|-------|------|--------|----------|
| **Phase 1** | Convert to StatefulWidget, add _expandedIndex tracking, restructure GridView → paired ListView rows | 1 hr | P0 |
| **Phase 2** | Build _EquipmentPanel (guns/items sections with GameIcon rows) | 1 hr | P0 |
| **Phase 3** | Build _EquipmentTooltip (gun stats grid + item effect popup) | 1 hr | P1 |
| **Phase 4** | Add card flip animation (card GIF ↔ model GIF) | 45 min | P1 |
| **Phase 5** | Add confirmation button + wire up selection logic | 30 min | P0 |
| **Phase 6** | Polish: animations, haptics, edge cases (Paradox empty loadout) | 45 min | P2 |

### Dependencies
- Phase 1 must come first (state infrastructure)
- Phases 2-5 can be done in sequence within the same file
- Phase 6 is polish after everything works

---

## 7. Edge Cases

- **The Paradox:** No starting guns or items. Panel shows "No starting equipment — The Paradox starts with random gear."
- **The Gunslinger:** Only 1 gun, no items. Panel shows gun section only.
- **The Convict / The Hunter:** 2 starting guns. Panel shows both.
- **The Pilot:** 3 starting items. Panel wraps item rows.
- **Multiplayer pick mode:** Confirmation flow still works — confirm button pops with the selected Gungeoneer.
- **Coop mode:** Same flow — confirm button calls `startCoopPlayer`.
- **Missing gun/item lookup:** If `gunByName` or `itemByName` returns null (data mismatch), show fallback row with name only and a warning icon.

---

## 8. Testing Checklist

- [ ] All 9 characters display correctly with card GIF
- [ ] Tapping character graphic flips to model GIF and back
- [ ] Tapping chevron expands equipment panel
- [ ] Expanding one card auto-collapses the previous
- [ ] Gun tooltip shows correct stats (verify against guns.json)
- [ ] Item tooltip shows correct effect/recharge
- [ ] Confirmation button starts the correct run mode
- [ ] The Paradox shows empty state message
- [ ] Multiplayer pick mode returns correct character on confirm
- [ ] Coop mode adds second player on confirm
- [ ] `flutter analyze` passes with 0 issues
- [ ] No missing `dispose()` for AnimationControllers
- [ ] `context.mounted` checked before any overlay/snackbar
