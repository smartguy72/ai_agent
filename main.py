import os
from dotenv import load_dotenv
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai

client = genai.Client(api_key=api_key)

if len(sys.argv) > 1:
    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=" ".join(sys.argv[1:]))
    print(response.text)
else:
    print("Error: No response received")
    sys.exit(1)


prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count
print(f"Prompt tokens: {prompt_tokens}")
print(f"Response tokens: {response_tokens}")