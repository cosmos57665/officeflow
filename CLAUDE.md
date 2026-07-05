# OfficeFlow — Project Context

## What this is
AI-powered office automation suite. Streamlit web app with 4 modules.
Built by a solo student developer for a school AI project with a LIVE DEMO on Aug 8.
Reliability > features. A crash during the live demo is the worst possible outcome.

## Stack (fixed — do not substitute)
- UI: Streamlit (single app.py entry, sidebar navigation between modules)
- LLM: Anthropic API, model "claude-sonnet-4-6", key from .env via python-dotenv
- Transcription: faster-whisper, model size "small", CPU
- Word output: python-docx
- PDF output: fpdf2
- PDF reading: PyMuPDF (fitz)
- Data: pandas

## Architecture
officeflow/
├── app.py                  # Streamlit entry — sidebar nav, branding, module routing
├── modules/
│   ├── minutes.py          # Module 1: audio → minutes
│   ├── inbox.py            # Module 2: email triage
│   ├── docs.py             # Module 3: bulk document generator
│   └── ask.py              # Module 4: PDF Q&A
├── lib/
│   ├── llm.py              # single shared Claude client + call wrapper
│   ├── transcribe.py       # faster-whisper wrapper
│   └── docgen.py           # docx + pdf generation helpers
├── samples/                # sample audio, emails.txt, students.csv, policy.pdf
├── cache/                  # pre-generated outputs for demo mode
└── outputs/                # generated files land here

## Non-negotiable rules
1. Every API call wrapped in try/except. On failure: friendly st.error, never a stack trace.
2. Every long operation shows st.spinner with a status message.
3. All Claude calls go through lib/llm.py — one function `ask_claude(system, user, max_tokens)`.
   Never instantiate the client inside modules.
4. DEMO MODE: global toggle in the sidebar. When ON, modules return pre-generated
   outputs from cache/ instead of calling the API. This is the wifi-failure fallback.
5. When Claude must return structured data, prompt for JSON only, parse with
   json.loads inside try/except, and strip markdown fences first.
6. Keep every file under ~200 lines. Split if larger.
7. No feature I did not ask for. No extra modules, no auth, no database.
8. GIT DISCIPLINE: after each module (or prompt) passes its end-to-end test,
   commit with a descriptive message ("feat: minutes module — audio to docx
   pipeline") and push to origin main. Never commit .env or cache/ contents
   with API outputs containing the key. If push fails (auth), tell me and
   continue — do not block on it.

## Definition of done (per module)
- Works end-to-end with the sample file in samples/
- Works in demo mode with cached output
- Handles: empty input, wrong file type, API failure — each with a clear message
- Timed: show elapsed seconds after completion (this is a presentation metric)