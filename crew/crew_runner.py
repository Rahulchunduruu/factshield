import os
os.environ["OTEL_SDK_DISABLED"] = "true"

from crewai import Crew, Process
from .task import *
from .agent import *
import json
import re

def run_factcheck(user_input: str, input_type: str):
    
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
            "verdict" :     data["verdict"],
            "explanation":  data["explanation"],
            "confidence_score": data.get("score", "N/A"),
            "claims_analyzed": data.get("claims", "N/A")
            }
    if data.get("sources") and data["sources"] != "None":
        result['sources'] = data["sources"] if isinstance(data["sources"], list) else [data["sources"]]
    
    return result                   



if __name__ == "__main__":
    #run_factcheck("https://www.bbc.com/news/world-asia-66973315","url")
    print(run_factcheck('Videos circulating online show Iranian missiles successfully striking and heavily damaging the USS Abraham Lincoln aircraft carrier in early 2026.',"text"))
