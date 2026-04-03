from crewai.tools import BaseTool
from tavily import TavilyClient
from .config import config
from pydantic import BaseModel
from typing import Optional, Type

TRUSTED_DOMAINS = [
    "reuters.com", "apnews.com", "bbc.com",
    "who.int", "cdc.gov", "nature.com",
    "snopes.com", "politifact.com",
    "factcheck.org", "wikipedia.org"
]

class SearchInput(BaseModel):
    query: str
    domain: Optional[str] = None
    max_search: int = 5

class SearchTool(BaseTool):
    name: str = "Web Search Tool"
    description: str = "Searches the web for evidence related to a claim using Tavily. Include new website if you need --> domain"
    args_schema: Type[SearchInput] = SearchInput
    trusted_only: bool = True   # False = general web (no domain filter)

    def _run(self, query: str, domain: Optional[str] = None, max_search: int = 5) -> dict:
        client = TavilyClient(api_key=config.TAVILY_API_KEY)

        include_domains = None
        if self.trusted_only:
            include_domains = list(TRUSTED_DOMAINS)
            if domain:
                include_domains.append(domain)

        try:
            kwargs = dict(
                query=query,
                search_depth="advanced",
                max_results=max_search,
                include_answer=True,
            )
            if include_domains:
                kwargs["include_domains"] = include_domains

            result = client.search(**kwargs)
        except Exception as e:
            print(f"Search error: {e}")
            return {"answer": None, "content": []}

        answer  = result.get("answer")
        results = result.get("results", [])
        content = [r.get("content") for r in results]

        return {"answer": answer, "content": content}

# ── Instances ──
search_tool = SearchTool()                              # trusted sources only
