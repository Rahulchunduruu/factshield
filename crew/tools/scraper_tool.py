from crewai.tools import BaseTool
from tavily import TavilyClient
from .config import config

class SearchTool(BaseTool):
    name: str = "Web Search Tool"
    description: str = "Searches the web for evidence related to a claim using Tavily"

    def _run(self, query: str) -> dict:
        tavilyClient = TavilyClient(api_key=config.TAVILY_API_KEY)

        try:
            search_results_general = tavilyClient.search(
                query,
                search_depth="advanced",
                topic='general',
                max_results=5,
                days=10,
                include_answer=True
            )
        except Exception as e:
            print(f"An error occurred during searching: {e}")
            return {"answer": None, "content": []}

        answer  = search_results_general.get("answer")
        results = search_results_general.get("results", [])
        content = [r.get("content") for r in results]

        return {
            "answer":  answer,
            "content": content
        }

# ── Instance ──
scrap_tool = SearchTool()      # ← import this in agent.py


if __name__ == "__main__":
    query = input("Enter the search query: ")
    result = scrap_tool._run(query)
    print(result)