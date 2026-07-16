"""
Upload Resume Page
"""

import streamlit as st

from services.api_client import APIClient
from services.api_client import APIError


# ============================================================
# Configuration
# ============================================================

st.set_page_config(
    page_title="Upload Resume",
    page_icon="📄",
    layout="wide"
)

client = APIClient()


# ============================================================
# Helper
# ============================================================

def display_resume(resume: dict):

    st.success("✅ Resume parsed successfully!")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("👤 Candidate")

        st.write("**Name:**", resume.get("name", "N/A"))
        st.write("**Email:**", resume.get("email", "N/A"))
        st.write("**Phone:**", resume.get("phone", "N/A"))

    with col2:

        st.subheader("🎯 Skills")

        skills = resume.get("skills", [])

        if skills:

            for skill in skills:
                st.success(skill)

        else:
            st.info("No skills found.")

    st.divider()

    # ----------------------------------------------------

    st.subheader("🎓 Education")

    education = resume.get("education", [])

    if education:
        for edu in education:

            st.markdown(f"### 🎓 {edu.get('degree','')}")

            st.write(f"**College:** {edu.get('college','')}")

            st.write(f"**Year:** {edu.get('year','')}")

            st.divider()

       
            

    else:
        st.info("No education found.")

    # ----------------------------------------------------

    st.subheader("💼 Experience")

    experience = resume.get("experience", [])

    if experience:

        for item in experience:
            st.write("•", item)

    else:
        st.info("No experience found.")

    # ----------------------------------------------------

    st.subheader("📂 Projects")

    projects = resume.get("projects", [])

    if projects:
        for project in projects:

            st.markdown(f"### 📁 {project.get('title','')}")

            st.write(project.get("description",""))

            st.divider()

        
            

    else:
        st.info("No projects found.")


# ============================================================
# UI
# ============================================================

st.title("📄 Upload Resume")

st.write(
    "Upload a PDF or DOCX resume. "
    "The backend will parse it using OpenAI and store it in the database."
)

st.divider()

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