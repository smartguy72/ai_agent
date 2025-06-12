import os
from dotenv import load_dotenv
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai
client = genai.Client(api_key=api_key)

from google.genai import types

user_prompt = " ".join(sys.argv[1:])

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]



if len(sys.argv) > 1:
    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages)
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    if "--verbose" in sys.argv:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
    print(response.text)
else:
    print("Error: No response received")
    sys.exit(1)



