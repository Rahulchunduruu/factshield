from crewai.tools import BaseTool
from pydantic import BaseModel
from typing import Type
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI 
from tavily import TavilyClient
from .config import config
import json
import re

llm = ChatOpenAI(
    model="grok-4-fast",          
    api_key=config.XAI_API_KEY,
    base_url="https://api.x.ai/v1",
    temperature=0.9
)

class SocialMediaInput(BaseModel):
    claim: str

class SocialMediaTool(BaseTool):
    name: str = "Social Media Analyzer"
    description: str = "Analyzes social media trends and discussions related to a claim"
    args_schema: Type[SocialMediaInput] = SocialMediaInput

    def _run(self, claim: str) -> str:
        client = TavilyClient(api_key=config.TAVILY_API_KEY)       
        try:

            twitter_results = client.search(
                    query=f"{claim} site:twitter.com OR site:x.com",
                    search_depth="advanced",
                    topic="news",
                    days=7,
                    max_results=5,
                    include_answer=True
                )

            reddit_results = client.search(
                    query=f"{claim} site:reddit.com",
                    search_depth="advanced",
                    topic="news",
                    days=7,
                    max_results=5,
                    include_answer=True
                )

            general_results = client.search(
                    query=f"{claim} social media viral misinformation",
                    search_depth="advanced",
                    topic="news",
                    days=7,
                    max_results=5,
                    include_answer=True
                )

        except Exception as e:
            print(f"Tavily error: {e}")
            return {"error": str(e)}


        def extract(results):

            return [
                {
                    "title":   r.get("title"),
                    "url":     r.get("url"),
                    "content": r.get("content")
                }
                for r in results.get("results", [])
            ]

        # ── Step 3: LLM analyzes spread ──
        prompt = PromptTemplate.from_template("""
        You are a social media analyst expert.

        Claim: "{claim}"

        Twitter/X Mentions:
        {twitter}

        Reddit Mentions:
        {reddit}

        General Viral Results:
        {general}

        Analyze and return ONLY this JSON:
        {{
            "is_viral":            true/false,
            "spread_speed":        "slow / moderate / fast / viral",
            "platforms":           ["twitter", "reddit"],
            "sentiment":           "positive / negative / mixed / neutral",
            "misinformation_risk": "low / medium / high",
            "viral_score":         number (0-100),
            "summary":             "short summary of how claim is spreading"
        }}
        """)

        chain  = prompt | llm
        result = chain.invoke({
            "claim":   claim,
            "twitter": json.dumps(extract(twitter_results)),
            "reddit":  json.dumps(extract(reddit_results)),
            "general": json.dumps(extract(general_results))
        })

        clean = re.sub(r"```json|```", "", result.content).strip()
        return json.loads(clean)

# ── Instance ──
social_media_tool = SocialMediaTool()


if __name__ == "__main__":
    claim  = input("Enter claim: ")
    result = social_media_tool._run(claim)
    print(json.dumps(result, indent=2))