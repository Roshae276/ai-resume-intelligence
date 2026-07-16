from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.resume import Resume

from app.services.embedding_service import EmbeddingService
from app.services.qdrant_service import QdrantService
from app.services.llm_service import LLMService


class RecruitService:

    def __init__(self):

        self.embedding_service = EmbeddingService()
        self.qdrant_service = QdrantService()
        self.llm = LLMService()

    def search_candidates(
        self,
        job_id: int,
        top_k: int,
        db: Session
    ):

        job = (
            db.query(Job)
            .filter(Job.id == job_id)
            .first()
        )

        if job is None:
            raise ValueError("Job not found.")

        document = self.embedding_service.build_job_document(
            job.job_json
        )

        embedding = self.embedding_service.create_embedding(
            document
        )

        results = self.qdrant_service.search(
            embedding=embedding,
            top_k=top_k
        )

        candidates = []

        for result in results:

            payload = result.payload or {}

            if payload.get("document_type") != "resume":
                continue

            resume = (
                db.query(Resume)
                .filter(Resume.id == result.id)
                .first()
            )

            if resume is None:
                continue

            report = self.llm.generate_ats_report(
                resume.resume_json,
                job.job_json
            )

            candidates.append(
                {
                    "resume_id": resume.id,
                    "score": report.score,
                    "name": resume.name,
                    "matched_skills": report.matched_skills,
                    "missing_skills": report.missing_skills,
                    "suggestions": report.suggestions
                }
            )

        candidates.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return {
            "candidates": candidates
        }