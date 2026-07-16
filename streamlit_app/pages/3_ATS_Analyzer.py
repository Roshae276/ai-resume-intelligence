"""
ATS Analyzer Page
"""

import streamlit as st

from services.api_client import APIClient
from services.api_client import APIError


# ============================================================
# Configuration
# ============================================================

st.set_page_config(
    page_title="ATS Analyzer",
    page_icon="📊",
    layout="wide"
)

client = APIClient()


# ============================================================
# Load Data
# ============================================================

@st.cache_data
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

    col1, col2 = st.columns([1, 3])

    with col1:

        st.metric(
            "ATS Score",
            f"{score}%"
        )

    with col2:

        st.progress(score / 100)

    st.divider()

    # ----------------------------------------------------

    st.subheader("✅ Matched Skills")

    matched = report.get(
        "matched_skills",
        []
    )

    if matched:

        cols = st.columns(3)

        for i, skill in enumerate(matched):

            with cols[i % 3]:

                st.success(skill)

    else:

        st.info("No matched skills.")

    # ----------------------------------------------------

    st.divider()

    st.subheader("❌ Missing Skills")

    missing = report.get(
        "missing_skills",
        []
    )

    if missing:

        cols = st.columns(3)

        for i, skill in enumerate(missing):

            with cols[i % 3]:

                st.error(skill)

    else:

        st.success("No missing skills.")

    # ----------------------------------------------------

    st.divider()

    st.subheader("💪 Strengths")

    strengths = report.get(
        "strengths",
        []
    )

    if strengths:

        for item in strengths:

            st.success(item)

    else:

        st.info("No strengths returned.")

    # ----------------------------------------------------

    st.divider()

    st.subheader("⚠ Weaknesses")

    weaknesses = report.get(
        "weaknesses",
        []
    )

    if weaknesses:

        for item in weaknesses:

            st.warning(item)

    else:

        st.success("No weaknesses.")

    # ----------------------------------------------------

    st.divider()

    st.subheader("🚀 Suggestions")

    suggestions = report.get(
        "suggestions",
        []
    )

    if suggestions:

        for item in suggestions:

            st.info(item)

    else:

        st.success("No suggestions.")


# ============================================================
# Main Page
# ============================================================

st.title("📊 ATS Resume Analyzer")

st.write(
    "Compare a stored resume against a stored job description."
)

st.divider()


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


st.divider()


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