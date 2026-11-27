import pytest

from app.services.analysis_service import calculate_sentiment
from app.schemas.analysis import GeminiAnalysisResult, Opinion


def make_extraction(mentioned, opinions):
    return GeminiAnalysisResult(
        company="Apple",
        mentioned=mentioned,
        relevant_context=["Apple is discussed."] if mentioned else [],
        opinions=opinions,
        explanation="Test case."
    )


@pytest.mark.parametrize(
    "name, mentioned, opinions, expected_sentiment, expected_score",
    [
        (
            "Not mentioned",
            False,
            [],
            "not_applicable",
            None
        ),
        (
            "Neutral",
            True,
            [],
            "neutral",
            None
        ),
        (
            "Positive",
            True,
            [
                Opinion(
                    opinion="Excellent performance",
                    polarity="positive",
                    intensity=2
                )
            ],
            "positive",
            None
        ),
        (
            "Negative",
            True,
            [
                Opinion(
                    opinion="Poor performance",
                    polarity="negative",
                    intensity=2
                )
            ],
            "negative",
            None
        ),
        (
            "Mixed - Negative",
            True,
            [
                Opinion(
                    opinion="Good design",
                    polarity="positive",
                    intensity=1
                ),
                Opinion(
                    opinion="Poor battery life",
                    polarity="negative",
                    intensity=2
                )
            ],
            "negative",
            0.3333
        ),
        (
            "Mixed - Neutral",
            True,
            [
                Opinion(
                    opinion="Good design",
                    polarity="positive",
                    intensity=1
                ),
                Opinion(
                    opinion="Poor battery life",
                    polarity="negative",
                    intensity=1
                )
            ],
            "neutral_mixed",
            0.5
        ),
        (
            "Mixed - Positive",
            True,
            [
                Opinion(
                    opinion="Excellent design",
                    polarity="positive",
                    intensity=2
                ),
                Opinion(
                    opinion="High price",
                    polarity="negative",
                    intensity=1
                )
            ],
            "positive",
            0.6667
        ),
        (
            "Lower threshold boundary - 0.4",
            True,
            [
                Opinion(
                    opinion="Good design",
                    polarity="positive",
                    intensity=2
                ),
                Opinion(
                    opinion="Poor battery life",
                    polarity="negative",
                    intensity=2
                ),
                Opinion(
                    opinion="High price",
                    polarity="negative",
                    intensity=1
                )
            ],
            "neutral_mixed",
            0.4
        ),
        (
            "Upper threshold boundary - 0.6",
            True,
            [
                Opinion(
                    opinion="Excellent design",
                    polarity="positive",
                    intensity=2
                ),
                Opinion(
                    opinion="Impressive performance",
                    polarity="positive",
                    intensity=1
                ),
                Opinion(
                    opinion="High price",
                    polarity="negative",
                    intensity=2
                )
            ],
            "neutral_mixed",
            0.6
        )
    ],
    ids=lambda value: value if isinstance(value, str) else None
)
def test_calculate_sentiment(
    name,
    mentioned,
    opinions,
    expected_sentiment,
    expected_score
):
    extraction = make_extraction(mentioned, opinions)

    sentiment, score = calculate_sentiment(extraction)

    assert sentiment == expected_sentiment, (
        f"{name}: Expected {expected_sentiment}, got {sentiment}"
    )

    assert score == expected_score, (
        f"{name}: Expected score {expected_score}, got {score}"
    )
