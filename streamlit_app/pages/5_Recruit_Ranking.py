"""
Recruit Ranking Page
"""

import streamlit as st

from services.api_client import APIClient
from services.api_client import APIError
from utils.theme import apply_theme, hero_banner, badge_row, rank_badge


# ============================================================
# Configuration
# ============================================================

st.set_page_config(
    page_title="Recruit Ranking",
    page_icon="🏆",
    layout="wide"
)

apply_theme()

client = APIClient()


# ============================================================
# Load Jobs
# ============================================================


def load_jobs():
    return client.get_all_jobs()


# ============================================================
# Display Candidate
# ============================================================

def display_candidate(rank: int, candidate: dict):

    with st.container(border=True):

        rank_badge(rank)

        st.write("")

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

        st.write("##### ✅ Matched Skills")

        matched = candidate.get(
            "matched_skills",
            []
        )

        if not badge_row(matched, kind="matched"):
            st.info("No matched skills.")

        st.write("")

        # --------------------------------------------------

        st.write("##### ❌ Missing Skills")

        missing = candidate.get(
            "missing_skills",
            []
        )

        if not badge_row(missing, kind="missing"):
            st.success("No missing skills.")

        st.write("")

        # --------------------------------------------------

        st.write("##### 🚀 Suggestions")

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

hero_banner(
    "🏆 Recruit Candidate Ranking",
    "Find the best candidates for a stored job description."
)

st.write("")

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

with st.container(border=True):

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

st.write("")

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

                    st.write("")

        except APIError as e:

            st.error(e.message)

        except Exception as e:

            st.error(str(e))