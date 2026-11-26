
import json

from sqlalchemy.orm import Session

from app.database.models import Analysis
from app.schemas.analysis import AnalysisResult


def save_analysis(
    db: Session,
    company: str,
    answer: str,
    result: AnalysisResult
) -> Analysis:

    analysis_record = Analysis(
        company=company,
        answer=answer,
        mentioned=result.mentioned,
        sentiment=result.sentiment,
        sentiment_score=result.sentiment_score,
        relevant_context=json.dumps(
            result.relevant_context,
            ensure_ascii=False
        ),
        opinions=json.dumps(
            [
                opinion.model_dump()
                for opinion in result.opinions
            ],
            ensure_ascii=False
        ),
        explanation=result.explanation
    )

    try:
        db.add(analysis_record)
        db.commit()
        db.refresh(analysis_record)

        return analysis_record

    except Exception:
        db.rollback()
        raise

def get_analysis_history(db: Session) -> list[Analysis]:
    return (
        db.query(Analysis)
        .order_by(Analysis.created_at.desc())
        .all()
    )
def get_analysis_by_id(db: Session, analysis_id: int) -> Analysis | None:
    return db.query(Analysis).filter(Analysis.id == analysis_id).first()
def delete_analysis(db: Session, analysis_id: int) -> bool:
    record = get_analysis_by_id(db, analysis_id)

    if record is None:
        return False

    try:
        db.delete(record)
        db.commit()
        return True

    except Exception:
        db.rollback()
        raise