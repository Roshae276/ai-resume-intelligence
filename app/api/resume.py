from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import HTTPException,Depends
from app.core.dependencies import get_db
from sqlalchemy.orm import Session
from app.services.resume_service import ResumeService
from app.schemas.resume_schema import UploadResponse

app = APIRouter(
    prefix="/api/v1/resume",
    tags=["Resume"]
)

resume_service = ResumeService()


@app.post(
    "/upload",
    response_model=UploadResponse
)

def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    try:

        result = resume_service.save_resume(
            file,
            db
        )

        return UploadResponse(
            id=result["id"],
            original_filename=result["original_filename"],
            saved_filename=result["saved_filename"],
            resume=result["resume"],
            success=True,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@app.get("/")
def get_all_resumes(

    db: Session = Depends(get_db)

):

    resumes = resume_service.get_all_resumes(db)

    return resumes

@app.get("/{resume_id}")
def get_resume(

    resume_id: int,

    db: Session = Depends(get_db)

):

    resume = resume_service.get_resume_by_id(
        resume_id,
        db
    )

    if resume is None:

        raise HTTPException(

            status_code=404,

            detail="Resume not found."

        )

    return resume