from langchain.tools import WikipediaQueryRun
from langchain.utilities import WikipediaAPIWrapper

def get_wikipedia_tool():
    # Configurar el wrapper para Wikipedia en español
    wiki_wrapper = WikipediaAPIWrapper(lang="es")
    
    # Crear herramienta compatible con LangChain Agent
    wiki_tool = WikipediaQueryRun(api_wrapper=wiki_wrapper)
    
    return wiki_tool
