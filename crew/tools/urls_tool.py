from exa_py import Exa
from .config import config
from pydantic import BaseModel
from typing import Type
from crewai.tools import BaseTool
from concurrent.futures import ThreadPoolExecutor
import requests


def _check_url(url: str) -> str | None:
    try:
        resp = requests.head(url, timeout=5)
        return url if resp.status_code == 200 else None
    except Exception:
        return None


class url_SearchTool(BaseTool):
    name: str = "URL Media Analyzer"
    description: str = "Analyzes claim over internet and bring revelant URL"
    def _run(self, claim: str) -> str:

        try:
            exa = Exa(api_key=config.EXA_API_KEY)
            response = exa.answer(
                claim,
                text=True
            )
            summary = response.answer

            citation_urls = [cite.url for cite in response.citations[:10]]
            with ThreadPoolExecutor(max_workers=10) as executor:
                checked = list(executor.map(_check_url, citation_urls))

            urls = "\n".join(u for u in checked if u)

            return {
                "url": urls.strip(),
                "summary": summary
            }

        except Exception as e:
            return f"Error: {str(e)}"
        
tool = url_SearchTool()

if __name__ == "__main__":
    tool = url_SearchTool()
    print(tool._run("Donald Trump resigined from his presidency after 100 days in office"))