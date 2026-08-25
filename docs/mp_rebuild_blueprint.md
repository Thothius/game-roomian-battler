# MP Full Rebuild — Implementation Blueprint (Foolproof Edition)

> **Author:** Slot 3 — Planner-Architect-Mockupper
> **Date:** 2026-08-24
> **Status:** APPROVED by user — Option C (full rebuild)
> **Decisions locked:**
> - Sidekick flow: **List always visible**. Paired partners at top with one-tap connect (no PIN). Unpaired games require PIN entry.
> - Reconnect UX: **Dismissable blocking dialog**. Auto-closes on reconnect. User can dismiss to keep using the app.
> - **Remove** manual Saved Sessions list and diagnostic console from UI.
> - Rebuild from scratch — replace `MultiplayerSession` + `MultiplayerService`.
> - **Protocol version bumped to 2** (both devices are user-controlled; no gradual migration).
> - **Simulated mode (PIN 0000) kept** — useful for solo dev testing.
> - **Pause/Resume feature REMOVED** — persistent advertising + instant reconnect makes it unnecessary. Removes a confusing button.
> - **`RunProvider.mpDisconnected` flag REMOVED** — users can modify their own inventory while disconnected; changes sync on reconnect via full snapshot. The peer's slot is read-only mirror anyway.
> - **Old SharedPreferences keys cleaned up** on first launch of new version.

---

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         UI Layer                             │
│  MpLobbyScreen · MpConnectScreen · MpReconnectBanner         │
│  MpRequestListener (gifts/requests/dice/emotes)              │
└────────────┬──────────────────────────────────┬──────────────┘
             │ ChangeNotifier                    │ ValueNotifiers
┌────────────▼──────────────────────────────────▼──────────────┐
│                       MpSession                              │  ← thin facade
│  (ChangeNotifier — the ONLY thing UI talks to)               │
│  Owns: MpLink, MpSync, MpPairing, MpRecovery, MpStore        │
└───┬───────┬──────────┬──────────────┬───────────┬────────────┘
    │       │          │              │           │
┌───▼──┐ ┌──▼───────┐ ┌▼──────────┐ ┌─▼────────┐ ┌▼───────┐
│MpLink│ │MpSync    │ │MpPairing  │ │MpRecovery│ │MpStore │
│      │ │          │ │           │ │          │ │        │
│trans-│ │state     │ │one-time   │ │reconnect │ │persist- │
│port  │ │sync      │ │pairing    │ │+ app-kill│ │ence    │
│layer │ │snapshots │ │flow       │ │restore   │ │        │
└──────┘ └──────────┘ └───────────┘ └──────────┘ └────────┘
         │                            │           │
         └────────── RunProvider ─────┘           │
                      (shared run state)          │
                                                   │
                    SharedPreferences ◄────────────┘
```

**Ownership:** `MpSession` constructs and owns all five sub-components in its constructor. Sub-components receive references to each other and to `RunProvider` via constructor injection. `MpSession` is the only `ChangeNotifier`; sub-components communicate via callbacks and `ValueNotifier`s.

**Key principle:** Each component has one job. No component exceeds ~400 lines. `MpSession` is a thin facade — it delegates to sub-components and exposes a clean API for the UI.

---

## 2. Component Specifications

### 2.1 MpLink — Transport Layer

**File:** `lib/services/mp/mp_link.dart` (~350 lines)

Owns one peer-to-peer Nearby Connections connection. Replaces `MultiplayerService`.

**Internal state machine:**
```
idle → advertising → handshaking → connected → lost
                                    ↑              │
                                    └── (reconnect)─┘
idle → discovering → handshaking → connected → lost
                                    ↑              │
                                    └── (reconnect)─┘
```

**Internal states (not exposed to UI — MpSession maps these to MpPhase):**
```dart
enum _LinkState { idle, advertising, discovering, handshaking, connected, lost }
```

**Responsibilities:**
- Start/stop advertising (Main) and discovery (Sidekick).
- Surface discovered endpoints via callback: `void Function(List<MpEndpoint>) onEndpointsChanged`.
- Auto-accept connection requests (no token dialog).
- Send/receive `MpMessage` bytes via `sendMessage(MpMessage)` / `onMessage(MpMessage)` callback.
- Signal disconnect via `void Function() onDisconnected`.
- Signal connect via `void Function() onConnected`.
- **Persistent advertising:** Main advertises continuously while in `advertising`, `connected`, or `lost` state. No search timeout. BLE advertising is low-power; switches to Wi-Fi Direct on connection.
- **Discovery loop for Sidekick:** MpLink owns the timer. Cadence is controlled by `setDiscoveryCadence(Duration on, Duration off)`. Default: 3s on / 1s off. Endpoints accumulate in an internal list; stale ones (not seen in 8s) are removed. Fires `onEndpointsChanged` on every change.
- **Auto-connect behavior** — controlled by a mode flag:
  - `AutoConnectMode.none` — don't auto-connect; surface endpoints to UI for manual selection (PIN sessions, initial Sidekick browse).
  - `AutoConnectMode.pairId(String pairId)` — auto-connect to endpoints whose name ends with `#<pairId>` (paired connections, reconnect).
  - `AutoConnectMode.pin(String pin)` — auto-connect to endpoints whose name ends with `#<pin>` (pairing flow).
- **Reentrancy guard:** `_busyTransition` bool — set during `stopAll()` + `startAdvertising()` / `startDiscovery()` transitions. Prevents double-connect races. Cleared in finally block.
- **Native radio cooldown:** 800ms delay after `stopAll()` before starting new advertising/discovery. This is a Nearby Connections plugin requirement (same as current code).

**Endpoint model:**
```dart
class MpEndpoint {
  final String endpointId;
  final String nickname;    // parsed from "Nickname#PIN" (before the #)
  final String pin;         // parsed from "Nickname#PIN" (after the #)
  final int lastSeenMs;

  /// True if this endpoint's pin matches a known pairId.
  /// Computed by MpSession (which has access to PairedPartnersStore),
  /// NOT by MpLink (which has no knowledge of pairing).
  bool get isPaired => false; // overridden by MpSession when surfacing
}
```

**Heartbeat:** Simple liveness only.
- Every 10s while `connected`: send `MpPing` (no `lastSeq` field — dropped in protocol v2).
- If no message (any type) received in 25s → fire `onDisconnected`.
- On receiving `MpPing`: reply `MpPong` immediately.
- No desync/sequencing logic — Nearby Connections is a reliable ordered stream.

**Public API:**
```dart
class MpLink {
  // Callbacks (set by MpSession)
  void Function(List<MpEndpoint>)? onEndpointsChanged;
  void Function(MpMessage)? onMessage;
  void Function()? onConnected;
  void Function()? onDisconnected;
  void Function(String error)? onError;

  // Lifecycle
  Future<bool> requestPermissions();
  Future<void> startAdvertising(String nickname);  // nickname = "Nick#PIN"
  Future<void> startDiscovery(String nickname, {required AutoConnectMode autoConnect});
  Future<void> setDiscoveryCadence(Duration on, Duration off);
  Future<void> stopAll();  // stop advertising + discovery + disconnect peer
  Future<void> disconnectPeer();  // drop peer only, keep searching

  // Messaging
  Future<void> sendMessage(MpMessage msg);
  bool get isConnected;

  // Endpoint list
  List<MpEndpoint> get discoveredEndpoints;

  // Cleanup
  Future<void> dispose();
}

enum AutoConnectMode { none, pairId(String), pin(String) }
```

### 2.2 MpSync — State Synchronization

**File:** `lib/services/mp/mp_sync.dart` (~300 lines)

Keeps the local `RunProvider` in sync with the peer. Replaces the snapshot/gift/request handling in `MultiplayerSession`.

**Critical guard: `_applyingRemote`**
- Owned by `MpSync`. Set to `true` before applying any peer state to `RunProvider`.
- Cleared in a **finally block** — if an exception occurs during apply, the guard MUST be cleared or the session deadlocks (no snapshots would ever broadcast).
- Purpose: prevents the infinite echo loop (apply peer → RunProvider notifies → our listener broadcasts → peer applies → ...).

**Responsibilities:**
- **On connect (fresh or reconnect):** send a **full snapshot** immediately. Both sides do this, so both slots are rebuilt from the peer's data. This is the "instant resume" mechanism.
- **On local `RunProvider` change:** send a **full snapshot** (debounced 200ms). Always send full state, not deltas. A snapshot is ~300 bytes; cheap over Wi-Fi Direct.
- **On receiving a snapshot:** apply to the peer's slot in `RunProvider` (wrapped in `_applyingRemote` guard). Role-aware: Main receives Sidekick data into coop slot; Sidekick receives Main data into main slot.
- **Gifts, requests, dice, emotes:** same protocol as today, handlers moved here. Includes:
  - `sendGift` — remove locally + send `MpGift`. Rollback on send failure. Track as pending.
  - `sendAddToPeer` — send `MpGift` without local removal.
  - `sendRequest` — send `MpRequest`, 30s timeout, returns reqId.
  - `respondToPendingRequest` — send gift first (if approved), then `MpRequestResp`.
  - Dice: `sendDiceChallenge/Accept/Decline/Cancel/Result`.
  - Emote: `sendEmote`.
- **Pending gifts:** `List<_PendingGift>` — items sent but not confirmed by peer snapshot. On reconnect, re-send all. On cancel, restore to inventory. Confirmed when peer's snapshot includes the item.
- **Dedup:** `_seenReqIds` (max 20) and `_seenGiftIds` (max 20) — same as current.

**Public API:**
```dart
class MpSync {
  MpSync(this._link, this._runProvider, this._session);

  // Called by MpSession when connection establishes
  void onConnected();
  // Called by MpSession when connection drops
  void onDisconnected();
  // Called by MpSession when a message arrives
  void onMessage(MpMessage msg);

  // Outgoing operations (called by MpSession, delegated from UI)
  Future<void> sendGift({required String kind, required String name});
  Future<void> sendAddToPeer({required String kind, required String name});
  Future<String?> sendRequest({required String kind, required String name});
  Future<void> respondToPendingRequest(bool approved);
  Future<void> sendDiceChallenge(String challengerName);
  Future<void> sendDiceAccept();
  Future<void> sendDiceDecline();
  Future<void> sendDiceCancel();
  Future<void> sendDiceResult(int score, List<int> dice);
  Future<void> sendEmote(String action);

  // Called by MpSession on cancel — restore pending gifts to inventory
  void restorePendingGifts();
  // Called by MpSession on reconnect — re-send pending gifts
  void resendPendingGifts();

  // Request/response state (read by MpSession for UI)
  MpRequest? get pendingRequest;
  ({String name, bool approved})? get lastResp;
  void consumeLastResp();

  // Dice/emote callbacks (set by MpSession, fired to UI)
  void Function(String challengerName)? onDiceChallenge;
  void Function()? onDiceAccept;
  void Function()? onDiceDecline;
  void Function()? onDiceCancel;
  void Function(int peerScore, List<int> peerDice)? onDiceResult;
  void Function(String from, String action)? onEmote;

  void dispose();
}
```

**Snapshot content (protocol v2 — `tsMs` dropped):**
- character, gunNames, itemNames, coolness, curse, shrinesUsed
- No timestamp/sequence — full-snapshot-on-every-change, both sides apply latest. Concurrent edits within 200ms debounce are acceptable (same as current behavior).

### 2.3 MpPairing — One-Time Pairing

**File:** `lib/services/mp/mp_pairing.dart` (~200 lines)

Isolated one-time pairing flow. Produces a `PairedPartner` record. Reuses `PairedPartnersStore` (unchanged) and `MpPair`/`MpPairAck` messages (unchanged).

**State:**
```dart
bool _isPairingMode = false;
String? _pendingPairId;
bool _pairPersistedLocally = false;
String? _pairingPeerNickname;
```

**Flow:**
1. Initiator (Main) calls `startPairing(nickname, pairingPin)` → MpLink advertises as `nickname#pairingPin` with `AutoConnectMode.pin(pairingPin)`.
2. Joiner (Sidekick) calls `joinPairing(nickname, pairingPin)` → MpLink discovers with `AutoConnectMode.pin(pairingPin)`.
3. On hello, initiator generates `pairId` (8-char hex), sends `MpPair(pairId, nickname)`.
4. Joiner persists `PairedPartner`, sends `MpPairAck`, fires `pairingCompleteNotifier`.
5. Initiator persists on ack, fires `pairingCompleteNotifier`.
6. Both sides tear down. Pair is ready for one-tap `connectPaired`.

**Edge cases handled:**
- **Disconnect during pairing:** `onDisconnected` fires → abort pairing → set error "Pairing interrupted. Please try again." → return to idle. (Same as current `_endPairingSession` + error.)
- **Duplicate MpPair/MpPairAck:** `_pairPersistedLocally` guard — ignore duplicates. (Same as current.)
- **Re-pairing same partner (pairId already in store):** `PairedPartnersStore.upsert` replaces the old record with the new one (keyed by pairId). No special handling needed.
- **Both sides try to initiate simultaneously:** Can't happen — one must be Main (advertiser) and the other Sidekick (discoverer). The roles are chosen in the UI before pairing starts.

**Paired connect (ongoing sessions):**
- `connectPaired(partner, role, character)` → sets `_pinCode = partner.pairId`, calls `startAsMain`/`startAsSidekick` with `AutoConnectMode.pairId(partner.pairId)`.
- MpLink auto-connects to endpoint matching `#<pairId>` — no user action needed.
- Elevated privileges:
  - **Faster reconnect:** `MpRecovery` uses 2s backoff cap for paired connections vs 10s for PIN sessions.
  - **Character swap for Sidekick:** `startAsSidekick` accepts a `character` override (not forced to Cultist).
  - **"Reset Run with New Gungeoneer" for Main:** `resetRunWithNewGungeoneer(Gungeoneer)` — clears Main slot, sets new character, broadcasts snapshot. Only valid for paired Main sessions.

**Public API:**
```dart
class MpPairing {
  MpPairing(this._link, this._session);

  bool get isPairingMode;
  String? get pendingPairId;

  Future<void> startPairing({required String nickname, required String pairingPin});
  Future<void> joinPairing({required String nickname, required String pairingPin});
  Future<void> cancelPairing();

  // Called by MpSync when MpPair/MpPairAck message arrives
  void onPair(MpPair msg);
  void onPairAck(MpPairAck msg);

  // Called by MpSession on disconnect during pairing
  void onDisconnected();

  void dispose();
}
```

### 2.4 MpRecovery — Reconnect + App-Kill Restore

**File:** `lib/services/mp/mp_recovery.dart` (~250 lines)

Owns the "peer came back" and "app was killed" logic. This is the component that fixes the user's core complaint.

**On peer disconnect (MpLink fires `onDisconnected`):**
1. `MpSession` sets phase → `MpPhase.disconnected`. Fires `reconnectNotifier` (UI shows dismissable dialog).
2. `MpRecovery` takes over:
   - **Main:** tells MpLink to keep advertising (it already is — persistent). No timeout. The Sidekick will find us when they come back.
   - **Sidekick:** tells MpLink to start discovery loop with cadence 3s on / 1s off. Sets `AutoConnectMode.pairId(pairId)` if paired, else `AutoConnectMode.pin(pin)`.
3. **Run state stays in memory.** No save/load. The `RunProvider` keeps both slots' inventory. On reconnect, `MpSync` sends a full snapshot and both slots are confirmed/rebuilt.
4. **Backoff schedule for Sidekick discovery cadence:**
   - First 60s: 3s on / 1s off (aggressive).
   - After 60s: 5s on / 5s off (moderate).
   - After 5 min: 5s on / 15s off (relaxed). **Never stops.** The run is alive until the user cancels.
   - Paired connections: cap at 3s on / 1s off forever (priority reconnect).
5. When MpLink reconnects → `MpSync` sends full snapshot → `MpSession` sets phase → `MpPhase.connected` → fires `reconnectSuccessNotifier` (UI closes dialog, shows "Connection restored" snackbar).
6. `MpRecovery` resets its backoff timer.

**On app kill (app process terminated):**
1. `MpStore` has been writing `mp.active_run` (full RunState JSON) every 5s while connected, and on every disconnect.
2. On app start, `MpRecovery.tryRestore()` is called from `HomeScreen` (same pattern as current `tryRestorePersistedSession`):
   - Read `mp.session_active` from `MpStore`. If false → no-op.
   - Read `mp.active_run` → restore `RunState` into `RunProvider` via `restoreEntireRunState`.
   - Read `mp.role`, `mp.nickname`, `mp.character`, `mp.pin`, `mp.is_paired`, `mp.pair_id`.
   - If paired: call `connectPaired` with the stored partner + role. No PIN, no lobby.
   - If PIN session: call `startAsMain`/`startAsSidekick` with the stored PIN. The peer (if still alive) will see us and reconnect.
   - **Conflict check:** If the user has a different active solo run (different character than `mp.character`), do NOT silently overwrite. Instead, save the solo run to `mp.solo_run_backup` and restore it if the MP session is later cancelled. If the characters match, just proceed (the MP restore has the full state).
   - **Corrupt JSON:** `MpStore.load()` catches all parse errors, returns null, falls back to fresh start. No crash.
3. This is **silent** — no lobby, no user action. The user opens the app and they're back in the run, reconnecting to the peer.

**On app foreground (after backgrounding):**
- Dart timers stop during OS doze. On `AppLifecycleState.resumed` (handled by `MpSession.didChangeAppLifecycleState`), if phase is `disconnected`, tell `MpRecovery` to trigger an immediate reconnect attempt (reset cadence to aggressive, tell MpLink to restart discovery immediately).

**Public API:**
```dart
class MpRecovery {
  MpRecovery(this._link, this._session, this._store);

  // Called by MpSession when peer disconnects
  void onPeerDisconnected();
  // Called by MpSession when peer reconnects
  void onPeerReconnected();
  // Called by MpSession on app foreground
  void onAppResumed();
  // Called by MpSession on cancel — stop all retry loops
  void cancel();

  // Called once at app start from HomeScreen
  Future<void> tryRestore();

  void dispose();
}
```

### 2.5 MpStore — Persistence

**File:** `lib/services/mp/mp_store.dart` (~150 lines)

Single persistence mechanism. Replaces `_persistSession`, `saveCurrentSession`, `loadSavedSession`, `SavedMpSession`, and the "Saved Sessions" UI.

**Keys (SharedPreferences):**
```
mp.session_active     → bool    (is there a live MP session?)
mp.role               → String  (main | sidekick)
mp.nickname           → String
mp.character          → String  (character name)
mp.pin                → String  (PIN or pairId)
mp.is_paired          → bool    (paired connection?)
mp.pair_id            → String? (pairId if paired)
mp.active_run         → String  (full RunState JSON, written every 5s)
mp.pre_sidekick_run   → String? (pre-MP run snapshot for Sidekick cancel-restore)
mp.solo_run_backup    → String? (solo run saved before MP restore, restored on cancel)
```

**Old keys to clean up on first launch of new version:**
```
mp_last_role, mp_last_character, mp_last_nickname, mp_session_active,
mp_last_pin, mp_pre_sidekick, mp_paused, saved_mp_sessions
```
→ `MpStore.cleanupOldKeys()` called once from `main.dart` after `PairedPartnersStore.load()`.

**Throttled run-state save:**
- `saveRunState` is called by `MpSession` every 5s via a `Timer.periodic` while connected.
- Also called on disconnect (immediate, not throttled).
- Internal `_lastSaveMs` guard — if called within 4s of last write, skip (prevents spam).

**Public API:**
```dart
class MpStore {
  static Future<void> saveSession({
    required MpRole role,
    required String nickname,
    required String character,
    required String pin,
    required bool isPaired,
    String? pairId,
  });
  static Future<void> saveRunState(RunState state);  // throttled 5s
  static Future<void> savePreSidekickRun(RunState state);
  static Future<void> saveSoloRunBackup(RunState state);
  static Future<MpSavedSession?> load();
  static Future<void> clear();
  static Future<void> cleanupOldKeys();
}

class MpSavedSession {
  final MpRole role;
  final String nickname;
  final String character;
  final String pin;
  final bool isPaired;
  final String? pairId;
  final RunState runState;
  final RunState? preSidekickRun;
  final RunState? soloRunBackup;
}
```

**No manual save/load UI.** Everything is automatic. The "Saved Sessions" list is deleted.

### 2.6 MpSession — Thin Facade

**File:** `lib/services/mp_session.dart` (~400 lines)

The only `ChangeNotifier` the UI talks to. Wires the components together. Created in `main.dart` via `ChangeNotifierProxyProvider` (same pattern as current).

**Phase enum (replaces MpStatus):**
```dart
enum MpPhase {
  idle,              // no session, not trying — lobby is shown
  connecting,        // advertising / discovering / handshaking / reconnecting
  connected,         // live peer, snapshots flowing
  disconnected,      // peer dropped, auto-reconnecting (UI shows dismissable dialog)
  permissionDenied,  // BT/Wi-Fi permissions denied (UI shows banner + Open Settings)
  error,             // terminal error: protocol mismatch, advertising failed (UI shows banner + Retry)
}
```

**Why `disconnected` is separate from `connecting`:** The UI needs to show the reconnect dialog only on `disconnected`, not on initial `connecting`. On `connecting`, the UI shows the normal "waiting for partner" view. On `disconnected`, the UI shows the dismissable reconnect dialog.

**Connect reason (for UI messaging):**
```dart
enum MpConnectReason {
  hosting,        // Main waiting for Sidekick to join (initial)
  browsing,       // Sidekick browsing game list (initial)
  joining,        // Sidekick connecting to selected game (handshaking)
  reconnecting,   // peer dropped, auto-retrying
  restoring,      // app-kill restore in progress
}
MpConnectReason get connectReason;
```
The UI uses `connectReason` to show the right message:
- `hosting` → "Waiting for a partner to join…"
- `browsing` → "Searching for games…"
- `joining` → "Connecting to [peer nickname]…"
- `reconnecting` → "Reconnecting to [peer nickname]…"
- `restoring` → "Restoring your run…"

**Full public API (every property/method the UI uses — verified against all 16 consuming files):**

```dart
class MpSession extends ChangeNotifier with WidgetsBindingObserver {
  // ── Phase & error ──────────────────────────────────────────
  MpPhase get phase;
  MpConnectReason get connectReason;
  String? get error;                    // human-readable error string (permissionDenied / error phases)
  bool get isConnected => phase == MpPhase.connected;
  bool get isActive => phase != MpPhase.idle;

  // ── Identity ───────────────────────────────────────────────
  MpRole? get myRole;
  String get myNickname;
  String get myCharacterName;
  PlayerSlot? get mySlot;               // Main → PlayerSlot.main, Sidekick → PlayerSlot.coop
  PlayerSlot? get peerSlot;             // mirror of mySlot

  // ── Peer metadata ──────────────────────────────────────────
  String? get peerNickname;
  String? get peerCharacterName;

  // ── PIN / pairing ──────────────────────────────────────────
  String? get pinCode;
  bool get isPairedConnection;
  bool get isPairingMode;
  bool get isSimulated;                 // PIN 0000 fake partner

  // ── Discovered endpoints (for Sidekick lobby list) ─────────
  List<MpEndpoint> get discoveredEndpoints;

  // ── Reconnect state ────────────────────────────────────────
  // (No public reconnect state — reconnect is automatic and invisible.
  //  The UI only sees: disconnected phase → reconnectNotifier → connected phase)

  // ── Notifiers (one-shot, auto-reset by listener) ───────────
  final ValueNotifier<bool> reconnectNotifier = ValueNotifier(false);
  final ValueNotifier<bool> reconnectSuccessNotifier = ValueNotifier(false);
  final ValueNotifier<bool> pairingCompleteNotifier = ValueNotifier(false);

  // ── Request/gift state (delegated to MpSync) ───────────────
  MpRequest? get pendingRequest;
  ({String name, bool approved})? get lastResp;
  void consumeLastResp();

  // ── Dice/emote callbacks (set by UI) ───────────────────────
  void Function(String challengerName)? onDiceChallenge;
  void Function()? onDiceAccept;
  void Function()? onDiceDecline;
  void Function()? onDiceCancel;
  void Function(int peerScore, List<int> peerDice)? onDiceResult;
  void Function(String from, String action)? onEmote;

  // ── Session start ──────────────────────────────────────────
  Future<void> startAsMain({required String nickname, required Gungeoneer character});
  Future<void> startAsSidekick({required String nickname, String pinCode = '', Gungeoneer? character});
  Future<void> connectPaired({required PairedPartner partner, required MpRole role, String? nickname, Gungeoneer? character});
  Future<void> startPairing({required String nickname, required String pairingPin});
  Future<void> joinPairing({required String nickname, required String pairingPin});
  Future<void> cancelPairing();

  // ── Session lifecycle ──────────────────────────────────────
  Future<void> cancel();                // user cancels — tear down, restore pre-MP run
  Future<void> disconnect();            // user drops peer — stay in disconnected, can reconnect
  Future<void> reconnect();             // manual retry (rarely needed — auto-reconnect handles it)
  Future<void> notifyEndRunAndCancel(); // end run + tear down (called from settings)

  // ── Paired privilege ───────────────────────────────────────
  Future<void> resetRunWithNewGungeoneer(Gungeoneer newCharacter);

  // ── Gift/request API (delegated to MpSync) ─────────────────
  Future<void> sendGift({required String kind, required String name});
  Future<void> sendAddToPeer({required String kind, required String name});
  Future<String?> sendRequest({required String kind, required String name});
  Future<void> respondToPendingRequest(bool approved);

  // ── Dice/emote API (delegated to MpSync) ───────────────────
  Future<void> sendDiceChallenge(String challengerName);
  Future<void> sendDiceAccept();
  Future<void> sendDiceDecline();
  Future<void> sendDiceCancel();
  Future<void> sendDiceResult(int score, List<int> dice);
  Future<void> sendEmote(String action);

  // ── App-kill restore (called from HomeScreen) ──────────────
  Future<void> tryRestorePersistedSession();  // delegates to MpRecovery.tryRestore()

  // ── ProxyProvider support ──────────────────────────────────
  void updateRunProvider(RunProvider newProvider);

  // ── Static ─────────────────────────────────────────────────
  static String appVersionString = 'unknown';  // set in main.dart

  // ── Cleanup ────────────────────────────────────────────────
  @override
  void dispose();
}
```

**REMOVED from public API (vs current MultiplayerSession):**
- `status` (MpStatus) → replaced by `phase` (MpPhase)
- `connectionLogs` → deleted (no diagnostic console)
- `showReconnectHubNotifier` → deleted (no reconnect hub)
- `requestReconnectHub()` → deleted (no manual re-pair)
- `fullReconnectCycle()` → deleted (no manual re-pair)
- `setPinCode(String)` → deleted (no manual re-pair)
- `saveCurrentSession()` → internal only (MpStore handles it)
- `loadSavedSession()` → deleted (no manual saved sessions)
- `pauseRun()` / `resumeRun()` → deleted (pause feature removed)
- `isPaused` → deleted
- `canReconnect` → deleted (reconnect is automatic, no manual button)
- `autoReconnectAttempts` → deleted (no attempt counter in UI)
- `isAutoReconnecting` → deleted
- `peerLikelyGone` → deleted
- `lastCharacter` / `lastNickname` → deleted (not needed without manual reconnect)
- `sessionName` / `sessionId` → deleted (not displayed in new UI)
- `sessionStartedAtMs` → deleted (not displayed)

---

## 3. Protocol (v2)

**File:** `lib/models/multiplayer_messages.dart` — modify in place.

**Keep unchanged:** All message classes stay. The sealed `MpMessage` hierarchy, `encode()`, `decode()`, and all `fromJson`/`toJson` remain.

**Changes:**
- `MpHello.protocolVersion` → bump `currentProtocolVersion` from `1` to `2`. Old v1 clients are rejected with a friendly error: "Both devices need the latest app version. Update and try again."
- `MpSnapshot`: drop `tsMs` field. Remove from `toJson`/`fromJson`. `fromJson` ignores it if present (forward-compat with old saved data, though we're cleaning that up).
- `MpPing` / `MpPong`: drop `lastSeq` field. Remove from `toJson`/`fromJson`. Heartbeat is liveness-only.
- `MpHello`: keep `pinCode` for validation (security guard against wrong-endpoint connections).

**Delete:** `SavedMpSession` class (was in `multiplayer_session.dart`, replaced by `MpStore.MpSavedSession` in `mp_store.dart`).

---

## 4. UI Changes

### 4.1 MpLobbyScreen (replaces MultiplayerLobbyScreen)

**File:** `lib/screens/mp_lobby_screen.dart` (~600 lines)

**Main Player flow (unchanged from current):**
1. Enter nickname → pick character → START HOSTING.
2. Gets a 4-digit PIN shown on screen.
3. Navigates to `MpConnectScreen` (waiting for Sidekick).

**Sidekick flow (NEW — available games list):**
1. Enter nickname → tap FIND HOST.
2. Discovery starts. Screen shows a **live list of discovered games:**
   ```
   ┌──────────────────────────────────────┐
   │ ❤️ Partner: GF           [CONNECT]   │  ← paired partner (one-tap, no PIN)
   ├──────────────────────────────────────┤
   │ 🎮 Brave Bullet Kin    PIN: 1234     │  ← tap to select
   │ 🎮 Swift Dragun        PIN: 5678     │
   │ 🎮 Mighty Lich         PIN: 9012     │
   └──────────────────────────────────────┘
   ```
3. **Paired partners section (top):** If a paired partner is advertising (endpoint pin matches a known pairId), they appear at the top with a one-tap "CONNECT" button. No PIN entry. Filtered by pairId from `PairedPartnersStore`.
4. **Unpaired games section (below):** Each discovered endpoint shows nickname + PIN. User taps one → PIN entry field pre-fills with the PIN from the endpoint name → tap CONNECT.
5. If no games found after 5s, show "Searching for games… make sure the host has started hosting."
6. Endpoints disappear from the list automatically when not seen for 8s (stale removal in MpLink).

**Bottom links (simplified):**
- "Pair a Partner" — same as current pairing flow.
- "Paired Partners (N)" — same as current, one-tap connect.
- "How to Play" — same.
- ~~"Saved Sessions"~~ — **DELETED.**
- ~~"DIAGNOSTIC CONSOLE"~~ — **DELETED.**

**Permission rationale dialog:** Keep (same as current — explains BT + Wi-Fi before requesting permissions).

### 4.2 MpConnectScreen (replaces MultiplayerConnectScreen)

**File:** `lib/screens/mp_connect_screen.dart` (~300 lines)

Shows the connecting/connected state. Clean, no logs.
- **Connecting (hosting):** animated Main portrait + "Waiting for a partner to join…" + PIN displayed.
- **Connecting (browsing):** (this state is handled in the lobby screen — Sidekick doesn't navigate here until they've picked a game.)
- **Connecting (joining):** animated both portraits + "Connecting to [peer nickname]…"
- **Connecting (reconnecting):** "Reconnecting to [peer nickname]…" (shown only if user dismissed the reconnect dialog and navigated here manually — normally the dialog handles this.)
- **Connected:** both portraits + "Connected!" + auto-navigate to active run after 1s.
- **Error:** small banner with "Connection failed — RETRY" button. No scary error dialogs.
- **Permission denied:** banner with "Bluetooth/Wi-Fi permissions required" + "Open Settings" button.
- **No diagnostic console.** No log lines. No attempt counters. Clean.

### 4.3 MpReconnectBanner (replaces drop dialog)

**File:** `lib/widgets/mp_reconnect_banner.dart` (~150 lines)

Mounted in `HomeScreen` (same location as current `MpRequestListener`). Listens to `MpSession.reconnectNotifier`.

When peer drops (`reconnectNotifier` fires):
- Show a **dismissable modal dialog**: "Connection lost — reconnecting…" with a spinner and two buttons:
  - **DISMISS** — closes the dialog. User keeps using the app. A small persistent banner stays at the top of the active run screen: "Reconnecting… (tap to cancel)".
  - **CANCEL RUN** — tears down the session (`session.cancel()`).
- Auto-closes when `reconnectSuccessNotifier` fires → shows "Connection restored" snackbar (green, 2s).
- No "RE-PAIR" button. No "RETRY NOW" button. No log lines. No attempt counters. No "peer seems gone" warnings.
- Either it reconnects (auto, within seconds) or the user cancels. Simple.

**Top banner (persistent after dismiss):**
- Small pill at top of active run: "Reconnecting… (tap to cancel)"
- Tap → opens the dialog again (with CANCEL RUN option).
- Disappears automatically when reconnected.

### 4.4 MpRequestListener (simplified)

**File:** `lib/widgets/mp_request_listener.dart` — modify in place.

**Keep:**
- Gift/request incoming dialog (accept/deny sheet).
- Response toast snackbar ("peer accepted/denied X").
- Reconnect success snackbar (green "Connection restored!").

**Remove:**
- The drop dialog logic (moved to `MpReconnectBanner`).
- The `_ReconnectScreen` class (deleted — no manual re-pair).
- `showReconnectHubNotifier` listener (deleted — no reconnect hub).
- `peerLikelyGone` / `autoReconnectAttempts` references (deleted — no counters in UI).

---

## 5. State Machine (MpSession)

```
                    ┌──────────┐
                    │  idle    │◄────── cancel() / notifyEndRunAndCancel()
                    └────┬─────┘
                         │ startAsMain / startAsSidekick / connectPaired
                         │   (connectReason = hosting / browsing / restoring)
                         ▼
                    ┌───────────┐
        ┌──────────►│ connecting│───────────┐
        │           └─────┬─────┘           │
        │                 │ hello exchanged │
        │                 ▼                 │
        │           ┌──────────┐            │
        │           │ connected│            │ peer drops
        │           └────┬─────┘            │
        │                │ disconnect()     │
        │                ▼                  │
        │           ┌─────────────┐         │
        │           │ disconnected│◄────────┘
        │           └─────┬───────┘
        │                 │ peer reconnects
        │                 ▼
        │           ┌──────────┐
        │           │ connected│
        │           └──────────┘
        │
        │  peer reconnects (from disconnected)
        └──────────────────────────► connected

  permission denied ←── permissions rejected at start
  error             ←── protocol mismatch / advertising failed
```

**State transitions (exact conditions):**

| From | To | Trigger |
|------|-----|---------|
| idle | connecting | `startAsMain` / `startAsSidekick` / `connectPaired` / `tryRestorePersistedSession` |
| idle | permissionDenied | permissions rejected during start |
| connecting | connected | hello exchanged successfully |
| connecting | error | advertising/discovery failed, or search timeout (initial only, not reconnect) |
| connected | disconnected | peer drop (MpLink `onDisconnected` or heartbeat timeout) |
| disconnected | connected | peer reconnects (MpLink `onConnected` + hello) |
| disconnected | idle | `cancel()` |
| connected | idle | `cancel()` / `notifyEndRunAndCancel()` |
| any | idle | `cancel()` |

**On peer drop (connected → disconnected):**
- `MpSession` sets phase → `disconnected`, `connectReason` → `reconnecting`.
- Fire `reconnectNotifier` → UI shows dismissable dialog.
- `MpRecovery.onPeerDisconnected()` starts the reconnect loop.
- `MpStore.saveRunState()` fires immediately (belt-and-suspenders for app-kill).

**On peer reconnect (disconnected → connected):**
- `MpSync.onConnected()` sends full snapshot.
- `MpSession` sets phase → `connected`.
- Fire `reconnectSuccessNotifier` → UI closes dialog, shows snackbar.
- `MpRecovery.onPeerReconnected()` resets backoff.

**On cancel (any → idle):**
- `MpLink.stopAll()`.
- `MpSync.restorePendingGifts()` — restore in-transit gifts to inventory.
- If Sidekick: restore pre-MP run from `MpStore` (`pre_sidekick_run`).
- If `solo_run_backup` exists (app-kill restore overwrote a solo run): restore it.
- `MpStore.clear()`.
- `MpRecovery.cancel()`.
- `MpSession` sets phase → `idle`.

---

## 6. RunProvider Changes

**File:** `lib/providers/run_provider.dart` — modify.

**Remove:**
- `mpDisconnected` flag + setter + the `if (_mpDisconnected && !force) return;` guards in `addGun`, `removeGun`, `addItem`, `removeItem`.
- **Rationale:** With the new design, users CAN modify their own inventory while disconnected. Changes are included in the next full snapshot on reconnect. The peer's slot is a read-only mirror (only `MpSync` writes to it, wrapped in `_applyingRemote`), so there's no risk of the user corrupting peer state.

**Keep unchanged:**
- `applyPeerSnapshot` — used by `MpSync` to apply peer data to the correct slot.
- `applySharedStateFromPeer` — used by `MpSync` for coolness/curse/shrines.
- `startCoopPlayer` / `endCoopPlayer` — used by `MpSession` on start/cancel.
- `restoreEntireRunState` — used by `MpRecovery` on app-kill restore.
- `restoreRunScopeState` / `restoreMainSlot` — used by `MpSession` on Sidekick cancel.
- `addGun` / `addItem` / `removeGun` / `removeItem` (with `force` param, but without the `mpDisconnected` guard).

---

## 7. Complete File Inventory

### New files (create)
| File | Lines (est.) | Purpose |
|------|------|---------|
| `lib/services/mp/mp_link.dart` | ~350 | Transport layer (Nearby Connections wrapper) |
| `lib/services/mp/mp_sync.dart` | ~300 | State sync (snapshots, gifts, requests, dice, emotes) |
| `lib/services/mp/mp_pairing.dart` | ~200 | One-time pairing flow |
| `lib/services/mp/mp_recovery.dart` | ~250 | Reconnect loop + app-kill restore |
| `lib/services/mp/mp_store.dart` | ~150 | Persistence (single mechanism) |
| `lib/services/mp_session.dart` | ~400 | Thin facade (ChangeNotifier for UI) |
| `lib/screens/mp_lobby_screen.dart` | ~600 | Lobby with game list |
| `lib/screens/mp_connect_screen.dart` | ~300 | Connecting/connected view |
| `lib/widgets/mp_reconnect_banner.dart` | ~150 | Dismissable reconnect dialog + persistent banner |

### Modified files (EVERY file that references MultiplayerSession — verified via grep)
| File | Change |
|------|--------|
| `lib/main.dart` | Replace `MultiplayerSession` with `MpSession`. Replace `MultiplayerService` with `MpLink`. Call `MpStore.cleanupOldKeys()`. Set `MpSession.appVersionString`. Update `ChangeNotifierProxyProvider` types. |
| `lib/screens/home_screen.dart` | Replace `MultiplayerSession` with `MpSession`. Replace `tryRestorePersistedSession()` call (same method name, delegates to `MpRecovery`). Mount `MpReconnectBanner`. |
| `lib/screens/active_run_screen.dart` | Replace all `MpStatus.*` checks with `MpPhase.*`. Remove `saveCurrentSession()` calls (internal now). Remove error dialog logic for MP errors (handled by banner). Update `_mpSession` type. |
| `lib/screens/multiplayer_lobby_screen.dart` | **DELETE** — replaced by `mp_lobby_screen.dart`. (Old file removed, new file created.) |
| `lib/widgets/mp_request_listener.dart` | Remove drop dialog + `_ReconnectScreen` + `showReconnectHubNotifier` listener. Keep gift/request/dice/emote dialogs + reconnect success snackbar. |
| `lib/widgets/active_run/player_header.dart` | Replace `requestReconnectHub()` with nothing (auto-reconnect). Replace `connectionLogs` display with nothing (removed). Replace `saveCurrentSession()` with nothing (internal). Replace `MpStatus.*` with `MpPhase.*`. |
| `lib/widgets/active_run/player_page.dart` | Replace `MpStatus.idle` with `MpPhase.idle`. Replace `MultiplayerSession` type. |
| `lib/widgets/active_run/mode_helpers.dart` | Replace `MpStatus.idle` with `MpPhase.idle`. Replace `MultiplayerSession` type. |
| `lib/widgets/active_run/active_run_helpers.dart` | Replace `MultiplayerSession` type. Update any `MpStatus` references. |
| `lib/widgets/active_run/dice_roll.dart` | Replace `MultiplayerSession` type. |
| `lib/widgets/active_run/summary_tab.dart` | Replace `MultiplayerSession` type. Update `MpStatus` references. |
| `lib/screens/browse_screen.dart` | Replace `MultiplayerSession` type. |
| `lib/widgets/settings/settings_tab.dart` | Replace `MultiplayerSession` with `MpSession`. Remove `pauseRun()`/`resumeRun()` buttons (feature removed). Remove `saveCurrentSession()` call (internal). Remove `isPaused` check. Update `MpStatus` references. |
| `lib/providers/run_provider.dart` | Remove `mpDisconnected` flag + guards in addGun/addItem/removeGun/removeItem. |
| `lib/models/multiplayer_messages.dart` | Bump `currentProtocolVersion` to 2. Drop `tsMs` from `MpSnapshot`. Drop `lastSeq` from `MpPing`/`MpPong`. |
| `pubspec.yaml` | Version bump. |
| `assets/data/changelog.json` | New entry. |
| `lib/utils/asset_paths.dart` | Version string. |
| `lib/screens/main_menu_screen.dart` | Version string. |
| `VERSION_HISTORY.md` | New section. |

### Deleted files / classes
| File / Class | Reason |
|------|--------|
| `lib/services/multiplayer_session.dart` | Replaced by `mp/` components + `MpSession` |
| `lib/services/multiplayer_service.dart` | Replaced by `mp/mp_link.dart` |
| `lib/screens/multiplayer_lobby_screen.dart` | Replaced by `mp_lobby_screen.dart` |
| `SavedMpSession` class (was in multiplayer_session.dart) | Replaced by `MpStore.MpSavedSession` |
| `MpStatus` enum | Replaced by `MpPhase` |
| `_ReconnectScreen` class (was in mp_request_listener.dart) | No manual re-pair |
| "Saved Sessions" UI section | Auto-save/restore replaces it |
| "Diagnostic Console" UI section | Removed per user request |
| `MpServiceEvent` class hierarchy (was in multiplayer_service.dart) | Replaced by MpLink callbacks |

### Kept unchanged
| File | Reason |
|------|--------|
| `lib/models/paired_partner.dart` | Sound model |
| `lib/services/paired_partners_store.dart` | Sound store |
| `lib/models/multiplayer_messages.dart` | Sound messages (minor field drops — see §3) |

---

## 8. Implementation Phases

### Phase 1 — Transport + Facade + Store (Day 1-2)
**Create:**
- `lib/services/mp/mp_link.dart` — transport with persistent advertising + discovery loop + endpoint list + auto-connect modes + heartbeat.
- `lib/services/mp/mp_store.dart` — persistence + `cleanupOldKeys()`.
- `lib/services/mp_session.dart` — facade with `MpPhase` enum, `MpConnectReason` enum, basic start/cancel/connect. Sub-components stubbed (MpSync/MpPairing/MpRecovery created but with minimal implementations — just enough for Phase 1 testing).

**Modify:**
- `lib/main.dart` — wire `MpSession` into providers, call `MpStore.cleanupOldKeys()`.
- `lib/screens/home_screen.dart` — mount `MpReconnectBanner` (stub), call `tryRestorePersistedSession()`.

**Test gate:** Main can advertise, Sidekick can discover and see endpoint list, basic connection + hello exchange works. `flutter analyze` clean.

### Phase 2 — Sync + Recovery (Day 2-3)
**Create:**
- `lib/services/mp/mp_sync.dart` — full snapshot on connect/reconnect, debounced on change, gifts/requests/dice/emotes, pending gift tracking, `_applyingRemote` guard.
- `lib/services/mp/mp_recovery.dart` — reconnect loop with backoff cadence, app-kill restore, app-foreground resume.

**Modify:**
- `lib/services/mp_session.dart` — wire `MpSync` and `MpRecovery` into the facade. Implement all gift/request/dice/emote API delegation.
- `lib/providers/run_provider.dart` — remove `mpDisconnected` flag + guards.

**Test gate:** Two devices connect, add items, see them sync. Kill one app, restart, auto-restores. Walk out of range, come back, auto-reconnects within 10s. `flutter analyze` clean.

### Phase 3 — Pairing (Day 3-4)
**Create:**
- `lib/services/mp/mp_pairing.dart` — one-time pairing flow, edge case handling.

**Modify:**
- `lib/services/mp_session.dart` — wire `MpPairing`, implement `connectPaired` + elevated privileges + `resetRunWithNewGungeoneer`.

**Test gate:** Pair two devices, one-tap connect works, reconnect uses fast backoff. `flutter analyze` clean.

### Phase 4 — UI (Day 4-5)
**Create:**
- `lib/screens/mp_lobby_screen.dart` — lobby with game list (paired section + unpaired section).
- `lib/screens/mp_connect_screen.dart` — clean connecting/connected view.
- `lib/widgets/mp_reconnect_banner.dart` — dismissable dialog + persistent banner.

**Modify:**
- `lib/widgets/mp_request_listener.dart` — remove drop dialog + `_ReconnectScreen` + `showReconnectHubNotifier`. Keep gift/request/dice/emote + reconnect snackbar.
- `lib/widgets/active_run/player_header.dart` — remove reconnect hub button, console, save button. Update phase references.
- `lib/widgets/active_run/player_page.dart` — update phase references.
- `lib/widgets/active_run/mode_helpers.dart` — update phase references.
- `lib/widgets/active_run/active_run_helpers.dart` — update type references.
- `lib/widgets/active_run/dice_roll.dart` — update type references.
- `lib/widgets/active_run/summary_tab.dart` — update type references.
- `lib/screens/browse_screen.dart` — update type references.
- `lib/screens/active_run_screen.dart` — update phase references, remove error dialog, remove save call.
- `lib/widgets/settings/settings_tab.dart` — remove pause/resume buttons, update phase references.

**Test gate:** Full user flow — host, see list, connect, play, drop, reconnect, pair, one-tap. All 16 consuming files compile. `flutter analyze` clean.

### Phase 5 — Cleanup + Release (Day 5-6)
**Delete:**
- `lib/services/multiplayer_session.dart`
- `lib/services/multiplayer_service.dart`
- `lib/screens/multiplayer_lobby_screen.dart`

**Modify:**
- `lib/models/multiplayer_messages.dart` — bump protocol version to 2, drop `tsMs`/`lastSeq`.
- Remove all dead imports.

**Verify:**
- `flutter analyze lib/` — MUST be 0 issues.
- `flutter build apk --release` — MUST succeed.
- Full regression test: all MP features work (host, join, pair, one-tap, gifts, requests, dice, emotes, reconnect, app-kill restore).
- Version bump + release checklist (5 files: pubspec.yaml, asset_paths.dart, changelog.json, VERSION_HISTORY.md, main_menu_screen.dart).

---

## 9. Reconnect Timing Targets

| Scenario | Current | Target |
|----------|---------|--------|
| Peer walks out of range, comes back in 30s | 30-60s detection + maybe never reconnects (timing lottery) | < 5s detection (25s heartbeat) + < 5s reconnect = **< 10s total** |
| Peer closes app, reopens | Manual lobby + PIN + saved session load | **Silent auto-restore** — app opens, run is back, advertising starts, peer reconnects when seen |
| Peer loses Wi-Fi, reconnects to same network | Same as out-of-range | **< 10s total** |
| Both apps killed simultaneously | Both must manually re-host/join | Both auto-restore on next launch, reconnect when both scanning |

---

## 10. Edge Cases (Foolproof Checklist)

| Edge case | Handling |
|-----------|----------|
| Both devices pick same role (Main+Main or Sidekick+Sidekick) | Hello validation rejects with "Both players picked Main. One needs to pick Join." → phase = error |
| Protocol version mismatch (v1 vs v2) | Hello validation rejects with "Both devices need the latest app version." → phase = error |
| PIN mismatch (wrong endpoint) | Hello validation rejects with "Connection code mismatch." → disconnect, keep searching |
| Permissions denied | phase = permissionDenied → UI shows "Open Settings" button |
| Advertising fails (BT off) | phase = error → UI shows "Try toggling Bluetooth" + RETRY |
| Discovery fails (BT off) | phase = error → UI shows "Try toggling Bluetooth" + RETRY |
| Disconnect during pairing | Abort pairing → "Pairing interrupted. Try again." → idle |
| Disconnect during initial handshake | Treat as peer drop → start reconnect loop |
| Disconnect during connected (mid-run) | phase = disconnected → reconnect dialog → auto-retry |
| App killed mid-session | MpStore has saved state every 5s → silent restore on next launch |
| App killed during reconnect | MpStore saved on disconnect → silent restore on next launch |
| Corrupt persisted state | MpStore.load() catches parse errors → returns null → fresh start |
| User starts solo run after app kill, then MP restore fires | Save solo run to `solo_run_backup` → restore on MP cancel |
| Gift sent, connection drops before peer receives | Pending gift tracked → re-sent on reconnect |
| Gift sent, peer receives but connection drops before confirmation | Peer's snapshot will include the item → confirmed on reconnect |
| User cancels while gifts are pending | Pending gifts restored to inventory |
| Duplicate MpPair message | `_pairPersistedLocally` guard → ignore |
| Duplicate MpGift message | `_seenGiftIds` dedup → ignore |
| Duplicate MpRequest message | `_seenReqIds` dedup → ignore |
| Request sent, peer never responds | 30s timeout → toast "peer didn't respond" |
| Nearby Connections plugin throws platform exception | Caught in MpLink → fire `onError` → phase = error |
| User taps CONNECT on stale endpoint (already gone) | MpLink `requestConnection` fails → toast "Game no longer available" → stay in lobby |
| Multiple endpoints found simultaneously | All shown in list → user picks one → only that one is connected to |
| Paired partner not found (offline) | Paired section shows "No paired partners nearby" → user uses PIN flow instead |
| User dismisses reconnect dialog, keeps playing | Changes queue locally → included in next full snapshot on reconnect |
| User dismisses reconnect dialog, wants to cancel later | Persistent banner "Reconnecting… (tap to cancel)" → tap → dialog with CANCEL RUN |

---

## 11. Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Nearby Connections persistent advertising drains battery | BLE advertising is low-power (~1mA). Wi-Fi Direct only activates on connection. Monitor in testing. |
| Discovery loop (3s on / 1s off) drains battery on Sidekick | After 60s of no results, slow to 5s on / 5s off. After 5 min, 5s on / 15s off. Never stops (run is alive). |
| Full snapshot on every change is wasteful | Snapshot is ~300 bytes. Debounced 200ms. Over Wi-Fi Direct this is negligible. |
| Reconnect state machine has race conditions | MpLink owns single `_busyTransition` guard. MpRecovery is the only thing that controls reconnect cadence. No parallel retry paths. |
| App-kill restore fails (corrupt JSON) | MpStore.load() catches all parse errors, returns null, falls back to fresh start. |
| Gifts lost in transit on disconnect | MpSync tracks pending gifts, re-sends on reconnect, restores on cancel. |
| `_applyingRemote` guard not cleared on exception | Set in try block, cleared in finally block — guaranteed cleanup. |
| Old SharedPreferences keys linger after upgrade | `MpStore.cleanupOldKeys()` called once on first launch. |
| User confused by removed features (Saved Sessions, console, pause) | Changelog entry explains: "MP rebuilt from scratch — reconnect is now automatic. No manual save/load needed." |
| Protocol v2 breaks old v1 clients | Both devices are user-controlled. Error message is friendly: "Update both devices to the latest version." |

---

## 12. Acceptance Criteria (Definition of Done)

The rebuild is complete when ALL of these pass:

1. **`flutter analyze lib/`** — 0 issues.
2. **`flutter build apk --release`** — succeeds.
3. **Host + Join flow:** Main hosts → gets PIN → Sidekick sees game in list → enters PIN → connects → both see each other's character + inventory.
4. **Pairing flow:** Pair two devices → both appear in Paired Partners → one-tap connect works → no PIN needed.
5. **Reconnect (out of range):** Both connected → one walks away → reconnect dialog appears → walk back → auto-reconnects within 10s → dialog closes → "Connection restored" snackbar → both slots synced.
6. **Reconnect (app kill):** Both connected → kill one app → reopen → silent restore → run is back → reconnects to peer automatically.
7. **Reconnect (both killed):** Kill both apps → reopen both → both restore → reconnect to each other.
8. **Dismiss dialog + keep playing:** Peer drops → dismiss dialog → add items to own inventory → peer returns → reconnect → items sync.
9. **Gifts:** Send gift → peer receives → disconnect mid-send → reconnect → gift re-sent → confirmed.
10. **Requests:** Send request → peer sees dialog → accept/deny → toast on sender.
11. **Dice:** Challenge → accept → both roll → results shown.
12. **Emotes:** Send kiss → peer sees animation.
13. **No logs in UI:** No diagnostic console, no log lines, no attempt counters anywhere.
14. **No manual save/load:** No Saved Sessions list. Everything automatic.
15. **No pause/resume:** No pause button in settings.
16. **Version bump:** All 5 release-checklist files updated.
