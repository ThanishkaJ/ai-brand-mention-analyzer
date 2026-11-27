
import json
from pathlib import Path

import pytest

from app.schemas.analysis import GeminiAnalysisResult, Opinion
from app.services.analysis_service import calculate_sentiment


DATASET_PATH = Path(__file__).parent / "evaluation_cases.json"

with DATASET_PATH.open("r", encoding="utf-8") as file:
    EVALUATION_CASES = json.load(file)


@pytest.mark.parametrize(
    "case",
    EVALUATION_CASES,
    ids=lambda case: f"case_{case['id']}_{case['category']}"
)
def test_evaluation_case_sentiment(case):
    opinions = [
        Opinion(**opinion)
        for opinion in case["expected_opinions"]
    ]

    extraction = GeminiAnalysisResult(
        company=case["company"],
        mentioned=case["expected_mentioned"],
        relevant_context=case["expected_context"],
        opinions=opinions,
        explanation="Evaluation dataset test."
    )

    actual_sentiment, actual_score = calculate_sentiment(extraction)

    assert actual_sentiment == case["expected_sentiment"], (
        f"Case {case['id']}: expected "
        f"{case['expected_sentiment']}, got {actual_sentiment}"
    )

    expected_score = case.get("expected_normalized_score")

    if expected_score is not None:
        assert actual_score == pytest.approx(expected_score, abs=0.0001)
    else:
        assert actual_score is None
