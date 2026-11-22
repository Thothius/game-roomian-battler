# Next Steps Masterplan — README relaunch + Online Co-op bridge

> Authored 2026-11-25 (CORE / Slot 2). Planning doc only — nothing here is
> committed to build yet. Two workstreams: **A) GitHub/README relaunch**
> (Reddit + sideload push) and **B) GungeonOnlineCoOpMod companion plugin**
> (PC overlay idea). Both feed the same goal: get GungeonMate in front of
> players discovering it.

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

- [ ] **Hero banner** (~1600×400 or 1200×300 WebP): key art — gungeon
      hallway + drifting gun/item sprites echoing the new menu backdrop.
      Could composite from existing `wp_*` wallpapers + sprite assets,
      or generate fresh.
- [ ] **Section dividers** (optional, ~1200×60): thin ornament strips
      between OVERVIEW / FEATURES / REFERENCE.
- [ ] **Feature card icons** (optional): 6 small glyphs matching feature
      bullets — or skip and use emoji/text only (Ponytail: prefer skip).
- [ ] **OG/social preview image**: GitHub repo social preview setting —
      reuse hero banner (1200×630 crop) so Reddit link unfurls nicely.
- [ ] **Screenshots** (6–8): capture list above; name `docs/media/*.webp`.
- [ ] Tools: image gen via existing asset pipeline or PIL composites;
      store sources in `tools/` or `design-lab/`.

### Work packages

- **R1**: capture/produce all art (banners + screenshots) — needs a debug
  build or design-lab renders.
- **R2**: rewrite `gungeon_mate/README.md` per structure above.
- **R3**: repo hygiene for discovery — topics/tags on GitHub repo
  (`enter-the-gungeon`, `gungeon`, `flutter`, `multiplayer`, `companion-app`),
  About section blurb, social preview image, maybe pin README topics.
- **R4**: Reddit post draft (separate doc when ready) — lead with the
  online-co-op angle if B lands first.

---

## B. GungeonOnlineCoOpMod companion — "party overlay" plugin

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

### Approach options

1. **Separate BepInEx plugin (recommended start)** — our own plugin DLL
   installed alongside theirs. Harmony-patches the game's player/inventory
   APIs (or reads the mod's replicated state on clients). Renders an
   in-game IMGUI/overlay panel toggled by a hotkey (e.g. F9). No upstream
   dependency beyond the game itself — works with or without their mod,
   but shines with it (remote players' inventories).
   - Pros: self-contained, MIT-compatible, we control release cadence.
   - Cons: needs EtG game-assembly reversing (Assembly-CSharp hooks);
     their mod already solves desync so we only need *read* access.
2. **Upstream contribution / coordination** — open an issue/PR to
   Hero88go adding an overlay or a state-export hook (e.g. JSON dump of
   party inventories to a local socket/file per tick). Pros: canonical
   data path, maintainer goodwill, cross-promotion. Cons: dependent on
   their roadmap; 1.0 beta means APIs will churn.
3. **Hybrid**: plugin writes a localhost feed (JSON over TCP/UDP or a
   file) → our existing Flutter Windows/Linux app (or a tiny overlay
   exe) renders it. Reuses GungeonMate's whole UI/theme stack.
   - Pros: richest UI (our actual app, themes, Ammonomicon lookups,
     synergy predictions!). Cons: two processes, packaging complexity.

### PC-tailored feature ideas (the fun part — data is free)

- **Party loadout board**: every member's guns/items/actives/passives,
  quality colors, cool/curse, health — one hotkey glance.
- **Cross-player synergy radar**: "you + Alex could complete *Bullet
  Time*" — we already have full synergy data + matching logic.
- **Boss/room callouts**: who's in combat, revive status, floor/seed info.
- **Shared scratchpad**: quick notes/pings per member (ties into our
  existing MP event-log patterns).
- **Draft assistant**: shop restock alerts, "Alex needs a blast shield".

### Phases (when approved)

- **P0 — research spike**: clone the mod, map where party inventory state
  lives (Replication/ inventory sync + Game/ player slots), confirm read
  path on host AND client. Output: short tech note + go/no-go.
- **P1 — minimal overlay**: BepInEx plugin, hotkey toggles a panel listing
  local + remote player inventories (names/characters/items). Proves the
  pipeline end-to-end.
- **P2 — polish**: quality-tier colors, collapsible sections, config for
  hotkey/position, compatibility check vs their 4-player dev builds.
- **P3 — GungeonMate integration (optional)**: localhost feed → Flutter
  desktop overlay reusing theme/flair stack; or upstream PR for a
  first-party hook.
- **P4 — distribution**: r2modman package + mention in our README/docs;
  cross-link from their repo if they engage.

### Open questions to resolve in P0

- Does client-side replicated inventory include *item quality*, gun
  details, and actives — or just names? (Affects overlay fidelity.)
- Hotkey conflicts: their mod uses F8/Back+Start; pick a free default.
- License: MIT both sides — fine; still credit upstream in our plugin.
- EtG EAC/anti-cheat: EtG has none (single-player game) — mods are
  normal; verify no online-service ToS issue (there is none; it's P2P).

---

## Recommended order

1. **README rework first** (R1–R3) — it's the funnel for the Reddit post;
   everything else benefits from it. Art capture can happen alongside.
2. **P0 research spike** for the co-op plugin — cheap, informs whether the
   overlay is a weekend plugin or a bigger build. Do BEFORE promising it
   publicly.
3. Reddit post draft once README + (optionally) plugin teaser exist.

## Risks / honest notes

- The co-op mod is **1.0 beta, solo dev** — APIs will churn; our plugin
  should pin/test against tagged releases and degrade gracefully.
- "Made for consoles" → our app is couch/nearby-first; the online-co-op
  bridge is genuinely new territory and a differentiator vs the other
  EtG companion apps.
- README banners need either generated art or composited screenshots —
  budget a session for it; cheap version = styled screenshot grid with
  the menu backdrop as hero (we already have the assets).
