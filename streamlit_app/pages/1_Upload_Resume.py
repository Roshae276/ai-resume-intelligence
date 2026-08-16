"""
Upload Resume Page
"""

import streamlit as st

from services.api_client import APIClient
from services.api_client import APIError
from utils.theme import apply_theme, hero_banner, section_title, badge_row


# ============================================================
# Configuration
# ============================================================

st.set_page_config(
    page_title="Upload Resume",
    page_icon="📄",
    layout="wide"
)

apply_theme()

client = APIClient()


# ============================================================
# Helper
# ============================================================

def display_resume(resume: dict):

    st.success("✅ Resume parsed successfully!")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        section_title("👤", "Candidate")

        with st.container(border=True):

            st.write("**Name:**", resume.get("name", "N/A"))
            st.write("**Email:**", resume.get("email", "N/A"))
            st.write("**Phone:**", resume.get("phone", "N/A"))

    with col2:

        section_title("🎯", "Skills")

        skills = resume.get("skills", [])

        with st.container(border=True):

            if not badge_row(skills, kind="neutral"):
                st.info("No skills found.")

    st.divider()

    # ----------------------------------------------------

    section_title("🎓", "Education")

    education = resume.get("education", [])

    if education:
        for edu in education:

            with st.container(border=True):

                st.markdown(f"#### 🎓 {edu.get('degree','')}")

                st.write(f"**College:** {edu.get('college','')}")

                st.write(f"**Year:** {edu.get('year','')}")

            st.write("")

    else:
        st.info("No education found.")

    # ----------------------------------------------------

    section_title("💼", "Experience")

    experience = resume.get("experience", [])

    if experience:

        with st.container(border=True):

            for item in experience:
                st.write("•", item)

    else:
        st.info("No experience found.")

    st.write("")

    # ----------------------------------------------------

    section_title("📂", "Projects")

    projects = resume.get("projects", [])

    if projects:
        for project in projects:

            with st.container(border=True):

                st.markdown(f"#### 📁 {project.get('title','')}")

                st.write(project.get("description",""))

            st.write("")

    else:
        st.info("No projects found.")


# ============================================================
# UI
# ============================================================

hero_banner(
    "📄 Upload Resume",
    "Upload a PDF or DOCX resume. The backend will parse it using OpenAI and store it in the database."
)

st.write("")

uploaded_file = st.file_uploader(

    "Choose Resume",

    type=["pdf", "docx"]

)

if uploaded_file is not None:

    st.write("Selected File:", uploaded_file.name)

    if st.button(

        "🚀 Upload Resume",

        use_container_width=True,

        type="primary"

    ):

        with st.spinner(

            "Uploading and parsing resume..."

        ):

            try:

                response = client.upload_resume(
                    uploaded_file
                )

                display_resume(
                    response["resume"]
                )

            except APIError as e:

                st.error(e.message)

            except Exception as e:

                st.error(str(e))