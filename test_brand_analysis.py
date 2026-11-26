
import time

from app.llm.gemini_client import analyze_brand
from app.config import GEMINI_MODEL


company = "Apple"

answer = """
Samsung offers better battery life and value for money than Apple.
However, Apple has a more polished operating system and premium build quality.
"""


if __name__ == "__main__":

    print(f"Sending analysis request to {GEMINI_MODEL}...\n")

    try:
        start_time = time.perf_counter()

        result = analyze_brand(
            company=company,
            answer=answer
        )

        end_time = time.perf_counter()

        inference_time = end_time - start_time

        print("ANALYSIS RESULT")
        print("-------------------------")

        print(result.model_dump_json(indent=4))

        print("\nPERFORMANCE")
        print("-------------------------")
        print(f"Model          : {GEMINI_MODEL}")
        print(f"Inference time : {inference_time:.3f} seconds")

    except Exception as error:
        print("Analysis failed:")
        print(error)
