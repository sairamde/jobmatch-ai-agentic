from tavily import TavilyClient
import os
import streamlit as st


try:
    api_key = st.secrets["TAVILY_API_KEY"]
except:
    api_key = os.getenv("TAVILY_API_KEY")

client = TavilyClient(api_key=api_key)

def web_search(query):
    try:
        res = client.search(query=query, max_results=3)
        results = res.get("results", [])
        return " ".join([r["content"] for r in results])
    except:
        return ""