from crewai import Agent,LLM

from .tools import validate_tool, search_tool, scrap_tool, social_media_tool
from .tools.config import config

#llm-OPENAI
llm = LLM(
    model="gpt-4o",
    api_key=config.OPENAI_API_KEY,
    temperature=0.8
)

#llm-XAPI
llm2 = LLM(
    model="grok-4-fast",          
    api_key=config.XAI_API_KEY,
    base_url="https://api.x.ai/v1",
    temperature=0.9
)

#Agent0
Validater = Agent(
    role='Text Validater',
    goal='Understand the text whether they are claiming something or not',
    tools=[validate_tool],      # ← pass instance here
    backstory='Expert at text understanding and the emotion',
    llm=llm
)

#Agent1
scraper=Agent(
    role='web_scraper',
    goal='Extract clean text from the URL and html pages and use topic:genral|news|finance based requriemnt',
    tools=[scrap_tool],
    backstory='Expert at collecting raw data from web pages',
    llm=llm 
)

#Agent2
claim_expert=Agent(
    role='claim_analyzer',
    goal='"Identify all specific, checkable factual claims from the content and use topic:genral|news|finance based requriemnt',
    tools=[],
    backstory='Linguist who breaks complex text into verifiable facts',
    llm=llm2
)
#Agent3
researcher= Agent(
    role='Evidence Researcher',
    goal='Search Tier 1-5 trusted sources to find supporting or contradicting evidence and  use topic:genral|news|finance based requriemnt',
    tools=[search_tool],
    backstory='Investigative journalist with access to global databases',
    llm=llm 
)

# Agent 4 — Analyst
analyst = Agent(
    role="Fact Analyst",
    goal="Cross-reference claims against evidence and assign confidence scores and Search Tier 1-5 trusted sources and use topic:genral|news|finance based requriemnt",
    tools=[search_tool],
    backstory="Data scientist who evaluates source credibility objectively",
    llm=llm 
)

# Agent 5 — Socialmedia Analyst
Socialmedia = Agent(
    role="social media Viralness Expert",
    goal="Detect the information and trace original news",
    tools=[social_media_tool],
    backstory="social media Expert in trained on all socialmedia platforms",
    llm=llm 
)

# Agent 6 — Verdict Writer
verdict_agent = Agent(
    role="Verdict Reporter",
    goal="Generate a clear, human-readable verdict with score and explanation",
    tools=[],
    backstory="Senior editor who translates complex analysis into plain English",
    llm=llm2
)


