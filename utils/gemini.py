from google import genai
import os
import time
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def ask_llm(prompt):
    try:
        time.sleep(5)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except:
        return None   # IMPORTANT → handled in scorer