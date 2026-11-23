# Backpack — Masterplan

> Status: **PLANNED — awaiting build GO**
> Decisions locked via 8-question interview (2026-11-25). See "Locked decisions" below — do not re-litigate.

## Vision

End-of-run inventories get fat (10–20 guns + items per player). The **Backpack** is per-player storage: stash gear out of sight into a designed 12-slot bag. Pure visual declutter — **everything inside still counts** toward synergies, passives, coolness/curse, DPS, dashboards.

## Locked decisions

| # | Question | Answer |
|---|----------|--------|
| 1 | Slot layout | **Mixed pool, 12 total** (guns + items share slots) |
| 2 | Do stored items count? | **Everything counts** — backpack is view-layer declutter only |
| 3 | Backpack item | **App-only custom `Item`** injected at run start (not items.json) |
| 4 | Retrieve UX | Long-press inside backpack → TAKE OUT / DELETE / SEND |
| 5 | Backpack item rules | **Normal item rules** — deletable/transferable like anything |
| 6 | Full backpack (12/12) | **Block with toast** — item stays in open inventory |
| 7 | MP behavior | **Own backpack only** — transfers target partner's *open* inventory |
| 8 | Lifecycle | **Per-run, autosaved** — clears on new run, survives restart via save file |

## Architecture

### Data model — `Player.backpackKeys`

Store backpack membership as a `Set<String>` on `Player` — keys `'g:<GunName>'` / `'i:<ItemName>'`. Guns/items **stay in `player.guns`/`player.items`** — they are never removed, only flagged.

**Why this wins:** every existing reader (`ownedNamesLowerCombined`, synergy matching, `EffectTagger.scan`, dashboards, `composition`, `topGunAcross`, `gunDps`, quick-add OWNED check, coolness/curse aggregation) keeps working untouched → "everything counts" is structural, not bolted-on. The alternative (separate `Player.backpack` list) would require auditing ~10 aggregation points and risks silent misses.

- `Player.backpackKeys` — `Set<String>`, default empty, `copyWith` copies it.
- `Player.toJson`/`fromJson` — serialize as `'backpack': [...]` → autosave + run-restore get it free.
- **MP snapshots need NO wire change** — `MpSnapshot` syncs `gunNames`/`itemNames` only; backpacked items keep their names → peer still sees them owned (counts peer-side too). Backpack *placement* is local-only, matching "own backpack only". Protocol version unchanged.
- Known edge (accepted): force-added duplicate names share one key — stashing flags both. Rare; documented.

### RunProvider API

```dart
static const kBackpackItemName = 'Backpack';
static const kBackpackCapacity = 12;

Item get backpackItem;                    // synthetic Item factory
bool isBackpacked(Gun g, PlayerSlot s);   // 'g:name' ∈ keys
bool isBackpackedItem(Item i, PlayerSlot s);
int backpackCount(PlayerSlot s);
List<({Gun? gun, Item? item})> backpackEntries(PlayerSlot s); // mixed, pickup order
bool stash(Gun g, PlayerSlot s);          // false if full / is Backpack item
bool stashItem(Item i, PlayerSlot s);
bool unstash(Gun g, PlayerSlot s);
bool unstashItem(Item i, PlayerSlot s);
```

- `stash*` guards: capacity, `item.name == 'Backpack'` ("the bag can't hold itself"), already-stashed.
- `removeGun`/`removeItem` also drop the corresponding key (no ghost flags after delete/transfer/gift).
- RunLogEntry category `backpack` (or reuse closest existing) for stash/unstash audit trail.
- `_buildPlayerFor` appends `backpackItem` to `startingItems` — covers main + coop/Paradox automatically (fresh Player each).

### Synthetic Backpack item

```dart
Item(name: 'Backpack', type: 'Passive', quality: 'S',
     effect: 'Holds 12 pieces of gear out of sight. Everything inside still counts.',
     icon: '')
```

- `isPassive` → sits in ITEMS section, never consumed, no active effect.
- Effect text deliberately avoids EffectTagger damage/ammo regexes (verified wording — no "damage", "coolness", stat tokens).
- `icon: ''` → renderers special-case `'Backpack'` → `Icons.backpack` fallback (one-line check in the two icon call sites, or a `backpackItemIcon` helper).
- **Normal item rules** consequence: deleting it locks retrieval for that run (contents still count — cosmetic-only loss). Mitigation: small backpack shortcut button in the ITEMS section header is ALWAYS present when `backpackCount > 0 || player owns Backpack` — cheap insurance, doesn't violate "normal rules" (it's a shortcut, not a second item).

## UI

### 1. Long-press quick-actions pill — redesign + BACKPACK button

Current: two small icon-only circles (transfer, trash) floating over the card.

New: up to 3 larger buttons (~56px), icon + tiny caption under each:

```
[⇄ SEND]  [🎒 STASH]  [🗑 DELETE]
```

- Always shows STASH (solo included — that's the point).
- SEND only when `canTransfer` (existing rule).
- Same armed-tap pattern for SEND (tap once → arms orange, tap again → sends).
- STASH → `p.stash*(…, _slot)` → toast 'Stowed in backpack' or 'Backpack full (12/12)'.
- DELETE unchanged (existing undo snackbars).
- Backpacked items never appear in open grid → no unstash path needed here.

### 2. BackpackScreen — `lib/screens/backpack_screen.dart`

Pushed via `fastRoute` when the Backpack item tile is tapped (items grid + list row detect `item.name == kBackpackItemName` → open screen instead of detail). Also reachable from the ITEMS-header shortcut button.

Layout (dark neon, theme tokens, `Sliver`/`GridView` per conventions):

- **Header** — character avatar + name, `BACKPACK  n/12` counter, close button.
- **Bag visual** — stitched-panel container (flair.card, dashed inner border, subtle inner shadow) containing a responsive grid of stored entries.
- **Stored tiles** (~56–64px): `GameIcon` + tiny name label; guns get quality ring, items get type glyph fallback. Mixed order = pickup order (guns-then-items interleaved? — keep single list sorted by stash order via insertion… simplest: guns block then items block inside one scroll, OR true mixed by re-stash order — store order isn't tracked in a Set; use guns-then-items sections inside the bag, still "mixed pool" capacity-wise).
  - *Decision:* capacity is mixed (any item takes any slot); display groups GUNS / ITEMS inside the bag for scannability.
- **Empty slots** — dashed outlines filling remaining capacity so 12-ness is visible.
- **Empty state** — "Bag's empty — long-press gear and hit STASH" hint.
- **Tap stored tile** → opens the **full item/gun detail view** (`ItemDetailScreen`/gun detail — same destination as the open inventory, so wiki text, stats, synergies, LEB toggle all work identically). Consistent with inventory tap behavior; retrieval is one long-press away.
- **Long-press stored tile** → quick-action pill: TAKE OUT / DELETE / SEND (send = existing transfer-to-partner flow, partner's *open* inventory only). TAKE OUT returns it to the open grid instantly.
- Capacity full state is informational only (no add path inside backpack).

### 3. Open-inventory filtering

`player_page.dart` build: `guns`/`items` lists filtered with `!p.isBackpacked*(…, _slot)` before grid/list render. Section counts show **open** counts (what you see); backpack screen shows stored count. `topDpsName` crown — backpacked guns still eligible (everything counts).

### 4. DPS screen marker (small polish)

`DamageBreakdownScreen` gun rows get a tiny `Icons.backpack` badge when `p.isBackpacked(g, slot)` — overview stays honest about what's stowed.

## MP notes

- No protocol/wire changes. `kMpSocialEnabled` untouched.
- Peer editing: partner can still delete/transfer your backpacked items by name (open-trust model preserved); their client just doesn't see your stash placement.
- `sendAddToPeer` / gifts unaffected — gifted items land in partner's *open* inventory and can be stashed by them.

## Edge cases

| Case | Behavior |
|------|----------|
| Backpack item deleted | Retrieval locked that run; contents still count; ITEMS-header shortcut still opens the bag if `backpackCount > 0` |
| Stash the Backpack item itself | Blocked — toast |
| Backpack full | Blocked — toast 'Backpack full (12/12)' |
| Transfer/delete a backpacked item from... | Can't happen from open grid (filtered); inside backpack long-press DELETE removes item + key |
| Duplicate item names (force-add) | Share one key — both flag together (accepted) |
| New run | `backpackKeys` empty — `_buildPlayerFor` fresh Player |
| App restart mid-run | `Player.fromJson` restores keys |
| Coop slot | Independent `backpackKeys` per Player — P1/P2 bags are separate |

## Files

**New:**
- `lib/screens/backpack_screen.dart` — bag UI + stored-tile actions
- `test/widget/backpack_test.dart` — provider + widget coverage

**Modified:**
- `lib/models/player.dart` — `backpackKeys` field, copyWith, toJson/fromJson
- `lib/providers/run_provider.dart` — `backpackItem`, stash/unstash/count/entries API, `_buildPlayerFor` grant, key cleanup in remove*, RunLogEntry category
- `lib/models/run_log_entry.dart` — `backpack` category + icon/label (if enum extension needed)
- `lib/widgets/active_run/player_page.dart` — inventory filtering, redesigned action pill (+STASH), backpack-item tap → screen, ITEMS-header shortcut
- `lib/screens/damage_breakdown_screen.dart` — stashed-gun badge
- `VERSION_HISTORY.md`, `AGENT_STATUS.md` (task queue + slot)

## Test plan

- Provider: stash/unstash round-trip, capacity block at 12, Backpack-item stash block, key cleanup on removeItem/removeGun, toJson/fromJson round-trip, `_buildPlayerFor` grants item for main + coop.
- Widget: long-press pill shows STASH; stash → item leaves grid, appears in backpack; backpack screen renders n/12 + tiles; tap opens detail view; long-press TAKE OUT retrieves / DELETE removes / SEND transfers; full-backpack toast; Backpack item tap opens screen; narrow viewport no overflow.
- Regression: synergy count unchanged after stash (everything-counts proof), OWNED tag still shows for stashed item in quick-add.

## Verification

- `flutter analyze` clean; targeted tests; full suite green before commit.
- Manual: stash 12+ items, restart app mid-run, confirm bag persists.
