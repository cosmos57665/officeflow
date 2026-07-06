# OfficeFlow

OfficeFlow is an AI-powered office automation suite with a FastAPI backend,
a React frontend, and a Streamlit fallback.

It turns meeting audio into formatted Word minutes, triages pasted emails,
generates personalized student PDFs from a CSV, and answers questions from
office PDFs with page citations.

## Run the full-stack app

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd frontend
npm install
cd ..
.\start-officeflow.ps1
```

Open `http://localhost:5173` if the browser does not open automatically.
Demo Mode defaults ON so cached outputs work without API keys or Wi-Fi.

Optional live AI keys in `.env`:

```text
GEMINI_API_KEY=your_google_ai_studio_key
GROQ_API_KEY=your_groq_key
OPENROUTER_API_KEY=your_openrouter_key
DEFAULT_DEMO_MODE=true
```

The AI fallback order is Gemini, then Groq, then OpenRouter.

## Streamlit fallback

```powershell
streamlit run app.py
```

Use Demo Mode in either app when the API key or internet connection is unavailable.
