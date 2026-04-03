from crewai import Task
from .agent import *


t0 = Task(
    description="""
        Use the Search Tool inside the model to find CURRENT information about: {input}"
    """,
    agent=Validater,
    expected_output="Clean text content with json format"
)

t1 = Task(
    description="Scrape content from {input}",
    agent=scraper,
    expected_output="Clean text content",
    context=[t0]
)

t2 = Task(
    description="Extract all checkable factual claims from the scraped content",
    agent=claim_expert,
    expected_output="List of specific claims",
    context=[t1]          
)

t3 = Task(
    description="Search trusted sources for each claim and return evidence",
    agent=researcher,
    expected_output="Evidence dict per claim with source tier",
    context=[t2]
)

t4 = Task(
    description="Cross-reference claims vs evidence, score each claim 0-100",
    agent=analyst,
    expected_output="Scored claims with confidence levels",
    context=[t1,t2, t3]
)

t5 = Task(
    description="detect text and trace information in the current time line if requried",
    agent=Socialmedia,
    expected_output="summarise the information in 3 lines and return all urls links which are provided",
    context=[t1]
)

t6 = Task(
    description="""Generate the final fact-check verdict by synthesizing insights from all previous analysis tasks.
                    Determine whether the claim is Genuine, Fake, or Misleading.
                    Provide a structured JSON response including verdict, confidence score, explanation, summarized claim, and verified sources.
                    Think carefully before assigning the final verdict.""",
    agent=verdict_agent,
    expected_output="""json:{ verdict: Genuine/Fake/Misleading ("Think little bit longer before giving verdict" and verdict should based on input passed by the user), 
                             score:"0-100",, 
                             explanation:"Detailed reasoning explaining why the claim is Genuine, Fake, or Misleading", 
                             claims: in one line summary, 
                             sources:Provide a verified, working source URL that best supports the verdict.Prioritize Tier 1 sources top3 websites }
                    Rules:
                        - Use only verified and working URLs.
                        - Prioritize Tier 1 sources (government websites, major news outlets, academic institutions).
                        - Provide up to 3 high-quality sources.                       
                    """,
    context=[t0,t3,t4,t5]
)

