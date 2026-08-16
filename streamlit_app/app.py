"""
AI Resume Intelligence Platform
Home Dashboard
"""

import streamlit as st

from services.api_client import APIClient
from services.api_client import APIError
from utils.theme import apply_theme, hero_banner, section_title, feature_card, app_footer


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="AI Resume Intelligence",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_theme()

client = APIClient()


# ============================================================
# Helper Functions
# ============================================================

def load_dashboard_data():

    try:

        resumes = client.get_all_resumes()
        jobs = client.get_all_jobs()

        return {
            "backend": True,
            "resume_count": len(resumes),
            "job_count": len(jobs)
        }

    except APIError:

        return {
            "backend": False,
            "resume_count": 0,
            "job_count": 0
        }


# ============================================================
# Header
# ============================================================

hero_banner(
    "🤖 AI Resume Intelligence Platform",
    "An AI-powered recruitment system using FastAPI, OpenAI, Qdrant and Streamlit."
)

st.write("")


# ============================================================
# Dashboard Metrics
# ============================================================

with st.spinner("Loading dashboard..."):

    dashboard = load_dashboard_data()


col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "📄 Total Resumes",
        dashboard["resume_count"]
    )

with col2:

    st.metric(
        "💼 Total Jobs",
        dashboard["job_count"]
    )

with col3:

    if dashboard["backend"]:

        st.success("🟢 Backend Online")

    else:

        st.error("🔴 Backend Offline")


st.divider()


# ============================================================
# Project Overview
# ============================================================

section_title("🚀", "Features")

col1, col2 = st.columns(2)

with col1:

    feature_card(
        "📄 Resume Management",
        ["Upload Resume", "Resume Parsing", "Resume Database"]
    )

    st.write("")

    feature_card(
        "💼 Job Management",
        ["Parse Job Description", "Store Jobs", "Job Database"]
    )

with col2:

    feature_card(
        "📊 AI Features",
        ["ATS Evaluation", "Semantic Search", "Recruit Ranking"]
    )

    st.write("")

    feature_card(
        "⚙ Technology Stack",
        ["FastAPI", "OpenAI", "Qdrant", "SQLAlchemy"]
    )


st.divider()


# ============================================================
# Navigation
# ============================================================

section_title("🧭", "Navigate")

col1, col2, col3 = st.columns(3)

with col1:

    st.page_link(
        "pages/1_Upload_Resume.py",
        label="📄 Upload Resume",
        use_container_width=True
    )

    st.page_link(
        "pages/2_Create_Job.py",
        label="💼 Create Job",
        use_container_width=True
    )

with col2:

    st.page_link(
        "pages/3_ATS_Analyzer.py",
        label="📊 ATS Analyzer",
        use_container_width=True
    )

    st.page_link(
        "pages/4_Semantic_Search.py",
        label="🔍 Semantic Search",
        use_container_width=True
    )

with col3:

    st.page_link(
        "pages/5_Recruit_Ranking.py",
        label="🏆 Recruit Ranking",
        use_container_width=True
    )


st.divider()


# ============================================================
# Footer
# ============================================================

app_footer("Built using FastAPI • OpenAI • Qdrant • Streamlit")