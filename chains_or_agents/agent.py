import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from retrievers.pdf_vectorstore import load_config, build_pdf_vectorstore
from retrievers.wikipedia_tool import get_wikipedia_tool
from langchain_community.vectorstores import FAISS  # necesario si cargás desde disco

def create_agent():
    load_dotenv()
    config = load_config()
    api_key = os.getenv(config["llm"]["api_key_env_var"])

    # LLM Gemini
    llm = ChatGoogleGenerativeAI(
        model=config["llm"]["model"],
        temperature=config["llm"]["temperature"],
        google_api_key=api_key
    )

    # Memoria
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # Wikipedia tool
    wikipedia_tool = get_wikipedia_tool()

    # PDF vectorstore
    vectordb = build_pdf_vectorstore(config)  # o FAISS.load_local(...) si ya existe
    retriever = vectordb.as_retriever()

    pdf_tool = Tool(
        name="PDFs Filosóficos",
        func=lambda q: "\n".join([doc.page_content for doc in retriever.get_relevant_documents(q)]),
        description="Consulta manuales filosóficos relevantes en PDF"
    )

    # Inicializar agente
    agent = initialize_agent(
        tools=[wikipedia_tool, pdf_tool],
        llm=llm,
        agent="chat-conversational-react-description",
        memory=memory,
        verbose=True
    )

    return agent
