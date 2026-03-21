from langgraph.graph import StateGraph, END
from typing import TypedDict
from tools.web_search import web_search
from tools.jd_scorer import jd_scorer
from tools.db_tool import db_tool

MAX_ITER = 8


# ---------------- STATE ----------------
class State(TypedDict):
    query: str
    name: str
    step: int
    search_data: str
    score: int
    strengths: list
    gaps: list
    recommendation: str
    saved: bool
    verified: bool
    final: str


# ---------------- UTIL ----------------
def extract_name(query: str):
    try:
        return query.split("Evaluate")[1].split("for")[0].strip()
    except:
        return "Unknown"


# ---------------- AGENT NODE ----------------
def agent_node(state: State):

    step = state["step"]

    # ❌ Stop condition
    if step > MAX_ITER:
        return {"final": "Stopped due to max iterations"}

    # ❌ Invalid input
    if state["name"].lower() in ["python", "java", "ai", "test", "abc"]:
        return {"final": "Invalid candidate name. Please enter a real person name."}

    # ---------------- STEP 1: SEARCH ----------------
    if not state["search_data"]:
        print("\nThought: I need to find candidate information online")
        print("Action: web_search")

        search_query = f"{state['name']} Python developer GitHub LinkedIn portfolio"
        data = web_search(search_query)

        print("Observation:", data[:100])

        # EDGE CASE: no profile
        if not data or len(data) < 30:
            return {
                "final": f"""
{state['name']} scored 45/100

Strengths:
- Limited information

Gaps:
- No online profile found

Recommendation: Request Resume
"""
            }

        return {
            "search_data": data,
            "step": step + 1
        }

    # ---------------- STEP 2: SCORE ----------------
    if state["score"] == 0:
        print("\nThought: I will score the candidate based on profile + skills")
        print("Action: jd_scorer")

        combined_data = state["search_data"] + " " + state["query"]

        score, strengths, gaps, rec = jd_scorer(combined_data)

        print("Observation: Score =", score)

        return {
            "score": score,
            "strengths": strengths,
            "gaps": gaps,
            "recommendation": rec,
            "step": step + 1
        }

    # ---------------- STEP 3: SAVE ----------------
    if not state["saved"]:
        print("\nThought: Saving candidate data to database")
        print("Action: db_tool INSERT")

        db_tool(
            "INSERT",
            name=state["name"],
            score=state["score"],
            strengths=", ".join(state["strengths"]),
            gaps=", ".join(state["gaps"]),
            url="N/A"
        )

        print("Observation: Saved successfully")

        return {
            "saved": True,
            "step": step + 1
        }

    # ---------------- STEP 4: VERIFY ----------------
    if not state["verified"]:
        print("\nThought: Verifying saved data from database")
        print("Action: db_tool SELECT")

        record = db_tool("SELECT", name=state["name"])

        print("Observation:", record)

        return {
            "verified": True,
            "step": step + 1
        }

    # ---------------- FINAL ----------------
    final_output = f"""
{state['name']} scored {state['score']}/100

Strengths:
- {state['strengths'][0] if state['strengths'] else ""}
- {state['strengths'][1] if len(state['strengths']) > 1 else ""}

Gaps:
- {state['gaps'][0] if state['gaps'] else ""}

Recommendation: {state['recommendation']}
"""

    return {"final": final_output}


# ---------------- GRAPH ----------------
def build_graph():
    graph = StateGraph(State)

    graph.add_node("agent", agent_node)

    graph.set_entry_point("agent")

    graph.add_conditional_edges(
        "agent",
        lambda s: "end" if s.get("final") else "agent",
        {
            "agent": "agent",
            "end": END
        }
    )

    return graph.compile()


graph = build_graph()


# ---------------- RUN ----------------
def run_agent(query: str):

    result = graph.invoke({
        "query": query,
        "name": extract_name(query),
        "step": 1,
        "search_data": "",
        "score": 0,
        "strengths": [],
        "gaps": [],
        "recommendation": "",
        "saved": False,
        "verified": False,
        "final": ""
    })

    return result["final"]