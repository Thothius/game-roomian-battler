---
description: Full screen tour — navigate every screen, capture screenshots, verify rendering
---

# Playwright Full Screen Tour

Navigate through every screen in the app and capture screenshots for verification.

## Prerequisites
- Complete the smoke test first (`/playwright-smoke`)
- App served at `http://localhost:8099`
- Mobile viewport set (390x844)

## Screens to Visit

### 1. Home Screen
- `browser_snapshot()` — verify "Start New Run" button visible
- `browser_take_screenshot(filename="01-home.png")`

### 2. Character Select
- Tap "Start New Run"
- `browser_wait_for(text="Select")` or similar
- `browser_take_screenshot(filename="02-character-select.png")`

### 3. Active Run (empty)
- Select any character (e.g., tap "The Marine")
- `browser_wait_for(text="Marine")` or character name
- `browser_take_screenshot(filename="03-active-run-empty.png")`

### 4. Browse Screen
- Tap the browse/add FAB
- `browser_wait_for(text="Guns")` — verify browse loaded
- `browser_take_screenshot(filename="04-browse-guns.png")`
- Tap "Items" tab
- `browser_take_screenshot(filename="05-browse-items.png")`
- Tap "All" tab
- `browser_take_screenshot(filename="06-browse-all.png")`

### 5. Item Detail
- Tap any item in the browse list
- `browser_wait_for(text="Quality")` or similar
- `browser_take_screenshot(filename="07-item-detail.png")`

### 6. Synergies Overview
- Navigate back to active run
- Tap synergies button
- `browser_wait_for(text="Synergy")` or similar
- `browser_take_screenshot(filename="08-synergies.png")`

### 7. Stats Detail
- Navigate back to active run
- Tap coolness or curse stat
- `browser_wait_for(text="Coolness")` or "Curse"
- `browser_take_screenshot(filename="09-stats-detail.png")`

### 8. Shrine Picker
- Navigate back to active run
- Tap shrine button
- `browser_wait_for(text="Shrine")`
- `browser_take_screenshot(filename="10-shrine-picker.png")`

### 9. Settings
- Navigate back to active run
- Open settings (gear icon or menu)
- `browser_wait_for(text="Settings")` or "Theme"
- `browser_take_screenshot(filename="11-settings.png")`

### 10. Theme Picker
- In settings, tap theme picker
- `browser_wait_for(text="Theme")`
- `browser_take_screenshot(filename="12-theme-picker.png")`

### 11. Favourites
- Navigate back to home
- Tap favourites
- `browser_take_screenshot(filename="13-favourites.png")`

## After Each Screenshot
- `browser_console_messages(level="error")` — check for errors on each screen
- Record any errors with the screen name

## Pass Criteria
- All 13+ screenshots captured
- Every screen renders with content (not blank)
- Zero console errors on any screen
- Navigation works in both directions (forward and back)

## Output
Store screenshots in `gungeon_mate/test/screenshots/` for visual regression comparison.
