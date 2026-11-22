# Free-App Positioning Report + Bug Report System Masterplan

> Authored 2026-11-25 (CORE / Slot 2). Two parts: **A)** the legal/positioning
> report on shipping free with no ads/server + donation links; **B)** the
> in-app bug-report system masterplan (context-aware reporter → Gmail →
> free pipeline).

---

## Part A — The "free, local, no-server" angle (report)

### What the model actually is

- **Free forever, no ads, no analytics, no account, no server.** The app
  is 100% local — all game data ships in the APK, MP is device-to-device
  (Nearby Connections), nothing phones home.
- **Donation links** (Ko-fi / Patreon) for "keep developing it" — tips,
  not payment for the app.

### Why this is the *right* structure for this app

1. **Legal exposure drops sharply.** Fan/companion apps are the most
   tolerated category on both stores. "Free + no tracking + no server" is
   the easiest possible posture to defend: we're not competing with
   Dodge Roll, not monetizing their IP, not harvesting data. A DMCA
   complaint is still *possible* (assets/text — see below), but the
   "commercial infringement" argument is gone; worst case is usually a
   takedown, not a lawsuit.
2. **Privacy is a feature, not a burden.** No data collection → no
   privacy policy legally required, trivial Play data-safety form
   ("no data collected"), no GDPR surface. That's a *marketing* bullet
   for the Reddit post too.
3. **Donations ≠ sales.** Ko-fi/Patreon tips don't make the app a
   commercial product in any meaningful legal sense — they're the
   standard fan-project model. Low risk. (Keep the links clearly
   "support development", never "buy the app".)
4. **Community goodwill.** "I'm building this because it's fun, here's a
   bug button" is exactly the tone that gets upvoted on r/Gungeon and
   forgiven on IP grounds.

### What free does NOT fix (honest)

- **Ripped sprites + verbatim descriptions/wiki text** are still
  copyright exposure — free reduces the *stakes*, not the *violation*.
  Store listing can still be DMCA'd. Mitigation order if we ever go to
  stores: replace sprites → paraphrase descriptions → keep names/stats
  (facts/rules aren't copyrightable).
- **Trademark**: don't put "Enter the Gungeon" in the store title;
  "GungeonMate" + "companion for Enter the Gungeon" in the description
  is nominative fan-app usage — normal, low risk, add "unofficial,
  not affiliated" disclaimer.
- Sideload APK (current plan) has **zero gatekeeping** — all of this
  only matters when/if we list on Play/App Store.

### Verdict

Ship it free, local, donation-supported. It's the correct risk posture,
the best marketing angle, and it makes the bug-report pipeline (below)
the natural feedback loop for the Reddit push.

---

## Part B — Bug Report System masterplan

### Goal

Every screen gets a bug-report affordance. Tapping it opens a panel that
**already knows where you are** — category + entity auto-filled — so the
user only writes what went wrong and hits send. Reports land in a
dedicated Gmail, auto-parsed into a Sheet = one triage list. Free,
no server, works offline-ish (mailto needs *an* email app, not our infra).

### Architecture

```
BugReportButton (icon)  →  BugReportSheet.show(context, BugReportContext)
                              │ auto-fills: category, entity, screen, version
                              │ user types notes → [Send] [Copy]
                              ▼
                    mailto:gungeonmate.bugs@gmail.com
                    subject: [GM|Items|Gun Name|v3.7.0]
                    body:   ---NOTES--- + ---CONTEXT--- block
                              │
                    Gmail filter/label → Apps Script → Google Sheet
                    (date, version, platform, category, entity, notes, status)
```

### Components

1. **`BugReportContext`** (model, `lib/models/bug_report.dart`):
   `category` (Bug / Content error / Suggestion / Other — auto-set per
   screen), `entity` (item/gun/synergy name etc., nullable), `screen`
   (route/screen name), plus auto-appended `appVersion`, `platform`,
   `device` (via `device_info_plus` or `Platform`), timestamp.
2. **`BugReportSheet`** (`lib/widgets/bug_report/bug_report_sheet.dart`):
   bottom sheet matching app chrome (flair-driven, skeuo-aware). Shows
   read-only context chips (CATEGORY / LOCATION / ITEM) so the user sees
   what's attached, one multiline TextField ("What happened?"), SEND +
   COPY buttons. Validates non-empty notes.
3. **`BugReport` service** (`lib/services/bug_report.dart`):
   - `buildMailto(context)` → `Uri(scheme:'mailto', path: kBugReportEmail,
     query: {subject, body})` launched via `url_launcher` (already a dep).
   - Subject format: `[GM-BUG v3.7.0|Items|Gunknight Bullets]` — pipe-
     delimited, parseable by the Apps Script.
   - Body: user notes first, then `---` + context block (version,
     platform, device model, screen, entity, timestamp).
   - `copyReport()` fallback: `Clipboard.setData` — for users with no
     email app; sheet shows "copied — paste it anywhere" snackbar.
   - Optional second fallback: `share_plus` share sheet (already a dep)
     — lets gamers send via Discord/WhatsApp directly. Cheap to add.
4. **`BugReportButton`** — small `Icons.bug_report_outlined` icon button,
   accent-colored ("stands out" per request), consistent 44px target,
   tooltip "Report a bug". Two variants: `appBar` action style and
   `sheetRow` style for lists.

### Entry-point matrix (context auto-fill)

| Surface | Category | Entity auto-fill |
|---|---|---|
| Active-run gear sheet — bug row **before Settings**, accent icon | Bug | current floor/character if cheap |
| Item detail (AppBar action) | Content error | item name |
| Gun detail | Content error | gun name |
| Synergy detail | Content error | synergy name |
| Ammonomicon detail | Content error | entry name |
| Gungeoneer detail | Content error | character name |
| Stats detail | Bug | stat name |
| Dice roller | Bug | — |
| Quiz (home + session) | Bug / Content error | question/chest if available |
| Cool & Curse | Bug | — |
| Settings | Bug / Suggestion | section if opened from one |
| Experience Studio | Bug / Suggestion | current tab |
| Main menu (small bug icon near version?) | Bug | — |
| MP lobby / connect | Bug | session state |

Rule: **the button lives where the bug is** — detail views get AppBar
actions; tool screens get a header icon; the gear sheet gets a dedicated
accent row. Category defaults per surface but is user-changeable in the
sheet (dropdown: Bug / Content error / Suggestion / Other).

### Email pipeline (all free, no server)

1. **User creates** `gungeonmate.bugs@gmail.com` (or similar).
2. App hardcodes it as `kBugReportEmail` (one const, easy to change).
3. **Gmail filter** → apply label `bug-reports` (one-time setup, doc it).
4. **Google Apps Script** (~40 lines, bound to that account, trigger:
   on new labeled email) parses `[GM-BUG vX|Cat|Entity]` subject +
   context block → appends row to a **Google Sheet** = the single triage
   list. Columns: `received, version, platform, device, category,
   entity, screen, notes, sender, status, fixed-in`.
5. We review the Sheet; status column tracks new → triaged → fixed →
   shipped-in-version. Sheet link shared with co-devs.

Script is committed to `tools/bug_report_pipeline.gs` with setup notes —
I write it, user just creates the Gmail + pastes it into script.google.com.

### Privacy note (put in sheet footer subtly)

"Sends app version + device info + what you type. No account, no
tracking." — accurate and reassuring.

### Phases

- **BR1 — core**: model + `BugReportSheet` + mailto builder + copy
  fallback + `BugReportButton`. Unit-testable URI generation.
- **BR2 — entry sweep**: gear-sheet row (before Settings) + AppBar
  actions on the 6 detail screens + dice/quiz/stats/settings/studio/menu.
- **BR3 — pipeline**: user creates Gmail; I ship `tools/bug_report_
  pipeline.gs` + `docs/BUG_REPORT_SETUP.md`; test end-to-end with a real
  send.
- **BR4 — polish (optional)**: screenshot attach via share_plus,
  dedup hint, "known issues" link in sheet, Sheet→changelog workflow.

### Open questions for user

- Gmail address to use (need it before BR3; can hardcode placeholder
  until then).
- Bug icon color: accent (theme primary) vs. warning amber — recommend
  accent for theme-reactivity, amber reads more "alert". Pick one.
- Include screenshot button in v1? (share_plus makes it ~free; mailto
  can't attach — would need share-sheet path instead. Recommend: skip
  v1, add in BR4.)
