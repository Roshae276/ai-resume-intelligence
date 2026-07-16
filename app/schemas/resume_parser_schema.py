from pydantic import BaseModel
from typing import List


class Education(BaseModel):
    degree: str
    college: str
    year: str


class Project(BaseModel):
    title: str
    description: str


class ResumeParserResponse(BaseModel):
    name: str
    email: str
    phone: str

    skills: List[str]

    education: List[Education]

    projects: List[Project]