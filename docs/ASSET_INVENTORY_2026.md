# Asset Inventory — 2026-11-25 (Slot 4 audit)

Snapshot of everything under `gungeon_mate/assets/` and its consumers.

## Totals

| Dir | Files | Size |
|-----|-------|------|
| `images/` | ~1,900 | 30 MB |
| `data/` (15 JSON) | 15 | 3.9 MB |
| `fonts/` | 33 TTF | 3.0 MB |
| `animations/` | 11 GIF | 46 KB |
| `shaders/` | 2 GLSL | 8 KB |

## Image categories

| Folder | Files | Size | Consumer |
|--------|-------|------|----------|
| `images/guns/` | 239 webp | 287 KB | gun icons everywhere (catalog/detail/browse/MP/sprite picker) |
| `images/items/` | 270 webp | 318 KB | item icons + synergy pieces + menu flock items |
| `images/synergies/` | 108 webp | 1.5 MB | synergy badge icons |
| `images/gungeoneers/` | 36 | 1.3 MB | character portraits + 8 animated card GIFs |
| `images/avatars/` | 99 webp | 2.1 MB | avatar picker grid + MP frames |
| `images/enemies/` | 146 png | 183 KB | enemy codex |
| `images/bosses/` | 26 png | 164 KB | boss icons |
| `images/npcs/` | 34 png | 50 KB | shopkeeper/NPC icons |
| `images/objects/` | 40 png | 1.2 MB | shrines/chests/environment |
| `images/pickups/` | 16 png | 20 KB | hearts/blanks/keys/shells |
| `images/shrines/` | 15 webp | 50 KB | shrine icons |
| `images/junkan/` | 8 webp | 19 KB | Junkan HP-bar digits |
| `images/ammonomicon/` | 9 | 937 KB | section headers + tab icons |
| `images/end_run/` | 1 | 1 KB | Lord of the Jammed dialog art |
| `images/home/` | 23 | 78 KB | logo + `junk/` 22 webp/png home junk pile |
| `images/themes/splash/` | 14 jpg | 1.6 MB | theme splash art (12 slugs missing → U-013) |
| `images/wallpapers/custom/` | 46 webp | **12 MB** | wallpaper picker (~270 KB each → U-014) |
| `images/wallpapers/animated/` | 1 mp4 | 2.4 MB | home galaxy vortex (`kHomeGalaxyAsset`) |
| `images/game/` | 614 png | 911 KB | **mostly dead** — only 13 gun sprites used (U-012) |

## Other dirs

- `assets/animations/` — 11 NPC idle GIFs, name-mapped in `asset_paths.dart`.
- `assets/shaders/` — `digital_rain.frag`, `dark_neon_fog.frag` (opt-in prefs).
- `assets/fonts/` — 4 custom TTFs + 29 `GoogleFonts.*` bundled families = font picker 1:1.
- `assets/data/` — guns, items, synergies, synergy_meta, shrines, gungeoneers,
  back_refs, objects, pickups, npcs, enemies, bosses, chapters, game_modes,
  changelog — all loaded at startup.

## Open findings

- **U-012** — `images/game/` ~97% unused (13 of 614 referenced).
- **U-013** — 12 theme splash slugs lack JPGs (see USER_BUG_LIST for list).
- **U-014** — wallpapers = 40% of image payload; re-encode deferred.
