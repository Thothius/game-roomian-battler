# Next Steps Masterplan — README relaunch (+ parked: Online Co-op bridge)

> Authored 2026-11-25 (CORE / Slot 2). Planning doc only — nothing here is
> committed to build yet. **Active workstream: A) GitHub/README relaunch**
> (Reddit + sideload push). **PARKED — future plans only: B)
> GungeonOnlineCoOpMod companion plugin** — researched and specced below,
> explicitly NOT scheduled; revisit when the README/release push is done
> or the user asks.

---

## 0. Git state — push readiness

- `gh` CLI authed as `Thothius`; both remotes are HTTPS.
- **Already in sync** — `master` == `origin/master` on both repos
  (app `5604432`, root `aaddb08`). Another agent pushed recently; nothing
  is waiting. Future pushes: `git push` works as-is; if auth ever fails,
  `gh auth setup-git` fixes the credential helper.
- Reminder: app repo = code/APK assets; root repo = docs/coordination.
  README lives in the **app repo** (`gungeon_mate/README.md`).

---

## A. README rework — "storefront for sideloaders"

Goal: a Reddit-scrolling player lands on the repo and in 15 seconds knows
what it is, that it's safe/legit, and how to get the APK. Current README
predates the whole customization/menu rework — it's stale.

### Structure (3 custom sections + everything else)

User direction: fully custom **OVERVIEW** and **FEATURES** sections;
everything else (install, controls, troubleshooting, credits, license)
groups into a third catch-all section — working title **"GETTING STARTED
& REFERENCE"** (alt: "INSTALL / DOCS", "EVERYTHING ELSE"). Pick at write
time; it should read as a drawer, not a peer section.

1. **Hero block** — centered: banner image → app name → one-line pitch →
   badge row → screenshot strip → 3-button CTA (Download APK / Features↓ /
   Wiki-or-docs).
2. **OVERVIEW** (~3 short paragraphs, custom-written):
   - What it is: a companion app for Enter the Gungeon — run tracker,
     Ammonomicon-grade codex, quiz, themes, couch/nearby co-op.
   - The hook for this audience: "made for couch co-op, now with online
     co-op via GungeonOnlineCoOpMod" (cross-link once B ships).
   - Platform honesty: Android APK sideload + Windows/Linux desktop.
3. **FEATURES** (curated, scannable — NOT a changelog dump):
   - Run tracking / live dashboards / special-gun panels
   - Ammonomicon (full game-data codex: guns, items, synergies, shrines)
   - Gungeonmaster Quiz
   - Nearby co-op (host/join, surprise gifts, emotes, shared state)
   - Experience Studio: 27+ themes, palettes, particles, wallpapers,
     Neo-Skeuo skin
   - Cool & Curse, dice roller, stat tracking
4. **GETTING STARTED & REFERENCE** (the "third" bucket): install APK,
   desktop builds, controls, FAQ/troubleshooting, data sources
   (gungeon-dump provenance), credits, MIT/license note, links.

### Design/composition rules (for enticement)

- Centered hero, generous whitespace, max-width ~900px feel.
- Real screenshots, not mockups: menu backdrop, Ammonomicon, co-op lobby,
  studio theme gallery, Neo-Skeuo. Capture from design-lab or a debug APK.
- Badge row: version, platform, license, "offline-first", maybe
  `made for Enter the Gungeon`.
- Emoji: sparse, only where they aid scanning (per current app tone).
- Keep it fast-loading: hero banner WebP <300KB, screenshots WebP/JPG.

### TODO — header banners & art assets

- [x] **Hero banner** — DONE 2026-11-23: `gungeon_mate/docs/media/hero.webp`
      (1600×400, PIL composite: bullet_hell splash + app_icon + 14 sprites).
- [ ] **Section dividers** (optional, ~1200×60): thin ornament strips
      between OVERVIEW / FEATURES / REFERENCE.
- [ ] **Feature card icons** (optional): 6 small glyphs matching feature
      bullets — or skip and use emoji/text only (Ponytail: prefer skip).
- [x] **OG/social preview image** — DONE: `docs/media/og-image.jpg`
      (1200×630). **MANUAL STEP REMAINING:** upload at repo
      Settings → General → Social preview (no API exists).
- [x] **Screenshots** (8): real v3.7.0 captures via `flutter build web` +
      Playwright at 390×844 → `gungeon_mate/docs/media/shot-*.webp`.
- [x] Tools: PIL composites + Playwright MCP (no external gen needed).

### Work packages

- **R1**: DONE 2026-11-23 — hero.webp + og-image.jpg + 8 screenshots.
- **R2**: DONE 2026-11-23 — README rewritten (hero/OVERVIEW/FEATURES/
  GETTING STARTED & REFERENCE), dynamic version badge, stable APK link.
- **R3**: DONE 2026-11-23 — topics set (7), description/homepage already
  good, **v3.7.0 released** with stable `GungeonMate.apk` asset;
  social-preview upload is the only manual remainder.
- **R4**: Reddit post draft (separate doc when ready) — lead with the
  online-co-op angle if B lands first.

---

## B. GungeonOnlineCoOpMod companion — "party overlay" plugin

> **STATUS: PARKED / FUTURE PLANS — do not build unless the user asks.**
> Research is complete and the read path is proven cheap; this section is
> kept so the idea isn't lost. Nothing here is scheduled.

### What the mod actually is (researched 2026-11-25)

- Repo: `github.com/Hero88go/GungeonOnlineCoOpMod` — 17★, MIT license,
  1.0 beta, BepInEx 5.4 plugin in C# (Harmony). Installer exe or r2modman.
- Architecture (`docs/ARCHITECTURE.md`): **host-authoritative** — host runs
  the real game; clients simulate only their own player and follow host
  state. Once-a-second summary check compares enemies/rooms/chests/health/
  money/**inventories** and auto-repairs drift.
- Consequence for us: **inventory/loadout state for ALL players already
  exists in memory on the host** (and replicated copies exist on clients).
  We don't need to "hook up and know what each one has" — the mod already
  does. Our plugin just reads it.
- 2 players live, 4 in dev; invite codes; Steam/GOG/Epic cross-play;
  run persistence/reconnect is solid.
- `src/GungeonOnline/` layout: Net/, Session/, Input/, Replication/,
  Game/, Camera/, Dev/. `Replication/` handles inventories/vitals/pickups.

### The idea (user's framing, refined)

A companion that shows **all party members' inventories** — auto-filled
from the game, so our effort goes into PC-tailored features instead of
data plumbing. Hotkey-toggled overlay.

### Approach options (post-research ranking)

1. **Standalone BepInEx plugin (confirmed best fit)** — own DLL,
   references only game assemblies. Enumerate players via
   `GameManager.AllPlayers`, read inventories directly, render IMGUI
   overlay on a configurable hotkey. Works in vanilla couch co-op AND
   with GungeonOnlineCoOpMod (remote replicas are real PlayerControllers
   with reconciled inventories). Optional reflection layer adds their
   roster names/session info when the assembly is present.
   - Pros: zero upstream dependency, works today without their mod,
     future-proof vs their churn, MIT-clean.
   - Cons: needs item-name/quality DB lookup confirmed (P0 spike).
2. **Upstream contribution** — still worth an issue/PR later for a
   first-party state hook or cross-promotion, but no longer blocking.
3. **Hybrid localhost feed → Flutter app** — deferred to P3; only if the
   in-game IMGUI overlay proves too limiting.

### PC-tailored feature ideas (the fun part — data is free)

- **Party loadout board**: every member's guns/items/actives/passives,
  quality colors, cool/curse, health — one hotkey glance.
- **Cross-player synergy radar**: "you + Alex could complete *Bullet
  Time*" — we already have full synergy data + matching logic.
- **Boss/room callouts**: who's in combat, revive status, floor/seed info.
- **Shared scratchpad**: quick notes/pings per member (ties into our
  existing MP event-log patterns).
- **Draft assistant**: shop restock alerts, "Alex needs a blast shield".

### Phases (P0 research done — see findings above)

- **P0 — research spike** ✅ DONE 2026-11-25: repo mapped; read path is
  `GameManager.AllPlayers` → per-player inventory objects, no internal
  deps. Remaining P0 loose end: confirm item name/quality DB lookup API
  + EtG Unity/BepInEx target framework (30-min check in a decompiled
  Assembly-CSharp or their csproj references).
- **P1 — minimal overlay**: new BepInEx plugin project (netstandard2.0
  or match their net35), hotkey (default F9, configurable) toggles an
  IMGUI panel: per-player card with character name, HP hearts, guns
  (name+ammo+quality color), actives/passives. Test in couch co-op.
- **P2 — polish + online verification**: quality-tier colors, collapsible
  sections, position/scale config; verify remote-player data shows
  correctly inside a GungeonOnlineCoOpMod session (host AND client).
- **P3 — GungeonMate integration (optional)**: localhost JSON feed →
  Flutter desktop overlay reusing theme/flair stack; synergy radar.
- **P4 — distribution**: r2modman package + README/docs mention;
  optional upstream PR/issue for cross-promotion.

### P0 research findings (done 2026-11-25 — repo cloned to `.research/GungeonOnlineCoOpMod`)

Cloned and mapped. ~21k lines C#, `net35` target, BepInEx 5.4 + Harmony,
references the game's `Assembly-CSharp.dll` directly (Steam/GOG/Epic
identical). Version `1.2.19`.

**Player enumeration — the key unlock:**
- Vanilla API `GameManager.AllPlayers` already returns every
  `PlayerController` — their codebase has 168 call sites for it
  (`docs/COOP-INTERACTIONS.md`). Remote players spawned by the mod are
  real `PlayerController`s in the scene.
- Fallback: `Object.FindObjectsOfType<PlayerController>()`.
- **Zero dependency on their assembly internals** — `PlayerSlots` is
  `internal`, but we don't need it. `AllPlayers` covers vanilla couch
  co-op AND their online co-op AND future 4-player builds.

**Inventory data per player (all local, no netcode needed):**
- `p.inventory.AllGuns` → `Gun` objects: `PickupObjectId`, `CurrentAmmo`,
  quality tier, display name (resolve via game's item DB — exact API
  to confirm in P0; their `InventorySync` works in raw `PickupObjectId`s).
- `p.passiveItems`, `p.activeItems` → `Item`/`ActiveItem` lists.
- `p.CurrentGun`, health (`healthHats`), character identity
  (`characterID` → name/portrait via game DB).
- Their `Replication/InventorySync.cs` proves the shape: it serializes
  exactly these fields for all players every 0.25s — we read the same
  objects post-reconcile, so data is already correct on every machine.

**UI/rendering precedent (copy, don't invent):**
- IMGUI `OnGUI` panels — proven in `Session/OnlineMenu.cs`,
  `Session/Toasts.cs`, `Game/PartnerUI.cs`, `Game/MapPing.cs`.
- Hotkey toggle precedent: `NetConfig.OverlayKey` ConfigEntry +
  `Input.GetKeyDown` in `OnlineMenu` update loop.
- Config pattern: BepInEx `Config.Bind` entries (`Session/NetConfig.cs`).
- Plugin structure: `Plugin.cs` `BaseUnityPlugin` + per-feature
  `Install(harmony)` statics — copy this modular layout.
- Target framework `net35` (they chose max compat); we can likely use
  `netstandard2.0`/`net48` — verify against BepInEx 5.4 + EtG's Unity
  version in P0.

**Names/roster caveat:** player display names live in their
`Session/Lobby` roster (per-machine `PlayerName` config), not on
`PlayerController`. v1 labels players by character name + P1/P2 slot;
names can come later via optional reflection into `GungeonOnline`
assembly when present (graceful fallback to character names).

**Testing:** they ship a `Dev/` harness (`GO_SAVE_DIR` env) for offline
sim — worth checking if it can spawn fake remote players for dev.
Otherwise couch co-op locally exercises the same `AllPlayers` path.

**Docs goldmine:** `docs/COOP-INTERACTIONS.md` — decompiled-game
knowledge of every per-screen/per-person assumption; read before any
Harmony work.

---

## Recommended order (current)

1. **README rework only** (R1–R3) — the funnel for the Reddit post.
   Art capture can happen alongside.
2. Reddit post draft once README lands.
3. Workstream B stays parked until explicitly revived.

## Risks / honest notes

- The co-op mod is **1.0 beta, solo dev** — APIs will churn; our plugin
  should pin/test against tagged releases and degrade gracefully.
- "Made for consoles" → our app is couch/nearby-first; the online-co-op
  bridge is genuinely new territory and a differentiator vs the other
  EtG companion apps.
- README banners need either generated art or composited screenshots —
  budget a session for it; cheap version = styled screenshot grid with
  the menu backdrop as hero (we already have the assets).
