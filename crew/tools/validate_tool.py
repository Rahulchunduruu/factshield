from crewai.tools import BaseTool
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from .config import config
from typing import Optional, Type
from pydantic import BaseModel              # ← ADD THIS

# ── Define LLM inside the file ──
llm = ChatOpenAI(
    model="gpt-4o",
    api_key=config.OPENAI_API_KEY,
    temperature=0.7
)

# ── Input Schema ──
class ValidateInput(BaseModel):
    statement: str

class ValidateTool(BaseTool):
    name: str = "Statement Validator"
    description: str = "Validates whether a statement is a factual claim or not"
    args_schema: Type[ValidateInput] = ValidateInput    # ← use proper schema

    def _run(self, statement: str) -> str:
        prompt = PromptTemplate.from_template("""
            You are an expert fact-checker. Evaluate the following statement:

            Statement: "{statement}"

            Return JSON:
            {{
                "is_factual": boolean,
                "confidence_score": number (0-1),
                "evidence": "string",
                "explanation": "string"
            }}
        """)

        chain = prompt | llm
        result = chain.invoke({"statement": statement})
        return result.content

# ── Instance ──
validate_tool = ValidateTool()