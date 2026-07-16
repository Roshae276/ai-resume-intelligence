"""
Create Job Page
"""

import streamlit as st

from services.api_client import APIClient
from services.api_client import APIError


# ============================================================
# Configuration
# ============================================================

st.set_page_config(
    page_title="Create Job",
    page_icon="💼",
    layout="wide"
)

client = APIClient()


# ============================================================
# Display Parsed Job
# ============================================================

def display_job(job: dict):

    st.success("✅ Job Description Parsed Successfully!")

    st.divider()

    st.subheader("💼 Job Title")

    st.write(job.get("job_title", "N/A"))

    st.divider()

    # ----------------------------------------------------

    st.subheader("🛠 Required Skills")

    skills = job.get("skills", [])

    if skills:

        cols = st.columns(3)

        for index, skill in enumerate(skills):

            with cols[index % 3]:

                st.success(skill)

    else:

        st.info("No skills found.")

    # ----------------------------------------------------

    st.divider()

    st.subheader("💼 Experience")

    experience = job.get("experience", "")

    if experience:

        st.write(experience)

    else:

        st.info("Not specified.")

    # ----------------------------------------------------

    st.divider()

    st.subheader("🎓 Education")

    education = job.get("education", "")

    if education:

        st.write(education)

    else:

        st.info("Not specified.")

    # ----------------------------------------------------

    st.divider()

    st.subheader("📋 Responsibilities")

    responsibilities = job.get(
        "responsibilities",
        []
    )

    if responsibilities:

        for responsibility in responsibilities:

            st.write("•", responsibility)

    else:

        st.info("No responsibilities found.")


# ============================================================
# UI
# ============================================================

st.title("💼 Create Job")

st.write(
    "Paste a Job Description. "
    "The backend will parse it using OpenAI."
)

st.divider()

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