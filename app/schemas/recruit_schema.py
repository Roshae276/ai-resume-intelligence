from pydantic import BaseModel
from typing import List


class RecruitRequest(BaseModel):

    job_id: int

    top_k: int = 5


class Candidate(BaseModel):

    resume_id: int

    score: int

    name: str

    matched_skills: List[str]

    missing_skills: List[str]

    suggestions: List[str]


class RecruitResponse(BaseModel):

    candidates: List[Candidate]