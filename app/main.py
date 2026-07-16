from fastapi import FastAPI

from app.api.health import app as health_router
from app.api.resume import app as resume_router
from app.core.settings import settings
from app.core.database import Base
from app.core.database import engine
from app.models.job import Job

from app.models.resume import Resume
from app.api.jobs import app as jobs_router
from app.api.ats import app as ats_router
from app.services.qdrant_service import QdrantService
from app.api.search import app as search_router
from app.api.recruit import app as recruit_router
from app.core.exceptions import (
    ResumeException,
    JobException,
    ATSException
)

from app.core.error_handler import (
    resume_exception_handler,
    job_exception_handler,
    ats_exception_handler
)

Base.metadata.create_all(bind=engine)
qdrant_service = QdrantService()

qdrant_service.create_collection()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered Resume Intelligence Platform",
)

app.add_exception_handler(
    ResumeException,
    resume_exception_handler
)

app.add_exception_handler(
    JobException,
    job_exception_handler
)

app.add_exception_handler(
    ATSException,
    ats_exception_handler
)

app.include_router(health_router)



app.include_router(resume_router)
app.include_router(
    jobs_router
)
app.include_router(
    ats_router
)

app.include_router(
    search_router
)

app.include_router(
    recruit_router
)