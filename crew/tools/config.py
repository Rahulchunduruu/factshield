import os
from dotenv import load_dotenv

load_dotenv()

class config:
    TAVILY_API_KEY = os.getenv('TAVILY_API_KEY2')
    XAI_API_KEY    = os.getenv("XAI_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    EXA_API_KEY    = os.getenv("EXA_API_KEY")
    #Simba@512526
