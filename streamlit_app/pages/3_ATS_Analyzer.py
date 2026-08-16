"""
ATS Analyzer Page
"""

import streamlit as st

from services.api_client import APIClient
from services.api_client import APIError
from utils.theme import apply_theme, hero_banner, section_title, badge_row


# ============================================================
# Configuration
# ============================================================

st.set_page_config(
    page_title="ATS Analyzer",
    page_icon="📊",
    layout="wide"
)

apply_theme()

client = APIClient()


# ============================================================
# Load Data
# ============================================================


def load_data():

    resumes = client.get_all_resumes()

    jobs = client.get_all_jobs()

    return resumes, jobs


# ============================================================
# Display ATS Report
# ============================================================

def display_report(report: dict):

    st.success("ATS Analysis Completed Successfully")

    st.divider()

    score = report.get("score", 0)

    with st.container(border=True):

        col1, col2 = st.columns([1, 3])

        with col1:

            st.metric(
                "ATS Score",
                f"{score}%"
            )

        with col2:

            st.write("")
            st.progress(score / 100)

    st.divider()

    # ----------------------------------------------------

    section_title("✅", "Matched Skills")

    matched = report.get(
        "matched_skills",
        []
    )

    with st.container(border=True):

        if not badge_row(matched, kind="matched"):
            st.info("No matched skills.")

    # ----------------------------------------------------

    st.divider()

    section_title("❌", "Missing Skills")

    missing = report.get(
        "missing_skills",
        []
    )

    with st.container(border=True):

        if not badge_row(missing, kind="missing"):
            st.success("No missing skills.")

    # ----------------------------------------------------

    st.divider()

    section_title("💪", "Strengths")

    strengths = report.get(
        "strengths",
        []
    )

    if strengths:

        with st.container(border=True):

            for item in strengths:

                st.success(item)

    else:

        st.info("No strengths returned.")

    # ----------------------------------------------------

    st.divider()

    section_title("⚠", "Weaknesses")

    weaknesses = report.get(
        "weaknesses",
        []
    )

    if weaknesses:

        with st.container(border=True):

            for item in weaknesses:

                st.warning(item)

    else:

        st.success("No weaknesses.")

    # ----------------------------------------------------

    st.divider()

    section_title("🚀", "Suggestions")

    suggestions = report.get(
        "suggestions",
        []
    )

    if suggestions:

        with st.container(border=True):

            for item in suggestions:

                st.info(item)

    else:

        st.success("No suggestions.")


# ============================================================
# Main Page
# ============================================================

hero_banner(
    "📊 ATS Resume Analyzer",
    "Compare a stored resume against a stored job description."
)

st.write("")


try:

    resumes, jobs = load_data()

except APIError as e:

    st.error(e.message)

    st.stop()


if not resumes:

    st.warning("No resumes found.")

    st.stop()

if not jobs:

    st.warning("No jobs found.")

    st.stop()


resume_options = {

    f"{resume['id']} - {resume['name']}": resume["id"]

    for resume in resumes

}

job_options = {

    f"{job['id']} - {job['job_title']}": job["id"]

    for job in jobs

}


with st.container(border=True):

    col1, col2 = st.columns(2)

    with col1:

        selected_resume = st.selectbox(

            "Select Resume",

            options=list(resume_options.keys())

        )

    with col2:

        selected_job = st.selectbox(

            "Select Job",

            options=list(job_options.keys())

        )


st.write("")


if st.button(

    "🚀 Analyze Resume",

    use_container_width=True,

    type="primary"

):

    with st.spinner(

        "Running ATS Analysis..."

    ):

        try:

            report = client.analyze_resume(

                resume_options[selected_resume],

                job_options[selected_job]

            )

            display_report(report)

        except APIError as e:

            st.error(e.message)

        except Exception as e:

            st.error(str(e))