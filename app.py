"""OfficeFlow — Streamlit entry point: branding, navigation, module routing."""
import streamlit as st

from lib import cloud_config
from modules import ask, docs, inbox, minutes

st.set_page_config(page_title="OfficeFlow", layout="wide")

ACCENT = "#0F766E"

MODULES = {
    "Minutes": minutes,
    "Inbox": inbox,
    "Docs": docs,
    "Ask": ask,
}


def _apply_theme():
    st.markdown(
        f"""
        <style>
        :root {{
            --of-accent: {ACCENT}; --of-ink: #111827; --of-muted: #64748b;
            --of-panel: #ffffff; --of-line: #d9e2ea; --of-bg: #f4f7fa;
        }}
        header[data-testid="stHeader"] {{ background: transparent; height: 0; }}
        [data-testid="stToolbar"], [data-testid="stDecoration"], .stDeployButton {{ display: none !important; }}
        .stApp {{ background: radial-gradient(circle at 82% 0%, #e8f3f1 0, #f4f7fa 32rem); color: var(--of-ink); }}
        .main .block-container {{ max-width: 1180px; padding-top: 3rem; padding-bottom: 3rem; }}
        h1, h2, h3 {{ color: var(--of-ink); letter-spacing: 0; }}
        h1 {{ font-size: 2.25rem; line-height: 1.05; margin-bottom: 0.35rem; }}
        h2 {{ font-size: 1.35rem; }} h3 {{ font-size: 1.05rem; }}
        hr {{ border-color: var(--of-line); margin: 2rem 0 1rem; }}
        [data-testid="stSidebar"] {{ background: #111827; border-right: 1px solid #233044; }}
        [data-testid="stSidebar"] * {{ color: #e5edf5; }}
        [data-testid="stSidebar"] .stCaption, [data-testid="stSidebar"] small {{ color: #9fb0c2 !important; }}
        [data-testid="stSidebar"] [role="radiogroup"] label {{
            border: 1px solid transparent; border-radius: 8px; padding: 0.2rem 0.35rem;
        }}
        [data-testid="stSidebar"] [role="radiogroup"] label:hover {{ background: #182235; border-color: #334155; }}
        [data-testid="stSidebar"] [data-testid="stExpander"] {{ border-color: #334155; background: #151f31; border-radius: 8px; }}
        .of-demo-note {{
            margin: 0.65rem 0 1rem; padding: 0.75rem 0.85rem; border: 1px solid #134e4a;
            border-radius: 8px; background: #0f2f34; color: #b9f3e6; font-size: 0.88rem;
        }}
        .of-topline {{ color: var(--of-accent); font-size: 0.78rem; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; }}
        .of-shell {{
            background: rgba(255,255,255,0.86); border: 1px solid var(--of-line); border-radius: 8px;
            padding: 1.2rem; box-shadow: 0 18px 45px rgba(15, 23, 42, 0.07);
        }}
        .of-hero {{ padding: 1.2rem 0 1rem; max-width: 960px; }}
        .of-title {{ font-size: clamp(2.8rem, 6vw, 5.7rem); font-weight: 850; line-height: 0.94; letter-spacing: -0.02em; }}
        .of-tagline {{ color: var(--of-muted); font-size: 1.08rem; margin-top: 0.9rem; max-width: 720px; }}
        .of-status-row {{ display: flex; flex-wrap: wrap; gap: 0.7rem; margin: 1.15rem 0; }}
        .of-badge {{
            display: inline-flex; align-items: center; gap: 0.45rem; border-radius: 999px;
            padding: 0.4rem 0.7rem; background: #e7f6f2; color: #075e57; font-weight: 750; font-size: 0.86rem;
        }}
        .of-card-grid {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0.85rem; margin-top: 1rem; }}
        .of-card {{
            background: var(--of-panel); border: 1px solid var(--of-line); border-radius: 8px;
            padding: 1rem; min-height: 154px; box-shadow: 0 10px 25px rgba(15, 23, 42, 0.05);
        }}
        .of-card small {{ color: var(--of-accent); font-weight: 800; letter-spacing: 0.06em; text-transform: uppercase; }}
        .of-card h3 {{ margin: 0.35rem 0 0.55rem; }}
        .of-card p {{ margin: 0; color: var(--of-muted); font-size: 0.94rem; line-height: 1.4; }}
        .of-card strong {{ display: block; color: var(--of-ink); margin-top: 0.9rem; }}
        .of-module-head {{
            border: 1px solid var(--of-line); border-left: 6px solid var(--of-accent); border-radius: 8px;
            background: rgba(255,255,255,0.9); padding: 1rem 1.1rem; margin-bottom: 1rem;
        }}
        .of-module-head p {{ color: var(--of-muted); margin: 0.35rem 0 0; }}
        .of-section-label {{ color: var(--of-muted); font-weight: 800; font-size: 0.78rem; letter-spacing: 0.07em; text-transform: uppercase; }}
        [data-testid="stVerticalBlockBorderWrapper"] {{ border-color: var(--of-line); border-radius: 8px; background: rgba(255,255,255,0.74); }}
        div.stButton > button {{ border-radius: 8px; border-color: #bfd0dc; font-weight: 750; }}
        div.stButton > button[kind="primary"] {{ background: var(--of-accent); border-color: var(--of-accent); color: white; }}
        [data-testid="stFileUploader"], [data-testid="stTextArea"], [data-testid="stSelectbox"] {{
            background: rgba(255,255,255,0.62); border-radius: 8px;
        }}
        .stAlert {{ border-radius: 8px; }}
        @media (max-width: 900px) {{ .of-card-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}
        @media (max-width: 560px) {{ .of-card-grid {{ grid-template-columns: 1fr; }} .main .block-container {{ padding-top: 1.5rem; }} }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def _home():
    st.markdown(
        """
        <section class="of-hero">
            <div class="of-topline">Live demo operations console</div>
            <div class="of-title">OfficeFlow</div>
            <p class="of-tagline">
                Four practical office automations in one reliable Streamlit workspace,
                built for a smooth school AI project demo.
            </p>
        </section>
        <div class="of-status-row">
            <span class="of-badge">Demo Mode fallback ready</span>
            <span class="of-badge">Sample files included</span>
            <span class="of-badge">Outputs timed for presentation</span>
        </div>
        <div class="of-card-grid">
            <article class="of-card">
                <small>Audio to Word</small>
                <h3>Meeting Minutes</h3>
                <p>Turns meeting audio into structured Word minutes.</p>
                <strong>Saves about 30 minutes per meeting</strong>
            </article>
            <article class="of-card">
                <small>Email triage</small>
                <h3>Inbox Triage</h3>
                <p>Sorts pasted emails and drafts professional replies.</p>
                <strong>Saves about 20 minutes per inbox batch</strong>
            </article>
            <article class="of-card">
                <small>CSV to PDFs</small>
                <h3>Bulk Documents</h3>
                <p>Generates personalized student PDFs from a CSV.</p>
                <strong>Saves about 5 minutes per document</strong>
            </article>
            <article class="of-card">
                <small>Policy Q&A</small>
                <h3>Ask PDF</h3>
                <p>Answers questions from an uploaded PDF with page citations.</p>
                <strong>Saves about 15 minutes per policy lookup</strong>
            </article>
        </div>
        """,
        unsafe_allow_html=True,
    )


_apply_theme()

with st.sidebar:
    st.title("OfficeFlow")
    st.caption("AI Office Automation Suite")
    choice = st.radio("Navigation", ["Home", *MODULES.keys()])
    st.toggle("Demo Mode", key="demo_mode", value=cloud_config.default_demo_mode())
    if st.session_state.get("demo_mode"):
        st.caption("Demo mode — showing cached results. Live AI runs in the presentation.")
    st.markdown(
        "<div class='of-demo-note'>Demo Mode is the safety switch: cached outputs keep the presentation moving without API or Wi-Fi.</div>",
        unsafe_allow_html=True,
    )
    with st.expander("About"):
        st.markdown(
            "- Python: app runtime and automation glue\n"
            "- Streamlit: web interface and navigation\n"
            "- Whisper: local audio transcription\n"
            "- Claude API: summaries, triage, remarks, and answers\n"
            "- python-docx: Word meeting-minutes output\n"
            "- fpdf2: PDF document generation\n"
            "- PyMuPDF: PDF reading and previews"
        )

if choice == "Home":
    _home()
else:
    MODULES[choice].render()

st.divider()
st.caption("Built with Python · Streamlit · Whisper · Claude API")
