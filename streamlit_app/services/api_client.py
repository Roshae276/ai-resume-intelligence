"""
API Client for AI Resume Intelligence Platform

This is the ONLY file that communicates with the FastAPI backend.

Every Streamlit page should import APIClient.
No page should call requests.get() or requests.post() directly.
"""

from dataclasses import dataclass
from typing import Any, Optional

import requests


# ============================================================
# Configuration
# ============================================================

BASE_URL = "http://127.0.0.1:8000"
TIMEOUT = 60


# ============================================================
# Custom Exception
# ============================================================

class APIError(Exception):

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


# ============================================================
# API Client
# ============================================================

@dataclass
class APIClient:

    base_url: str = BASE_URL
    timeout: int = TIMEOUT

    # --------------------------------------------------------
    # Internal Helpers
    # --------------------------------------------------------

    def _url(self, endpoint: str) -> str:
        return f"{self.base_url}{endpoint}"

    def _handle_response(
        self,
        response: requests.Response
    ) -> Any:

        try:
            response.raise_for_status()

        except requests.HTTPError:

            try:
                detail = response.json().get(
                    "detail",
                    response.text
                )

            except Exception:
                detail = response.text

            raise APIError(
                detail,
                response.status_code
            )

        if response.content:
            return response.json()

        return None

    def _get(
        self,
        endpoint: str,
        params: dict | None = None
    ):

        try:

            response = requests.get(
                self._url(endpoint),
                params=params,
                timeout=self.timeout
            )

            return self._handle_response(response)

        except requests.ConnectionError:

            raise APIError(
                "Cannot connect to FastAPI server."
            )

        except requests.Timeout:

            raise APIError(
                "Request timed out."
            )

    def _post(
        self,
        endpoint: str,
        json: dict | None = None,
        files: dict | None = None
    ):

        try:

            response = requests.post(
                self._url(endpoint),
                json=json,
                files=files,
                timeout=self.timeout
            )

            return self._handle_response(response)

        except requests.ConnectionError:

            raise APIError(
                "Cannot connect to FastAPI server."
            )

        except requests.Timeout:

            raise APIError(
                "Request timed out."
            )

    # ========================================================
    # Resume APIs
    # ========================================================

    def upload_resume(
        self,
        uploaded_file
    ):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type
            )
        }

        return self._post(
            "/api/v1/resume/upload",
            files=files
        )

    def get_all_resumes(self):

        return self._get(
            "/api/v1/resume/"
        )

    def get_resume(
        self,
        resume_id: int
    ):

        return self._get(
            f"/api/v1/resume/{resume_id}"
        )

    # ========================================================
    # Job APIs
    # ========================================================

    def create_job(
        self,
        job_description: str
    ):

        return self._post(

            "/api/v1/jobs/",

            json={
                "job_description": job_description
            }

        )

    def get_all_jobs(self):

        return self._get(
            "/api/v1/jobs/"
        )

    # ========================================================
    # ATS APIs
    # ========================================================

    def analyze_resume(
        self,
        resume_id: int,
        job_id: int
    ):

        return self._post(

            "/api/v1/ats/",

            json={
                "resume_id": resume_id,
                "job_id": job_id
            }

        )

    # ========================================================
    # Semantic Search
    # ========================================================

    def semantic_search(
        self,
        query: str,
        top_k: int
    ):

        return self._post(

            "/api/v1/search/",

            json={
                "query": query,
                "top_k": top_k
            }

        )

    # ========================================================
    # Recruit Ranking
    # ========================================================

    def recruit_search(
        self,
        job_id: int,
        top_k: int
    ):

        return self._post(

            "/api/v1/recruit/search/",

            json={
                "job_id": job_id,
                "top_k": top_k
            }

        )