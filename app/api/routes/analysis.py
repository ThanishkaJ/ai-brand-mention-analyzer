
import logging
import json


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool
from google.genai.errors import APIError

from app.database.connection import get_db
from app.schemas.analysis import AnalysisRequest, AnalysisResult
from app.services.analysis_service import analyze_brand_text
from app.services.database_service import save_analysis, get_analysis_history, get_analysis_by_id, delete_analysis


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api",
    tags=["Brand Analysis"]
)


@router.post(
    "/analyze",
    response_model=AnalysisResult
)
async def analyze(
    request: AnalysisRequest,
    db: Session = Depends(get_db)
):
    try:
        company = request.company.strip()
        answer = request.answer.strip()

        # Step 1: Analyze the brand using Gemini
        result = await run_in_threadpool(
            analyze_brand_text,
            company=company,
            answer=answer
        )

        # Step 2: Save the analysis result in SQLite
        await run_in_threadpool(
            save_analysis,
            db=db,
            company=company,
            answer=answer,
            result=result
        )

        # Step 3: Return the analysis result
        return result

    except APIError as error:
        status_code = getattr(error, "code", None)

        logger.exception("Gemini API request failed")

        if status_code == 429:
            raise HTTPException(
                status_code=429,
                detail="Gemini API rate limit reached. Please try again later."
            ) from error

        if isinstance(status_code, int) and status_code >= 500:
            raise HTTPException(
                status_code=503,
                detail="The AI service is temporarily unavailable. Please try again later."
            ) from error

        raise HTTPException(
            status_code=502,
            detail="The AI service could not process the analysis request."
        ) from error

    except HTTPException:
        raise

    except Exception as error:
        logger.exception("Unexpected error during brand analysis")

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while analyzing the brand."
        ) from error


@router.get("/history")
async def get_history(
    db: Session = Depends(get_db)
):
    try:
        records = await run_in_threadpool(
            get_analysis_history,
            db=db
        )

        
        return [
            {
                "id": record.id,
                "company": record.company,
                "mentioned": record.mentioned,
                "sentiment": record.sentiment,
                "sentiment_score": record.sentiment_score,
                "relevant_context": json.loads(record.relevant_context),
                "opinions": json.loads(record.opinions),
                "explanation": record.explanation,
                "created_at": record.created_at
            }
            for record in records
        ]


    except Exception as error:
        logger.exception("Failed to retrieve analysis history")

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while retrieving analysis history."
        ) from error


@router.get("/history/{analysis_id}")
async def get_history_by_id(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    try:
        record = await run_in_threadpool(
            get_analysis_by_id,
            db=db,
            analysis_id=analysis_id
        )

        if record is None:
            raise HTTPException(
                status_code=404,
                detail="Analysis record not found."
            )

        return {
            "id": record.id,
            "company": record.company,
            "mentioned": record.mentioned,
            "sentiment": record.sentiment,
            "sentiment_score": record.sentiment_score,
            "relevant_context": json.loads(record.relevant_context),
            "opinions": json.loads(record.opinions),
            "explanation": record.explanation,
            "created_at": record.created_at
        }

    except HTTPException:
        raise

    except Exception as error:
        logger.exception("Failed to retrieve analysis by ID")

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while retrieving the analysis."
        ) from error

@router.delete("/history/{analysis_id}")
async def delete_history_by_id(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    try:
        deleted = await run_in_threadpool(
            delete_analysis,
            db=db,
            analysis_id=analysis_id
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Analysis record not found."
            )

        return {
            "message": f"Analysis record {analysis_id} deleted successfully."
        }

    except HTTPException:
        raise

    except Exception as error:
        logger.exception("Failed to delete analysis")

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while deleting the analysis."
        ) from error
