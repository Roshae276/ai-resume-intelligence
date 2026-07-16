
from pydantic import BaseModel
from typing import List
from app.core.logger import logger


class Education(BaseModel):
    degree: str
    college: str
    year: str


class Project(BaseModel):
    title: str
    description: str


class ResumeData(BaseModel):
    name: str
    email: str
    phone: str

    skills: List[str]

    education: List[Education]

    projects: List[Project]


# class UploadResponse(BaseModel):
#     original_filename: str
#     saved_filename: str
#     extracted_text: str
#     success: bool

from app.schemas.resume_parser_schema import ResumeParserResponse


class UploadResponse(BaseModel):
    id: int
    original_filename: str
    saved_filename: str
    resume: ResumeParserResponse
    success: bool
    
    