from langgraph.graph import StateGraph, END
from typing import TypedDict
from tools.web_search import web_search
from tools.jd_scorer import jd_scorer
from tools.db_tool import db_tool
import re


class State(TypedDict):
    query: str
    name: str
    search: str
    score_text: str
    score: int
    final: str


def extract_name(q):
    words = q.split()
    return words[1] + " " + words[2] if len(words) >= 3 else "Unknown"


def extract_score(text):
    match = re.search(r"Score[: ]+(\d+)", text)
    return int(match.group(1)) if match else 50


def extract_skills(q):
    skills = []
    for s in ["fastapi", "postgresql", "django", "aws"]:
        if s in q.lower():
            skills.append(s)
    return ", ".join(skills)


def search_node(s):
    return {"search": web_search(s["query"])}


def score_node(s):
    data = s["search"] + " Skills: " + extract_skills(s["query"])
    res = jd_scorer(data)
    return {"score_text": res, "score": extract_score(res)}


def db_node(s):
    db_tool("INSERT", name=s["name"], score=s["score"],
            strengths="From LLM", gaps="From LLM", url="N/A")
    return {}


def final_node(s):
    return {
        "final": f"{s['name']} scored {s['score']}/100\n\n{s['score_text']}"
    }


def build():
    g = StateGraph(State)

    g.add_node("search", search_node)
    g.add_node("score", score_node)
    g.add_node("db", db_node)
    g.add_node("final", final_node)

    g.set_entry_point("search")
    g.add_edge("search", "score")
    g.add_edge("score", "db")
    g.add_edge("db", "final")
    g.add_edge("final", END)

    return g.compile()


graph = build()


def run_agent(query):

    if not query.strip():
        return "Invalid input"

    if "show all" in query.lower():
        return db_tool("LIST")

    if "top" in query.lower():
        return db_tool("TOP")

    if "remove" in query.lower():
        return db_tool("DELETE", name=extract_name(query))

    result = graph.invoke({
        "query": query,
        "name": extract_name(query),
        "search": "",
        "score_text": "",
        "score": 0,
        "final": ""
    })

    return result["final"]