from langgraph.graph import StateGraph, END
from typing import TypedDict
from tools.web_search import web_search
from tools.jd_scorer import jd_scorer
from tools.db_tool import db_tool
import re


class AgentState(TypedDict):
    query: str
    name: str
    search_result: str
    score_result: str
    score: int
    final: str


def extract_name(query):
    words = query.split()
    if len(words) >= 3:
        return words[1] + " " + words[2]
    return "Unknown"


def extract_score(text):
    match = re.search(r"Score[: ]+(\d+)", text)
    return int(match.group(1)) if match else 50


# -------- NODES --------

def search_node(state: AgentState):
    print("\n[LangGraph] Searching...")
    return {"search_result": web_search(state["query"])}


def scoring_node(state: AgentState):
    print("\n[LangGraph] Scoring...")
    result = jd_scorer(state["search_result"])
    score = extract_score(result)
    return {"score_result": result, "score": score}


def db_node(state: AgentState):
    print("\n[LangGraph] Saving...")
    db_tool("INSERT",
            name=state["name"],
            score=state["score"],
            strengths="From LLM",
            gaps="From LLM",
            url="N/A")
    return {}


def final_node(state: AgentState):
    return {
        "final": f"""
{state["name"]} scored {state["score"]}/100.

{state["score_result"]}
"""
    }


# -------- GRAPH --------

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("search", search_node)
    graph.add_node("score", scoring_node)
    graph.add_node("db", db_node)
    graph.add_node("final", final_node)

    graph.set_entry_point("search")

    graph.add_edge("search", "score")
    graph.add_edge("score", "db")
    graph.add_edge("db", "final")
    graph.add_edge("final", END)

    return graph.compile()


graph = build_graph()


def run_agent(query):

    # DATABASE COMMANDS
    if "show all" in query.lower():
        return db_tool("LIST")

    if "top" in query.lower():
        return db_tool("TOP")

    if "remove" in query.lower():
        return db_tool("DELETE", name=extract_name(query))

    if "show" in query.lower():
        return db_tool("SELECT", name=extract_name(query))

    result = graph.invoke({
        "query": query,
        "name": extract_name(query),
        "search_result": "",
        "score_result": "",
        "score": 0,
        "final": ""
    })

    return result["final"]