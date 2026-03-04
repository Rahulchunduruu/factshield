import os
import streamlit as st
from dotenv import load_dotenv


load_dotenv()

class config:
    #If you prefer to run this in the terminal, make sure the first 3 lines is active and the next 3 lines is commented out
    #TAVILY_API_KEY=os.getenv('TAVILY_API_KEY')
    #OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    #XAI_API_KEY=os.getenv('XAI_API_KEY')
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    TAVILY_API_KEY=st.secrets['TAVILY_API_KEY']
    XAI_API_KEY=st.secrets['XAI_API_KEY']

