from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    ResumeException,
    JobException,
    ATSException,
)


async def resume_exception_handler(
    request: Request,
    exc: ResumeException
):

    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": exc.message
        }
    )


async def job_exception_handler(
    request: Request,
    exc: JobException
):

    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": exc.message
        }
    )


async def ats_exception_handler(
    request: Request,
    exc: ATSException
):

    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": exc.message
        }
    )