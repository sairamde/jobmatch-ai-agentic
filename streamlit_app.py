import streamlit as st
from agent.agent import run_agent
from tools.db_tool import db_tool

# ---------------- CONFIG ----------------
st.set_page_config(page_title="JobMatch AI", page_icon="🤖", layout="wide")

# ---------------- HEADER ----------------
st.title("🤖 JobMatch AI System")
st.subheader("Agentic AI Candidate Evaluation (LangGraph + Gemini)")

# ---------------- SIDEBAR ----------------
st.sidebar.title("📌 Menu")

menu = st.sidebar.radio("Select Option", [
    "Evaluate Candidate",
    "Show All Candidates",
    "Top 3 Candidates",
    "Remove Candidate",
    "Clear Database"
])

# ---------------- PAGE 1 ----------------
if menu == "Evaluate Candidate":

    st.header("🧠 Evaluate Candidate")

    name = st.text_input("Candidate Name")
    role = st.text_input("Role", value="Python backend")

    if st.button("Evaluate"):

        if name:
            query = f"Evaluate {name} {role}"

            with st.spinner("Processing..."):
                result = run_agent(query)

            st.success("Evaluation Complete ✅")
            st.text_area("Result", result, height=300)

        else:
            st.warning("Enter candidate name")

# ---------------- PAGE 2 ----------------
elif menu == "Show All Candidates":

    st.header("📋 All Candidates")

    data = db_tool("LIST")

    if isinstance(data, str):
        st.warning(data)
    else:
        for row in data:
            st.write(f"👤 {row[0]} — Score: {row[1]}")

# ---------------- PAGE 3 ----------------
elif menu == "Top 3 Candidates":

    st.header("🏆 Top 3 Candidates")

    data = db_tool("TOP")

    if data:
        for i, row in enumerate(data, 1):
            st.write(f"{i}. {row[0]} — Score: {row[1]}")
    else:
        st.warning("No data available")

# ---------------- PAGE 4 ----------------
elif menu == "Remove Candidate":

    st.header("❌ Remove Candidate")

    name = st.text_input("Enter Candidate Name")

    if st.button("Remove"):
        result = db_tool("DELETE", name=name)
        st.success(result)

# ---------------- PAGE 5 ----------------
elif menu == "Clear Database":

    st.header("🧹 Clear Database")

    if st.button("Clear All Data"):
        result = db_tool("CLEAR")
        st.success(result)