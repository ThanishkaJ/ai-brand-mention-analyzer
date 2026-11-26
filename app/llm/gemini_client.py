
import time

from google import genai
from google.genai import types, errors

from app.config import GEMINI_API_KEY, GEMINI_MODEL
from app.llm.prompt import SYSTEM_PROMPT, build_analysis_prompt
from app.schemas.analysis import AnalysisResult


# Create the Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


# Temporary HTTP errors for which retrying is appropriate
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}

# Maximum number of API attempts
MAX_ATTEMPTS = 3

# Waiting time before the second and third attempts
RETRY_DELAYS = [2, 5]


def analyze_brand(
    company: str,
    answer: str,
    model: str | None = None
) -> AnalysisResult:

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
                    response_schema=AnalysisResult,
                    temperature=0.1
                )
            )

            if not response.text:
                raise ValueError(
                    "Gemini returned an empty response."
                )

            result = AnalysisResult.model_validate_json(
                response.text
            )

            if (
                result.company.strip().casefold()
                != company.strip().casefold()
            ):
                raise ValueError(
                    "The returned company does not match "
                    "the requested company."
                )

            return result

        except errors.APIError as error:

            status_code = getattr(error, "code", None)

            # Do not retry permanent API errors
            if status_code not in RETRYABLE_STATUS_CODES:
                raise RuntimeError(
                    f"Gemini API error ({status_code}): {error}"
                ) from error

            # Stop if all attempts have been exhausted
            if attempt == MAX_ATTEMPTS - 1:
                raise RuntimeError(
                    f"Gemini API failed after {MAX_ATTEMPTS} "
                    f"attempts. Last error: {error}"
                ) from error

            delay = RETRY_DELAYS[attempt]

            print(
                f"Temporary Gemini API error ({status_code}). "
                f"Retrying in {delay} seconds..."
            )

            time.sleep(delay)

    raise RuntimeError("Gemini analysis could not be completed.")
