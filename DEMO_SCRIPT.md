# OfficeFlow 8-Minute Live Demo Script

## Before the Demo

- Open a terminal in `D:\Sachin\SACHIN PROJECTS\officeflow`.
- Run `.\venv\Scripts\streamlit.exe run app.py`.
- Open the Local URL, usually `http://localhost:8501`.
- Keep `samples/` visible in File Explorer.
- In the sidebar, turn **Demo Mode** ON if Wi-Fi is weak, the API key fails, or you want the safest run.

## 0:00-0:45 — Opening

1. Show the Home page.
2. Say: "OfficeFlow is an AI office automation suite with four practical workflows: meeting minutes, inbox triage, bulk documents, and PDF Q&A."
3. Point to the sidebar **Demo Mode** toggle.
4. Say: "This switch is my reliability fallback. If Wi-Fi or the API fails, cached outputs keep the demo moving without a crash."

Fallback: If the app is not open, run `streamlit run app.py` again and start from the Home page. If the browser is slow, refresh once.

## 0:45-2:20 — Module 1: Meeting Minutes

1. In the sidebar, click **Minutes**.
2. Click **Use sample audio**.
3. Use `samples/meeting_sample.wav` if asked for the sample file.
4. While the spinner runs, say: "This module takes meeting audio, transcribes it with Whisper, asks Gemini for structured minutes, and creates a Word document."
5. When results appear, show the title, summary bullets, decisions, action items, elapsed seconds, and **Download Word document** button.
6. Say: "The manual version is listening to the whole recording, writing minutes, and formatting the document. Here it is one click."

Fallback: If transcription or Gemini fails, turn **Demo Mode** ON in the sidebar, stay on **Minutes**, click **Use sample audio** again, and say: "I am switching to cached demo output, which is the planned Wi-Fi failure fallback."

## 2:20-3:45 — Module 2: Inbox Triage

1. In the sidebar, click **Inbox**.
2. Click **Load sample emails**.
3. Click **Triage Inbox**.
4. While the spinner runs, say: "The prompt asks for JSON only, so the app can safely turn messy emails into three priority buckets and draft replies."
5. Show the **Urgent**, **Action Needed**, and **FYI** columns.
6. Open one **Suggested reply** expander.
7. Say: "The value here is deciding what needs attention today and drafting a professional response."

Fallback: If the API fails or results do not appear, turn **Demo Mode** ON, click **Triage Inbox** again, and continue from the cached triage.

## 3:45-5:15 — Module 3: Bulk Document Generator

1. In the sidebar, click **Docs**.
2. If **Demo Mode** is ON, confirm the app shows `Demo Mode: using samples/students.csv`.
3. If **Demo Mode** is OFF, upload `samples/students.csv`.
4. Keep **Document type** set to **Merit Certificate**.
5. Click **Generate All**.
6. While the spinner runs, say: "This batches the AI call for remarks, then generates one PDF per student and packages everything into a zip."
7. Show the document count, elapsed seconds, **Download all PDFs (zip)**, and the sample previews.
8. Say: "This is useful for certificates, progress reports, notices, or any repeated office document."

Fallback: If upload or API fails, turn **Demo Mode** ON, confirm the sample CSV is loaded automatically, and click **Generate All** again.

## 5:15-6:45 — Module 4: Ask PDF

1. In the sidebar, click **Ask**.
2. If **Demo Mode** is OFF, upload `samples/policy.pdf`.
3. In the question box, type: `What is the deadline for reimbursement claims?`
4. Press Enter.
5. While the spinner runs, say: "The app extracts text from the PDF, sends only the document context and question, and asks for page citations."
6. Show the answer with `(p. 4)` citations and the elapsed seconds.
7. Say: "This saves time when someone needs a precise answer from a policy document."

Fallback: Turn **Demo Mode** ON and ask one of these exact cached questions:

- `How many annual leave days do full-time employees receive?`
- `What is the deadline for reimbursement claims?`
- `Are meal reimbursements capped during approved travel?`

## 6:45-7:35 — Reliability Close

1. Return to the Home page.
2. Say: "The important reliability choices are shared API handling, try/except around failures, spinners for long work, elapsed time after completion, and Demo Mode for no-network fallback."
3. Say: "Each module has a clear manual-time comparison: minutes about 30 minutes, inbox about 20 minutes, documents about 5 minutes per file, and PDF lookup about 15 minutes."

Fallback: If any module still fails, stay calm, leave **Demo Mode** ON, and summarize the cached result already shown. Do not debug live.

## 7:35-8:00 — Final Line

Say: "OfficeFlow is not trying to replace office staff. It removes repetitive formatting, sorting, and searching so people can spend more time on decisions and communication."

Final fallback: If the app stops responding, show the generated files in `outputs/` and say: "These are the generated artifacts from the same workflows."
