from google import genai
from app.config import GEMINI_API_KEY, GEMINI_MODEL


def test_gemini_connection():

    # Initialize Gemini client
    client = genai.Client(api_key=GEMINI_API_KEY)

    # Send a simple test prompt
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents="Reply with exactly: Gemini connection successful."
    )

    # Display response
    print("\nGemini Response:")
    print(response.text)


if __name__ == "__main__":
    test_gemini_connection()