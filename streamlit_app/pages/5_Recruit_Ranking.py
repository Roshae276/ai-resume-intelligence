"""
Recruit Ranking Page
"""

import streamlit as st

from services.api_client import APIClient
from services.api_client import APIError


# ============================================================
# Configuration
# ============================================================

st.set_page_config(
    page_title="Recruit Ranking",
    page_icon="🏆",
    layout="wide"
)

client = APIClient()


# ============================================================
# Load Jobs
# ============================================================

@st.cache_data
def load_jobs():
    return client.get_all_jobs()


# ============================================================
# Display Candidate
# ============================================================

def display_candidate(rank: int, candidate: dict):

    with st.container(border=True):

        st.subheader(
            f"🏅 Rank #{rank}"
        )

        col1, col2 = st.columns([3, 1])

        with col1:

            st.write(
                f"### {candidate.get('name','Unknown')}"
            )

        with col2:

            score = candidate.get(
                "score",
                0
            )

            st.metric(
                "ATS Score",
                f"{score}%"
            )

        st.progress(score / 100)

        st.divider()

        # --------------------------------------------------

        st.write("### ✅ Matched Skills")

        matched = candidate.get(
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

        # --------------------------------------------------

        st.write("### ❌ Missing Skills")

        missing = candidate.get(
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

        # --------------------------------------------------

        st.write("### 🚀 Suggestions")

        suggestions = candidate.get(
            "suggestions",
            []
        )

        if suggestions:

            for suggestion in suggestions:

                st.info(suggestion)

        else:

            st.success(
                "No suggestions."
            )


# ============================================================
# UI
# ============================================================

st.title("🏆 Recruit Candidate Ranking")

st.write(
    "Find the best candidates for a stored job description."
)

st.divider()

try:

    jobs = load_jobs()

except APIError as e:

    st.error(e.message)

    st.stop()

if not jobs:

    st.warning(
        "No jobs found."
    )

    st.stop()


job_options = {

    f"{job['id']} - {job['job_title']}": job["id"]

    for job in jobs

}

selected_job = st.selectbox(

    "Select Job",

    list(job_options.keys())

)

top_k = st.slider(

    "Top Candidates",

    min_value=1,

    max_value=20,

    value=5

)

st.divider()

if st.button(

    "🏆 Find Candidates",

    use_container_width=True,

    type="primary"

):

    with st.spinner(

        "Finding best candidates..."

    ):

        try:

            response = client.recruit_search(

                job_options[selected_job],

                top_k

            )

            candidates = response.get(
                "candidates",
                []
            )

            if not candidates:

                st.warning(
                    "No candidates found."
                )

            else:

                st.success(
                    f"{len(candidates)} candidates found."
                )

                st.divider()

                for index, candidate in enumerate(

                    candidates,

                    start=1

                ):

                    display_candidate(
                        index,
                        candidate
                    )

        except APIError as e:

            st.error(e.message)

        except Exception as e:

            st.error(str(e))