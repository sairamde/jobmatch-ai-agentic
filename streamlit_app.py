import streamlit as st
from agent.langgraph_agent import run_agent
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

        # 🔥 STRONG VALIDATION
        invalid_names = ["python", "java", "ai", "ml", "test", "abc", "none", "unknown"]
        invalid_roles = ["sairam", "abc", "none", "unknown"]

        if not name.strip():
            st.warning("⚠️ Please enter candidate name")

        elif name.lower() in invalid_names or len(name.strip()) < 3:
            st.warning("⚠️ Enter a valid person name (not skills or random text)")

        elif not role.strip():
            st.warning("⚠️ Please enter role (e.g., Python backend)")

        elif role.lower() in invalid_roles or len(role.strip()) < 3:
            st.warning("⚠️ Enter a valid job role")

        else:
            # ✅ CORRECT QUERY FORMAT
            query = f"Evaluate {name} for {role}"

            with st.spinner("🔍 Evaluating candidate..."):
                result = run_agent(query)

            st.success("✅ Evaluation Complete")

            # ✅ CLEAN RESULT UI
            st.markdown("### 📊 Result")
            st.code(result, language="text")


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
        if not name.strip():
            st.warning("Enter a valid name")
        else:
            result = db_tool("DELETE", name=name)
            st.success(result)


# ---------------- PAGE 5 ----------------
elif menu == "Clear Database":

    st.header("🧹 Clear Database")

    st.warning("⚠️ This will delete ALL records permanently!")

    if st.button("Clear All Data"):
        result = db_tool("CLEAR")
        st.success(result)