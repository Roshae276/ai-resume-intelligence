"""
Create Job Page
"""

import streamlit as st

from services.api_client import APIClient
from services.api_client import APIError
from utils.theme import apply_theme, hero_banner, section_title, badge_row


# ============================================================
# Configuration
# ============================================================

st.set_page_config(
    page_title="Create Job",
    page_icon="💼",
    layout="wide"
)

apply_theme()

client = APIClient()


# ============================================================
# Display Parsed Job
# ============================================================

def display_job(job: dict):

    st.success("✅ Job Description Parsed Successfully!")

    st.divider()

    section_title("💼", "Job Title")

    st.markdown(f"### {job.get('job_title', 'N/A')}")

    st.divider()

    # ----------------------------------------------------

    section_title("🛠", "Required Skills")

    skills = job.get("skills", [])

    with st.container(border=True):

        if not badge_row(skills, kind="neutral"):
            st.info("No skills found.")

    # ----------------------------------------------------

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        section_title("💼", "Experience")

        experience = job.get("experience", "")

        with st.container(border=True):

            if experience:
                st.write(experience)
            else:
                st.info("Not specified.")

    with col2:

        section_title("🎓", "Education")

        education = job.get("education", "")

        with st.container(border=True):

            if education:
                st.write(education)
            else:
                st.info("Not specified.")

    # ----------------------------------------------------

    st.divider()

    section_title("📋", "Responsibilities")

    responsibilities = job.get(
        "responsibilities",
        []
    )

    if responsibilities:

        with st.container(border=True):

            for responsibility in responsibilities:

                st.write("•", responsibility)

    else:

        st.info("No responsibilities found.")


# ============================================================
# UI
# ============================================================

hero_banner(
    "💼 Create Job",
    "Paste a Job Description. The backend will parse it using OpenAI."
)

st.write("")

job_description = st.text_area(
    "Paste Job Description",
    height=300,
    placeholder="Paste complete Job Description here..."
)

if st.button(
    "🚀 Parse Job Description",
    type="primary",
    use_container_width=True
):

    if not job_description.strip():

        st.warning("Please enter a Job Description.")

    else:

        with st.spinner(
            "Parsing Job Description..."
        ):

            try:

                response = client.create_job(
                    job_description
                )

                display_job(
                    response["job"]
                )

            except APIError as e:

                st.error(e.message)

            except Exception as e:

                st.error(str(e))