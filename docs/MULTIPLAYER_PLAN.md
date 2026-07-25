# Multiplayer (Bluetooth) — Architecture Plan

## North star

Two phones, one run, no internet. Each player tracks their **own** loadout on
their own device but every change (add/remove/transfer item or gun, coolness/
curse adjustment, shrine use, character pick) is mirrored to the paired phone.
Both devices stay viewable as "primary"; swiping into the other player shows
their loadout in near-real-time. The run can be paused, saved, and resumed
later because both phones are always writing the merged run state to disk.

Constraints:

- Free, local — Bluetooth Classic RFCOMM (or BLE GATT, see *Transport*)
- Not strictly real-time. ~3 s latency on a change is fine; the app
  is a tracker, not a multiplayer game.
- Conflict-resilient — players can both touch the run simultaneously
  without corrupting state.

## Core concepts

### 1. Stable IDs for guns + items

Today the app keys things by `name`. Names are unique enough for tracking but
will become brittle for sync (a rename, a typo, a coop transfer race). We add
a deterministic ID derived from the wiki name:

```dart
String stableId(String name) =>
    name.toLowerCase().replaceAll(RegExp(r'[^a-z0-9]+'), '_');
```

Examples: `Bee Hive` → `bee_hive`, `+1 Bullets` → `_1_bullets`,
`A.W.P.` → `a_w_p_`. Stored alongside `name` in JSON; never sent to the wire
without the canonical name as a fallback.

### 2. Run snapshot file

A single source of truth, written on every mutation:

```
<documents>/runs/<runId>.json
{
  "runId": "uuid-...",
  "version": 17,            // monotonically incremented per change
  "lastChangeAt": "2026-04-29T10:55:12Z",
  "lastChangeBy": "host" | "guest",
  "main":  { "characterId": ..., "gunIds": [...], "itemIds": [...],
             "coolness": 0, "curse": 0 },
  "coop":  { ... } | null,
  "shrinesUsed": ["chamber_4_shrine_of_glass"]
}
```

`version` lets us reconcile (last-writer-wins per field is fine; entire-file
wins when there's a clear "behind" peer).

### 3. Wire protocol

```
{ "type": "hello",   "v": 1, "role": "host"|"guest", "runId": "..." }
{ "type": "snapshot","ver": 17, "state": {...} }            // full
{ "type": "patch",   "ver": 18, "ops": [{ "op":"add_gun",
                                          "slot":"main",
                                          "id":"bee_hive" }] }
{ "type": "ack",     "ver": 18 }
{ "type": "ping" }      { "type": "pong" }
```

Patches enumerated:

| op            | fields                              |
| ------------- | ----------------------------------- |
| `add_gun`     | slot, id                            |
| `remove_gun`  | slot, id                            |
| `add_item`    | slot, id                            |
| `remove_item` | slot, id                            |
| `transfer`    | from, to, kind, id                  |
| `set_stat`    | which (cool/curse), delta or value  |
| `use_shrine`  | id, target slot                     |
| `set_char`    | slot, characterId                   |
| `clear_run`   | (end run)                           |

Coalesce: queue patches in a 250 ms tick; if a coalesce window fills more
than ~10 ops we send a fresh `snapshot` instead of a patch list.

### 4. Transport — Bluetooth Classic RFCOMM

Decision: **RFCOMM (Bluetooth Classic)** over BLE.

- Throughput is irrelevant (a snapshot is < 4 KB).
- RFCOMM gives us a familiar socket abstraction (`InputStream` /
  `OutputStream` on Android), no GATT attribute juggling.
- Pairing UX is the standard "select device" picker users already know.
- Plugin: `flutter_bluetooth_serial` (community-maintained) or roll our own
  over a thin platform channel + Kotlin `BluetoothSocket`.

Flow:
1. Host taps **Host Run** → starts an RFCOMM server with our service UUID.
2. Guest taps **Join Run** → discovers nearby paired devices, picks host,
   connects to the same UUID.
3. Both exchange `hello`. Host sends current `snapshot`. Guest's local
   provider replaces its run state with the snapshot.
4. Either side: every mutation goes through the provider, which fans the
   patch out to (a) local persistence and (b) the open socket.
5. On disconnect, both fall back to local-only mode but keep the snapshot
   on disk; reconnect resumes from highest version.

Permissions (Android 12+): `BLUETOOTH_CONNECT`, `BLUETOOTH_SCAN`,
`BLUETOOTH_ADVERTISE`. iOS: out of scope for this build.

### 5. UI surfaces

- `MultiplayerScreen` (already stubbed):
  - Host: button → "Waiting for partner…" → connected.
  - Join: list of paired devices, refresh, connect.
- Active-run header gets a small bluetooth pill: green = synced, amber =
  reconnecting, grey = solo.
- Header overflow menu gains "Disconnect" while a session is live.
- Inventory PageView already supports swiping between Player 1, Player 2,
  Summary — that surface stays unchanged.

### 6. Conflict policy

Every patch carries a monotonic `ver`. Both peers track:

```
localVer  : last version we *applied* locally
remoteVer : last version the peer told us about
```

- A peer receiving `ver <= localVer` discards the patch.
- A peer noticing it has fallen behind by ≥ 5 versions requests a fresh
  `snapshot` instead of catching up patch-by-patch.
- Add-then-remove the same id within one tick collapses to a no-op.
- Stat sets are last-writer-wins.

### 7. Persistence cadence

- **On mutation**: write the snapshot file immediately (already what we do
  for `current_run`). The disk write is on the same provider hook the
  mutation goes through, so persistence ≡ broadcast.
- **Backup snapshot**: rotate `runs/<runId>.bak.json` once per minute while
  a session is live. Lets a corrupted JSON be recovered.
- **Resume**: opening the app with a finished session intact prompts
  "Resume run?" with the last `lastChangeAt` timestamp.

## Build phases

1. **Stable IDs everywhere** (Dart-only, no transport yet). Touches model
   classes + provider; serialise alongside `name`. Backfill `stableId` on
   parser run.
2. **Run-file persistence v2** — write/read by `runId`, version-stamped.
3. **Local mock transport** — pretend "Bluetooth" sends are just method
   calls between two providers in the same process. Build the conflict
   plumbing here.
4. **RFCOMM transport** — platform channel + plugin, replace mock.
5. **Multiplayer screen wiring** — Host/Join, live-status pill.
6. **Resume UX**.

## Known unknowns

- Android 12 permission rejection flow (need a "permissions denied" empty
  state on the multiplayer screen).
- Reconnect on app backgrounding — the OS will tear down the socket;
  reopening should attempt rebind once.
- iOS / cross-platform: out of scope for this milestone. Long-term, BLE
  with a custom GATT service would unlock both platforms.

## Out of scope (for now)

- Networked > 2-player co-op.
- Spectator mode / shared dungeon map view.
- Shrine voting between paired phones.
