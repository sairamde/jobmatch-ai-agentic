from agent.agent import run_agent

while True:
    query = input("\nEnter command: ")

    if query.lower() == "exit":
        break

    result = run_agent(query)
    print("\nFINAL OUTPUT:")
    print(result)