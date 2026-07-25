---
description: Pre-session sync — check git state, review recent work, load context before starting new work
---

# Pre-Session Protocol

Before starting any new feature work in a session, complete these steps in order:

## Step 0: Claim an Agent Slot (AC1)

1. **Read `AGENT_STATUS.md`** (project root)
2. Find an empty slot (Agent field is `_(none)_`)
3. If all slots are full, check for stale sessions (AC6). If none are stale, STOP and ask the user.
4. Set **Agent** to your role, fill in **Session started**, **Last board update**, **Working on**
5. If claiming a task from the Task Queue, check the **Blocked by** column — don't claim if the blocking task isn't DONE
6. If another agent is active in a different slot, create a git branch (AC5): `git checkout -b <agent-type>/<task-slug>`
7. **Self-check:** Re-read `AGENT_STATUS.md` and verify your slot is actually filled. Only then proceed.
8. Leave **Files in progress** and **Uncommitted changes** empty (fill as you go)
9. This is step zero — before everything else below

## Step 1: Load Full Context

1. **Load your primary file(s) in full** — no offset/limit for files >1000 lines:
   - Coder: `read_file` the files you'll be working with — start with `lib/main.dart`, then specific modules
   - Maintainer: `read_file` the files that were recently modified (check `git log` and `git diff`)
2. **Load your own rules**: `read_file(.devin/workflows/bot-[your-role].md)`

## Step 2: Sync & Review

1. **Check recent activity** — `git log -5 --oneline` to see what was done last
2. **Check working tree** — `git status` for uncommitted changes
3. **Review uncommitted changes** — `git diff` to see what's pending
4. **Check memories** — review any system-retrieved memories for context from previous sessions
5. **Identify which agent made recent changes** — commit prefixes (`[Coder]`, `[Maintainer]`) tell you who did what
6. **Read the bug tracker** — `read_file(docs/bug_tracker.md)` to see all known open bugs. If you're about to work on a file with an OPEN bug, mention it to the user before proceeding. (See AGENTS.md → Bug Tracker Rules B3)

## Step 3: Bughunt Completed Tasks

For each task completed in the previous session:

1. **Re-read the code** — Load the modified files and trace the full execution path
2. **Check edge cases**:
   - Null/undefined inputs
   - Empty lists / empty data
   - Disposed controllers still being referenced
   - State transitions (run start → active → end)
   - Pre-existing bugs that new code interacts with
3. **Verify integration points**:
   - Does the new code interact correctly with existing systems?
   - Are there other callers of modified functions that could break?
   - Do UI refresh functions show correct data after state changes?
4. **Run static analysis**: `flutter analyze` on modified files
5. **Run tests** (if they exist): `flutter test`
6. **Add regression tests** for non-trivial logic (per Ponytail Rules)

## Step 4: Verify Git State

Check that the repository is in a clean, expected state:
- `git status` — should show clean working tree (or known uncommitted changes)
- `git log -3 --oneline` — verify recent commits match expectations
- If something looks wrong (unexpected files, missing commits), investigate before starting work

## Step 5: Update TODO List

- Mark bughunt items as completed
- Add any newly discovered bugs to the todo list
- Set the next feature task as in_progress
