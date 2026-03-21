import os
import time
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def ask_llm(prompt: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")

        for _ in range(2):
            try:
                response = model.generate_content(prompt)
                if response and hasattr(response, "text"):
                    return response.text.strip()
            except Exception as e:
                print("Retrying LLM...", e)
                time.sleep(3)

        return ""

    except Exception as e:
        print("LLM Error:", e)
        return ""