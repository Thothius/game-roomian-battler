---
description: Post-session wrap — analyze, test, commit, document. Run before ending a session or switching agents.
---

# Post-Session Protocol

Run this before ending a session or switching to a different agent. This ensures your work is committed, tested, and discoverable by the next agent.

## Mid-Session Agent Switch

When switching from Coder to Maintainer (or vice versa), do a **lightweight switch**:

1. **Commit your current work** — even if the task isn't fully done, commit with `[Agent] wip: description` so it's safe
2. **Note uncommitted state** — if you have experimental changes that aren't ready to commit, note them in memory
3. **Release your slot (AC3)** — update `AGENT_STATUS.md`: set Agent to `_(none)_`, fill Last commit, clear working fields, append structured handoff row to session log
4. **Switch** — user invokes the new agent's slash command (e.g. `/bot-maintainer`)
5. **Incoming agent reads `AGENT_STATUS.md`** (AC1) — finds an empty slot, claims it, sees the last handoff in the session log

The full post-session protocol below is for **ending a session entirely** (closing the IDE, ending the conversation).

## Step 1: Release Agent Slot (AC3)

Update `AGENT_STATUS.md`:
- Set **Agent** to `_(none)_`
- Update **Last board update** to current timestamp
- Fill **Last commit** with SHA + message
- Clear **Working on**, **Files in progress**, **Uncommitted changes**
- If you have WIP that can't be committed, note it under **Uncommitted changes** with `WIP:` prefix
- Append a structured handoff row to the Session Log with columns: `Agent | Date | Branch | Commit | Task | Files | Status | Next | Watch out for`
- If you were on a feature branch (AC5), merge to master and delete the branch

## Step 2: Static Analysis & Test
1. `flutter analyze` on modified files — paste output, must pass with zero warnings
2. `flutter test` — run if tests exist, paste pass/fail counts
3. **Playwright UI test** — if UI/screens changed, run `/playwright-smoke` at minimum. For screen changes, run `/playwright-screens`. For feature changes, run `/playwright-features`. Paste console error counts.
4. Check: did you add tests for any non-trivial logic? (per Ponytail Rules)

## Step 3: Bughunt Your Own Work (Goal-Oriented, Proof-Based)
1. `grep_search` for patterns relevant to your changes — **paste result counts**:
   - Coder: missing `dispose()` in classes with controllers, missing `context.mounted` before overlays, unused imports
   - Maintainer: convention violations, stale test references, missing test coverage
2. Trace every caller of functions you modified — list them, confirm safe
3. Check edge cases: null inputs, empty lists, disposed controllers, state transitions
4. **Paste actual command outputs** — "analyzer passes" must include `flutter analyze` output, not just the claim

## Step 4: Update Bug Tracker (B1/B2)
1. **Found bugs during bughunt?** Add them to `docs/bug_tracker.md` under "Open Bugs" with next `BUG-NNN` ID, severity, file, lines, description, root cause, fix proposal. (See AGENTS.md → B1)
2. **Fixed bugs this session?** Move their entries from "Open Bugs" to "Fixed Bugs" in `docs/bug_tracker.md`. Add commit hash and date. Set status to `FIXED`. (See AGENTS.md → B2)
3. **Do NOT** log speculative findings. Only bugs you confirmed by reading the actual code.
4. **Do NOT** create bug lists in chat, memory, or other files — `docs/bug_tracker.md` is the single source of truth. (See AGENTS.md → B4)

## Step 5: Pre-Commit Verify (S9)
Before committing, verify:
- `git status` shows only your intended changes
- `flutter analyze` passes on modified files
- No stale uncommitted changes from previous sessions
- No unintended files staged

## Step 6: Commit
1. Stage all changed files
2. Commit with prefix: `[Coder]` or `[Maintainer]`
3. Commit message format: `[Agent] type: short description` (e.g. `[Coder] feat: add Winchester mini-game physics`)
4. If you have uncommitted experimental changes, commit them as `[Agent] wip: description`

## Step 7: Update Memory
1. `create_memory` for significant changes, new patterns, or architectural decisions
2. Update existing memories if they reference stale information
3. Tag appropriately: `coder`, `maintainer`, `gungeonmate`

## Step 8: Report
Summarize to the user:
```
Session Complete:
- Tasks done: [list]
- Files modified: [list]
- Commits: [SHA list]
- flutter analyze: PASS/FAIL
- flutter test: PASS/FAIL/skipped
- Handoffs: [list or "none"]
- Next steps: [suggestions]
```
