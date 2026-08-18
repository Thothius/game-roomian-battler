# Agent Protocol v0.0.2 — Improvement Proposal

> **Status:** DECISIONS LOCKED — all 20 design questions answered by the user
> on 2026-08-18. Ready for Maintainer to apply patches one-per-session. No rule
> files (`AGENTS.md`, `AGENT_STATUS.md`, `.windsurfrules`) are modified yet —
> first patch lands on explicit go-ahead.
>
> **Author:** Coder (Design Specialist), drafted from observed friction in the
> 2026-08-12 → 2026-08-18 Bullet Hell Edition + Active Run Rework sessions.
>
> **Scope:** Targeted patches to the existing AC1–AC6 + Safety S1–S10 + Bug B1–B4
> framework. Additive only — no existing rule is weakened or removed.

---

## Background

The current protocol (v0.0.1, encoded in `AGENTS.md`) has held up well: 56 bugs
tracked, 20 task-queue items cleared, three parallel branches merged cleanly,
zero data-loss incidents since the Safety rules were written. The friction
points below are real but narrow — they don't justify a rewrite, just surgical
patches.

Each friction point is documented with: **evidence** (what actually happened),
**root cause** (which existing rule gap allowed it), and **proposed patch**
(the exact rule edit, ready to apply on approval).

---

## Friction Point 1 — `master_plan.md` referenced but never created

### Evidence
- The orchestration directive in the system prompt configuration declares
  `master_plan.md` as the "immutable source of truth" with a slot matrix +
  task queue + protocol upgrade tracker.
- The file does not exist on disk. The real coordination file is
  `AGENT_STATUS.md`, which has the proven AC1–AC6 + S1–S10 + B1–B4 framework
  and a 20+ row session log.
- Agents have been correctly ignoring the missing `master_plan.md` and
  coordinating via `AGENT_STATUS.md` — no incidents resulted, but the gap
  between documented protocol and actual protocol is itself a liability.

### Root cause
The directive was authored top-down without reconciling against the existing
`AGENT_STATUS.md` board. Two "sources of truth" can't coexist — one will drift.

### Proposed patch
**Do NOT create `master_plan.md`.** Instead, amend the orchestration directive
to bind to the existing file. Concretely:

1. The system prompt configuration's `<state_file>` should reference
   `AGENT_STATUS.md`, not `master_plan.md`.
2. Add a one-line note to the top of `AGENT_STATUS.md` (above the existing
   header) clarifying its role as the **single canonical coordination file**
   for the triple-worker protocol — slot matrix, task queue, session log,
   and protocol upgrade notes all live here.
3. The "Protocol Upgrade & Revision Tracker" concept (from the directive)
   maps onto a new lightweight section at the bottom of `AGENT_STATUS.md`:
   `## Protocol Revision Log` — append-only, one row per approved patch
   (`| Version | Date | Patch summary | Approved by |`).

**Why not create `master_plan.md`:** It would duplicate the slot matrix and
task queue that already live in `AGENT_STATUS.md`, and the duplication would
drift within one session. The existing file is battle-tested; the directive
should conform to it, not the other way around.

---

## Friction Point 2 — Stale-slot churn from a single heartbeat field

### Evidence
- 2026-08-17: Slot 1 held by Maintainer, last board update 2026-08-16 18:30
  (>24h stale). User confirmed takeover.
- 2026-08-18: Slot 3 held by Coder (Design Specialist), last board update 09:50
  vs real clock 09:24 — flagged as stale-takeover when the branch HEAD had
  advanced but no rework code was written yet. User confirmed takeover.
- Two stale-takeovers in 48h. Both were legitimate (the slots were genuinely
  dead), but the threshold logic is brittle: a single `Last board update`
  timestamp conflates "agent is editing code and forgot to bump the board"
  with "agent crashed."

### Root cause
AC6 uses one field (`Last board update`) for two different signals:
- "I am alive and working" (heartbeat)
- "I recently changed the board" (audit trail)

A long edit cycle on a single file (e.g. 40 min heads-down on
`active_run_screen.dart`) produces a stale-looking board even though the
agent is healthy. The 30-min threshold then triggers a false-positive
stale-takeover prompt.

### Proposed patch
**Split the single timestamp into two fields.** Edit the Slot table schema
in `AGENT_STATUS.md` and AC2/AC6 in `AGENTS.md`:

**Current slot fields:**
```
| **Last board update** | <timestamp> |
```

**Proposed slot fields:**
```
| **Last board update** | <timestamp>   |  ← when the board itself was last edited (audit)
| **Last heartbeat**    | <timestamp>   |  ← when the agent last did any work (alive signal)
```

**AC2 (proposed addition):**
> Update **Last heartbeat** when you start editing a file and when you finish
> it (two bumps per file). This is a 5-second edit. **Last board update** only
> changes when you actually modify `AGENT_STATUS.md`.

**AC6 (proposed rewrite of the threshold logic):**
> - Check **Last heartbeat** first — if recent (< 30 min ago), the agent is
>   likely still active even if `Last board update` is older. Do not claim.
> - If **Last heartbeat** is more than 30 min old AND **Last commit** is empty
>   or also stale, the slot is likely dead. Proceed with the user-confirmation
>   takeover as today.
> - There is **no hard cap** on board staleness when heartbeat is recent —
>   an alive agent with a stale board is sloppy but not dead. Do not claim.

**Cost:** One extra column per slot. No new files. The 5-second heartbeat
edit is strictly easier than the current "update the whole board" pressure.

---

## Friction Point 3 — `app_theme.dart` is a repeated AC4 collision point

### Evidence
`app_theme.dart` has been touched by, or blocked, at least 5 distinct work
items in the last week:
- BUG-038 (Unicorn theme particles)
- Task 6 (Stat-group tag upgrade — `ThemeFlair` fields)
- Task 7 (Quick theme selection — particle defaults map)
- Active Run Rework Phase 1 (`RunDisplayMode` + `VisualPrefs` fields)
- Experience Studio (user WIP — glow color/effect rows)

Two of the stale-takeovers trace back to this file: an agent claims work that
requires `app_theme.dart`, another agent also needs it, AC4 forces
serialization, and the second agent goes idle long enough to look stale.

### Root cause
AC4 treats all files identically. But `app_theme.dart` is a **shared core** —
it holds `ThemeFlair` (theme palette) + `VisualPrefs` (persisted user prefs) +
`AppTheme.notifier` (rebuild trigger). Almost any visual feature touches it.
Treating it like a normal "Files in progress" entry causes unnecessary
serialization and stale-slot pressure.

### Proposed patch
**Promote `app_theme.dart` (and one or two other hot files) to a dedicated
"Shared Core" coordination tier.** Add a new rule AC7 and a board section:

**New `## Shared Core Files` section in `AGENT_STATUS.md`:**
```
## Shared Core Files

Files that many features touch. Editing one requires:
1. Announce in your slot's "Files in progress" (as today).
2. Post a one-line intent in the Shared Core row below (what field/section
   you're touching).
3. Keep the edit window short — extract new logic to a sibling file when
   possible, don't park WIP here.

| File | Current editor | Intent | Since |
|------|----------------|--------|-------|
| lib/services/app_theme.dart | _(none)_ | — | — |
| lib/widgets/particle_engine.dart | _(none)_ | — | — |
| lib/providers/run_provider.dart | _(none)_ | — | — |
| lib/widgets/theme_overlay.dart | _(none)_ | — | — |
```

**New AC7 in `AGENTS.md`:**
> ### AC7. Shared Core files require announced intent
> - The board's `## Shared Core Files` section lists files that many features
>   touch (initial list: `lib/services/app_theme.dart`,
>   `lib/widgets/particle_engine.dart`, `lib/providers/run_provider.dart`,
>   `lib/widgets/theme_overlay.dart`).
> - Before editing a Shared Core file, claim it in that section (file, your
>   name, one-line intent, timestamp). This is in addition to AC1/AC2.
> - Other agents MUST NOT edit a Shared Core file while it's claimed — same
>   rule as AC4, but the claim is visible in a dedicated section so it can't
>   be missed in a long Files-in-progress list.
> - Keep the edit window short. If you're adding a new persisted pref, add
>   the field + setter + persist line and stop — don't bundle unrelated
>   changes into the same edit.
> - Release the claim (set editor back to `_(none)_`) the moment your edit
>   is committed, not at session end.
> - **Adding a file to the Shared Core list requires user approval** — don't
>   silently expand the locked set.

**Why a tier instead of just being more careful:** The problem isn't care, it's
visibility. A 20-row Files-in-progress list across 3 slots makes it easy to
miss that someone has `app_theme.dart`. A dedicated 2-row section is
impossible to miss.

**Cost:** One new rule, one new board section, ~2 hot files initially. No
new files. The "keep the edit window short" guidance is the real fix — the
tier just makes the coordination visible.

---

## Friction Point 4 — User WIP tracked only in prose

### Evidence
- 2026-08-18: `experience_studio_screen.dart` is being actively edited by the
  user (glow effect/color rows converted to `Wrap`, named color swatches,
  animated containers). The only record that this file is off-limits is a
  prose note in Slot 3's "Uncommitted changes" field: `"user has WIP on
  experience_studio_screen.dart + untracked .commit_msg.txt — off-limits per
  AC4"`.
- An agent skimming the board for "what can I touch" has to read every slot's
  free-text Uncommitted changes field to discover user WIP. That's fragile.

### Root cause
AC4 is written for agent-agent coordination, not user-agent coordination.
There's no dedicated place on the board for "the user is editing this file,
nobody touch it."

### Proposed patch
**Add a dedicated `## User WIP (off-limits)` section to `AGENT_STATUS.md`.**
Machine-readable, one row per file:

```
## User WIP (off-limits)

Files the user is actively editing. All agents MUST NOT touch these until
the user removes the row (or confirms handoff). This is AC4 for user work.

| File | Since | Note |
|------|-------|------|
| lib/screens/experience_studio_screen.dart | 2026-08-18 | Glow effect/color row rework |
```

**New AC4 addendum in `AGENTS.md`:**
> ### AC4 addendum — User WIP
> - The board's `## User WIP (off-limits)` section lists files the user is
>   actively editing. Treat these exactly like another agent's
>   "Files in progress" — do not touch.
> - Only the user adds rows to this section. An agent may *propose* adding a
>   row ("I see you have uncommitted edits to X — should I mark it
>   off-limits?") but never adds it unilaterally.
> - When an agent notices (via `git status` at session start) that a User WIP
>   file has been committed, the agent **asks** the user before removing the
>   row: "X is now committed — remove from User WIP?" No unilateral removal.
> - No staleness rule — rows stay until the user removes them or confirms
>   removal.
> - At pre-session sync (S5), if `git status` shows uncommitted changes in
>   a file not listed in User WIP, ask the user before touching it.

**Cost:** One new board section. No new rule files beyond the AC4 addendum
line. The section is user-owned — agents propose, user decides.

---

## Summary of Proposed Changes

| # | Friction point | Patch | Files touched on approval |
|---|----------------|-------|---------------------------|
| 1 | `master_plan.md` missing | Bind directive to `AGENT_STATUS.md`; add `## Protocol Revision Log` section | `AGENT_STATUS.md` (new section), system prompt config (state_file) |
| 2 | Stale-slot false positives | Split `Last board update` into `Last board update` + `Last heartbeat`; rewrite AC6 threshold logic | `AGENT_STATUS.md` (slot schema), `AGENTS.md` (AC2, AC6) |
| 3 | Shared Core file collisions | New Shared Core tier + AC7; dedicated board section (4 files: `app_theme.dart`, `particle_engine.dart`, `run_provider.dart`, `theme_overlay.dart`) | `AGENT_STATUS.md` (new section), `AGENTS.md` (new AC7) |
| 4 | User WIP invisible | New `## User WIP (off-limits)` board section + AC4 addendum | `AGENT_STATUS.md` (new section), `AGENTS.md` (AC4 addendum) |

**Total cost:** 2 new rules (AC7 + AC4 addendum), 3 new board sections, 1
schema split. No new files. No existing rule weakened.

---

## What This Proposal Does NOT Do

- **No `master_plan.md` creation.** The existing `AGENT_STATUS.md` is the
  coordination file; the directive should conform to it.
- **No "self-improving loop" or agent self-mutation.** Rule changes are
  authored as proposals, reviewed by the user, and applied by the Maintainer
  (per existing Maintainer domain: "AGENTS.md — rules enforcement, convention
  auditing (propose changes, user approves)"). Agents don't rewrite their own
  operating parameters at session close.
- **No new agent roles.** The 2-Coder + 1-Maintainer structure is unchanged.
- **No change to Safety S1–S10 or Bug B1–B4 in v0.0.2.** S6 (post-task
  bughunt) enforcement and the Ponytail "ONE runnable check" rule are
  flagged for v0.0.3 (see v0.0.3 Preview below) — not touched here.

---

## Approval & Rollout

On user approval, the Maintainer (per existing domain ownership of
`AGENTS.md`) applies the patches **one per session** (4 sessions total),
so each patch gets a full session of real use before the next lands:

1. **Session 1 — Friction Point 4** (User WIP section) — lowest risk,
   immediate benefit.
2. **Session 2 — Friction Point 1** (bind to `AGENT_STATUS.md`) — clears
   the documented-vs-actual protocol gap.
3. **Session 3 — Friction Point 2** (heartbeat split) — schema change,
   apply at a clean session boundary.
4. **Session 4 — Friction Point 3** (Shared Core tier) — largest
   behavioral change, apply last so agents can adjust.

Each patch is a **separate commit** to `AGENTS.md` / `AGENT_STATUS.md`
with message `Protocol v0.0.2 — <patch name>` (one commit per patch,
independently revertable). Log each in the new `## Protocol Revision Log`
section as it lands.

**Patch approval policy (decided):**
- **Behavioral changes** (new rules, threshold tweaks, schema changes)
  require user approval.
- **Editorial fixes** (typos, formatting, section reordering) the
  Maintainer can apply and log without explicit approval.
- **Any patch touching Safety S1–S10 or Bug B1–B4** always requires user
  approval, no exceptions.

---

## Resolved Decisions (User-Approved 2026-08-18)

All 20 design questions answered. Locked decisions:

| # | Question | Decision |
|---|----------|----------|
| Q1 | `master_plan.md` vs `AGENT_STATUS.md` | **Bind to `AGENT_STATUS.md`.** No `master_plan.md`. |
| Q2 | Protocol Revision Log archiving | **Keep forever.** No archiving. |
| Q3 | Patch approval policy | **Maintainer can approve minor** (editorial). Behavioral + S/B rules need user. |
| Q4 | Staleness signals | **Two fields: `Last board update` + `Last heartbeat`.** `Last commit` stays separate (handoff only). |
| Q5 | Heartbeat cadence | **Start + finish of file.** Two bumps per file. |
| Q6 | Stale threshold | **Keep 30 min** for `Last heartbeat`. |
| Q7 | Board stale cap | **No hard cap.** Heartbeat recent = alive, regardless of board staleness. |
| Q8 | Shared Core initial list | **All four:** `app_theme.dart` + `particle_engine.dart` + `run_provider.dart` + `theme_overlay.dart`. |
| Q9 | `theme_overlay.dart` confirm | **Confirmed** (via Q8). |
| Q10 | Shared Core edit window limit | **No hard limit.** Trust the agent to keep it short. |
| Q11 | Waiting agent behavior | **Pick a different task.** No prep, no scratch branch. |
| Q12 | Demote from Shared Core | **Maintainer can demote** (reversible; log in Revision Log). |
| Q13 | Auto-add User WIP rows | **Propose only, never auto-add.** Agent asks; user confirms. |
| Q14 | User WIP staleness | **No staleness rule.** Rows stay until user removes them. |
| Q15 | WIP removal on commit | **Agent asks, user confirms.** No unilateral edits to User WIP section. |
| Q16 | Rollout pace | **One patch per session** (4 sessions). |
| Q17 | Commit shape | **One commit per patch** (4 commits, independently revertable). |
| Q18 | Safety rule friction | **S6 (post-task bughunt) inconsistent** — v0.0.3 target. |
| Q19 | Ponytail friction | **"ONE runnable check" rule skipped** — v0.0.3 target. |
| Q20 | v0.0.3 target | **Test infrastructure.** |

---

## v0.0.3 Preview (Not Part of This Proposal)

Based on Q18 + Q19 + Q20, the next protocol proposal should tackle:

1. **S6 enforcement — post-task bughunt is inconsistent.** Some agents do
   a real bughunt (grep for missing `dispose()`, trace callers, paste
   `flutter analyze` output); others just run `flutter analyze` and call
   it done. v0.0.3 should define a minimum bughunt checklist tied to the
   type of change (UI = dispose/mounted check; data = integrity script;
   logic = caller trace) with proof-paste requirements sharpened.
2. **Ponytail "ONE runnable check" rule is routinely skipped.** Agents
   write non-trivial logic but don't leave a test or self-check behind.
   v0.0.3 should make the check mandatory at commit time (Maintainer
   verifies a check exists before approving the commit) or define a
   clearer "trivial" exemption so agents know when they can skip.
3. **Test infrastructure.** The Maintainer owns `test/` but it's thin —
   few regression tests exist. v0.0.3 could mandate a test per bugfix
   (one regression test per BUG-NNN fixed) and define a minimum test
   surface for new features.

These are **not** part of v0.0.2. They'll be drafted as a separate
`docs/protocol_v0.0.3_proposal.md` after v0.0.2 lands and gets a few
sessions of real use.
