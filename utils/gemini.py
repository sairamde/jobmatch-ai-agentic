import google.generativeai as genai
import os


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def ask_llm(prompt):
    try:
    
        model = genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content(prompt)
        return response.text if response else None

    except Exception as e:
        print("Gemini Error:", e)
        return None