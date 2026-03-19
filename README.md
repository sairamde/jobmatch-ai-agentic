## JobMatch AI – Agentic AI Candidate Evaluation System

##  Overview
JobMatch AI is an Agentic AI system that evaluates candidates for backend roles using LLM reasoning, tool-based execution, and database storage.

The system follows a multi-step workflow:
- Search candidate information
- Evaluate using AI (Gemini)
- Store results in SQLite database
- Display structured output

---

##  Tech Stack

| Component | Technology |
|----------|-----------|
| Framework | LangGraph |
| LLM | Gemini API |
| Database | SQLite |
| Language | Python |
| UI  | Streamlit |

---

##  Features

 Evaluate candidates using natural language  
 AI-based scoring (LLM + fallback logic)  
 Store results in database  
 View all candidates  
 Get top 3 candidates  
 Remove candidate records  
 Handle edge cases (unknown, wrong domain)  
 Streamlit UI for easy interaction  

---

##  Project Structure


jobmatch_ai/
│
├── streamlit_app.py # Streamlit UI
├── main.py # CLI interface
│
├── agent/
│ └── agent.py # LangGraph agent logic
│
├── tools/
│ ├── web_search.py # Search tool
│ ├── jd_scorer.py # AI scoring logic
│ ├── db_tool.py # Database operations
│
├── utils/
│ └── gemini.py # LLM integration
│
├── requirements.txt
├── README.md


---

##  Installation & Setup

###  Clone Repository

git clone <your_repo_link>
cd jobmatch_ai


---

###  Create Virtual Environment

python -m venv myenv
myenv\Scripts\activate


---

###  Install Dependencies

pip install -r requirements.txt


---

###  Setup Environment Variables

Create `.env` file:


GEMINI_API_KEY=YOUR_API_KEY
TAVILY_API_KEY=YOUR_API_KEY


---

##  How to Run

###  Run CLI Version

python main.py


---

###  Run Streamlit UI (Recommended)

streamlit run streamlit_app.py


---

##  Example Commands


Evaluate Rahul Sharma Python backend
Evaluate Ankit Verma FastAPI PostgreSQL
Evaluate Anil Kumar Civil Engineer
Show all evaluated candidates
Who are the top 3 candidates
Remove Rahul Sharma


---

##  Sample Output


Rahul Sharma scored 78/100

Strengths:

Python development

Backend APIs

Gaps:

No PostgreSQL

Recommendation: Interview


---

##  Edge Case Handling

| Scenario | Output |
|---------|--------|
| Unknown person | Need Info |
| Wrong domain | Reject |
| Strong backend skills | High score |
| Missing skills | Medium score |

---

##  Architecture


User Input
↓
LangGraph Agent
↓
Search Tool
↓
LLM (Gemini)
↓
Database (SQLite)
↓
Final Output


---

##  ReAct Framework

This system follows **ReAct-style reasoning**:

- Thought → decide next step  
- Action → use tool  
- Observation → process result  
- Final Answer  

Implemented using LangGraph nodes.

---

##  Learnings

- LangGraph workflow design  
- Agentic AI system development  
- Prompt engineering  
- Tool integration  

---

##  Challenges

- API rate limits  
- Data inconsistency  
- Output parsing  

---

##  Future Improvements

- Better data sources  
- UI enhancements  
- Advanced scoring models  

---

##  Conclusion

This project demonstrates a complete Agentic AI system using LangGraph, integrating LLM reasoning, tools, and database operations to automate candidate evaluation.

---