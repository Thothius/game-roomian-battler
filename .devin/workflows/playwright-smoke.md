---
description: Quick smoke test — build Flutter web, serve, verify app loads with no errors
---

# Playwright Smoke Test

Quick verification that the app loads and renders without errors.

> **Agent coordination:** During the web build, update **Last board update** in
> `AGENT_STATUS.md` so stale detection doesn't fire on you.

## Steps

### 1. Build Flutter Web
```bash
flutter build web --release
```
Run in `X:\GungeonMate\gungeon_mate`. Non-blocking — poll with `command_status` until done.

### 2. Serve Locally
```bash
cd gungeon_mate/build/web
python -m http.server 8099
```
Non-blocking. The server stays running for the test session.

### 3. Navigate & Resize
- `browser_navigate(url="http://localhost:8099")`
- `browser_resize(width=390, height=844)`

### 4. Verify Load
- `browser_wait_for(text="Gungeon", time=10)` — wait up to 10s for app to render
- `browser_snapshot()` — capture accessibility tree, verify home screen visible

### 5. Console Error Check
- `browser_console_messages(level="error")` — must return empty

### 6. Screenshot
- `browser_take_screenshot(type="png", scale="css", filename="smoke-test.png")`

## Pass Criteria
- App loads at `http://localhost:8099`
- Home screen renders with visible content
- Zero console errors
- Screenshot captured

## Failure Handling
- **Blank page**: Check if Flutter web build completed. Check console for missing assets.
- **Console errors**: Record errors, report to Coder for fixing.
- **Timeout**: Try `--web-renderer html` flag or increase wait time.
