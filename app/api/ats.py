from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.ats_request_schema import ATSRequest
from app.schemas.ats_schema import ATSResponse
from app.services.ats_service import ATSService


app = APIRouter(
    prefix="/api/v1/ats",
    tags=["ATS"]
)

ats_service = ATSService()

@app.post(
    "/",
    response_model=ATSResponse
)
def evaluate_resume(
    request: ATSRequest,
    db: Session = Depends(get_db)
):

    try:

        report = ats_service.evaluate(
            resume_id=request.resume_id,
            job_id=request.job_id,
            db=db
        )

        return report

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )