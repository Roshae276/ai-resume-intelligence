from sqlalchemy.orm import Session

from app.models.resume import Resume

from app.services.embedding_service import EmbeddingService
from app.services.qdrant_service import QdrantService


class SearchService:

    def __init__(self):

        self.embedding_service = EmbeddingService()

        self.qdrant_service = QdrantService()

    def search_resumes(
        self,
        query: str,
        top_k: int,
        db: Session
    ):

        embedding = self.embedding_service.create_embedding(
            query
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
                .filter(
                    Resume.id == result.id
                )
                .first()
            )

            if resume:

                candidates.append(
                    {
                        "score": result.score,
                        "resume": resume
                    }
                )

        return candidates