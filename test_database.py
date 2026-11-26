
from app.database.connection import SessionLocal
from app.database.models import Analysis
from app.schemas.analysis import AnalysisResult
from app.services.database_service import save_analysis


def test_save_analysis():
    db = SessionLocal()
    test_record = None

    try:
        # Create a sample analysis result without calling Gemini
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

        # Save the sample analysis
        test_record = save_analysis(
            db=db,
            company="Apple",
            answer="Apple produces excellent smartphones.",
            result=result
        )

        print("Analysis saved successfully!")
        print("Record ID:", test_record.id)
        print("Company:", test_record.company)
        print("Sentiment:", test_record.sentiment)
        print("Context:", test_record.relevant_context)
        print("Opinions:", test_record.opinions)
        print("Created at:", test_record.created_at)

        # Verify that the record can be retrieved
        retrieved = db.query(Analysis).filter(
            Analysis.id == test_record.id
        ).first()

        assert retrieved is not None
        assert retrieved.company == "Apple"
        assert retrieved.sentiment == "positive"

        print("\nDatabase retrieval verification passed!")

    finally:
        # Remove the temporary test record
        if test_record is not None:
            db.delete(test_record)
            db.commit()

        db.close()


if __name__ == "__main__":
    test_save_analysis()
