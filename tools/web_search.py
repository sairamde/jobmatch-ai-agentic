import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def web_search(query: str) -> str:
    try:
        res = client.search(query=query, max_results=3)
        results = res.get("results", [])
        return " ".join([r.get("content", "") for r in results])
    except Exception as e:
        print("Search Error:", e)
        return ""