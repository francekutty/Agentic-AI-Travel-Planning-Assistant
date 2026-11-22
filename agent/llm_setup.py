
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("Google API key not found.")

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=api_key
)

if __name__ == "__main__":
    response = llm.invoke(
        "Say: Travel Planning AI Agent connected successfully!"
    )
    print(response.content)
