# Paradox Avatar Style Assessment

## Source set

9 webp portraits in `gungeon_mate/assets/images/avatars/` (seeded from
`C:\Users\saare\Desktop\Avatars`): the_bullet, the_convict, the_cultist,
the_gunslinger, the_hunter, the_marine, the_paradox, the_pilot, the_robot.

## Style DNA

Enter the Gungeon-style pixel-art **portrait busts**:

- Head-and-shoulders framing, slight angle, "versus-screen character card" feel
- Chunky visible pixels (~64–96px effective resolution)
- Dramatic single-hue neon rim lighting against near-black moody backgrounds
- One saturated accent color per character (violet for Paradox, orange/rust for Marine)
- Hard shadow contrast, subtle bloom on lit edges
- NOT clean icon art — painterly pixel portraits with atmosphere

## Generation prompts (3x3 grids)

### Base grid
```
A 3x3 grid of pixel-art character portrait busts in the style of Enter the
Gungeon key art. Each cell shows a different original character:
head-and-shoulders framing, chunky visible pixels, dramatic single-color
neon rim lighting, near-black moody background, saturated accent glow,
retro 16-bit aesthetic, no text, no borders between cells.
```

### Male gungeoneer variants
```
A 3x3 grid of pixel-art male character portrait busts, Enter the Gungeon
style. Varied archetypes: a grizzled gunslinger with a hat, a cybernetic
robot soldier, a cloaked cultist, a space marine, a masked bullet-kin
hunter, a royal knight, a mechanic, a rat-person rogue, a mysterious
paradox entity. Chunky pixels, neon rim light, dark background, one
saturated accent color per character.
```

### Female gungeoneer variants
```
A 3x3 grid of pixel-art female character portrait busts, Enter the Gungeon
style. Varied archetypes: a huntress with a bow, a witch with glowing
runes, an armored paladin, a rogue with twin revolvers, an android girl,
a plague doctor, a bullet-witch, a pilot with goggles, a spectral
assassin. Chunky pixels, neon rim light, dark moody background, distinct
saturated accent per character.
```

## Wire format

`kAvatarIds` + `avatarPath()` in `lib/utils/asset_paths.dart`. Avatars are
exchanged by string id in the MP hello (`MpHello.avatarId`); unknown ids
fall back to the gungeoneer map icon. Registry is append-only.
