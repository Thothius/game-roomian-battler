# Codex View — Ultimate Gungeon Encyclopedia

## Overview
A new in-app Codex accessible from the player dashboard settings menu. Six categories covering the full Gungeon bestiary and lore, with rich data, visuals, and smooth UX.

## Categories & Wiki Sources

| # | Category | Wiki URL | Est. Entries |
|---|----------|----------|--------------|
| 1 | Pickups | https://enterthegungeon.wiki.gg/wiki/Pickups | ~15 (Blanks, Keys, Hearts, Armor, Shells, Ammo, etc.) |
| 2 | Objects | https://enterthegungeon.wiki.gg/wiki/Objects | ~30 (Chests, Tables, Crests, Altars, etc.) |
| 3 | NPCs | https://enterthegungeon.wiki.gg/wiki/NPCs | ~25 (Bello, Trorc, Flynt, Tinker, etc.) |
| 4 | Bosses | https://enterthegungeon.wiki.gg/wiki/Bosses | ~20 (Bullet King, Gatling Gull, Dragun, Lich, etc.) |
| 5 | Enemies | https://enterthegungeon.wiki.gg/wiki/Cult_of_the_Gundead | ~60 (Bullet Kin, Shotgun Kin, Bookllet, etc.) |
| 6 | Gungeoneers | https://enterthegungeon.wiki.gg/wiki/Gungeoneers | 9 (Marine, Pilot, Convict, Hunter, Bullet, Robot, Cultist, Paradox, Gunslinger) |

## Data Pipeline

### Phase 1: Scrape & Cache (Python)
New script: `scripts/scrape_codex.py`

For each category:
1. Fetch the wiki.gg category page (master list)
2. Parse the HTML table/list to extract all sub-entry names + wiki links
3. Fetch each sub-entry's wiki page → cache to `cache_wikigg/codex/<category>/<slug>.html`
4. Parse each cached page to extract:
   - **Name** — from page title
   - **Summary** — first paragraph(s) before infobox/TOC
   - **Infobox data** — type, health, location, drops, notes (varies per category)
   - **Image URL** — main infobox image or thumbnail
   - **Quote/Flavor text** — if present
   - **Notes/Trivia** — section content
   - **See also** — related entries

Output: `assets/data/codex/<category>.json` — one file per category, array of entry objects.

### Phase 2: Download Images
Extend `scripts/download_images.py` or new `scripts/download_codex_images.py`:
- Download each entry's image to `assets/images/codex/<category>/<slug>.png`
- Rewrite JSON `image` field to local asset path
- Fallback: placeholder icon for entries without images

### Data Schema (per entry)
```json
{
  "name": "Bullet Kin",
  "category": "enemies",
  "wiki_url": "https://enterthegungeon.wiki.gg/wiki/Bullet_Kin",
  "image": "assets/images/codex/enemies/bullet_kin.png",
  "summary": "The most common enemy in the Gungeon...",
  "infobox": {
    "type": "Bullet",
    "health": 10,
    "location": "All chambers",
    "drops": "Shells, occasionally ammo"
  },
  "quote": null,
  "notes": ["Bullet Kin can be jammed at higher curse levels..."],
  "trivia": ["Canonically do not have arms..."],
  "see_also": ["Shotgun Kin", "Veteran Bullet Kin", "Keybullet Kin"]
}
```

Schema is flexible — `infobox` fields vary per category. The model handles this as a `Map<String, dynamic>`.

## Flutter Architecture

### Models
- `lib/models/codex_entry.dart` — `CodexEntry` class with `fromJson`, `toJson`
  - Fields: name, category, wikiUrl, image, summary, infobox (Map), quote, notes (List), trivia (List), seeAlso (List)
  - `infobox` is `Map<String, String>` — displayed as key-value rows

### Data Loading
- `RunProvider` or a dedicated `CodexProvider` loads all 6 JSON files at startup
- Lightweight — each file is a simple `List<CodexEntry>`
- Lazy load: only load category JSON when its tab is first opened (keeps startup fast)

### Screens

#### `lib/screens/codex_hub_screen.dart`
- **Entry point**: Pushed from SettingsSheet "Codex" button
- **Layout**: TabBar with 6 tabs (Pickups, Objects, NPCs, Bosses, Enemies, Gungeoneers)
- **Each tab**: `CodexCategoryTab` widget
- **AppBar**: Themed with Gungeon dark neon aesthetic, back button
- **Tab icons**: Themed icons per category (pickups = inventory, objects = chest, NPCs = person, bosses = skull, enemies = groups, gungeoneers = hero)

#### `lib/screens/codex_category_tab.dart`
- **Default view**: SliverGrid of entry cards (2 columns on phone, 3 on tablet)
- **Each card**: Entry image + name + type badge
- **Tap card** → pushes `CodexEntryDetailScreen`
- **Search bar** at top: filters entries by name (instant filter)
- **Sort options**: alphabetical (default), by type/health/location
- **SliverGrid** for performance with large lists (Enemies has ~60 entries)

#### `lib/screens/codex_entry_detail_screen.dart`
- **Hero animation**: Image transitions from card to detail
- **Layout** (SliverList, scrollable):
  1. **Header**: Large image + name + category badge
  2. **Quote**: Italicized flavor text (if present)
  3. **Infobox section**: Key-value rows in a dark container (type, health, location, drops, etc.)
  4. **Summary**: Full text, GoopText-wrapped for theme consistency
  5. **Notes**: Bulleted list if present
  6. **Trivia**: Bulleted list if present
  7. **See Also**: Tappable chips that navigate to related entries
- **Themed**: Dark containers (`0xFF1E1E22`), neon accent borders per category color

### Category Colors (loot-tier inspired)
| Category | Accent Color |
|----------|-------------|
| Pickups | Cyan `0xFF00E5FF` |
| Objects | Amber `0xFFFFC107` |
| NPCs | Green `0xFF00E676` |
| Bosses | Pink `0xFFFF4081` |
| Enemies | Purple `0xFFB388FF` |
| Gungeoneers | White/Gold `0xFFFFD54F` |

### Widgets
- `lib/widgets/codex_entry_card.dart` — Grid card with image, name, type badge
- `lib/widgets/codex_infobox_row.dart` — Key-value row for infobox data
- `lib/widgets/codex_see_also_chip.dart` — Tappable chip for related entries

### Entry Point Integration
In `settings_sheet.dart`, add a new section between "Run Tools" and the danger tiles:
```dart
const _SectionLabel(label: 'Codex'),
_CodexTile(
  icon: Icons.library_books,
  label: 'Gungeon Codex',
  subtitle: 'Browse pickups, objects, NPCs, bosses, enemies & gungeoneers',
  onTap: () => Navigator.push(context,
    MaterialPageRoute(builder: (_) => const CodexHubScreen()),
  ),
),
```

## Implementation Order

1. **Data pipeline** — `scripts/scrape_codex.py` (scrape + cache + parse → JSON)
2. **Image download** — `scripts/download_codex_images.py`
3. **Model** — `lib/models/codex_entry.dart`
4. **Provider** — Load codex data (in RunProvider or dedicated CodexProvider)
5. **CodexHubScreen** — TabBar shell with 6 tabs
6. **CodexCategoryTab** — Grid + search + sort
7. **CodexEntryDetailScreen** — Full detail view with hero animation
8. **Entry point** — Wire into SettingsSheet
9. **Polish** — Animations, haptics, GoopText integration, theme consistency
10. **Bughunt** — flutter analyze, grep leaks, test all tabs

## UX Principles
- **Fast**: Lazy-load category data, SliverGrid for smooth scrolling
- **Searchable**: Instant filter in each category tab
- **Visual**: Every entry has an image; hero transitions between card → detail
- **Themed**: Category-specific accent colors, dark Gungeon containers
- **Interlinked**: See Also chips navigate between related entries
- **Offline**: All data and images cached locally — no network needed at runtime
- **GoopText**: Summary text wrapped in GoopText for dynamic theme consistency

## Asset Budget
- ~150 entries total across 6 categories
- ~150 images at ~5-20KB each (small wiki sprites) = ~1-3MB
- ~6 JSON files at ~5-50KB each = ~100-300KB
- Total: ~2-4MB added to APK — acceptable

## Risk Areas
- Wiki.gg rate limiting during scrape → add delays between requests (1-2s)
- Some entries may lack images → use placeholder asset
- Infobox schema varies wildly per category → flexible Map<String, String> model
- Enemies page is large (~60 entries) → SliverGrid + lazy load handles this
- Some wiki pages may not exist or redirect → skip with warning, don't crash
