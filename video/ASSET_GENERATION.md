# Character asset generation

Mode: built-in image generation followed by local chroma-key removal.

Final project asset: `public/characters/student-sheet-v2.png`

## Prompt

```text
Use case: stylized-concept
Asset type: consistent pixel-art character sprite sheet for a premium 16:9 AI product-launch film
Primary request: create one original student developer character shown in eight clearly separated full-body poses arranged as a clean 4-column by 2-row sprite sheet
Scene/backdrop: perfectly flat solid #FF00FF chroma-key background for local background removal; one uniform color with no shadows, gradients, texture, floor plane, reflections, or lighting variation
Subject: youthful student developer with warm-brown skin, short dark hair, teal hoodie, charcoal trousers, simple dark sneakers, and a slim dark laptop; not based on any real person
Pose cells in reading order: neutral standing, seated typing, thinking, walking, presenting, celebrating, friendly wink, and focused standing with an open laptop
Style/medium: crisp contemporary 32-bit pixel art, premium indie-game character design, clean readable silhouette, consistent identity and proportions
Constraints: exactly one character identity repeated across eight poses; no extra people; no text; no logos; no watermark; no shadows; do not use #FF00FF in the character
```

The key was removed with the installed imagegen helper using border auto-keying, a soft matte, despill, a 20-point transparent threshold, and one-pixel edge contraction. Validation confirmed RGBA output and transparent corners.
