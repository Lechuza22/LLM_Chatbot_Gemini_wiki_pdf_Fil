from chains_or_agents.agent import create_agent

def run_chat():
    agent = create_agent()
    print("🤖 Chatbot Filosófico listo. Escribí tu pregunta o 'salir'.\n")
    while True:
        prompt = input("🧠 Vos: ")
        if prompt.lower() in ['salir', 'exit', 'q']:
            break
        response = agent.run(prompt)
        print(f"🤖 Bot: {response}\n")

if __name__ == "__main__":
    run_chat()
