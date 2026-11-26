
from app.services.analysis_service import calculate_sentiment
from app.schemas.analysis import (
    GeminiAnalysisResult,
    Opinion
)


def make_extraction(mentioned, opinions):
    return GeminiAnalysisResult(
        company="Apple",
        mentioned=mentioned,
        relevant_context=["Apple is discussed."]
        if mentioned else [],
        opinions=opinions,
        explanation="Test case."
    )


test_cases = [
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
        [Opinion(
            opinion="Excellent performance",
            polarity="positive",
            intensity=2
        )],
        "positive",
        None
    ),
    (
        "Negative",
        True,
        [Opinion(
            opinion="Poor performance",
            polarity="negative",
            intensity=2
        )],
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
    )
]


for name, mentioned, opinions, expected_sentiment, expected_score in test_cases:

    extraction = make_extraction(mentioned, opinions)

    sentiment, score = calculate_sentiment(extraction)

    assert sentiment == expected_sentiment, (
        f"{name}: Expected {expected_sentiment}, got {sentiment}"
    )

    assert score == expected_score, (
        f"{name}: Expected score {expected_score}, got {score}"
    )

    print(f"PASS: {name}")


print("\nAll sentiment logic tests passed!")
