from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.dependencies import get_db

from app.schemas.recruit_schema import (
    RecruitRequest,
    RecruitResponse
)

from app.services.recruit_service import RecruitService

app = APIRouter(

    prefix="/api/v1/recruit",

    tags=["Recruitment"]

)

recruit_service = RecruitService()

@app.post(

    "/search",

    response_model=RecruitResponse

)
def search_candidates(

    request: RecruitRequest,

    db: Session = Depends(get_db)

):

    try:

        return recruit_service.search_candidates(

            job_id=request.job_id,

            top_k=request.top_k,

            db=db

        )

    except ValueError as e:

        raise HTTPException(

            status_code=404,

            detail=str(e)

        )