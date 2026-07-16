from pydantic import BaseModel

from typing import List


class JobResponse(BaseModel):

    job_title: str

    skills: List[str]

    experience: str

    education: str

    responsibilities: List[str]