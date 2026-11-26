
from app.llm.gemini_client import analyze_brand
from app.schemas.analysis import (
    AnalysisResult,
    GeminiAnalysisResult
)


def calculate_sentiment(
    extraction: GeminiAnalysisResult
) -> tuple[str, float | None]:

    # Case 1: Target company is not mentioned.
    if not extraction.mentioned:
        return "not_applicable", None

    positive_intensity = sum(
        opinion.intensity
        for opinion in extraction.opinions
        if opinion.polarity == "positive"
    )

    negative_intensity = sum(
        opinion.intensity
        for opinion in extraction.opinions
        if opinion.polarity == "negative"
    )

    # Case 2: No evaluative opinions.
    if positive_intensity == 0 and negative_intensity == 0:
        return "neutral", None

    # Case 3: Only positive opinions.
    if negative_intensity == 0:
        return "positive", None

    # Case 4: Only negative opinions.
    if positive_intensity == 0:
        return "negative", None

    # Case 5: Both positive and negative opinions.
    score = positive_intensity / (
        positive_intensity + negative_intensity
    )

    if score < 0.4:
        sentiment = "negative"

    elif score <= 0.6:
        sentiment = "neutral_mixed"

    else:
        sentiment = "positive"

    return sentiment, round(score, 4)


def analyze_brand_text(
    company: str,
    answer: str
) -> AnalysisResult:

    # Step 1: Extract information using Gemini.
    extraction = analyze_brand(
        company=company,
        answer=answer
    )

    # Step 2: Calculate sentiment using Python.
    sentiment, score = calculate_sentiment(extraction)

    # Step 3: Construct the final application response.
    return AnalysisResult(
        company=extraction.company,
        mentioned=extraction.mentioned,
        sentiment=sentiment,
        sentiment_score=score,
        relevant_context=extraction.relevant_context,
        opinions=extraction.opinions,
        explanation=extraction.explanation
    )
