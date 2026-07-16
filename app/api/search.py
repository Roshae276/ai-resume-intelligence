from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.dependencies import get_db

from app.schemas.search_schema import SearchRequest

from app.services.search_service import SearchService

app = APIRouter(
    prefix="/api/v1/search",
    tags=["Search"]
)

search_service = SearchService()

@app.post("/")
def search(
    request: SearchRequest,
    db: Session = Depends(get_db)
):

    return search_service.search_resumes(
        query=request.query,
        top_k=request.top_k,
        db=db
    )