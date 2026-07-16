import os
import shutil
import uuid

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.settings import settings
from app.parsers.parser_factory import ParserFactory
from app.models.resume import Resume
from app.services.llm_service import LLMService
from app.services.embedding_service import EmbeddingService
from app.services.qdrant_service import QdrantService
from app.core.logger import logger
from app.core.exceptions import ResumeException



ALLOWED_EXTENSIONS = {".pdf", ".docx"}


class ResumeService:

    def save_resume(
        self,
        file: UploadFile,
        db: Session
    ):
        logger.info("Resume upload started.")
        extension = os.path.splitext(file.filename)[1].lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise ValueError(
                "Only PDF and DOCX files are allowed."
            )

        os.makedirs(
            settings.UPLOAD_FOLDER,
            exist_ok=True
        )

        unique_filename = f"{uuid.uuid4()}{extension}"

        file_path = os.path.join(
            settings.UPLOAD_FOLDER,
            unique_filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text
        parser = ParserFactory.get_parser(file_path)
        text = parser.extract_text(file_path)
        logger.info("Resume text extracted successfully.")

        # Parse using LLM
        llm_service = LLMService()
        resume = llm_service.parse_resume(text)
        logger.info("Resume parsed successfully.")

        # Save to database
        db_resume = Resume(
            original_filename=file.filename,
            saved_filename=unique_filename,
            name=resume.name,
            email=resume.email,
            phone=resume.phone,
            resume_json=resume.model_dump()
        )

        db.add(db_resume)
        db.commit()
        db.refresh(db_resume)
        
        logger.info(
            f"Resume stored in database with ID {db_resume.id}"
        )
        
        embedding_service = EmbeddingService()

        qdrant_service = QdrantService()

        document = embedding_service.build_resume_document(
            resume.model_dump()
        )

        embedding = embedding_service.create_embedding(
            document
        )
        
        logger.info("Embedding created successfully.")
        
        payload = resume.model_dump()
        payload["document_type"] = "resume"

        qdrant_service.store_vector(
            point_id=db_resume.id,
            embedding=embedding,
            payload=payload
        )
        
        logger.info("Resume stored in Qdrant.")
        logger.info("Resume upload completed.")
        
        return {
            "id": db_resume.id,
            "original_filename": file.filename,
            "saved_filename": unique_filename,
            "resume": resume
        }

    def get_all_resumes(
        self,
        db: Session
    ):

        resumes = db.query(Resume).all()

        return resumes

    def get_resume_by_id(
        self,
        resume_id: int,
        db: Session
    ):

        resume = (
            db.query(Resume)
            .filter(Resume.id == resume_id)
            .first()
        )

        return resume