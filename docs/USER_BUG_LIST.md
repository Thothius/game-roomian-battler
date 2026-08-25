# User-Reported Bug List

> **Codeword: `bug list`** — say "bug list" and I'll append your notes here.
> Items are not acted on unless explicitly requested. Severity is user-assigned
> or TBD. Status tracks from report → triaged → fixed.

---

## Open

### U-001 — 08_char_select.png is a white/blank screenshot
- **Reported:** 2026-08-25
- **Source:** Playwright screenshot session
- **Notes:** "08 png seems white page. maybe accident." — likely captured
  the moment the page navigated to `about:blank` during the service-worker
  redirect issue. Not a real app bug; the screenshot should be re-captured
  in a clean session.
- **Severity:** Low (cosmetic — screenshot only)
- **Status:** Reported

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
- **Status:** Reported

---

## Resolved

_(none yet)_
