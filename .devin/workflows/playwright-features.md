---
description: Feature flow test — test core user interactions: start run, add items, check synergies, adjust stats, use shrines, favourites, end run
---

# Playwright Feature Flow Test

Test core feature interactions end-to-end.

## Prerequisites
- App served at `http://localhost:8099`
- Mobile viewport set (390x844)
- Smoke test passed

## Test Flows

### Flow 1: Start a Run
1. From home, tap "Start New Run"
2. Tap a character (e.g., "The Marine")
3. **Verify**: Active run screen shows character name and starter items
4. `browser_take_screenshot(filename="flow-01-start-run.png")`

### Flow 2: Add Items from Browse
1. From active run, tap browse FAB
2. Tap "Items" tab
3. Tap an item (e.g., "Spice" or any visible item)
4. Tap "Add" button on item detail
5. Navigate back to active run
6. **Verify**: The added item appears in the inventory list
7. `browser_take_screenshot(filename="flow-02-add-item.png")`

### Flow 3: Add Guns from Browse
1. From active run, tap browse FAB
2. Tap "Guns" tab
3. Tap a gun
4. Tap "Add" button
5. Navigate back to active run
6. **Verify**: The added gun appears in the inventory
7. `browser_take_screenshot(filename="flow-03-add-gun.png")`

### Flow 4: Check Synergies
1. From active run, tap synergies button
2. **Verify**: Synergies page shows items with active/potential synergies
3. `browser_take_screenshot(filename="flow-04-synergies.png")`

### Flow 5: Adjust Coolness/Curse
1. From active run, tap the coolness stat
2. Tap "+" to increase coolness
3. **Verify**: Coolness value changes
4. Tap the curse stat
5. Tap "+" to increase curse
6. **Verify**: Curse value changes
7. `browser_take_screenshot(filename="flow-05-adjust-stats.png")`

### Flow 6: Use a Shrine
1. From active run, tap shrine button
2. Tap a shrine (e.g., "Glass Shrine")
3. Tap "Use Shrine" or activate
4. **Verify**: Confirmation shows curse/coolness adjustments
5. `browser_take_screenshot(filename="flow-06-use-shrine.png")`

### Flow 7: Favourite an Item
1. From active run, tap browse FAB
2. Long-press an item (or tap item → tap favourite icon)
3. Navigate to favourites screen
4. **Verify**: The favourited item appears
5. `browser_take_screenshot(filename="flow-07-favourites.png")`

### Flow 8: End Run
1. Open settings from active run
2. Tap "End Run"
3. Confirm the dialog
4. **Verify**: Returns to home screen
5. `browser_take_screenshot(filename="flow-08-end-run.png")`

### Flow 9: Theme Switching
1. From home, start a new run (to have content on screen)
2. Open settings → theme picker
3. Tap a different theme
4. Tap "Use this theme"
5. **Verify**: Color palette changes visibly
6. `browser_take_screenshot(filename="flow-09-theme-switch.png")`

### Flow 10: Search in Browse
1. From active run, tap browse FAB
2. Tap the search field
3. Type a gun name (e.g., "Pistol")
4. **Verify**: Results filter to matching items
5. `browser_take_screenshot(filename="flow-10-search.png")`

## After Each Flow
- `browser_console_messages(level="error")` — check for errors
- Record any errors with the flow name

## Pass Criteria
- All 10 flows complete without errors
- State changes are visible and correct
- Zero console errors
- Navigation works smoothly between screens

## Failure Handling
- **Item not found**: Use `browser_find(text="item name")` to locate it
- **Button not tappable**: Use `browser_snapshot` to get the accessibility tree and find the correct ref
- **State not updating**: Wait a moment with `browser_wait_for(time=1)` then re-snapshot
