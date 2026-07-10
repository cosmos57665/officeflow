# OfficeFlow 90-Second Full-Stack Launch Film

## Goal

Create a 1920x1080, 30 FPS, 90-second Remotion film named `OfficeFlowLaunch` for a school presentation and YouTube. Codex narrates as Sachin's warm, youthful AI collaborator. An original pixel-art student represents Sachin, while Codex appears as a glowing cursor-orb.

The film presents the current OfficeFlow architecture: React, Vite, and Tailwind on the frontend; FastAPI and isolated workflow services on the backend; Gemini as the primary runtime AI provider; Groq and OpenRouter as fallbacks; and local Whisper, PyMuPDF, Word, and PDF tooling. Streamlit is legacy fallback context, not the featured interface.

## Storyboard and narration

| Time | Visual | Narration |
| --- | --- | --- |
| 0-7s | Pixel Sachin faces an empty workspace; an idea spark appears. | "I'm Codex. Sachin had an idea: what if repetitive office work could happen in seconds?" |
| 7-15s | The Codex orb arrives; prompts become an implementation plan. | "He brought the problem. I helped turn it into a plan, and then into a working product." |
| 15-27s | React/Vite/Tailwind, FastAPI, workflow services, and AI/document tools assemble. | "Together, we built OfficeFlow: a modern React interface backed by FastAPI, with four practical workflows behind a clean API." |
| 27-38s | Audio travels through FastAPI, Whisper, AI processing, and Word generation. | "Meeting audio becomes a transcript, structured minutes, action items, and a downloadable Word document." |
| 38-47s | Real inbox cards animate into Urgent, Action Needed, and FYI. | "Messy emails are sorted by priority, summarized, and paired with professional draft replies." |
| 47-56s | CSV data becomes personalized PDFs and a ZIP. | "A single CSV becomes personalized documents, generated in one batch and packaged together." |
| 56-65s | A PDF enters FastAPI; PyMuPDF extracts pages and returns a cited answer. | "A policy PDF becomes a conversation, returning precise answers with page citations." |
| 65-75s | Backend view shows shared error handling, Gemini primary, and provider fallbacks. | "Built with Codex and powered at runtime by Gemini, OfficeFlow also has guarded operations and provider fallbacks to keep it dependable." |
| 75-82s | Wi-Fi fails; Demo Mode activates and cached results continue. | "When the internet disappears, Demo Mode keeps the presentation moving." |
| 82-90s | Completed React dashboard reveal; Sachin celebrates and the Codex orb winks. | "One student. One AI collaborator. One working idea. Built by Sachin—with the help of ChatGPT's Codex." |

Selective phrases are `ONE IDEA`, `REACT + FASTAPI`, `FOUR WORKFLOWS`, `POWERED BY GEMINI`, and `RELIABILITY FIRST`. Full subtitles are excluded.

## Visual system

- Palette: navy `#08111F`, teal `#0F766E`, cyan `#62E6D1`, amber `#FFB454`, and off-white `#F7FAFC`.
- Typography: locally bundled Geist at 400, 600, and 800.
- Character: original pixel student with dark hair, warm-brown skin, teal hoodie, charcoal trousers, and laptop; no real-person likeness.
- Character poses: typing, thinking, walking, presenting, celebrating, and winking.
- Codex: deterministic React/SVG cursor-orb, particles, data trails, and architectural connectors.
- UI: genuine compiled React interface captures inside cinematic glass frames.
- Motion: frame-driven interpolation, Bezier easing, restrained springs, 12-18-frame match cuts, wipes, and fades. No CSS transitions or CSS keyframes.

## Assets and capture

Generate the character using built-in image generation on a flat `#FF00FF` chroma-key background. Remove the key locally and verify alpha, crisp edges, and pose consistency.

Serve `frontend/dist` locally and capture with Playwright. Intercept `/api/health`, `/api/minutes`, `/api/inbox`, `/api/docs`, `/api/ask/load`, `/api/ask/question`, and `/api/files/*` using deterministic fixtures derived from project samples and cache files. Do not depend on live AI or the missing React/FastAPI source.

## Audio

- Narration: Edge TTS `en-US-AndrewMultilingualNeural`, neutral international delivery, normal pitch, approximately `+2%` rate.
- Music: "Stylz" by Ahjay Stelino from Mixkit, source and license recorded in `video/CREDITS.md`.
- Music level: 12-16 dB below narration with 1.2-second fades.
- Effects: restrained whoosh, click, switch, page-turn, and completion sounds stored locally.
- Mix target: narration near -16 LUFS and final true peak no higher than -1.5 dBTP.

## Deliverables and acceptance

The Remotion source lives under `video/`; the final ignored render is `video/out/officeflow-launch-1080p.mp4`. The composition is exactly 2,700 frames and renders as H.264 CRF 18 with AAC audio.

Acceptance requires successful TypeScript checks, automated timing/structure tests, representative stills, a half-resolution draft, a complete final render, FFprobe confirmation of 1920x1080 at 30 FPS for approximately 90 seconds, and an end-to-end visual/audio review. All four workflows, React/FastAPI architecture, Gemini runtime role, provider fallbacks, Demo Mode, exact closing credit, and final wink must be present.
