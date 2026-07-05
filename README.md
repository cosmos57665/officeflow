# OfficeFlow

OfficeFlow is a Streamlit app for AI-powered office automation.
It turns meeting audio into formatted Word minutes.
It triages pasted emails into priority buckets with draft replies.
It generates personalized student PDFs from a CSV.
It answers questions from office PDFs with page citations.

## Run

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Set-Content .env "ANTHROPIC_API_KEY=sk-..."
streamlit run app.py
```

Use Demo Mode in the sidebar when the API key or internet connection is unavailable.
