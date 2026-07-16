"""
Semantic Search Page
"""

import streamlit as st

from services.api_client import APIClient
from services.api_client import APIError


st.set_page_config(
    page_title="Semantic Search",
    page_icon="🔍",
    layout="wide"
)

client = APIClient()


def display_result(result):

    resume = result.get("resume", {})
    resume_json = resume.get("resume_json", {})

    with st.container(border=True):

        col1, col2 = st.columns([4, 1])

        with col1:

            st.subheader(
                resume.get(
                    "name",
                    "Unknown Candidate"
                )
            )

        with col2:

            st.metric(
                "Similarity",
                f"{result.get('score', 0):.3f}"
            )

        st.write(
            "**Email:**",
            resume.get(
                "email",
                "N/A"
            )
        )

        st.write(
            "**Phone:**",
            resume.get(
                "phone",
                "N/A"
            )
        )

        skills = resume_json.get(
            "skills",
            []
        )

        if skills:

            st.write("### Skills")

            cols = st.columns(4)

            for i, skill in enumerate(skills):

                with cols[i % 4]:

                    st.success(skill)

        education = resume_json.get(
            "education",
            []
        )

        if education:

            with st.expander(
                "🎓 Education"
            ):

                for edu in education:

                    st.write(
                        f"**{edu.get('degree','')}**"
                    )

                    st.write(
                        edu.get(
                            "college",
                            ""
                        )
                    )

                    st.write(
                        edu.get(
                            "year",
                            ""
                        )
                    )

                    st.divider()

        projects = resume_json.get(
            "projects",
            []
        )

        if projects:

            with st.expander(
                "📂 Projects"
            ):

                for project in projects:

                    st.write(
                        f"**{project.get('title','')}**"
                    )

                    st.write(
                        project.get(
                            "description",
                            ""
                        )
                    )

                    st.divider()


st.title("🔍 Semantic Resume Search")

st.write(
    "Search resumes using semantic similarity."
)

st.divider()

query = st.text_input(
    "Search Query",
    placeholder="Python FastAPI Docker"
)

top_k = st.slider(
    "Number of Results",
    1,
    20,
    5
)

st.divider()

if st.button(
    "🔍 Search",
    use_container_width=True,
    type="primary"
):

    if not query.strip():

        st.warning(
            "Please enter a search query."
        )

        st.stop()

    with st.spinner(
        "Searching..."
    ):

        try:

            # Backend returns LIST directly
            results = client.semantic_search(
                query,
                top_k
            )

            if not results:

                st.warning(
                    "No resumes found."
                )

            else:

                st.success(
                    f"{len(results)} resume(s) found."
                )

                st.divider()

                for result in results:

                    display_result(result)

        except APIError as e:

            st.error(e.message)

        except Exception as e:

            st.error(str(e))