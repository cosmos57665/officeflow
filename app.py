"""OfficeFlow — Streamlit entry point: branding, navigation, module routing."""
import streamlit as st

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
        :root {{ --officeflow-accent: {ACCENT}; }}
        .stApp {{ background: #f7f8fa; color: #172026; }}
        h1, h2, h3 {{ color: #172026; letter-spacing: 0; }}
        h1 {{ border-left: 5px solid var(--officeflow-accent); padding-left: 0.7rem; }}
        h2, h3 {{ border-left: 4px solid var(--officeflow-accent); padding-left: 0.55rem; }}
        [data-testid="stSidebar"] {{ border-right: 1px solid #dde3e8; }}
        [data-testid="stSidebar"] h1 {{ border-left: 0; padding-left: 0; }}
        hr {{ border-color: #d5dde3; }}
        .of-hero {{ padding: 1.25rem 0 0.75rem; max-width: 980px; }}
        .of-title {{ font-size: clamp(2.4rem, 5vw, 4.6rem); font-weight: 760; line-height: 1; }}
        .of-tagline {{ color: #52616b; font-size: 1.12rem; margin-top: 0.9rem; max-width: 680px; }}
        .of-card-grid {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0.85rem; }}
        .of-card {{
            background: #ffffff; border: 1px solid #dce4e8; border-left: 5px solid var(--officeflow-accent);
            border-radius: 8px; padding: 1rem; min-height: 148px;
        }}
        .of-card h3 {{ border: 0; padding: 0; margin: 0 0 0.55rem; font-size: 1.02rem; }}
        .of-card p {{ margin: 0; color: #52616b; font-size: 0.94rem; line-height: 1.35; }}
        .of-card strong {{ display: block; color: var(--officeflow-accent); margin-top: 0.9rem; }}
        div.stButton > button[kind="primary"] {{ background: var(--officeflow-accent); border-color: var(--officeflow-accent); }}
        @media (max-width: 900px) {{ .of-card-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}
        @media (max-width: 560px) {{ .of-card-grid {{ grid-template-columns: 1fr; }} }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def _home():
    st.markdown(
        """
        <section class="of-hero">
            <div class="of-title">OfficeFlow</div>
            <p class="of-tagline">
                A reliable AI office automation suite for meeting notes, inbox triage,
                document generation, and policy Q&A.
            </p>
        </section>
        <div class="of-card-grid">
            <article class="of-card">
                <h3>Meeting Minutes</h3>
                <p>Turns meeting audio into structured Word minutes.</p>
                <strong>Saves about 30 minutes per meeting</strong>
            </article>
            <article class="of-card">
                <h3>Inbox Triage</h3>
                <p>Sorts pasted emails and drafts professional replies.</p>
                <strong>Saves about 20 minutes per inbox batch</strong>
            </article>
            <article class="of-card">
                <h3>Bulk Documents</h3>
                <p>Generates personalized student PDFs from a CSV.</p>
                <strong>Saves about 5 minutes per document</strong>
            </article>
            <article class="of-card">
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
    st.toggle("Demo Mode", key="demo_mode")
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
