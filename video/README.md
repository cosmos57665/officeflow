# OfficeFlow launch film

Remotion source for the 90-second `OfficeFlowLaunch` presentation film.

## Setup

```powershell
npm install
npm run capture
npm run audio
```

`npm run capture` serves the compiled React application from `../frontend/dist` and intercepts its FastAPI requests with deterministic sample fixtures. `npm run audio` regenerates the Edge TTS narration and downloads the licensed music and sound effects listed in [CREDITS.md](CREDITS.md).

## Preview and verify

```powershell
npm run dev
npm run lint
npm test
npm run build
```

## Render

Use a D:-backed temporary directory on machines with limited system-drive space:

```powershell
$tmp = (Resolve-Path '.tmp').Path
$env:TEMP = $tmp
$env:TMP = $tmp
npx remotion render OfficeFlowLaunch out/officeflow-launch-1080p-raw.mp4 --codec=h264 --crf=18 --concurrency=4
```

The delivered, normalized master is `out/officeflow-launch-1080p.mp4`. Files under `out/`, `.tmp/`, and `build/` are generated and intentionally ignored.
