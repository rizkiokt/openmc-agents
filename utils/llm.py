from langchain_google_genai import ChatGoogleGenerativeAI
import os

MODEL = "gemini-2.0-flash"

class LLM:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=MODEL,
            google_api_key=os.getenv("GEMINI_API_KEY"))
        