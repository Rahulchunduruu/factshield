import os
import streamlit as st
from dotenv import load_dotenv


load_dotenv()

class config:
    TAVILY_API_KEY=os.getenv('TAVILY_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    XAI_API_KEY=os.getenv('XAI_API_KEY')
