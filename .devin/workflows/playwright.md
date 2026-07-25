---
description: Playwright UI testing for GungeonMate — build Flutter web, serve locally, test all screens and interactions
---

# Playwright UI Testing for GungeonMate

Flutter compiles to web (`flutter build web`), which means we can use the Playwright MCP tools to automate end-to-end UI testing — navigating screens, tapping buttons, verifying content, capturing screenshots, and checking the console for errors.

## Prerequisites

1. **Flutter web build** — the app must be compiled for web:
   ```
   flutter build web --release
   ```
   Output lands in `gungeon_mate/build/web/`.

2. **Local server** — serve the build directory:
   ```
   cd gungeon_mate/build/web
   python -m http.server 8099
   ```
   The app is then available at `http://localhost:8099`.

3. **Playwright MCP tools** — the IDE has two Playwright MCP servers available (`mcp0_browser_*` and `mcp3_browser_*`). Use either one.

## Available Playwright Tools

| Tool | Purpose |
|------|---------|
| `browser_navigate` | Go to a URL |
| `browser_snapshot` | Capture accessibility tree (better than screenshot for interaction) |
| `browser_take_screenshot` | Capture visual screenshot |
| `browser_click` | Click an element |
| `browser_type` | Type text into a field |
| `browser_fill_form` | Fill multiple form fields |
| `browser_press_key` | Press a keyboard key |
| `browser_find` | Search the page for text |
| `browser_console_messages` | Get console output (errors, warnings) |
| `browser_network_requests` | Inspect network traffic |
| `browser_evaluate` | Run JavaScript in the page |
| `browser_wait_for` | Wait for text to appear/disappear |
| `browser_resize` | Set viewport size (use mobile dimensions) |
| `browser_tabs` | Manage browser tabs |

## Mobile Viewport Setup

GungeonMate is a mobile app. Always set the viewport to mobile dimensions before testing:

```
browser_resize(width=390, height=844)  // iPhone 14 Pro
```

## Test Workflows

### 1. Quick Smoke Test (`/playwright-smoke`)

Verify the app loads, renders the home screen, and has no console errors.

1. Build web: `flutter build web --release`
2. Serve: `python -m http.server 8099` in `build/web/`
3. Navigate: `browser_navigate(url="http://localhost:8099")`
4. Resize: `browser_resize(width=390, height=844)`
5. Wait: `browser_wait_for(text="Gungeon")` or similar app title
6. Snapshot: `browser_snapshot()` — verify home screen rendered
7. Console check: `browser_console_messages(level="error")` — must be empty
8. Screenshot: `browser_take_screenshot(type="png", scale="css")`
9. **Pass criteria**: App loads, home screen visible, zero console errors

### 2. Full Screen Tour (`/playwright-screens`)

Navigate through every screen and capture screenshots.

1. Start from home screen
2. Tap "Start New Run" → character select screen → screenshot
3. Select a character → active run screen → screenshot
4. Tap browse FAB → browse screen → screenshot
5. Tap a gun/item → item detail screen → screenshot
6. Tap back → active run → tap synergies → synergies overview → screenshot
7. Tap back → active run → tap stats → stats detail → screenshot
8. Tap back → active run → tap shrine → shrine picker → screenshot
9. Tap back → active run → open settings → settings screen → screenshot
10. Tap theme picker → theme picker screen → screenshot
11. Tap back → back → back → home
12. **Pass criteria**: Every screen renders without errors, all screenshots captured

### 3. Theme Cycling Test (`/playwright-themes`)

Cycle through all themes and verify each renders correctly.

1. Navigate to settings → theme picker
2. For each theme:
   a. Tap the theme card
   b. Tap "Use this theme"
   c. Wait for transition
   d. Screenshot
   e. Verify no console errors
3. Return to default theme
4. **Pass criteria**: All themes apply without errors, screenshots show distinct color palettes

### 4. Feature Flow Test (`/playwright-features`)

Test core feature interactions.

1. **Start a run**: Home → Start New Run → Select character → Verify active run shows character
2. **Add items**: Active run → Browse → Tap item → Add to inventory → Verify it appears in active run
3. **Add guns**: Active run → Browse → Tap gun → Add to inventory → Verify it appears
4. **Check synergies**: Active run → Synergies → Verify synergies page shows items
5. **Adjust stats**: Active run → Tap coolness/curse → Adjust → Verify value changes
6. **Use shrine**: Active run → Shrine → Tap shrine → Activate → Verify curse/coolness adjusted
7. **Favourites**: Browse → Long-press item → Favourite → Go to favourites → Verify item appears
8. **End run**: Settings → End Run → Confirm → Verify returns to home
9. **Pass criteria**: All interactions complete without errors, state changes visible

### 5. Console Error Scan (`/playwright-errors`)

Navigate the entire app and collect any console errors.

1. Navigate to home
2. Use `browser_snapshot` to find all interactive elements
3. Systematically tap every visible button/link
4. After each navigation: `browser_console_messages(level="error")`
5. Record any errors with the screen that produced them
6. **Pass criteria**: Zero console errors across all screens

### 6. Visual Regression (`/playwright-visual`)

Capture baseline screenshots for visual comparison.

1. Set mobile viewport
2. For each screen, capture a full-page screenshot:
   - Home screen
   - Character select
   - Active run (with items)
   - Browse (guns tab, items tab, all tab)
   - Item detail (gun)
   - Item detail (item)
   - Synergies overview
   - Stats detail (coolness)
   - Stats detail (curse)
   - Shrine picker
   - Settings (each tab)
   - Theme picker
   - Favourites (empty + populated)
3. Store screenshots in `gungeon_mate/test/screenshots/`
4. **Pass criteria**: All screenshots captured, can be diffed against future runs

## Tips for Flutter Web + Playwright

- **Flutter web renders to a canvas** — `browser_snapshot` sees the accessibility tree, not DOM elements. Use `browser_find` to locate text, then click via coordinates or accessibility refs.
- **Flutter web uses CanvasKit** by default — it's heavier but more accurate. For faster test runs, use `--web-renderer html` (if still supported).
- **Text finding** — Flutter renders text as accessible nodes. `browser_find(text="Start New Run")` should work.
- **Clicking** — Use the `target` ref from `browser_snapshot` or `browser_find` results.
- **Waiting** — Flutter async operations (data loading) need `browser_wait_for` with visible text.
- **Console errors** — Flutter web logs Dart errors to the browser console. Check after every navigation.
- **Mobile dimensions** — Always use `browser_resize` to mobile dimensions (390x844 or similar) since the app is designed for mobile.
