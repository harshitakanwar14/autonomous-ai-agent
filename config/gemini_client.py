
import time

from google import genai
from google.genai import types

from config.settings import GEMINI_API_KEY, GEMINI_MODEL


# Explicitly use Gemini Developer API beta version
client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(
        api_version="v1beta"
    )
)


FALLBACK_MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash"
]


def generate_with_fallback(contents, config=None):

    models = list(dict.fromkeys([
        GEMINI_MODEL,
        *FALLBACK_MODELS
    ]))

    last_error = None

    for model in models:

        print(f"\nUsing Gemini model: {model}")

        for attempt in range(3):

            try:
                response = client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=config
                )

                if not response.text:
                    raise ValueError(
                        "Gemini returned an empty response."
                    )

                print(f"Successful model: {model}")

                return response

            except Exception as error:

                last_error = error
                error_text = str(error).upper()

                retryable = any(code in error_text for code in [
                    "503",
                    "429",
                    "500",
                    "502",
                    "504",
                    "UNAVAILABLE",
                    "RESOURCE_EXHAUSTED",
                    "INTERNAL"
                ])

                if not retryable:
                    raise

                if attempt < 2:

                    wait_time = 2 ** (attempt + 1)

                    print(
                        f"Temporary error. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                else:
                    print(
                        f"{model} unavailable. "
                        "Trying fallback..."
                    )

    raise RuntimeError(
        f"All Gemini models failed. Last error: {last_error}"
    )

