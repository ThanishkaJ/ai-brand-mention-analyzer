
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.connection import Base
from app.database.models import Analysis
from app.schemas.analysis import AnalysisResult
from app.services.database_service import save_analysis


@pytest.fixture
def db_session(tmp_path):
    database_path = tmp_path / "test_brand_analyzer.db"
    test_engine = create_engine(
        f"sqlite:///{database_path}",
        connect_args={"check_same_thread": False}
    )

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )

    Base.metadata.create_all(bind=test_engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        test_engine.dispose()


def test_save_analysis(db_session):
    result = AnalysisResult(
        company="Apple",
        mentioned=True,
        sentiment="positive",
        sentiment_score=None,
        relevant_context=[
            "Apple produces excellent smartphones."
        ],
        opinions=[
            {
                "opinion": "Excellent smartphones",
                "polarity": "positive",
                "intensity": 2
            }
        ],
        explanation="Apple receives positive evaluation."
    )

    saved_record = save_analysis(
        db=db_session,
        company="Apple",
        answer="Apple produces excellent smartphones.",
        result=result
    )

    assert saved_record.id is not None
    assert saved_record.company == "Apple"
    assert saved_record.sentiment == "positive"

    retrieved_record = db_session.query(Analysis).filter(
        Analysis.id == saved_record.id
    ).first()

    assert retrieved_record is not None
    assert retrieved_record.company == "Apple"
    assert retrieved_record.answer == (
        "Apple produces excellent smartphones."
    )
    assert retrieved_record.mentioned is True
    assert retrieved_record.sentiment == "positive"
