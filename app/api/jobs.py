from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.dependencies import get_db

from app.schemas.job_request_schema import JobRequest

from app.services.job_service import JobService


app = APIRouter(
    prefix="/api/v1/jobs",
    tags=["Jobs"]
)

job_service = JobService()
@app.post("/")
def create_job(
    request: JobRequest,
    db: Session = Depends(get_db)
):

    try:

        result = job_service.create_job(
            request.job_description,
            db
        )

        return result

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
@app.get("/")
def get_all_jobs(
    db: Session = Depends(get_db)
):

    jobs = job_service.get_all_jobs(db)

    return jobs

@app.get("/{job_id}")
def get_job(
    job_id: int,
    db: Session = Depends(get_db)
):

    job = job_service.get_job_by_id(
        job_id,
        db
    )

    if job is None:

        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )

    return job