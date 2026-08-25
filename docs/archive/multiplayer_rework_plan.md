# GungeonMate — Design Assessment & Multiplayer Rework Plan

> Created: Aug 2026, v1.9.27
> Part 1: Quality assessment of 3 approved reworks
> Part 2: Multiplayer lobby minimalist rework plan

---

## PART 1 — Assessment of 3 Approved Reworks

### Rework 1: Run Options Popup — Real Section Headers ✓

**Mockup quality: GOOD**

What the mockup does right:
- Replaces disabled buttons with styled text headers (accent color, uppercase, divider lines)
- Toggle switches give clear visual on/off state (green = on)
- "RUN TOOLS" title is clear and purposeful
- Sections are logically grouped: PANELS → NAVIGATION → ACTIONS → END SESSION
- End Session uses warning color (pink) to signal danger

Potential concerns:
- The popup will be taller with real headers + toggles — need to verify it fits in viewport on small screens
- Toggle switches are a new UI pattern not used elsewhere in the app — should match existing toggle style if any

**Verdict: Ready for implementation. May need scrollable wrapper for small screens.**

---

### Rework 2: Settings App Tab — Reorganization ✓

**Mockup quality: GOOD**

What the mockup does right:
- Three clear sections with labels: ACCOUNT & DATA, DEVELOPER, DANGER ZONE
- Dev Tools gets a warning icon (amber) to signal it's advanced
- Danger Zone uses pink/red icons — consistent with destructive action convention
- Event Log correctly grouped under ACCOUNT & DATA (it's a data view, not an action)
- Removing Add Co-op and Use Shrine from settings is correct — they're gameplay actions

Potential concerns:
- The tab is now shorter — there will be empty space below Danger Zone. That's fine (better than clutter)
- "Reset Character Loadout" name is clearer than "Reset The Marine" — good rename

**Verdict: Ready for implementation. Clean and well-organized.**

---

### Rework 3: Theme Picker — Section Labels + Taller Carousel ✓

**Mockup quality: GOOD (with the taller carousel improvement)**

What the mockup does right:
- 120px hero carousel is a major improvement — the old 50px area was too small to notice swipeability
- Left/right swipe arrows (‹ ›) on edges make it obvious you can browse
- Theme preview card inside carousel shows name, description, and color swatches
- Wide pill dot indicators (active = elongated bar) are more visible than tiny dots
- "← SWIPE TO BROWSE THEMES →" hint text is helpful for first-time users
- Section labels (PALETTE VARIANT, PARTICLE PRESET, COLOR SCHEMA, ANIMATION SPEED) make 24+ controls scannable

Potential concerns:
- 120px carousel + dots + hint = ~160px total at top. On a 900px viewport that's 18% — acceptable
- Color swatches inside the carousel card are a nice touch but need to pull actual palette colors per theme
- The hint text "← SWIPE TO BROWSE THEMES →" should probably disappear after first interaction (don't over-explain)

**Verdict: Ready for implementation. Best of the three reworks.**

---

## Overall Assessment of the 3 Reworks

**We did good.** All three reworks solve real problems without introducing new complexity:

| Rework | Problem Solved | Risk | Confidence |
|--------|---------------|------|------------|
| Run Options Popup | Disabled-button-as-header confusion | Low (just visual change) | HIGH |
| Settings App Tab | Mixed concerns in settings | Low (moves items, doesn't add) | HIGH |
| Theme Picker | Unlabeled controls + tiny carousel | Low (labels + taller carousel) | HIGH |

None of the reworks add new features or abstractions — they reorganize existing UI. That's the right approach. The Ponytail Rules apply: we're not building new things, just making existing things clearer.

---

## PART 2 — Multiplayer Lobby Rework Plan

### Current State Analysis

**Screenshot:** `docs/screenshots/13_multiplayer_lobby.png`
**File:** `lib/screens/multiplayer_lobby_screen.dart` (1300+ lines)

The current multiplayer lobby has these issues:

#### Problem 1: Too many sections on one screen
The lobby shows ALL of these at once:
- NICKNAME field
- CHOOSE ROLE (Main/Sidekick cards)
- YOUR CHARACTER / SIDEKICK picker
- CONNECTION PIN field
- Start Hosting / Find Host button
- Add Local Sidekick button
- LOAD SAVED SESSION (collapsible, with session cards)
- How to Play link (swipe to page 2)
- Page 2: Full multiplayer guide

That's 8+ sections crammed into one scrollable page. For a feature most users use rarely, this is overwhelming.

#### Problem 2: Role selection adds cognitive load
The Main/Sidekick split means the user has to understand the difference before they can start. The form changes based on role:
- Main: pick character, PIN auto-generated
- Sidekick: forced Cultist, must enter PIN

This is two different forms in one, which is confusing.

#### Problem 3: Connection PIN is always visible but context-dependent
The PIN field is shown for both roles, but:
- For Main: it's locked and auto-generated (why show it at all?)
- For Sidekick: it's required (but only relevant after picking Sidekick)

#### Problem 4: "Add Local Sidekick" is buried
The solo co-op button is below the main Start button, easy to miss. It's actually a great feature (play co-op without a second phone) but it looks like an afterthought.

#### Problem 5: Saved Sessions list is dense
Each saved session card shows: session name, duration, both characters, coolness/curse stats, item counts, delete button. That's 5+ data points per card. For a list that's collapsible, this is heavy.

#### Problem 6: "How to Play" guide is on a separate page
The guide is on page 2 of a vertical PageView. Users have to discover it by swiping down or tapping the "How to Play" link at the bottom. A 4-step guide should be more discoverable.

---

### Proposed Rework: Minimalist Multiplayer

**Goal:** Reduce from 8+ sections to 3 clear steps. Make it obvious what to do first.

#### New Layout — 3-Step Flow

```
┌─────────────────────────────┐
│ ← Multiplayer               │  ← standard AppBar
├─────────────────────────────┤
│                             │
│  STEP 1 — WHO ARE YOU?      │  ← section label
│  ┌───────────────────────┐  │
│  │ 👤 Nickname           │  │  ← single text field
│  │ "Player"              │  │
│  └───────────────────────┘  │
│                             │
│  STEP 2 — HOST OR JOIN?     │  ← section label
│  ┌─────────┐ ┌─────────┐    │
│  │  HOST   │ │  JOIN   │    │  ← two big buttons, not cards
│  │ 📡 Host │ │ 🔗 Join │    │
│  │ a game  │ │ a game  │    │
│  └─────────┘ └─────────┘    │
│                             │
│  STEP 3 — CHARACTER         │  ← section label (only for Host)
│  ┌───────────────────────┐  │
│  │ [avatar] The Marine   │  │  ← character picker (Host only)
│  │ Tap to change      ›  │  │
│  └───────────────────────┘  │
│                             │
│  ┌───────────────────────┐  │
│  │   ▶ START HOSTING     │  │  ← primary CTA (changes text)
│  └───────────────────────┘  │
│                             │
│  ── or ──                   │  ← divider
│                             │
│  ┌───────────────────────┐  │
│  │ 🤖 Solo Co-op         │  │  ← secondary option
│  │ Play with AI partner  │  │
│  └───────────────────────┘  │
│                             │
├─────────────────────────────┤
│  📖 How to Play  ›          │  ← guide link (opens dialog, not page)
├─────────────────────────────┤
│  💾 Saved Sessions (2)  ›   │  ← collapsed, opens separate screen
└─────────────────────────────┘
```

#### Key Changes

**1. Remove role cards → use two big buttons**
- Instead of Main/Sidekick "role cards" with icons + subtitles, use two simple buttons: HOST and JOIN
- Tapping HOST shows character picker + "Start Hosting" button
- Tapping JOIN shows PIN field + "Find Host" button
- Only one flow is visible at a time — no mixed form

**2. PIN field only shows for JOIN**
- Host: PIN is auto-generated, don't show the field at all
- Join: PIN field appears when JOIN is selected
- Removes the "locked field" confusion

**3. Character picker only shows for HOST**
- Host: pick your character (as current)
- Join: "You'll play as The Cultist" — simple text, no picker tile
- Removes the forced Cultist tile that takes space

**4. "Solo Co-op" promoted to clear secondary option**
- Shown below the primary CTA with a divider ("─ or ─")
- Clearer label: "Solo Co-op — Play with AI partner"
- No more "Add Local Sidekick" jargon

**5. "How to Play" opens a dialog, not a separate page**
- The 4-step guide opens as a modal dialog (like the Changelog dialog)
- No more hidden page 2 that users have to discover by swiping
- Dialog can be dismissed with one tap

**6. Saved Sessions → separate screen or bottom sheet**
- Instead of a collapsible list in the lobby, make "Saved Sessions (N)" a row that opens a dedicated screen or bottom sheet
- The lobby stays clean; saved sessions get their own focused view
- Each session card in the dedicated view can keep the rich info (characters, stats, items)

**7. Remove the vertical PageView**
- Currently the lobby is a 2-page vertical PageView (lobby + guide)
- With the guide as a dialog, the PageView is unnecessary
- The lobby becomes a single scrollable column — simpler, no hidden content

---

### Before/After Comparison

| Element | Current | Proposed |
|---------|---------|----------|
| Sections on screen | 8+ | 3 steps + 2 secondary |
| Role selection | 2 cards with icons/subtitles | 2 big buttons (HOST/JOIN) |
| PIN field | Always visible, locked for Main | Only visible for JOIN |
| Character picker | Shows for both roles (Cultist tile for Sidekick) | Only for HOST |
| Solo Co-op | Buried below Start button | Clear secondary option with divider |
| How to Play | Hidden page 2 (swipe to discover) | Dialog link, always visible |
| Saved Sessions | Collapsible list in lobby | Separate screen/bottom sheet |
| PageView | 2-page vertical | Single page (no PageView) |
| Total lines of UI | ~400 lines of build method | ~200 lines (estimated) |

---

### Implementation Notes

**Files to modify:**
- `lib/screens/multiplayer_lobby_screen.dart` — main rework

**What stays the same:**
- `MultiplayerConnectScreen` — the searching/connected screen is fine as-is
- `MultiplayerSession` service — no logic changes
- `SavedMpSession` model — no data changes
- All the connection/handshake logic — untouched

**What changes:**
- `build()` method — restructured into 3 steps
- Remove `_pageController` and PageView (no more page 2)
- `_buildGuideStep()` → becomes a dialog builder
- Saved sessions → extracted to a bottom sheet or separate route
- `_RoleCard` widget → replaced with simpler `_RoleButton`
- `_ForcedCultistTile` → replaced with simple text
- `_PinField` → only rendered for JOIN mode

**What's new:**
- `_GuideDialog` widget — modal with the 4-step guide
- `_SavedSessionsSheet` widget — bottom sheet for saved sessions
- `_StepLabel` widget — "STEP 1 — WHO ARE YOU?" style labels

**Risk:** LOW
- No logic changes (connection, pairing, session save/load all untouched)
- Pure UI reorganization
- Can be verified by navigating the lobby and confirming all flows still work

---

### Mockup

A visual mockup of the proposed multiplayer lobby will be added to the redesign comparison gallery after this plan is approved.
