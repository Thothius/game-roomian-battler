# Phase 4 — run_provider.dart Split Spec (verified 2026-10-30)

> Execute mechanically. `run_provider.dart` = 2,166 lines.
> `class RunProvider with ChangeNotifier` (mixin composition — mixins
> applied after `with ChangeNotifier` may use `on ChangeNotifier` safely).
> Guards: `test/persistence_contract_test.dart` (keys+shapes) and
> `test/mp_wire_contract_test.dart` must stay green throughout.

## Mechanism: mixins in part files (NOT `part` bodies)

A Dart class can't be split across files, but **mixins in part files
can** — same library, so private members stay visible. Pattern:

```dart
// lib/providers/run_provider.dart
part 'trackers/special_trackers.dart';
part 'run_persistence.dart';
part 'synergy_queries.dart';

class RunProvider with ChangeNotifier, _SpecialTrackers, _RunPersistence,
    _SynergyQueries {
```

```dart
// lib/providers/trackers/special_trackers.dart
part of '../run_provider.dart';

mixin _SpecialTrackers on ChangeNotifier {
  // abstract member requirements satisfied by RunProvider:
  RunState get _runState;
  void _scheduleSave();
  void _log(RunLogEntry e);
  void _checkNewSynergies(List<Synergy> before);
  ...
}
```

Abstract member signatures in a mixin are requirements fulfilled by the
composing class — legal Dart, resolves cross-mixin calls cleanly.

## Extraction 1 — `_SynergyQueries` — ✅ DONE (`783b5e9`)

Extracted to `lib/providers/synergy_queries.dart` (mixin in part file). Main file now ~1,993 lines. Note: `currentOwnedLower` is a 2-line arrow getter — arrow getters need multi-line capture in extraction scripts.

**Part file:** `lib/providers/synergy_queries.dart`

Move (line ranges, verified):
- `getActiveSynergies()` 1745–1764
- `getActiveSynergiesForSlot()` 1765–1790
- `getSynergiesByInventory()` 1791–1803
- `_collectFor()` 1804–1829
- `getActiveSynergiesCombined()` 2029–2038
- `synergyCountFor` + `_synergyCountCache` + `_buildSynergyCountCache` 2079–2090 + 2124–2140
- `synergiesCompletedBy` + `_completesSig`/`_completesOwnedLower`/`_completesCache` 2092–2122
- Top-level `SynergyStatus` (2142+) and `ItemSynergies` (2153–EOF) — move whole classes into the same part file.

**Abstract requirements:** `List<Synergy> get _allSynergies;`
`RunState get _runState;` — verify each moved method for `_gunByName`/
`_itemByName`/lookup-map references and declare those too.

## Extraction 2 — `_SpecialTrackers` — ✅ DONE (`815b3ed`)

Extracted to `lib/providers/trackers/special_trackers.dart` (mixin in part file). Main file now ~1,614 lines. Moved code needed NO abstract decls (removed 4 unused requirements — track them per-extraction, don't pre-declare).

Findings: `_windgunnerTimer` field at line ~105 travels with the tracker
group (startWindgunner/cancelWindgunner ~727-742, dispose cancels at ~748).
Reset block at ~1239-1242 (zeroes windgunner + robot armor, before
endRun ~1289) — move into `_resetRunScopedSpecials()` in the mixin.
Setters write prefs directly + notifyListeners (satisfied by
`on ChangeNotifier`); also declare `RunState get _runState;` and
`void _scheduleSave();` as abstract requirements if any setter touches
them — verify each moved method

**Part file:** `lib/providers/trackers/special_trackers.dart`

Move:
- Tracker fields 61–132 (gunderfury, tripleGun, evolver, spice, shellegun,
  chamberGun, platinum, ironCoin, polaris, gunther, gunSoul, sprun,
  windgunner, robot×5, huntress×2, metronome, boxingGlove, cigarettes)
- Getters 134–163
- All setters 573–877 (incl. `setHuntressRoomClears`…`setCigarettesUses`,
  `startWindgunnerCountdown`/`cancelWindgunnerCountdown` 723–742)
- `_persistSpecial` 880–~895
- `_loadSpecialUpgrades` 534–~570
- endRun's tracker-reset block — locate inside `endRun` and move resets
  into a `void _resetRunScopedSpecials()` in the mixin; call it from
  endRun.

**Abstract requirements:** `void _persistSpecial` internal; needs
`_scheduleSave()`? — check each setter; most write prefs directly +
`notifyListeners()` (available via `on ChangeNotifier`). Gunther/polaris
setters may call `_log`/`_checkNewSynergies` — declare as needed.

## Extraction 3 — `_RunPersistence` (markers verified 2026-10-30)

Extraction markers (post-4b line numbers):
- Fields: `Set<String> _favourites` (~63), `String _lastPlayedCharName` (~80),
  `Timer? _saveDebounce` (~93)
- Methods: saveRun (~399), _scheduleSave (~404), _saveRun (~411),
  _loadFavourites (~431), _saveFavourites (~441), _loadLastPlayedChar (~452),
  _saveLastPlayedChar (~461), saveLastPlayedCharacter (~473),
  isFavourite (~484), toggleFavourite (~487), resetFavourites (~499),
  favouritesCount (~505), restoreRunScopeState (later ~1074)
- Abstract requirements needed in mixin: ONLY `RunState get _runState;`
  (used by _saveRun toJson). _encodeRunState is top-level — visible to
  part files via shared library. _favourites field accessed by
  getFavouriteGuns/Items staying in main — legal (same class).
- endRun/_loadData call sites for _scheduleSave/_loadSpecialUpgrades/
  _loadFavourites/_loadLastPlayedChar stay in main — calling mixin
  members is legal within the composed class.
Part file: lib/providers/run_persistence.dart → part of 'run_provider.dart';
mixin _RunPersistence on ChangeNotifier. Then update class decl:
with ChangeNotifier, _SpecialTrackers, _SynergyQueries, _RunPersistence.

## Extraction 3 — `_RunPersistence`

**Part file:** `lib/providers/run_persistence.dart`

Move:
- `_scheduleSave` 461–467 + `_saveDebounce` field 105–~112
- `_saveRun` 469–484 (incl. compute + double-buffer — keep identical)
- `_loadFavourites`/`_saveFavourites` 486–503 + `_favourites` field 59
  + favourites methods 896–917 (or keep favourites in main — your call)
- `_loadLastPlayedChar`/`_saveLastPlayedChar` + `_lastPlayedCharName` 88
- `restoreRunScopeState` 1074 (check refs — may stay in main)

**Abstract requirements:** `RunState get _runState;` +
`set _runState` if restore writes it.

## What stays in run_provider.dart

imports + part decls, class decl, master data lists + lookup maps
(34–58), `runState`/`isLoading`/`hasCoop` getters, `loadData`,
`_refreshAgainstData`, `_log`, `_checkNewSynergies`, `_buildPlayerFor`,
run lifecycle (startNewRun/startCoopPlayer/endRun/endCoopPlayer/
restoreRunScopeState if it stays), inventory mutations (addGun/addItem/
removeGun/removeItem/adjust*), DPS/worth/quality aggregates (1855–2027),
dispose. Lands around ~1,300 lines.

## Verification per extraction

1. `C:\src\flutter\bin\flutter.bat analyze` — zero issues required
2. `flutter test test/persistence_contract_test.dart test/run_provider_test.dart test/synergy_logic_test.dart test/browse_synergies_test.dart` after each move
3. Full `flutter test` before commit
4. One commit per extraction

## Gotchas

- `on ChangeNotifier` works because `with ChangeNotifier` makes the
  mixin-superclass a ChangeNotifier — but mixin ORDER matters: declare
  `_SpecialTrackers` etc. AFTER `ChangeNotifier` in the `with` list.
- Private field names (`_runState`) are library-scoped — visible inside
  part files freely.
- If a moved method calls `_playerFor`/`_replacePlayer` (in main), either
  declare it abstract in the mixin or leave that method in main.
- `SynergyStatus`/`ItemSynergies` move cleanly — they're top-level.
