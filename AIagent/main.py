def main():
    print("Hello from aiagent!")


if __name__ == "__main__":
    main()

import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai
import sys

client = genai.Client(api_key=api_key)
if len(sys.argv) < 2:
    print("Missing Argument")
    sys.exit(1)

from google.genai import types
user_prompt = sys.argv[1]
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]
response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=messages
)
print(response.text)

if len(sys.argv)>=3 and sys.argv[2] == '--verbose':
    print(f'User prompt: {user_prompt}')
    print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
    print(f'Response tokens: {response.usage_metadata.candidates_token_count}')


