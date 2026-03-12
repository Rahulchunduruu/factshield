from exa_py import Exa
from .config import config
from pydantic import BaseModel
from typing import Type
from crewai.tools import BaseTool
import requests



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

            urls=""
            for cite in response.citations[:10]:
                resp = requests.head(cite.url, timeout=5)
                if resp.status_code == 200:
                    urls = urls + "\n" + cite.url


            return {
                "url":urls.strip(),
                "summary":summary
            }

        except Exception as e:
            return f"Error: {str(e)}"
        
tool = url_SearchTool()

if __name__ == "__main__":
    tool = url_SearchTool()
    print(tool._run("Donald Trump resigined from his presidency after 100 days in office"))