# Synergy & LEB Correctness Audit — 2026-11-20

External ground truth obtained via Gemini (Playwright session) describing
Enter the Gungeon's internal `AdvancedSynergyEntry.SynergyIsAvailable`
mechanic, cross-checked against our `synergies.json` /
`synergy_meta.json` / matching code.

## Ground truth (game mechanics)

1. **Co-op evaluation is strictly per-player.** The game checks
   `PlayerController.HasPickupID` on ONE player at a time — no cross-player
   inventory union. Pieces split across P1+P2 do NOT trigger a synergy.
   Lich's Eye Bullets is likewise not shared: only the holder gets
   simulated gun synergies.
2. **LEB** activates any synergy where the player owns ≥1 gun from the
   synergy's gun pools, bypassing all other requirements — EXCEPT
   synergies flagged `IgnoreLichEyeBullets` (confirmed example:
   Rubenstein's Monster, so the Gunslinger can't fuse a floor-1
   RUBE-ADY). Item-only synergies (zero guns in pools) can never be
   LEB-simulated. Even when simulated "active", effects requiring an
   unowned item/companion don't produce that item's behavior.
3. **"One of the following" is NOT always one-of.** Requirements are
   mandatory lists + optional pools gated by `NumberObjectsRequired`.
   Known multi-pick cases: Smart Bombs, Unbelievably Charming,
   Tea for Two, 360 Yes Scope (anchor + ≥2 from pool), Resourceful
   Indeed / Cormorant (all 4 pool items).
4. **Co-op quirks:** ghost form suspends a dead player's synergies;
   dual-wield binds to one inventory.DualWielding slot; orbitals/
   companions belong to the owning player only; Chamber Gun/Master
   Rounds and shop discounts check the interacting player.

## Audit findings vs. our code

| # | Finding | Severity | Status |
|---|---------|----------|--------|
| F1 | `getActiveSynergiesCombined()` + ALL pager page + item-detail statuses evaluated `active` against the UNION of both inventories — split pieces showed COMPLETE though the game never triggers them | High | FIXED — active now = either player's own inventory matches (`synergy_queries.dart`, `gun_synergies_tab.dart`, `item_detail_screen.dart`) |
| F2 | LEB ghost page listed every synergy including `IgnoreLichEyeBullets` exceptions | Medium | FIXED — `kLebExcludedSynergies` filter + `_LebBlockedNote` footnote (`gun_synergies_tab.dart`) |
| F3 | `any_of` model can't express mandatory+optional-pool-with-count (`NumberObjectsRequired ≥ 3`); known-bad data: `360 Yes Scope` (missing scope/accuracy pool entirely — data has items=[Scope], anyOf=[sniper guns] which is backwards), `Smart Bombs`/`Unbelievably Charming`/`Tea for Two` pools incomplete vs. game | High (data) | FIXED — `groups` field added; 3 synergies regrouped + Tea pool completed. NOTE: `360 Yes Scope` re-verified vs wiki — data was already correct (Scope + A.W.P./Sniper Rifle); audit claim was wrong |
| F4 | `Resourceful Indeed,` — trailing comma in synergy name | Low | FIXED — renamed; item effect_token cross-links now resolve |
| F5 | `synergy_meta.json.coop` (BOTH/P1/TEAM, 110 classified of 395) was parsed but never rendered | — | FIXED — CO-OP/TEAM/ONE PLAYER chip in `SynergyMetaChips`, gated by new `VisualPrefs.showSynergyCoopTags` toggle in Settings → SYNERGIES |
| F6 | LEB page can't distinguish gun-pool vs item-only synergies — verified OK: `getSynergiesFor(gun)` only returns synergies containing that gun, so every listed entry is LEB-eligible by the owns-a-gun rule | — | OK |
| F7 | `matchesOwnedSet` hardcodes Smart Bombs/Unbelievably Charming ≥2-alternatives and Super Serum gun+defense — consistent with game, but pool membership in JSON is incomplete (see F3) | Medium | OPEN (data) |

## Tests

- `test/coop_synergy_per_player_test.dart` — 4 tests pinning per-player
  co-op semantics: split pieces inactive, single-player pieces active
  (either slot), solo unchanged.

## Remaining work (recommend follow-up)

- Extend synergy schema for optional-pool counts, or curate the ~110
  `any_of` entries against the wiki; re-verify `360 Yes Scope`,
  `Smart Bombs`, `Unbelievably Charming`, `Tea for Two` first.
- Fix `Resourceful Indeed,` name typo (check references first).
- Expand `kLebExcludedSynergies` as more `IgnoreLichEyeBullets` cases
  are confirmed (Gemini cited unlock/quest-gated synergies generally).
- `synergy_meta.json` covers only 110/395 synergies — unclassified
  default to BOTH; a second classification pass would improve tag
  honesty.


## Addendum 2026-11-25 — full pool cross-validation vs `tools/gungeon_dump.json`

All 343 synergies with `game_name_key` were compared against the UnityPy
dump's `mandatoryGuns/Items` + `optionalGuns/Items` pools. **17 entries had
wrong/incomplete pools** — corrected in app `9e48e86` (Pea Cannon,
Plant Power, Alternative Rock, Natural Selection, Paperwork, Full Circle,
Lotus Bloom, I need scissors! 61!, What A Thrill, Sniper Woof, Relodestar,
Tile Match, The Void Corps, BEES, Deadly/Frosty Distraction, Blade Runner).
Notable: `required=2` in the dump is NOT total-pickups — Resourceful Indeed
confirmed all-4 via wiki; `Junk` id 580 collides with SackKnightBoon (U-015).
LEB exclusions expanded per official wiki (The Submachinist, Detective Mode).
