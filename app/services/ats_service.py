from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.models.job import Job

from app.services.llm_service import LLMService


class ATSService:

    def __init__(self):
        self.llm = LLMService()

    def evaluate(
        self,
        resume_id: int,
        job_id: int,
        db: Session
    ):

        resume = (
            db.query(Resume)
            .filter(Resume.id == resume_id)
            .first()
        )

        if resume is None:
            raise ValueError("Resume not found.")

        job = (
            db.query(Job)
            .filter(Job.id == job_id)
            .first()
        )

        if job is None:
            raise ValueError("Job not found.")

        report = self.llm.generate_ats_report(
            resume.resume_json,
            job.job_json
        )

        return report