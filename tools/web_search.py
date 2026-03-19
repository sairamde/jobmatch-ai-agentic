from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def web_search(query):
    try:
        result = client.search(query=query, max_results=2)
        return str(result)
    except:
        return "No profile found"