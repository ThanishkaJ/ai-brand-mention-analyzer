
import time

from google import genai
from google.genai import types, errors

from app.config import GEMINI_API_KEY, GEMINI_MODEL
from app.llm.prompt import SYSTEM_PROMPT, build_analysis_prompt
from app.schemas.analysis import GeminiAnalysisResult


client = genai.Client(api_key=GEMINI_API_KEY)

RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
MAX_ATTEMPTS = 3
RETRY_DELAYS = [2, 5]


def analyze_brand(
    company: str,
    answer: str,
    model: str | None = None
) -> GeminiAnalysisResult:

    selected_model = model or GEMINI_MODEL

    user_prompt = build_analysis_prompt(
        company=company,
        answer=answer
    )

    for attempt in range(MAX_ATTEMPTS):

        try:
            print(
                f"Gemini API attempt {attempt + 1}/{MAX_ATTEMPTS}"
            )

            response = client.models.generate_content(
                model=selected_model,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    response_mime_type="application/json",
                    response_schema=GeminiAnalysisResult,
                    temperature=0.1
                )
            )

            if not response.text:
                raise ValueError("Gemini returned an empty response.")

            result = GeminiAnalysisResult.model_validate_json(
                response.text
            )

            if result.company.strip().casefold() != company.strip().casefold():
                raise ValueError(
                    "The returned company does not match the requested company."
                )

            return result

        except errors.APIError as error:

            status_code = getattr(error, "code", None)

            if status_code not in RETRYABLE_STATUS_CODES:
                raise RuntimeError(
                    f"Gemini API error ({status_code}): {error}"
                ) from error

            if attempt == MAX_ATTEMPTS - 1:
                raise RuntimeError(
                    f"Gemini API failed after {MAX_ATTEMPTS} attempts. "
                    f"Last error: {error}"
                ) from error

            delay = RETRY_DELAYS[attempt]

            print(
                f"Temporary Gemini API error ({status_code}). "
                f"Retrying in {delay} seconds..."
            )

            time.sleep(delay)

    raise RuntimeError("Gemini analysis could not be completed.")
