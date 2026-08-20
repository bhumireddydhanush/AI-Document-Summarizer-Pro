import os
from dotenv import load_dotenv
from google import genai

# Load .env
load_dotenv()

print("API Key:", os.getenv("GEMINI_API_KEY"))
print("Length:", len(os.getenv("GEMINI_API_KEY") or ""))


# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def summarize_text(text, sentences=None):
    prompt = f"""
You are a professional AI document summarizer.

Summarize the following document.

Requirements:
- Keep only the important information.
- Make it easy to read.
- Use bullet points whenever suitable.
- Do not repeat information.
- Keep the summary concise.

Document:
{text}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text