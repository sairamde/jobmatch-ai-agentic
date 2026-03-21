from agent.langgraph_agent import run_agent

while True:
    q = input("\nEnter command: ")
    if q.lower() == "exit":
        break

    print(run_agent(q))