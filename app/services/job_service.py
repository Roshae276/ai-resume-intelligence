from sqlalchemy.orm import Session

from app.models.job import Job
from app.services.llm_service import LLMService
from app.services.embedding_service import EmbeddingService
from app.services.qdrant_service import QdrantService
llm = LLMService()


class JobService:

    def create_job(
        self,
        job_description: str,
        db: Session
    ):

        

        job = llm.parse_job_description(
            job_description
        )

        db_job = Job(

            job_title=job.job_title,

            experience=job.experience,

            education=job.education,

            job_json=job.model_dump()

        )

        db.add(db_job)

        db.commit()

        db.refresh(db_job)
        embedding_service = EmbeddingService()

        qdrant_service = QdrantService()

        document = embedding_service.build_job_document(
            job.model_dump()
        )

        embedding = embedding_service.create_embedding(
            document
        )

        payload = job.model_dump()
        payload["document_type"] = "job"

        qdrant_service.store_vector(
            point_id=100000 + db_job.id,
            embedding=embedding,
            payload=payload
        )

        return {

        "id": db_job.id,

        "job": job

    }
        
    def get_all_jobs(
        self,
        db: Session
    ):

        jobs = db.query(Job).all()

        return jobs
    
    def get_job_by_id(
        self,
        job_id: int,
        db: Session
    ):

        job = (
            db.query(Job)
            .filter(Job.id == job_id)
            .first()
        )

        return job