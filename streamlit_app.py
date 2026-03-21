import streamlit as st
from agent.agent import run_agent   # ✅ correct import
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

        # ❌ EMPTY CHECK
        if not name.strip():
            st.warning("Enter candidate name")

        # ❌ INVALID NAME (must be 2 words)
        elif len(name.split()) < 2:
            st.warning("Enter full name (e.g., Rahul Sharma)")

        # ❌ INVALID ROLE
        elif role.lower() in ["unknown", "", "none"]:
            st.warning("Enter valid role (e.g., Python backend)")

        # ❌ NON-TECH ROLE BLOCK
        elif not any(word in role.lower() for word in [
            "python", "backend", "developer", "engineer", "fastapi", "django"
        ]):
            st.warning("Enter valid technical role (e.g., Python Backend Developer)")

        # ✅ VALID INPUT
        else:
            query = f"Evaluate {name} {role}"

            with st.spinner("Processing..."):
                result = run_agent(query)

            st.success("Evaluation Complete ✅")

            st.markdown("### 📊 Result")
            st.code(result)

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

    remove_name = st.text_input("Enter Candidate Name")

    if st.button("Remove"):
        if remove_name.strip():
            result = db_tool("DELETE", name=remove_name)
            st.success(result)
        else:
            st.warning("Enter a valid name")

# ---------------- PAGE 5 ----------------
elif menu == "Clear Database":

    st.header("🧹 Clear Database")

    if st.button("Clear All Data"):
        result = db_tool("CLEAR")
        st.success(result)