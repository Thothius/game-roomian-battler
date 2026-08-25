# MP Assessment — Views, Networking, UX

**Date:** 2026-08-25  
**Assessed by:** Devin (Slot 1)  
**Method:** Code review + Playwright web testing + FakeMpLink integration tests

---

## 1. NETWORKING CODE ASSESSMENT

### 1.1 Architecture — Sound ✅

The MP layer is well-structured in 4 clean layers:

| Layer | File | Responsibility |
|-------|------|---------------|
| Transport | `mp_link.dart` | Nearby Connections wrapper (BT/Wi-Fi) |
| Sync | `mp_sync.dart` | State sync, gifts, requests, dice, emotes |
| Recovery | `mp_recovery.dart` | Reconnect logic, app-kill restore |
| Session | `mp_session.dart` | UI facade, lifecycle, phase management |

**Verdict:** Clean separation of concerns. The `MpTransport` interface extraction makes it testable. 137 tests pass (20 reliability + 12 integration + 105 existing).

### 1.2 Reconnect Logic — Works but Fragile ⚠️

**How it works:**
1. Peer drops → `onDisconnected` fires → `MpSession._onLinkDisconnected()` sets phase to `disconnected`
2. `reconnectNotifier` fires → `MpReconnectBanner` shows dialog
3. Main re-advertises, Sidekick re-discovers with adaptive cadence:
   - 0–1 min: 3s on / 1s off (aggressive)
   - 1–5 min: 5s on / 3s off (moderate)
   - 5+ min: 7s on / 7s off (gentle, reduces radio thrashing)
4. On reconnect: hello handshake → snapshot sync → `reconnectSuccessNotifier` fires → dialog closes

**Bug: Radio cooldown is fixed at 800ms**
- `radioCooldownMs = 800` is hardcoded. Some Android devices need 1000ms+.
- **Risk:** Reconnect silently fails on devices with slow BT stack.
- **Fix:** Make it adaptive — start at 800ms, increase on failure.

**Bug: No maximum reconnect duration**
- Recovery runs forever until the user cancels. If the peer is truly gone (left the building), the radio thrashes indefinitely.
- **Fix:** After 10 minutes, show "Partner seems gone — cancel?" prompt.

### 1.3 Heartbeat — Functional ✅

- 5-second ping interval, 25-second timeout.
- On timeout: `onDisconnected` fires → recovery starts.
- **Note:** The heartbeat timer is a `Timer.periodic` which may be killed by the OS when the app goes to background. `restartHeartbeat()` is called on app resume.

### 1.4 Snapshot Sync — Main-Authoritative ✅

- Main's snapshot is the source of truth for shared state (coolness, curse, shrines).
- Sidekick sends `MpSharedStateDelta` messages for shared state changes.
- Main applies the delta and re-broadcasts via snapshot.
- **Verdict:** Correct design — eliminates lost-write races.

### 1.5 Gift/Request Flow — Correct ✅

- Gifts remove from sender's inventory immediately, tracked as `_PendingGift`.
- Peer's snapshot confirms receipt → pending gift cleared.
- On cancel: `restorePendingGifts()` puts items back.
- On reconnect: `resendPendingGifts()` re-sends unconfirmed gifts.
- **Verdict:** Robust — handles disconnect mid-gift gracefully.

---

## 2. BLUETOOTH vs WI-FI

### 2.1 Current Strategy

```dart
static const Strategy _strategy = Strategy.P2P_POINT_TO_POINT;
```

`P2P_POINT_TO_POINT` uses **both Bluetooth and Wi-Fi Direct**. Nearby Connections automatically picks the best transport:
- **Bluetooth Classic:** Slower (~250 KB/s), longer range (~30m), lower power
- **Wi-Fi Direct:** Faster (~2 MB/s), shorter range (~15m), higher power
- **Hybrid:** Uses BT for discovery, Wi-Fi Direct for data transfer

### 2.2 Do We Need Both?

**Yes, for now.** Nearby Connections `P2P_POINT_TO_POINT` requires both:
- Bluetooth for discovery (low power, works in background)
- Wi-Fi Direct for data transfer (needed for snapshot sync speed)
- Android requires Location permission for both (security requirement)

**Could we go Wi-Fi only?** Not with `nearby_connections`. The plugin doesn't expose a Wi-Fi-only strategy. You'd need a different transport (e.g., Wi-Fi LAN with manual IP entry, or a WebSocket relay server).

**Recommendation:** Keep BT + Wi-Fi. It's the standard for local multiplayer on mobile. The permission dialog explains this to the user.

---

## 3. MP VIEW ASSESSMENT — Bugs & Visual Shortcomings

### 3.1 MP Lobby Screen (`mp_lobby_screen.dart`)

**Current state:** Functional but bland. A form with nickname, PIN, two buttons, and a help link.

| Issue | Severity | Description |
|-------|----------|-------------|
| **No visual identity** | Medium | Plain form — no Gungeon aesthetic, no character preview, no atmosphere. Looks like a settings page, not a multiplayer lobby. |
| **No character preview** | Medium | HOST picks a character but the lobby doesn't show which one you'll play. JOIN doesn't pick a character at all — defaults to The Cultist silently. |
| **No connection status indicator** | Low | No BT/Wi-Fi icon showing whether the radio is ready. |
| **PIN field is always visible** | Low | The PIN field is shown for both HOST and JOIN, but HOST auto-generates it. Confusing — HOST users might think they need to enter a PIN. |
| **"How to Play" modal text runs together** | Bug | The steps in the modal render as one continuous text block — no line breaks between numbered steps. The `_HowToStep` widgets are there but the accessibility snapshot shows them as one string. |
| **No recent partners** | Low | `PairedPartnersStore` saves nicknames but doesn't show recently played partners. |
| **No back navigation guard** | Low | Pressing back during an active session calls `cancel()` but doesn't confirm. |

### 3.2 MP Connect Screen (`mp_connect_screen.dart`)

**Current state:** Good — pulsing portraits, PIN display, status messages, auto-navigate on connect.

| Issue | Severity | Description |
|-------|----------|-------------|
| **No timeout feedback** | Medium | If connection takes >45s, it transitions to error. But there's no progress indicator showing "30s elapsed" or "still searching." |
| **Portraits are generic** | Low | The "partner" portrait is a person icon until connected. Could show a silhouette or question mark with Gungeon styling. |
| **No cancel-during-connect feedback** | Low | Tapping CANCEL during connecting works but doesn't show a "Cancelling..." state. |
| **Connected screen is brief** | Low | "Connected!" shows for ~1 frame before auto-navigating. Could use a 500ms delay with a success animation. |
| **Error tip says "Bluetooth and Wi-Fi"** | Info | Correct per the permission requirement, but could be more specific: "within 10 meters" rather than "within range." |

### 3.3 Reconnect Banner (`mp_reconnect_banner.dart`)

**Current state:** Functional — modal dialog + persistent banner.

| Issue | Severity | Description |
|-------|----------|-------------|
| **"tap to cancel" is misleading** | Bug | The persistent banner says "tap to cancel" but tapping reopens the dialog (which has DISMISS and CANCEL RUN). It doesn't cancel directly. |
| **No reconnect attempt counter** | Low | By design (no log lines), but users have no idea if it's been 30 seconds or 10 minutes. A subtle "Reconnecting for 2 min…" would help. |
| **Dialog can be dismissed by tapping outside** | Low | `barrierDismissible: true` means a stray tap closes the dialog. The persistent banner appears, but the user might not notice. |
| **Orange accent is harsh** | Low | `Colors.orangeAccent` is bright and doesn't match the Gungeon aesthetic. Consider amber or a warmer orange. |

### 3.4 Active Run MP Integration

| Issue | Severity | Description |
|-------|----------|-------------|
| **No gift-received feedback** | Medium | When the peer sends you a gift, it appears in your inventory silently. No snackbar, no animation, no haptic. |
| **No connection quality indicator** | Low | No visual indicator showing connection strength (like signal bars). |
| **No "peer is typing" indicator** | Low | For emotes — no indicator that the peer is about to emote. |

---

## 4. SUGGESTED MP VIEW REDESIGN

### 4.1 Lobby Screen — "The Breach"

**Concept:** Make the lobby feel like the Gungeon's breach point — where two gungeoneers meet before descending.

**Layout:**
```
┌─────────────────────────────┐
│  ← MULTIPLAYER              │
│                             │
│  [Your Character Portrait]  │
│  TestHost                   │
│  The Marine                 │
│                             │
│  ┌─ NICKNAME ─────────────┐ │
│  │ TestHost               │ │
│  └────────────────────────┘ │
│                             │
│  ┌─ PIN (JOIN only) ──────┐ │
│  │ 0 0 0 0                │ │
│  └────────────────────────┘ │
│                             │
│  ┌─────┐  ┌──────────────┐  │
│  │ HOST│  │ CONNECT      │  │
│  └─────┘  └──────────────┘  │
│                             │
│  How to Play                │
└─────────────────────────────┘
```

**Key changes:**
1. **Character portrait at top** — shows your selected character with aura. HOST picks before seeing this; JOIN defaults to Cultist but can tap to change.
2. **PIN field only visible for JOIN** — HOST gets auto-generated PIN, no need to show the field.
3. **HOST button: primary color, full width** — "HOST GAME" with wifi tethering icon.
4. **CONNECT button: secondary color, full width** — "JOIN GAME" with login icon.
5. **Atmospheric background** — subtle particle effect or theme gradient, not transparent.
6. **Recent partners** — show last 3 nicknames as quick-fill chips below the nickname field.

### 4.2 Connect Screen — "Linking Up"

**Keep the current design** — it's good. Just polish:

1. **Add a 500ms delay on "Connected!"** before navigating — let the user see the success state.
2. **Add elapsed time** — "Searching for 15s…" below the spinner.
3. **Partner portrait** — use a Gungeon-style silhouette instead of `Icons.person_rounded`.
4. **Connected animation** — the check icon should scale-in with a spring, not just appear.

### 4.3 Reconnect Banner — "Signal Lost"

1. **Fix the "tap to cancel" text** → "tap to expand" or "tap for options."
2. **Add elapsed time** — "Reconnecting… 2 min" in the persistent banner.
3. **Add a max-reconnect prompt** — after 10 minutes: "Partner seems gone. Cancel run?"
4. **Softer color** — use `Colors.amber` instead of `Colors.orangeAccent`.

### 4.4 Active Run MP Polish

1. **Gift-received snackbar** — "Received: Marine Sidearm 🎁" with haptic.
2. **Connection indicator** — small icon in the top bar showing connection state (green dot = connected, orange = reconnecting, red = disconnected).
3. **Peer inventory peek** — long-press an item to see if the peer has it too.

---

## 5. PLAYWRIGHT TEST RESULTS

### What was tested:
- ✅ Home screen → Multiplayer button → Lobby screen loads
- ✅ Lobby shows nickname field, PIN field, HOST and CONNECT buttons
- ✅ "How to Play" modal opens and shows 4 steps
- ❌ HOST flow — fails on web (`MissingPluginException` for `nearby_connections`)
- ❌ CONNECT flow — same plugin failure

### What can't be tested on Web:
- Nearby Connections (Bluetooth/Wi-Fi discovery)
- Permission requests
- Actual device-to-device connection
- Reconnect flow
- Gift/request/dice/emote message routing (tested via FakeMpLink integration tests instead)

### What IS tested via FakeMpLink (12 integration tests):
- ✅ Full handshake (hello exchange, role negotiation, PIN match)
- ✅ Peer metadata exchange
- ✅ Snapshot exchange (no crash)
- ✅ Gift send (no crash)
- ✅ Request flow (pending request received)
- ✅ Dice challenge + accept/decline
- ✅ Emote send/receive
- ✅ Disconnect detection (both sides)
- ✅ Cancel/teardown (MpEndRun propagation)
- ✅ Add-to-peer (gift without removal)
- ✅ Ping/Pong heartbeat

---

## 6. PRIORITY ORDER FOR MP UX REWORK

1. **Fix "How to Play" modal text layout** — bug, quick fix
2. **Fix reconnect banner "tap to cancel" text** — bug, quick fix
3. **Add gift-received feedback** — high impact, medium effort
4. **Redesign lobby screen** — high impact, high effort
5. **Polish connect screen** — medium impact, low effort
6. **Add connection indicator to active run** — medium impact, low effort
7. **Add reconnect elapsed time** — low impact, low effort
8. **Add max-reconnect prompt** — low impact, low effort

---

*This document is the canonical MP assessment. Update when views are reworked or new issues are found.*
