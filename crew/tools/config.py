import os
import streamlit as st
from dotenv import load_dotenv


load_dotenv()

class config:
    TAVILY_API_KEY = st.secrets.get("TAVILY_API_KEY") or os.getenv("TAVILY_API_KEY")
    XAI_API_KEY    = st.secrets.get("XAI_API_KEY")    or os.getenv("XAI_API_KEY")
    OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
