
from google import genai
from config.settings import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

print("\nChecking available Gemini models...\n")

try:
    available = []

    for model in client.models.list():

        name = getattr(model, "name", None)
        actions = getattr(model, "supported_actions", []) or []

        if name and "generateContent" in actions:

            clean_name = name.replace("models/", "")

            available.append(clean_name)

    if not available:
        print("No text-generation models found.")
    else:
        print("Models supporting text generation:\n")

        for index, name in enumerate(available, start=1):
            print(f"{index}. {name}")

        print(f"\nTotal available models: {len(available)}")

except Exception as error:
    print("Could not retrieve models:")
    print(error)
