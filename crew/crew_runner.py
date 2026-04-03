from crewai import Crew, Process
from .task import *
from .agent import *
import json
import re
import hashlib
from langchain.globals import set_llm_cache
from langchain_community.cache import SQLiteCache

# Cache LLM responses on disk — avoids re-calling the API for identical inputs
set_llm_cache(SQLiteCache(database_path=".langchain_cache.db"))

# In-memory cache for full fact-check results (keyed by claim hash)
_result_cache: dict = {}


def run_factcheck(user_input: str, input_type: str):
    # Return cached result if this exact claim was already analyzed
    cache_key = hashlib.md5(f"{user_input}:{input_type}".encode()).hexdigest()
    if cache_key in _result_cache:
        print("✅ Cache hit — returning cached result")
        return _result_cache[cache_key]

    crew=Crew(
        agents=[Validater,scraper, claim_expert, researcher, analyst,Socialmedia,verdict_agent],
        tasks=[t0,t1, t2, t3, t4,t5,t6],
        process=Process.sequential,   
        verbose=True,
        max_iter=1
    )

    result=crew.kickoff(inputs={'input': user_input, 'type': input_type})

    raw = result.raw
    clean = re.sub(r"```json|```", "", raw).strip()
    data  = json.loads(clean)

    result= {
            "verdict" :     data.get("verdict", "Unknown"),
            "explanation":  data.get("explanation", "No explanation provided"),
            "confidence_score": data.get("score", "N/A"),
            "claims_analyzed": data.get("claims", "N/A")
            }
    if data.get("sources") and data["sources"] != "None":
        result['sources'] = data["sources"] if isinstance(data["sources"], list) else [data["sources"]]

    _result_cache[cache_key] = result
    return result                   



if __name__ == "__main__":
    #run_factcheck("https://www.bbc.com/news/world-asia-66973315","url")
    print(run_factcheck('Videos circulating online show Iranian missiles successfully striking and heavily damaging the USS Abraham Lincoln aircraft carrier in early 2026.',"text"))
