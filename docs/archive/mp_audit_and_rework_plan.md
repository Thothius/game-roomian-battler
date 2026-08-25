# Multiplayer Audit & Rework Plan

> **Author:** Slot 3 — Planner-Architect-Mockupper
> **Date:** 2026-08-24
> **Status:** ANALYSIS — awaiting user decision on rework scope
> **Files audited:** `multiplayer_session.dart` (2662 lines), `multiplayer_service.dart` (348 lines), `multiplayer_messages.dart` (425 lines), `paired_partners_store.dart` (117 lines), `multiplayer_lobby_screen.dart` (~2780 lines), `mp_request_listener.dart` (~460 lines)

---

## 1. Executive Summary

The MP system **works on paper but fails in the real world** because of three structural problems:

1. **A 2662-line god class** (`MultiplayerSession`) that fuses transport, protocol, state machine, persistence, UI-notifiers, and run-state coordination into one object. Every reconnect bug fix has been a patch on a patch — the code is now full of special-case guards (`_busyTransition`, `_wasDisconnected`, `_isReconnecting`, `_isPaused`, `_protocolError`, `_autoReconnectAttempts`, `_pairPersistedLocally`) that interact in ways nobody can fully reason about.

2. **A reconnect model that requires both devices to be actively scanning at the same moment**, with a 20-second search window and up to 30-second backoff between attempts. When one player walks out of range and comes back, the two devices' retry loops are almost never aligned, so they miss each other repeatedly. The user experiences this as "can't reconnect."

3. **Three overlapping persistence mechanisms** (`_persistSession`, `saveCurrentSession`, `tryRestorePersistedSession`) plus a manual "Saved Sessions" list. The user is expected to understand which one applies when, and the restore paths don't perfectly rebuild the coop slot's inventory — leading to "P2 having to add items again."

On top of that, there is a **hard bug**: the RE-PAIR button rejects paired partners because it validates the pairId (an 8-char hex string like `AB12CD34`) as a 4-digit numeric PIN. Paired partners literally cannot use RE-PAIR.

---

## 2. Root-Cause Analysis (the user's complaints, traced to code)

### 2.1 "FIX or Reconnect options do not work at all"

**Root cause:** The reconnect relies on `_lastRole` + `_lastCharacter` + `_pinCode` all being non-null and matching the peer. But:

- `cancel()` sets `_pinCode = null` and `_lastRole = null` → `canReconnect` returns false → RE-PAIR button is disabled (`onPressed: null`).
- For paired connections, the RE-PAIR screen (`_ReconnectScreen._doReconnect`) requires a 4-digit numeric PIN via `int.tryParse(pin) == null`. A pairId is hex, so **this validation always fails for paired partners**. The reconnect never fires.
- Even when reconnect does fire, it calls `stopAll()` → 800ms hardcoded "native radio cooldown" → `startAsMain/Sidekick`. If the peer isn't scanning at that exact moment (their 20s search window expired and they're in backoff), the search times out and the loop reschedules. Two independent retry loops with 20s windows + up to 30s backoffs have a low probability of overlapping.

### 2.2 "GF goes out of range and comes back, then we can't RC at all"

**Root cause:** When the peer drops, the watchdog fires after 30–60s (adaptive, gets *slower* after each successful reconnect — the opposite of what you want). Then:

- Both sides enter `disconnected` and start auto-reconnect with independent exponential backoff.
- Each attempt: `stopAll` → 800ms delay → start search → 20s search window → timeout → backoff (1s, 2s, 4s, 8s, 16s, 30s, 30s...).
- For the reconnect to succeed, both devices must be in their 20s search window simultaneously. With independent backoff timers, this is a coin-flip at best, and gets worse as backoff grows.
- There is no "persistent advertising" — the Main only advertises during a 20s window then stops. A Sidekick coming back into range 25s later finds nothing.

### 2.3 "The whole process is too messy — loading a saved game with P2 having to add items again"

**Root cause:** The snapshot protocol only sends **item names**, not full state. When a saved session is loaded via `loadSavedSession`, the RunState is restored from JSON — but the coop slot's inventory is only as complete as the last snapshot the peer sent before the save. If the save fired during a disconnect (when snapshots weren't flowing), the coop slot is stale or empty. The user then has to manually re-add P2's items.

Additionally, the "Saved Sessions" UI is a **separate manual flow** from the auto-restore-on-app-kill flow. The user doesn't know which one will fire, and they do different things.

### 2.4 "I want no MP logs, no errors or headache"

**Root cause:** The code maintains a 200-line `_connectionLogs` buffer that triggers `notifyListeners()` (coalesced) on every line. The connect screen shows a "DIAGNOSTIC CONSOLE" with these logs. Auto-reconnect logs 3-4 lines per attempt. This is developer-facing noise that the user sees and finds alarming.

### 2.5 "I want to RC instantly when user closes app or goes out of range"

**Root cause:** `tryRestorePersistedSession` runs on app start and re-enters the lobby — but it's a full `startAsMain/Sidekick` which goes through permissions, advertising setup, etc. There's no "instant" path. And when the app is killed mid-session, the other side's watchdog takes 30-60s to even notice, then starts the slow backoff loop.

---

## 3. What the User Actually Wants (restated)

1. **HOST** creates a game → gets a 4-digit PIN shown on screen.
2. **SIDEKICK** sees a **list of available games** (discovered endpoints) → picks one → enters the PIN → connects.
3. **Paired devices** connect with **one tap, no PIN** — the pairing mechanic already exists for this.
4. **Reconnect is instant and invisible** — when a peer comes back into range (after closing app, losing Wi-Fi, or walking away), the session resumes automatically with **no user action, no dialogs, no PIN re-entry**.
5. **No MP logs, no error dialogs, no manual save/load** — the system handles persistence and recovery silently.

---

## 4. Rework Options

### Option A — Surgical Fix (smallest scope, ~1-2 days)

**Keep the current architecture. Fix the broken paths.**

Changes:
1. **Fix the RE-PAIR pairId bug** — `_ReconnectScreen._doReconnect` should skip the 4-digit validation for paired connections (use `session.isPairedConnection`).
2. **Persistent advertising for Main** — when auto-reconnecting as Main, advertise continuously (no 20s search timeout) until the peer connects or the user cancels. Sidekick discovers in short bursts but retries on a tight 2s loop.
3. **Remove the adaptive watchdog slowdown** — keep watchdog at a fixed 15s. The current "gets slower after reconnect" logic is backwards.
4. **Hide the diagnostic console** behind a dev-mode flag (already have dev settings).
5. **Make the drop dialog dismissable** — let the user keep interacting with the run while disconnected (changes queue and sync on reconnect).
6. **Auto-restore coop inventory** — on reconnect, the first snapshot from the peer rebuilds the coop slot. Stop relying on saved-session restore for this.

**Pros:** Minimal risk, fast to ship, addresses the worst pain points.
**Cons:** Doesn't fix the structural complexity. The god class stays. The "available games list" feature isn't included. Future bugs will be patches on patches.

---

### Option B — Targeted Rework (medium scope, ~3-5 days)

**Split the god class + add the available-games list + fix reconnect.**

Changes (everything in Option A, plus):

1. **Decompose `MultiplayerSession` into focused components:**
   - `MpConnectionManager` — transport lifecycle, connect/disconnect/reconnect.
   - `MpProtocol` — message encode/decode/handle (hello, snapshot, gift, etc.).
   - `MpReconnectEngine` — auto-reconnect state machine, backoff, persistent advertising.
   - `MpPersistence` — session save/restore (single mechanism, not three).
   - `MpSession` — thin facade that wires the above together and exposes `ChangeNotifier` for the UI.

2. **Available-games list for Sidekick:**
   - `MultiplayerService` stops auto-connecting on endpoint found. Instead, it surfaces `MpEndpointFound` events with the endpoint name (which contains `nickname#PIN`).
   - The lobby shows a live list: "🎮 Brave Bullet Kin — PIN 1234". User taps one → enters/confirms PIN → connects.
   - For paired partners, the list auto-filters to endpoints matching a known pairId.

3. **Single persistence mechanism:**
   - Delete `saveCurrentSession` / `loadSavedSession` / `SavedMpSession` / the "Saved Sessions" UI.
   - Replace with one auto-save: the full `RunState` (both slots + coolness/curse/shrines) is written to a single key `mp.active_run` every 5s while connected, and on disconnect. On app start, if `mp.active_run` exists and `mp.session_active` is true, restore silently.
   - The coop slot's inventory is part of `RunState`, so it restores correctly — no more "P2 has to add items again."

4. **Invisible reconnect:**
   - Remove the non-dismissable drop dialog. Replace with a small status banner ("Reconnecting…") that doesn't block interaction.
   - Main advertises persistently during reconnect (no timeout). Sidekick discovers on a 3s on/off cycle. When they overlap, connection is immediate.
   - On reconnect, both sides send a hello + full snapshot immediately. The coop slot is rebuilt from the peer's snapshot — no saved-session load needed.

5. **Remove the diagnostic console** from the UI entirely (keep `_log` for dev-mode `print` only, gated by a flag).

**Pros:** Fixes the structural problem, delivers the requested UX (game list, instant reconnect, no logs), makes future maintenance sane.
**Cons:** Bigger change, touches the lobby UI significantly, needs careful testing of the reconnect state machine.

---

### Option C — Full Rebuild from Scratch (largest scope, ~1-2 weeks)

**Throw away `MultiplayerSession` and `MultiplayerService`. Build a clean, purpose-built MP layer.**

Design:
1. **`MpLink`** — a single class that owns one peer connection. States: `idle → advertising → discovering → connected → lost → (auto-recovering) → connected`. No "error" or "handshaking" sub-states exposed to UI — those are internal. The UI sees three states: `disconnected`, `connecting`, `connected`.

2. **Persistent discovery model:**
   - Main: advertises continuously while in a session. No search timeout. Cheap on battery because Nearby Connections uses BLE advertising (low power) until a connection forms, then switches to Wi-Fi Direct.
   - Sidekick: discovers in a tight loop (3s scan, 1s pause). When an endpoint is found, it's surfaced to the UI as a list item. Auto-connect only for paired partners (filtered by pairId). For PIN sessions, the user picks from the list.

3. **`MpSync`** — the state-sync layer. On connect, both sides send a full `MpStateSnapshot` (character + guns + items + coolness/curse/shrines). On any local change, send a delta. On reconnect, send a full snapshot again (not a delta) — this is the "instant resume" mechanism. The coop slot is always rebuilt from the peer's full snapshot, so there's no stale-inventory problem.

4. **`MpPairing`** — the one-time pairing flow, isolated from the session logic. Produces a `PairedPartner` record. Future connections use the pairId as the endpoint filter.

5. **`MpRecovery`** — owns the "peer came back" logic. When a connection drops:
   - Status → `lost` (UI shows a small "Reconnecting…" pill, does NOT block interaction).
   - Both sides keep their run state. No save/load needed — the state is in memory and survives the disconnect.
   - Main keeps advertising. Sidekick keeps scanning. When they overlap, `MpLink` reconnects, `MpSync` sends full snapshots, and the session resumes. Target: < 5 seconds from "back in range" to "synced."
   - If the app is killed: on restart, `MpRecovery` reads `mp.active_run` (full RunState, written every 5s), restores it, and re-enters advertising/discovery automatically. No lobby, no PIN, no user action.

6. **No logs in UI. No error dialogs for transient failures.** Errors only surface if the user needs to act (e.g., permissions denied, or both sides need to re-pair after an app uninstall).

7. **Protocol simplification:** Drop `MpPing`/`MpPong`/`MpSnapshot.tsMs`/`lastSeq` desync logic. Nearby Connections is a reliable ordered byte stream — we don't need application-level heartbeats or LWW timestamps. The transport itself signals disconnects. If we want a liveness check, a single 10s heartbeat with no desync logic is enough.

**Pros:** Clean, maintainable, exactly the UX the user wants, no legacy patches. 5x smaller codebase.
**Cons:** Largest effort. Must be tested thoroughly before shipping. Risk of regressions in edge cases (gifts, requests, dice, emotes) that the current code handles.

---

## 5. Recommendation

**Option B (Targeted Rework)** is the right balance. It delivers every feature the user asked for (game list, instant reconnect, no logs, paired no-PIN connect) without the risk and effort of a full rebuild. The god class gets decomposed into manageable pieces, making future bugs fixable instead of patchable.

Option A is tempting for speed but leaves the structural rot — we'll be back here in 3 months.
Option C is the "right" engineering answer but is overkill given that the protocol and message types are sound; the problem is the session/state-machine layer above them.

---

## 6. Decision Needed from User

1. **Which option?** A (surgical), B (targeted rework), or C (full rebuild)?
2. **Available-games list:** Should the Sidekick always see a list of discovered games, or only when no paired partner is available? (i.e., paired = one-tap, unpaired = browse list)
3. **Reconnect UX:** Confirm the desired behavior — "small non-blocking 'Reconnecting…' pill, user can keep using the app, session auto-resumes when peer returns." No modal dialog?
4. **Saved Sessions UI:** OK to remove the manual "Saved Sessions" list entirely? (Auto-save/restore replaces it.)
5. **Diagnostic console:** OK to remove from the UI entirely? (Keep logging gated behind a dev flag for actual debugging.)
