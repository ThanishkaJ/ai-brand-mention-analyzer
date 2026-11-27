
import json
import time
from pathlib import Path

from app.config import GEMINI_MODEL
from app.services.analysis_service import analyze_brand_text


DATASET_PATH = Path("tests/evaluation_cases.json")
OUTPUT_PATH = Path("tests/smoke_test_results.json")

# One representative case from each evaluation category
SELECTED_CATEGORIES = {
    "direct_positive",
    "direct_negative",
    "competitor_comparison",
    "mixed",
    "neutral_factual",
    "not_mentioned",
}


def load_selected_cases():
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        cases = json.load(file)

    selected_cases = []

    for category in sorted(SELECTED_CATEGORIES):
        matching_case = next(
            (
                case for case in cases
                if case["category"] == category
            ),
            None
        )

        if matching_case:
            selected_cases.append(matching_case)
        else:
            print(f"WARNING: No test case found for category: {category}")

    return selected_cases


def evaluate_case(case):
    print(f"\nCase ID: {case['id']}")
    print(f"Category: {case['category']}")
    print(f"Company: {case['company']}")

    start_time = time.perf_counter()

    try:
        # Runs the complete pipeline:
        # Gemini extraction + backend sentiment calculation
        result = analyze_brand_text(
            company=case["company"],
            answer=case["answer"]
        )

        inference_time = time.perf_counter() - start_time

        mention_correct = (
            result.mentioned == case["expected_mentioned"]
        )

        sentiment_correct = (
            result.sentiment == case["expected_sentiment"]
        )

        print(f"Expected mention   : {case['expected_mentioned']}")
        print(f"Predicted mention  : {result.mentioned}")
        print(f"Mention correct    : {mention_correct}")

        print(f"Expected sentiment : {case['expected_sentiment']}")
        print(f"Predicted sentiment: {result.sentiment}")
        print(f"Sentiment correct  : {sentiment_correct}")

        print(f"Inference time     : {inference_time:.3f} seconds")

        print("\nExtracted context:")
        for sentence in result.relevant_context:
            print(f"- {sentence}")

        print("\nExtracted opinions:")
        for opinion in result.opinions:
            print(
                f"- {opinion.opinion} "
                f"({opinion.polarity}, intensity={opinion.intensity})"
            )

        print("\nExplanation:")
        print(result.explanation)

        return {
            "id": case["id"],
            "category": case["category"],
            "company": case["company"],
            "expected_mentioned": case["expected_mentioned"],
            "predicted_mentioned": result.mentioned,
            "mention_correct": mention_correct,
            "expected_sentiment": case["expected_sentiment"],
            "predicted_sentiment": result.sentiment,
            "sentiment_score": result.sentiment_score,
            "sentiment_correct": sentiment_correct,
            "inference_time_seconds": round(inference_time, 3),
            "extracted_context": result.relevant_context,
            "extracted_opinions": [
                opinion.model_dump()
                for opinion in result.opinions
            ],
            "explanation": result.explanation,
            "error": None
        }

    except Exception as error:
        inference_time = time.perf_counter() - start_time

        print(f"Evaluation failed: {error}")

        return {
            "id": case["id"],
            "category": case["category"],
            "company": case["company"],
            "inference_time_seconds": round(inference_time, 3),
            "error": str(error)
        }


if __name__ == "__main__":
    cases = load_selected_cases()
    results = []

    print(f"Model: {GEMINI_MODEL}")
    print(f"Selected cases: {len(cases)}")

    for case in cases:
        results.append(evaluate_case(case))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)

    # Exclude failed API calls from accuracy calculations
    successful_results = [
        result for result in results
        if result.get("error") is None
    ]

    print("\n" + "=" * 50)
    print("SMOKE TEST SUMMARY")
    print("=" * 50)

    print(f"Total cases          : {len(results)}")
    print(f"Successful cases     : {len(successful_results)}")
    print(f"Failed cases         : {len(results) - len(successful_results)}")

    if successful_results:
        mention_accuracy = (
            sum(r["mention_correct"] for r in successful_results)
            / len(successful_results)
        ) * 100

        sentiment_accuracy = (
            sum(r["sentiment_correct"] for r in successful_results)
            / len(successful_results)
        ) * 100

        print(f"Mention accuracy     : {mention_accuracy:.2f}%")
        print(f"Sentiment accuracy   : {sentiment_accuracy:.2f}%")

    else:
        print("No cases completed successfully.")

    print(f"\nDetailed results saved to: {OUTPUT_PATH}")
