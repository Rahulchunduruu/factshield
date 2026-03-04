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
    context=[t2, t3]
)

t5 = Task(
    description="detect text and trace information",
    agent=Socialmedia,
    expected_output="summarise the information in 3 lines",
    context=[t1]
)

t6 = Task(
    description="Compile all analysis into final verdict card",
    agent=verdict_agent,
    expected_output="""json:{verdict:Genuine/Fake/ Misleading, score, explanation, claims: in one line summary, sources:Provide a verified, working source URL that best supports the verdict.
                        Prioritize Tier 1 sources (reuters.com, apnews.com, bbc.com, who.int).
                        Return only the direct article link, not homepage if you not able find source just return None. }""",
    context=[t1,t2,t3,t4,t5]
)