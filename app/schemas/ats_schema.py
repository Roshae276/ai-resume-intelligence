from pydantic import BaseModel
from typing import List


class ATSResponse(BaseModel):

    score: int

    matched_skills: List[str]

    missing_skills: List[str]

    strengths: List[str]

    weaknesses: List[str]

    suggestions: List[str]