# MP Auto-Save / Reconnect System — Refined Spec

> **Status:** IMPLEMENTED — Specs 1-6 already shipped in prior sessions. Manual re-pair flow (Reconnection Hub + PIN display/entry + RE-PAIR button) implemented Jul 23, 2026.
> **Date:** July 21, 2026 (refined from July 5 draft) — updated Jul 23, 2026
> **Owner:** Coder implements, Maintainer verifies

## Current Infrastructure (Already Built)

The app has substantial MP reconnection plumbing. Here's what exists today:

### State Machine (`MpStatus` enum)
```
idle → searching → handshaking → connected → disconnected → error
                ↗                                  ↓
                  ←── auto-reconnect loop ←───────┘
```

### Auto-Reconnect Engine
- **Triggers:** `MpDisconnected` event OR watchdog (30s silence on heartbeat)
- **Backoff:** Exponential — 2s, 4s, 8s, 16s, 30s cap. Retries indefinitely.
- **Invariant:** Never gives up while the run is alive. Only user-initiated `cancel()` / `disconnect()` / `notifyEndRunAndCancel()` stops the loop.
- **Guard:** `_busyTransition` flag prevents double-reconnect races.
- **Failure resilience:** If `_fail()` fires during auto-reconnect (transient adapter hiccup), it falls back to `disconnected` and schedules the next retry instead of dead-ending at `error`.

### Session Persistence
- **`_persistSession()`** — saves role, character, nickname, active flag to `SharedPreferences` on successful hello handshake. Enables app-kill recovery.
- **`tryRestorePersistedSession()`** — called at app startup. If `mp_session_active` was true, re-enters lobby in same role + character. Peer's auto-reconnect finds us.
- **`saveCurrentSession()`** — serializes full `RunState` + session metadata to `SavedMpSession` in `SharedPreferences`. Called on disconnect (belt-and-suspenders) and every 20s while connected (auto-save timer).
- **`loadSavedSession()`** — restores `RunState` via `RunProvider.restoreEntireRunState()` and immediately starts advertising/discovery. Full resume in one call.

### Heartbeat / Watchdog
- **Heartbeat:** 5s ping/pong with sequence numbers. Desync detection: if peer's `lastSeq` > our `_peerLastSnapshotTs`, trigger immediate resync snapshot.
- **Watchdog:** Checks every 5s. If no message from peer in 30s, transitions to `disconnected` + starts auto-reconnect.
- **Auto-save timer:** Every 20s while connected, silently saves session to disk.

### UI Surfaces
- **`_MpHeader`** in active_run_screen — shows connection status pill (green/orange/Red), "Reconnecting (attempt N)…" text, manual Reconnect button when auto-reconnect is not running.
- **Drop dialog** (`mp_request_listener.dart`) — non-dismissable modal during `disconnected` state. "Trying to reconnect…" message. DISCONNECT + RETRY NOW buttons. Auto-closes on reconnect.
- **MP lobby diagnostic console** — live log feed with color-coded entries.
- **FIX LINK button** — in the MP header, calls `reconnect()` directly.

### Reconnect Flow (`reconnect()`)
1. Guard against double-tap (`_busyTransition`)
2. `_service.stopAll()` — tear down Nearby Connections transport
3. 800ms native radio cooldown delay (crucial for socket release)
4. Reset all transport state (peer info, request queues, timers, seq numbers)
5. Re-start with last known role + character via `startAsMain()` or `startAsSidekick()`
6. **Never touches `RunProvider`** — inventory state survives intact

## What's Missing — The Gaps

### Gap 1: No "Connection Restored" feedback
When auto-reconnect succeeds, the drop dialog closes silently. Users get no confirmation that the link is back. They might not notice for seconds.

**Spec:** Show a brief "Connection Restored" popup when transitioning `disconnected → connected`.

### Gap 2: No state-drift protection during disconnect
The drop dialog says "Don't add or remove items" but nothing prevents it. A user could dismiss the dialog (Android back button on some OEMs) and modify inventory. Those changes won't sync.

**Spec:** Block inventory mutations while `MpStatus == disconnected` when an MP session is active. Show a snackbar: "Reconnecting… changes paused until link is restored."

### Gap 3: FIX LINK doesn't do a full save-load-reconnect cycle
Current FIX button just calls `reconnect()` — restarts transport. If local state drifted during disconnect, the drift persists.

**Spec:** FIX LINK should: (1) save current state, (2) load last known-good saved state, (3) reconnect. This discards drift and restores the last synced snapshot.

### Gap 4: App-kill recovery is incomplete
`tryRestorePersistedSession()` re-enters the lobby but doesn't restore the `RunState` from `SavedMpSession`. It only restores role + character. The inventory from the saved session is lost.

**Spec:** On app startup, if `mp_session_active` is true AND a `SavedMpSession` exists, restore the full `RunState` before re-entering the lobby.

### Gap 5: No reconnect attempt progress in drop dialog
The drop dialog says "Trying to reconnect…" but doesn't show attempt count or next retry time. Users don't know if it's trying or stuck.

**Spec:** Show live attempt count in the drop dialog.

### Gap 6: Sidekick pre-MP state not always restored on cancel
`_preSidekickRun` captures the Sidekick's state before joining. On `cancel()`, it restores. But if the app is killed while in MP, `_preSidekickRun` is null on restart and the pre-MP state is lost.

**Spec:** Persist `_preSidekickRun` alongside the session. On `tryRestorePersistedSession()`, if role is sidekick, restore pre-MP state too.

### Gap 7: No graceful handling of peer app-kill
If the peer's app is killed, our watchdog fires after 30s and we start auto-reconnecting. But the peer might not come back (their app is dead). We retry forever.

**Spec:** After N failed attempts (e.g., 10), show a "Peer seems unreachable" notice in the drop dialog with a suggestion to save and exit. Auto-reconnect continues, but the user gets a clear signal.

---

## Implementation Specs

### Spec 1: Connection Restored Popup

**File:** `lib/services/multiplayer_session.dart`
**File:** `lib/widgets/mp_request_listener.dart`

```dart
// In MultiplayerSession:
bool _wasDisconnected = false;
final ValueNotifier<bool> reconnectSuccessNotifier = ValueNotifier(false);

// In _onServiceEvent → MpConnected case:
if (_wasDisconnected) {
  _wasDisconnected = false;
  reconnectSuccessNotifier.value = true;
}

// In _onServiceEvent → MpDisconnected case:
_wasDisconnected = true;
```

```dart
// In MpRequestListener, add a listener for reconnectSuccessNotifier:
// Show a themed SnackBar:
//   "Connection restored with {peerNickname}"
//   Green accent, auto-dismiss 3s, Haptics.heavy()
// Then reset notifier: reconnectSuccessNotifier.value = false
```

**Edge cases:**
- Notifier fires before widget tree is ready → guard with `context.mounted`
- Multiple rapid disconnect/reconnect cycles → notifier is edge-triggered (only fires on `true`), so no duplicates
- Peer changed during reconnect (unlikely but possible) → show new peer name, not old

### Spec 2: Block Inventory Mutations During Disconnect

**File:** `lib/providers/run_provider.dart`

```dart
// Add a flag that MultiplayerSession sets:
bool _mpDisconnected = false;
bool get mpChangesPaused => _mpDisconnected;

// Called by MultiplayerSession when status changes:
void setMpPaused(bool paused) {
  _mpDisconnected = paused;
  notifyListeners();
}

// In addGun, addGunByName, removeGun, addItem, addItemByName, removeItem,
// adjustCoolness, adjustCurse, useShrine, startCoopPlayer:
// If _mpDisconnected, ignore the mutation and set a flag for the UI.
bool _mpChangeBlocked = false;
bool get lastChangeWasBlocked => _mpChangeBlocked;
void clearBlockFlag() => _mpChangeBlocked = false;
```

**File:** `lib/services/multiplayer_session.dart`
```dart
// In _onServiceEvent → MpDisconnected case:
_runProvider.setMpPaused(true);

// In _onHello (successful handshake):
_runProvider.setMpPaused(false);
```

**File:** `lib/widgets/mp_request_listener.dart` or `lib/screens/active_run_screen.dart`
```dart
// Watch for blocked changes and show snackbar:
// "Reconnecting… inventory changes paused until link is restored."
```

**Edge cases:**
- User adds item right as disconnect fires → race condition. The mutation either completes before the flag is set (fine) or is blocked (fine, nothing changed).
- Gift arriving during disconnect → gifts are inbound messages, not local mutations. They should still be applied (the peer sent them before the drop).
- Favourites toggle → should NOT be blocked (favourites are local-only, not synced).

### Spec 3: Enhanced FIX LINK — Full Reconnect Cycle

**File:** `lib/services/multiplayer_session.dart`

```dart
/// Full save → load → reconnect cycle. Used by the FIX LINK button
/// when a simple transport restart isn't enough (state drift, corrupted
/// local state, or user wants a clean resync).
Future<void> fullReconnectCycle() async {
  _log('[FIX] Step 1/3: Saving current game state...');
  await saveCurrentSession();

  _log('[FIX] Step 2/3: Restoring last known-good state...');
  final prefs = await SharedPreferences.getInstance();
  final list = prefs.getStringList('saved_mp_sessions') ?? [];
  if (list.isNotEmpty) {
    final last = SavedMpSession.fromJson(json.decode(list.last));
    await loadSavedSession(last);
    // loadSavedSession already starts advertising/discovery
    _log('[FIX] Step 3/3: Transport restarted. Waiting for peer...');
    return;
  }

  // No saved session — fall back to simple reconnect
  _log('[FIX] No saved session found. Falling back to simple reconnect...');
  await reconnect();
}
```

**File:** `lib/screens/active_run_screen.dart` (FIX LINK button handler, ~line 1272)
```dart
// Change from:
onPressed: isConnected ? null : () { liveSession.reconnect(); ... }
// To:
onPressed: isConnected ? null : () { liveSession.fullReconnectCycle(); ... }
```

**Edge cases:**
- No saved session exists → falls back to `reconnect()` (current behavior)
- `loadSavedSession` fails (corrupted JSON) → catch, log, fall back to `reconnect()`
- `loadSavedSession` succeeds but starts advertising which fails → `_fail()` handles it, auto-reconnect loop picks up
- User taps FIX while auto-reconnect is mid-retry → `_busyTransition` guard prevents race

### Spec 4: Enhanced App-Kill Recovery

**File:** `lib/services/multiplayer_session.dart`

```dart
Future<void> tryRestorePersistedSession() async {
  // ... existing role/char/nick restoration ...

  // NEW: Also restore the full RunState from SavedMpSession
  final prefs = await SharedPreferences.getInstance();
  final list = prefs.getStringList('saved_mp_sessions') ?? [];
  if (list.isNotEmpty) {
    try {
      final last = SavedMpSession.fromJson(json.decode(list.last));
      final state = RunState.fromJson(last.runStateJson);
      _runProvider.restoreEntireRunState(state);
      _log('[Restore] RunState restored from saved session.');
    } catch (e) {
      _log('[Restore] Failed to restore RunState: $e. Continuing with empty run.');
    }
  }

  // Then re-enter lobby as before...
}
```

**Edge cases:**
- Saved session JSON is corrupted → catch, log, continue with whatever RunProvider already has
- Saved session is from a different run (stale) → acceptable, the user can end run if they notice
- Multiple saved sessions → use the most recent one (last in list)
- Role is sidekick and `_preSidekickRun` was not persisted → the restored RunState IS the MP state (main + coop), so pre-MP state is lost. Acceptable — the user's pre-MP run is gone, but their MP run is preserved.

### Spec 5: Live Reconnect Progress in Drop Dialog

**File:** `lib/widgets/mp_request_listener.dart`

```dart
// In the drop dialog content, replace static text with dynamic content:
content: Column(
  mainAxisSize: MainAxisSize.min,
  children: [
    const Text('Trying to reconnect to your peer…'),
    if (session.isAutoReconnecting) ...[
      const SizedBox(height: 12),
      Text(
        'Attempt ${session.autoReconnectAttempts}',
        style: TextStyle(color: Colors.orangeAccent, fontSize: 11),
      ),
    ],
    // ... existing warning text ...
  ],
),
```

**Recommendation:** Just show attempt count. Simpler, still informative. Add countdown timer later if users want it.

### Spec 6: Peer Unreachable Notice

**File:** `lib/services/multiplayer_session.dart`
```dart
// Add a getter:
bool get peerLikelyGone => _autoReconnectAttempts >= 10;
```

**File:** `lib/widgets/mp_request_listener.dart`
```dart
// In drop dialog, after attempt count:
if (session.peerLikelyGone) ...[
  const SizedBox(height: 8),
  Text(
    'Peer seems unreachable after ${session.autoReconnectAttempts} attempts. '
    'Consider saving the run and reconnecting later.',
    style: TextStyle(color: Colors.redAccent, fontSize: 11),
  ),
],
```

**Edge cases:**
- Peer comes back after 10+ attempts → notice disappears, reconnect succeeds, popup from Spec 1 fires
- User ignores notice → auto-reconnect continues indefinitely, no harm

## Seamless Reconnection — User Experience Flows

### Scenario A: Brief Bluetooth hiccup (5-30s drop)
1. Watchdog fires (30s silence) or `MpDisconnected` event
2. Status → `disconnected`, drop dialog appears
3. Auto-reconnect starts (2s backoff)
4. Inventory mutations blocked (Spec 2)
5. Attempt 1 fails (2s), attempt 2 fails (4s), attempt 3 succeeds (8s)
6. Hello handshake completes, status → `connected`
7. Drop dialog auto-closes
8. "Connection Restored" popup (Spec 1), haptic feedback
9. Inventory mutations unblocked
10. Snapshots resume, state syncs

**User experience:** Brief modal saying "reconnecting", then "restored!" popup. No data loss. No manual action needed.

### Scenario B: App killed on one device
1. Device A: App killed. `mp_session_active` flag persists.
2. Device B: Watchdog fires after 30s. Auto-reconnect starts. Drop dialog shows.
3. Device B: After 10 failed attempts, "Peer seems unreachable" notice (Spec 6).
4. Device A: User relaunches app. `tryRestorePersistedSession()` fires.
5. Device A: RunState restored from `SavedMpSession` (Spec 4). Re-enters lobby in same role.
6. Device A: Starts advertising/discovery.
7. Device B: Auto-reconnect attempt finds Device A. Hello handshake.
8. Both devices: Status → `connected`. Drop dialog closes. "Connection Restored" popup.
9. Snapshots resume. Both devices have the last saved state.

**User experience:** Device B sees "reconnecting" for a while. Device A relaunches and automatically re-enters the lobby. Connection re-establishes. No manual pairing needed.

### Scenario C: User presses FIX LINK
1. User sees drop dialog, taps RETRY NOW (or FIX LINK in header)
2. `fullReconnectCycle()` (Spec 3):
   a. Saves current state (in case it drifted)
   b. Loads last known-good saved state (discards drift)
   c. Starts advertising/discovery
3. Peer (still in lobby or auto-reconnecting) finds us
4. Hello handshake, status → `connected`
5. Drop dialog closes, "Connection Restored" popup

**User experience:** One tap. State is restored to last synced snapshot. Connection re-establishes.

### Scenario D: Both devices app-killed
1. Both devices: App killed. `mp_session_active` persists on both.
2. Both devices: User relaunches.
3. Both devices: `tryRestorePersistedSession()` restores RunState + re-enters lobby.
4. Both devices: Advertising/discovery starts.
5. Nearby Connections re-pairs them (auto-accept flow).
6. Hello handshake, both → `connected`.
7. "Connection Restored" popup on both.

**User experience:** Both users relaunch the app. Everything reconnects automatically. No manual pairing, no data loss.

## Files to Modify (Summary)

| File | Changes | Spec |
|------|---------|------|
| `lib/services/multiplayer_session.dart` | Add `_wasDisconnected` flag, `reconnectSuccessNotifier`, `peerLikelyGone` getter, `fullReconnectCycle()`, enhanced `tryRestorePersistedSession()` | 1, 3, 4, 6 |
| `lib/providers/run_provider.dart` | Add `setMpPaused()`, `mpChangesPaused` flag, `lastChangeWasBlocked` flag, guards in mutation methods | 2 |
| `lib/widgets/mp_request_listener.dart` | Add reconnect success popup, live attempt count in drop dialog, peer-unreachable notice | 1, 5, 6 |
| `lib/screens/active_run_screen.dart` | Change FIX LINK to call `fullReconnectCycle()`, add blocked-change snackbar listener | 2, 3 |

## Edge Cases & Considerations

- **Both devices must save** — Each device saves independently. Both have a copy of the session.
- **State drift during disconnect** — `fullReconnectCycle` loads the *saved* state, discarding drift. Intentional — the saved state is the last synced state.
- **App killed during disconnect** — On next launch, `tryRestorePersistedSession()` detects `mp_session_active` flag and restores. Spec 4 enhances this to also restore RunState.
- **PIN code reuse** — Same PIN is reused for reconnect. Both devices remember it from the initial session.
- **Role preservation** — Main stays Main, Sidekick stays Sidekick. No role swap on reconnect.
- **Timeout for full cycle** — If `loadSavedSession()` + `reconnect()` takes too long, show a progress indicator on the FIX button.
- **Favourites not blocked** — Favourites are local-only, not synced. Toggling favourites during disconnect is safe and should not be blocked.
- **Gifts during disconnect** — Inbound gifts are remote messages, not local mutations. They should still be applied if they arrive (though they won't arrive during disconnect since the transport is down).

## Testing Plan

### Manual Testing (with two devices)
1. **Brief disconnect:** Turn off Bluetooth on device A for 10s, turn back on. Verify auto-reconnect + "Connection Restored" popup.
2. **App kill:** Force-stop app on device A. Relaunch. Verify RunState restored + auto-reconnect.
3. **FIX LINK:** Disconnect Bluetooth on both devices. Turn back on. Press FIX LINK on one device. Verify save → load → reconnect cycle.
4. **State drift:** While disconnected, try adding an item. Verify it's blocked with snackbar.
5. **Peer unreachable:** Turn off Bluetooth on device A for 2+ minutes. Verify "Peer seems unreachable" notice after 10 attempts.
6. **Both killed:** Force-stop both apps. Relaunch both. Verify auto-reconnect.
7. **End run while disconnected:** Verify `cancel()` cleans up properly, auto-reconnect stops, persisted session cleared.

### Playwright Testing (limited — web build can't test Bluetooth)
- Verify drop dialog renders correctly when `MpStatus.disconnected` is set
- Verify "Connection Restored" popup renders
- Verify blocked-change snackbar renders
- These require injecting mock `MultiplayerSession` state — only feasible if we add a test mode

### Static Verification
- `flutter analyze` on all modified files — zero warnings
- `grep_search` for `dispose()` on any new controllers/notifiers
- `grep_search` for `context.mounted` before any `showDialog`/`showSnackBar` in new code
- Trace all callers of modified methods in `RunProvider` — verify guards don't break non-MP usage

---

## Priority Order

| Priority | Spec | Effort | Impact |
|----------|------|--------|--------|
| P0 | Spec 1: Connection Restored popup | Small | High — immediate user feedback |
| P0 | Spec 4: Enhanced app-kill recovery | Small | High — prevents data loss on app kill |
| P1 | Spec 2: Block mutations during disconnect | Medium | High — prevents silent desync |
| P1 | Spec 3: Full reconnect cycle on FIX | Small | Medium — better FIX button |
| P2 | Spec 5: Live attempt count in dialog | Small | Medium — user visibility |
| P2 | Spec 6: Peer unreachable notice | Tiny | Low — nice-to-have signal |

**Recommended batch:** Implement Specs 1 + 4 first (P0), then Specs 2 + 3 (P1), then Specs 5 + 6 (P2). Each batch is one commit.

---

## Manual Re-Pair Flow (Implemented Jul 23, 2026)

**Files modified:**
- `lib/services/multiplayer_session.dart` — `showReconnectHubNotifier`, `peerLikelyGone` getter, `setPinCode()`, `requestReconnectHub()`, `lastCharacter`/`lastNickname` getters, dispose cleanup
- `lib/widgets/mp_request_listener.dart` — `_onReconnectHubRequest()` method, fullscreen `_ReconnectScreen` widget with `_PortraitCard`, drop dialog peer-unreachable notice + RE-PAIR button
- `lib/screens/active_run_screen.dart` — FIX LINK button now calls `requestReconnectHub()` instead of `fullReconnectCycle()` directly

### How it works

1. **Entry points:** User taps FIX LINK (active run header) or RE-PAIR (drop dialog after peer-unreachable notice)
2. **Auto-save:** `requestReconnectHub()` fires `showReconnectHubNotifier`, which triggers `_onReconnectHubRequest()` in the listener — this immediately calls `saveCurrentSession()` so both devices have a fresh restore point
3. **Fullscreen Reconnection Screen opens** (replaces the old dialog):
   - **Top bar:** Title + close button
   - **Player portraits row:** Both players' animated gungeoneer card GIFs from `assets/images/gungeoneers/animated/`, with slot labels (P1·MAIN / P2·SIDEKICK), nicknames, and a "YOU" badge on the local player. Link status icon between them (LINKED/BROKEN)
   - **Status + save indicator:** Live status text (searching/handshaking/connected), save confirmation, auto-retry attempt count
   - **PIN display/entry:** Main shows their 4-digit PIN in a large cyan container. Sidekick gets a numeric text field with large 36px font
   - **Big action buttons:** Full-width RECONNECT (56px height, 16px font) and DISCONNECT (48px height, 14px font)
4. **Reconnect:** User taps RECONNECT. Sidekick's PIN is validated and set via `setPinCode()`. Then `fullReconnectCycle()` runs (save → reconnect)
5. **Auto-close:** Screen listens to `reconnectSuccessNotifier` and auto-pops when connection is restored
6. **Peer-unreachable notice:** After 10 failed auto-reconnect attempts, `peerLikelyGone` returns true. Drop dialog shows a red warning banner suggesting RE-PAIR

### Drop dialog enhancements
- **Attempt count:** Already shown in dialog text (Spec 5)
- **Peer-unreachable banner:** Red warning container with icon after 10 attempts
- **RE-PAIR button:** Cyan outlined button alongside RETRY NOW — opens fullscreen Reconnection Screen
