import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Gemini configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

# Validate API key
if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. Please check your .env file."
    )