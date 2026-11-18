import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gemini configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)

# Agent configuration
MAX_ITERATIONS = 10
MAX_TOOL_OUTPUT_CHARS = 12000

# Application configuration
APP_NAME = "Autonomous AI Agent"

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. "
        "Please configure your .env file."
    )