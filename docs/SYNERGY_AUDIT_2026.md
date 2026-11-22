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

---

## Re-audit pass 2 — 2026-11-25 (LEB eligibility deep-dive)

Second full pass over all 395 synergies focused on LEB simulation fidelity,
verified against the official Lich's Eye Bullets wiki page:

| Finding | Disposition |
|---------|-------------|
| Pure dual-wield synergies were ghost-listed as LEB-simulable | FIXED — `isLebExcludedSynergy` excludes every synergy whose effect is "guns are dual-wielded" (11 more beyond The Submachinist); Trigger Twins kept per wiki (non-wield bonuses still granted) |
| 3+-component synergies shown as LEB-only | FIXED — `lebNeedsRealPieces`/`lebSlotsNeeded`: Behold! (6 slots→+5), Cormorant (+3), In The Mood! (+2), Mmmmmmmmm MMMMmm! (+2), Resourceful Indeed (+3) now render in a "LEB counts as one piece" note instead of ghost rows |
| Run-context detail forced `lebView=false` even with real LEB | FIXED — resolves `playerHasLeb(slot) && showLichEyeBulletsSynergies`; toggle stays live |
| LEB prefs never auto-enabled on acquisition | FIXED — `_autoEnableLebViewsIfHeld` latch in RunProvider (startNewRun/startCoopPlayer/clearInventory/addItem/removeItem/transferItem/applyPeerSnapshot/endRun); flips both prefs once per acquisition, manual off respected until LEB leaves + returns |

Pool/structure/meta/icon audits from pass 1 remain valid — no data changes
this pass (all fixes are display/logic layer).

---

## Re-audit pass 3 — 2026-11-25 (structural K-of-N + activation correctness)

Third pass diffed every synergy against `tools/gungeon_dump.json` (440 raw
records, incl. duplicate/variant `#VOIDCORE`/`#SYNTHESIZERS*`/`#ZELDA`/
`#HOMINGBOMBS*` entries) **and** `tools/en_synergies.txt` (nameKey→localized
name cross-check, e.g. `#MERMAIDFISH` = すばらしい新世界 = "Brave New World",
`#PLASMARIFLE_ENCNAME` = "Thunderclap" confirming dump-internal names).

### Data fixes (app commit pending)

| Synergy | Was | Now (dump-verified) |
|---------|-----|---------------------|
| Smart Bombs | `Bomb` + anyOf[Crutch, Homing] — **Ice Bomb lost in the 9e48e86 pool pass** | groups `[[Bomb,Ice Bomb],[Crutch,Homing Bullets]]` (#HOMINGBOMBS2/3) |
| Deadly Distraction | Explosive Decoy + Monster Blood | **Decoy**(71) + Monster Blood → `#BLOODDECOY` |
| Deadlier Distraction | Explosive Decoy + Monster Blood, no key | `#BLOODEXPLOSIVEDECOY` |
| Frosty Distraction | Explosive Decoy + Heart of Ice | **Decoy**(71) + Heart of Ice → `#ICEDECOY` |
| Frostier Distraction | Explosive Decoy + Heart of Ice, no key | `#ICEEXPLOSIVEDECOY` |
| Blade Runner | exact duplicate of Running Blades (Deck4rd+Knife Shield, `#BLADESRUNNER`) | real `#BLADERUNNER` = Deck4rd+Origuni, ACTIVE_UNBOOSTED |
| In The Mood! | all 3 guns required | `any_of` 3 guns + **`any_of_min: 2`** (#QUAKE) |
| Chief Master | Alien Sidearm + 1-of-5 rounds | `any_of_min: 2` → +2 of 5 (#MASTER_CHIEF) |
| Synthetic Shield | Armor+Heart pair only | `any_of` 3 synthesizers + `any_of_min: 2` (#SYNTHESIZERS1/2/3) |
| The Void Corps | Cannon+Shotgun pair only | `any_of` 3 Void Core guns + `any_of_min: 2` (all 3 `#VOIDCORE` pairings = one synergy) |
| The Elephant in the Room | anyOf [Pig, Turkey, Owl] | + Chicken Flute, Super Space Turtle, Compressed Air Tank, Bait Launcher → `#ELEPHANTGUN` (7-piece pool) |
| Grouch | no key | `#GARBAGE` (Trash Gun 154 + Junk 127) |
| Klobbering Time | no key | `#KLOBBETIME` (already correct shape: Klobbe + anyOf[AU Gun, Moonscraper]) |
| Brave New World | no key, treated as needing all 3 | `#MERMAIDFISH` — already correct shape (Siren + anyOf[Trident, Bionic Leg]); Japanese string confirms name |
| Fairy Bow | `activation: INACTIVE` | `ACTIVE_UNBOOSTED` — dump has a live #ZELDA entry |

### Schema additions

- **`any_of_min`** (`Synergy.anyOfMin`, `requiredAnyOfCount`) — K-of-N pools.
  `matchesOwnedSet` counts owned pool members; `missingFor` reports the pick
  deficit ("any 2 of: …"); `prettyEffect` says "any N of"; detail screen labels
  the section `ANY N OF`; `lebSlotsNeeded` counts the pool as N slots.
- **`activation`** now parsed (`isGameInactive`) — `INACTIVE` entries are
  filtered out of active/partial/combined/predictor queries and the piece
  index. Post-fix zero INACTIVE synergies remain in the catalog; the guard is
  regression-proofing.

### LEB impact

- In The Mood! / The Void Corps are now 2 slots → gun + LEB satisfies them
  (previously misreported as needing real pieces).
- Chief Master = 3 slots → LEB + 2 real Master Rounds still needed.
- Item-only K-of-N synergies (Synthetic Shield, Smart Bombs) never reach gun
  LEB pages — unchanged.

### Provenance fixes (`items.json`)

- `Junk` id 580 → **127** (dump: 127=Junk, 580=SackKnightBoon) — resolves U-015's
  id collision.
- `Ser Junkan 1` id null → **580** (SackKnightBoon — the item that summons
  Ser Junkan; also explains the inactive `#TRASHJUNKAN` variant).
- `Master Round I–V` remain id-less — they have no dump item rows at all
  (ids 467–471 appear only inside `#MASTER_CHIEF.optionalItems`).

### Verified non-issues

- Dump `gunName`/`itemName` are **internal class names**, not display names —
  e.g. `Plasma Rifle`=Thunderclap, `Mermaid Gun`=Siren, `Trash Gun`=Trashcannon,
  `Wood Bow`=Bow, `Tiger`=Bait Launcher, `Cucco`=Chicken Flute, `Dog`(301)=
  Super Space Turtle, `Space Friend`(249)=Owl. All resolved via `en_items.txt`
  ENCNAME strings and id alignment — no catalog renames needed.
- `#HOMINGBOMBS4`, `#ELEPHANTGUN2`, `#GARBAGECOLLECTION` — first two absent
  from the dump (stale loc keys); GARBAGECOLLECTION already mapped to
  'Garbage Collecting'.

## Pass 4 — Deep Gemini verification (2026-11-22)

Batched audits run through Gemini web (gun stats ×239, item effects ×270,
synergy effects ×395 across 7 files, world/chapters/bosses/gungeoners,
catalog completeness). Raw Q&A saved in `.playwright-mcp/gemini_batches_v2/`.
**Every Gemini claim was re-verified against `tools/gungeon_dump.json` and/or
the official wiki before touching data — Gemini was wrong more often than
right.**

### Verified CORRECT (no change needed)

- All pass-3 synergy fixes re-confirmed vs dump records:
  - `#MASTER_CHIEF` = Alien Sidearm + **any 2 of 5** Master Rounds
    (`required:3`, optionalItems 467–471) — Gemini's "any ONE" claim was wrong.
  - `#KLOBBETIME` = Klobbe + (AU Gun | Moonscraper Laser) — "Cog of Battle"
    claim was wrong.
  - `#HOMINGBOMBS2/3` = (Bomb|Ice Bomb) + (Crutch|Homing Bullets) — Remote
    Bullets is NOT a valid third option.
  - `#GARBAGE` = Trashcannon + Junk(127) only — Lies/Ser Junkan alternatives
    unsupported by dump.
  - `#ZELDA` active record = Bow + Bomb only.
  - `#SYNTHESIZERS1/2/3` = three ACTIVE pairwise records = 2-of-3
    {Heart, Armor, Ammo Synthesizer(116, internal name 'Bullet Bait' —
    wiki.gg confirms display name Ammo Synthesizer, item ID 116)}.
  - `#ELEPHANTGUN` = Elephant Gun + any 1 of 7 (dump optionalGuns 359/369 +
    optionalItems 249/301/632/451/572 — ID-aligned to our Pig/Turkey/Owl/
    Chicken Flute/Super Space Turtle/Compressed Air Tank/Bait Launcher).
  - `#QUAKE` = any 2 of 3 guns; `#VOIDCORE` ×3 pairwise = 2-of-3;
    `#MERMAIDFISH` = Siren + (Trident|Bionic Leg); all four Distraction
    pairings; `#BLADERUNNER`/`#BLADESRUNNER`.
- **LEB semantics (official wiki)**: "Makes all guns act as if they have all
  of their synergies." 2-component synergies fully simulated; **3+
  component synergies count LEB as exactly ONE component** (Resourceful
  Indeed needs Elimentaler + 2 others). Dual-wield excluded except
  Trigger Twins; Rubenstein's Monster, Detective Mode (needs Badge),
  Jolter/There Is Only War special cases. **Our implementation already
  matches this** — K-of-N slot counting from pass 3 is correct.
- Boss HPs all match wiki infoboxes exactly (Mine Flayer 1760,
  Kill Pillars 555×4=2220, Lich 1995/2100/2100, Agunim, Interdimensional
  Horror) — Gemini's alternate values were wrong.
- syn_adv 1–4 (228 synergies): only flag was Chief Master — Gemini's own
  note contradicted it; wiki confirms our record is correct.

### Fixes applied from this pass

- `items.json`: Omega Bullets effect "final two shots"→"final shot"
  (wiki: final shot of magazine); Resourceful Sack type Passive→**Active**
  (wiki infobox + 3s recharge); Mustache effect — removed "Bello's shop
  15% cheaper" (that discount is **XtG-only** per wiki).
- `enemies.json`: removed exact-duplicate Chancellor row; Old Chancellor
  location Bullet Hell→**Gungeon Proper** (Old King is the floor-2 boss).
- `gungeoneers.json`: The Pilot `max_items` 1→**2** (starts with Hidden
  Compartment = +1 active slot; his own tips say "carry two actives").

### Rejected Gemini claims (verified wrong)

- syn_adv 5–7 adversarial pass flagged 55 synergies — nearly all false
  positives contradicting the dump (e.g. "Smart Bombs needs only Bomb +
  Homing Bullets", "Running Blades should be Excaliber + Knife Shield",
  "Tea for Two needs only one companion"). Adversarial prompting produced
  hallucinated "corrections"; dump structure wins.
- Gun stats: 30 flags, mostly dubious ("infinite ammo" claims vs wiki
  Ammonomicon stats, per-pellet vs total damage confusion). Left as
  `gun_stats_flags.txt` for optional future wiki spot-checks — none applied.
- Item flags Trusty Lockpicks ("can't open Rat Chests" — wiki says it CAN,
  uniquely among key items) and Vorpal Bullets (ours matches wiki verbatim)
  rejected.
- Catalog: "Glocktopus"/"Grygor"/"Shadow Magician"/"Fuselier" "missing
  bosses" are hallucinations; "missing guns" Armor/Heart Container/Rat Key/
  Old Crest are pickups not items; "Master Round VI" doesn't exist;
  "Sheathed Sword" is cut content; Com4nd0/Deck4rd stylizations are correct;
  "Ser Junkan 1" name is correct (Ser Junkan 1/2/3 are distinct items and
  the icon asset is `ser_junkan_1.webp`).
- Chapter floor:null+secret:true for secret floors is our schema, not an
  error; Marine max_guns:8 is a UI convention (no hard game cap).
